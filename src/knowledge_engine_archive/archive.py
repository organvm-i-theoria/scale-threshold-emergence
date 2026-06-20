from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Message:
    id: str
    role: str
    text: str


@dataclass(frozen=True)
class ThreadPair:
    pair_id: str
    title: str
    prompt: Message
    response: Message
    pair_path: Path


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _clean_line(line: str) -> str:
    line = line.strip()
    line = re.sub(r"^#{1,6}\s+", "", line)
    return re.sub(r"\s+", " ", line).strip()


def _is_thinking_line(line: str) -> bool:
    return re.fullmatch(r"Thought for \d+(?:\.\d+)?s", line.strip()) is not None


def derive_title(prompt: str, response: str) -> str:
    """Derive a stable pair title, preferring the assistant's first heading."""
    for raw_line in response.splitlines():
        line = _clean_line(raw_line)
        if not line or _is_thinking_line(line):
            continue
        if line.startswith("```"):
            continue
        return line[:120]

    for raw_line in prompt.splitlines():
        line = _clean_line(raw_line)
        if line:
            return line[:120]

    return "Untitled Thread Pair"


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s-]+", "-", value)
    return value.strip("-") or "thread-pair"


def _read_messages(source_path: Path) -> list[Message]:
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    raw_messages = payload.get("messages", [])
    messages: list[Message] = []

    for index, item in enumerate(raw_messages, start=1):
        role = str(item.get("role", "")).strip().lower()
        text = str(item.get("say", ""))
        messages.append(Message(id=f"MSG-{index:03d}", role=role, text=text))

    return messages


def _pair_messages(messages: list[Message]) -> list[tuple[Message, Message]]:
    pairs: list[tuple[Message, Message]] = []
    pending_prompt: Message | None = None

    for message in messages:
        if message.role in {"prompt", "user", "human"}:
            pending_prompt = message
            continue

        if message.role in {"response", "assistant", "ai"} and pending_prompt:
            pairs.append((pending_prompt, message))
            pending_prompt = None

    return pairs


def _write_pair(pair: ThreadPair, repo_root: Path) -> None:
    target = repo_root / pair.pair_path
    target.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(
        [
            f"# {pair.pair_id}: {pair.title}",
            "",
            "## Prompt",
            "",
            pair.prompt.text.strip(),
            "",
            "## Response",
            "",
            pair.response.text.strip(),
            "",
        ]
    )
    target.write_text(body, encoding="utf-8")


def _write_thread_manifest(pairs: list[ThreadPair], repo_root: Path) -> None:
    path = repo_root / "manifest/thread_manifest.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Thread Manifest",
        "",
        f"Generated: {_utc_now()}",
        "",
    ]

    for pair in pairs:
        lines.extend(
            [
                f"## {pair.pair_id}: {pair.title}",
                "",
                f"- Pair path: `{pair.pair_path.as_posix()}`",
                f"- Prompt message: `{pair.prompt.id}`",
                f"- Response message: `{pair.response.id}`",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def archive_thread(source_path: Path, repo_root: Path) -> dict[str, Any]:
    """Archive a JSON thread export into pair files and a pair manifest."""
    source_path = Path(source_path)
    repo_root = Path(repo_root)
    messages = _read_messages(source_path)
    empty_message_ids = [message.id for message in messages if not message.text.strip()]

    pairs: list[ThreadPair] = []
    for index, (prompt, response) in enumerate(_pair_messages(messages), start=1):
        pair_id = f"TH-{index:03d}"
        title = derive_title(prompt.text, response.text)
        pair_path = (
            Path("research/thread_pairs") / f"{pair_id.lower()}-{_slugify(title)}.md"
        )
        pair = ThreadPair(
            pair_id=pair_id,
            title=title,
            prompt=prompt,
            response=response,
            pair_path=pair_path,
        )
        _write_pair(pair, repo_root)
        pairs.append(pair)

    manifest_dir = repo_root / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    pair_manifest = [
        {
            "pair_id": pair.pair_id,
            "title": pair.title,
            "prompt_message_id": pair.prompt.id,
            "response_message_id": pair.response.id,
            "pair_path": pair.pair_path.as_posix(),
        }
        for pair in pairs
    ]
    pair_manifest_path = manifest_dir / "pair_manifest.json"
    pair_manifest_path.write_text(
        json.dumps(pair_manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_thread_manifest(pairs, repo_root)

    verification = verify_repo(repo_root)
    status = "pass" if verification["status"] == "pass" else "fail"
    return {
        "status": status,
        "source_path": str(source_path),
        "pair_count": len(pairs),
        "empty_message_ids": empty_message_ids,
        "pair_manifest_path": str(pair_manifest_path),
    }


def verify_repo(repo_root: Path) -> dict[str, Any]:
    """Verify that archived pair manifest entries point at existing files."""
    repo_root = Path(repo_root)
    manifest_path = repo_root / "manifest/pair_manifest.json"

    if not manifest_path.exists():
        return {
            "status": "fail",
            "errors": [f"missing manifest: {manifest_path}"],
        }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    for item in manifest:
        pair_path = repo_root / item.get("pair_path", "")
        if not pair_path.exists():
            errors.append(f"missing pair file: {pair_path}")

    return {
        "status": "pass" if not errors else "fail",
        "pair_count": len(manifest),
        "errors": errors,
    }

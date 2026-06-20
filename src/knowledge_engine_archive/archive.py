from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ThreadPair:
    pair_id: str
    prompt_id: str
    response_id: str
    title: str
    prompt: str
    response: str
    pair_path: str


def derive_title(prompt: str, response: str) -> str:
    """Derive a readable pair title from the response, falling back to prompt text."""
    for line in response.splitlines():
        candidate = line.strip().strip("#").strip()
        if not candidate or re.fullmatch(r"Thought for \d+s", candidate):
            continue
        return candidate

    for line in prompt.splitlines():
        candidate = line.strip().strip("#").strip()
        if candidate:
            return candidate

    return "Untitled Thread Pair"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72] or "untitled"


def _message_text(message: dict[str, Any]) -> str:
    value = message.get("say", "")
    return value if isinstance(value, str) else str(value)


def _message_role(message: dict[str, Any]) -> str:
    return str(message.get("role", "")).strip().lower()


def _pair_messages(
    messages: list[dict[str, Any]],
) -> tuple[list[ThreadPair], list[str]]:
    pairs: list[ThreadPair] = []
    empty_message_ids: list[str] = []
    pending_prompt: tuple[str, str] | None = None

    for index, message in enumerate(messages, start=1):
        message_id = f"MSG-{index:03d}"
        text = _message_text(message)
        if text == "":
            empty_message_ids.append(message_id)

        role = _message_role(message)
        if role == "prompt":
            pending_prompt = (message_id, text)
            continue

        if role == "response" and pending_prompt is not None:
            pair_id = f"TH-{len(pairs) + 1:03d}"
            title = derive_title(pending_prompt[1], text)
            pair_path = f"research/thread_pairs/{pair_id}-{_slugify(title)}.md"
            pairs.append(
                ThreadPair(
                    pair_id=pair_id,
                    prompt_id=pending_prompt[0],
                    response_id=message_id,
                    title=title,
                    prompt=pending_prompt[1],
                    response=text,
                    pair_path=pair_path,
                )
            )
            pending_prompt = None

    return pairs, empty_message_ids


def _render_pair(pair: ThreadPair) -> str:
    return (
        f"# {pair.pair_id}: {pair.title}\n\n"
        f"Prompt ID: {pair.prompt_id}\n"
        f"Response ID: {pair.response_id}\n\n"
        "## Prompt\n\n"
        f"{pair.prompt.rstrip()}\n\n"
        "## Response\n\n"
        f"{pair.response.rstrip()}\n"
    )


def archive_thread(source_path: Path | str, repo_root: Path | str) -> dict[str, Any]:
    source = Path(source_path)
    root = Path(repo_root)
    payload = json.loads(source.read_text(encoding="utf-8"))
    messages = payload.get("messages", [])
    if not isinstance(messages, list):
        raise ValueError("Thread export must contain a messages list")

    pairs, empty_message_ids = _pair_messages(messages)
    for pair in pairs:
        pair_path = root / pair.pair_path
        pair_path.parent.mkdir(parents=True, exist_ok=True)
        pair_path.write_text(_render_pair(pair), encoding="utf-8")

    manifest_dir = root / "manifest"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    pair_manifest = [
        {
            "pair_id": pair.pair_id,
            "prompt_id": pair.prompt_id,
            "response_id": pair.response_id,
            "title": pair.title,
            "pair_path": pair.pair_path,
        }
        for pair in pairs
    ]
    (manifest_dir / "pair_manifest.json").write_text(
        json.dumps(pair_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    thread_manifest = {
        "source_path": str(source),
        "title": payload.get("metadata", {}).get("title", source.stem),
        "pair_count": len(pairs),
        "empty_message_ids": empty_message_ids,
        "archived_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }
    (manifest_dir / "thread_manifest.json").write_text(
        json.dumps(thread_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    verification = verify_repo(root)
    return {
        "status": verification["status"],
        "pair_count": len(pairs),
        "empty_message_ids": empty_message_ids,
    }


def verify_repo(repo_root: Path | str) -> dict[str, Any]:
    root = Path(repo_root)
    manifest_path = root / "manifest/pair_manifest.json"
    errors: list[str] = []

    if not manifest_path.exists():
        return {"status": "fail", "errors": [f"Missing {manifest_path}"]}

    pair_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in pair_manifest:
        pair_path = root / entry["pair_path"]
        if not pair_path.exists():
            errors.append(f"Missing pair file: {entry['pair_path']}")

    return {
        "status": "fail" if errors else "pass",
        "pair_count": len(pair_manifest),
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Archive a research thread export.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args(argv)

    print(json.dumps(archive_thread(args.source, args.repo_root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

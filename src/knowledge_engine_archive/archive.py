from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def derive_title(prompt: str, response: str) -> str:
    """Choose a stable thread-pair title from a response, falling back to prompt text."""
    for line in response.splitlines():
        candidate = line.strip().strip("#").strip()
        if not candidate:
            continue
        if re.fullmatch(r"Thought for \d+s", candidate):
            continue
        return candidate[:120]

    for line in prompt.splitlines():
        candidate = line.strip().strip("#").strip()
        if candidate:
            return candidate[:120]

    return "Untitled Thread Pair"


def archive_thread(source_path: Path, repo_root: Path) -> dict[str, object]:
    source_path = Path(source_path)
    repo_root = Path(repo_root)
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    messages = _coerce_messages(payload.get("messages", []))

    manifest_dir = repo_root / "manifest"
    pairs_dir = repo_root / "thread_pairs"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    pairs_dir.mkdir(parents=True, exist_ok=True)

    message_manifest: list[dict[str, object]] = []
    empty_message_ids: list[str] = []

    for index, message in enumerate(messages, start=1):
        message_id = f"MSG-{index:03d}"
        content = message["say"]
        if not content.strip():
            empty_message_ids.append(message_id)
        message_manifest.append(
            {
                "message_id": message_id,
                "role": message["role"],
                "sha256": _sha256_text(content),
                "empty": not bool(content.strip()),
            }
        )

    pair_manifest: list[dict[str, object]] = []
    pair_index = 1
    for prompt_index, prompt_message in enumerate(messages):
        if prompt_message["role"].lower() != "prompt":
            continue

        response_message = _next_response(messages, prompt_index + 1)
        response_text = response_message["say"] if response_message else ""
        title = derive_title(prompt_message["say"], response_text)
        pair_id = f"TH-{pair_index:03d}"
        pair_path = Path("thread_pairs") / f"{pair_id}-{_slugify(title)}.md"
        pair_file = repo_root / pair_path

        pair_file.write_text(
            _render_pair(
                pair_id=pair_id,
                title=title,
                prompt=prompt_message["say"],
                response=response_text,
            ),
            encoding="utf-8",
        )

        pair_manifest.append(
            {
                "pair_id": pair_id,
                "title": title,
                "pair_path": pair_path.as_posix(),
                "prompt_message_id": f"MSG-{prompt_index + 1:03d}",
                "response_message_id": (
                    f"MSG-{response_message['index']:03d}" if response_message else None
                ),
                "sha256": _sha256_file(pair_file),
            }
        )
        pair_index += 1

    (manifest_dir / "message_manifest.json").write_text(
        json.dumps(message_manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (manifest_dir / "pair_manifest.json").write_text(
        json.dumps(pair_manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    integrity = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_file": source_path.name,
        "total_messages": len(messages),
        "pair_count": len(pair_manifest),
        "empty_message_ids": empty_message_ids,
        "all_hashes": [item["sha256"] for item in message_manifest],
    }
    (manifest_dir / "integrity_manifest.json").write_text(
        json.dumps(integrity, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    verification = verify_repo(repo_root)
    return {
        "status": verification["status"],
        "source_path": str(source_path),
        "repo_root": str(repo_root),
        "message_count": len(messages),
        "pair_count": len(pair_manifest),
        "empty_message_ids": empty_message_ids,
    }


def verify_repo(repo_root: Path) -> dict[str, object]:
    repo_root = Path(repo_root)
    manifest_path = repo_root / "manifest" / "pair_manifest.json"
    if not manifest_path.exists():
        return {
            "status": "fail",
            "missing_paths": [manifest_path.as_posix()],
            "pair_count": 0,
        }

    pair_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    missing_paths: list[str] = []
    hash_mismatches: list[str] = []

    for pair in pair_manifest:
        pair_path = repo_root / str(pair.get("pair_path", ""))
        if not pair_path.exists():
            missing_paths.append(pair_path.as_posix())
            continue
        expected_hash = pair.get("sha256")
        if expected_hash and _sha256_file(pair_path) != expected_hash:
            hash_mismatches.append(pair_path.as_posix())

    status = "pass" if not missing_paths and not hash_mismatches else "fail"
    return {
        "status": status,
        "pair_count": len(pair_manifest),
        "missing_paths": missing_paths,
        "hash_mismatches": hash_mismatches,
    }


def _coerce_messages(raw_messages: object) -> list[dict[str, str]]:
    if not isinstance(raw_messages, list):
        raise ValueError("source export must contain a messages list")

    messages: list[dict[str, str]] = []
    for raw_message in raw_messages:
        if not isinstance(raw_message, dict):
            raise ValueError("each message must be an object")
        role = str(raw_message.get("role", "")).strip() or "Unknown"
        content = str(raw_message.get("say", ""))
        messages.append({"role": role, "say": content})
    return messages


def _next_response(
    messages: list[dict[str, str]], start_index: int
) -> dict[str, object] | None:
    for index in range(start_index, len(messages)):
        message = messages[index]
        if message["role"].lower() == "response":
            return {"index": index + 1, "role": message["role"], "say": message["say"]}
        if message["role"].lower() == "prompt":
            return None
    return None


def _render_pair(pair_id: str, title: str, prompt: str, response: str) -> str:
    return (
        f"# {pair_id}: {title}\n\n"
        "## Prompt\n\n"
        f"{prompt.strip()}\n\n"
        "## Response\n\n"
        f"{response.strip()}\n"
    )


def _sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:80] or "untitled"

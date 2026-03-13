from __future__ import annotations

import json
from pathlib import Path

from knowledge_engine_archive.archive import archive_thread, derive_title, verify_repo


def write_fixture(path: Path) -> None:
    payload = {
        "metadata": {
            "title": "Fixture Thread",
            "user": {"name": "Tester", "email": "tester@example.com"},
            "dates": {"created": "3/11/2026 11:00:00", "updated": "3/11/2026 11:00:01", "exported": "3/11/2026 11:00:02"},
            "link": "https://chatgpt.com/c/fixture-thread-id",
            "powered_by": "fixture",
        },
        "messages": [
            {"role": "Prompt", "say": "Prompt one"},
            {"role": "Response", "say": "Primitive Interaction Map\n\nDetails here."},
            {"role": "Prompt", "say": "Prompt two"},
            {"role": "Response", "say": ""},
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_derive_title_prefers_response_heading() -> None:
    title = derive_title("Question text", "Thought for 12s\n\nResearch Knowledge Graph\n\nBody")
    assert title == "Research Knowledge Graph"


def test_archive_and_verify_round_trip(tmp_path: Path) -> None:
    source_path = tmp_path / "fixture.json"
    repo_root = tmp_path / "repo"
    write_fixture(source_path)

    result = archive_thread(source_path=source_path, repo_root=repo_root)
    assert result["status"] == "pass"
    assert result["pair_count"] == 2
    assert result["empty_message_ids"] == ["MSG-004"]

    pair_manifest = json.loads((repo_root / "manifest/pair_manifest.json").read_text(encoding="utf-8"))
    assert pair_manifest[0]["pair_id"] == "TH-001"
    assert pair_manifest[1]["pair_id"] == "TH-002"

    pair_file = repo_root / pair_manifest[0]["pair_path"]
    assert "Prompt one" in pair_file.read_text(encoding="utf-8")
    assert "Primitive Interaction Map" in pair_file.read_text(encoding="utf-8")

    verification = verify_repo(repo_root)
    assert verification["status"] == "pass"

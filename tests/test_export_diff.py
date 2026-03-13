from __future__ import annotations

import json
from pathlib import Path

from knowledge_engine_archive.export_diff import analyze_exports, normalize_markdown, write_outputs


def write_json_export(path: Path, title: str, exported: str, messages: list[dict[str, str]]) -> None:
    payload = {
        "metadata": {
            "title": title,
            "dates": {
                "created": "3/11/2026 11:00:00",
                "updated": "3/11/2026 11:30:00",
                "exported": exported,
            },
        },
        "messages": messages,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_json_equivalence_and_prefix_detection(tmp_path: Path) -> None:
    base_messages = [
        {"role": "Prompt", "say": "Prompt one"},
        {"role": "Response", "say": "Response one"},
    ]
    extended_messages = base_messages + [
        {"role": "Prompt", "say": "Prompt two"},
        {"role": "Response", "say": "Response two"},
    ]

    first = tmp_path / "ChatGPT-Branch · Example.json"
    second = tmp_path / "ChatGPT-Branch · Example (1).json"
    third = tmp_path / "ChatGPT-Branch · Example (2).json"

    write_json_export(first, "Branch · Example", "3/11/2026 11:35:00", base_messages)
    write_json_export(second, "Branch · Example", "3/11/2026 11:40:00", base_messages)
    write_json_export(third, "Branch · Example", "3/11/2026 11:45:00", extended_messages)

    manifest = analyze_exports([first, second, third])

    json_equivalence = [
        group
        for group in manifest["relationships"]["content_equivalence"]
        if group["relation_type"] == "json_message_equivalent"
    ]
    assert len(json_equivalence) == 1
    assert len(json_equivalence[0]["paths"]) == 2
    assert json_equivalence[0]["content_identical_but_raw_distinct"] is True
    diff_paths = {
        item["path"]
        for pair in json_equivalence[0]["pairwise_differences"]
        for item in pair["differences"]
    }
    assert diff_paths == {"metadata.dates.exported"}

    prefix_relations = manifest["relationships"]["json_prefix_relations"]
    assert len(prefix_relations) == 2
    assert all(relation["target_message_count"] == 4 for relation in prefix_relations)


def test_markdown_duplicate_and_normalized_equivalence(tmp_path: Path) -> None:
    first = tmp_path / "Branch-·-Example.md"
    second = tmp_path / "Branch-·-Example (1).md"
    third = tmp_path / "Branch-·-Example (2).md"

    first.write_text("# Title\n\nBody line.\n", encoding="utf-8")
    second.write_text("# Title\n\nBody line.\n", encoding="utf-8")
    third.write_text("# Title   \n\nBody line.   \n", encoding="utf-8")

    assert normalize_markdown(first.read_text(encoding="utf-8")) == normalize_markdown(
        third.read_text(encoding="utf-8")
    )

    manifest = analyze_exports([first, second, third])

    exact_duplicates = manifest["relationships"]["exact_duplicates"]
    assert len(exact_duplicates) == 1
    assert len(exact_duplicates[0]["paths"]) == 2

    markdown_equivalence = [
        group
        for group in manifest["relationships"]["content_equivalence"]
        if group["relation_type"] == "markdown_normalized_equivalent"
    ]
    assert len(markdown_equivalence) == 1
    assert len(markdown_equivalence[0]["paths"]) == 3


def test_write_outputs_creates_manifest_and_report(tmp_path: Path) -> None:
    export_path = tmp_path / "ChatGPT-Example.json"
    write_json_export(
        export_path,
        "Example",
        "3/11/2026 12:00:00",
        [{"role": "Prompt", "say": "Prompt"}, {"role": "Response", "say": "Response"}],
    )
    manifest = analyze_exports([export_path])
    report_path = tmp_path / "docs/report.md"
    manifest_path = tmp_path / "manifest/report.json"

    write_outputs(manifest, report_path=report_path, manifest_path=manifest_path)

    assert report_path.exists()
    assert manifest_path.exists()
    assert "Export Diff Report" in report_path.read_text(encoding="utf-8")

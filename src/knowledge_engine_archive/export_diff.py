from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExportRecord:
    path: str
    suffix: str
    raw: str
    payload: Any | None

    @property
    def raw_hash(self) -> str:
        return hashlib.sha256(self.raw.encode()).hexdigest()


def normalize_markdown(content: str) -> str:
    lines = [line.rstrip() for line in content.replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def _load_record(path: Path) -> ExportRecord:
    raw = path.read_text(encoding="utf-8")
    payload: Any | None = None
    if path.suffix.lower() == ".json":
        payload = json.loads(raw)
    return ExportRecord(
        path=str(path),
        suffix=path.suffix.lower(),
        raw=raw,
        payload=payload,
    )


def _message_signature(payload: Any) -> str:
    messages = payload.get("messages", []) if isinstance(payload, dict) else []
    return json.dumps(messages, sort_keys=True, separators=(",", ":"))


def _is_prefix(source: list[Any], target: list[Any]) -> bool:
    return len(source) < len(target) and target[: len(source)] == source


def _find_differences(left: Any, right: Any, prefix: str = "") -> list[dict[str, Any]]:
    if type(left) is not type(right):
        return [{"path": prefix or "$", "left": left, "right": right}]

    if isinstance(left, dict):
        differences: list[dict[str, Any]] = []
        for key in sorted(set(left) | set(right)):
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            if key not in left:
                differences.append(
                    {"path": child_prefix, "left": None, "right": right[key]}
                )
            elif key not in right:
                differences.append(
                    {"path": child_prefix, "left": left[key], "right": None}
                )
            else:
                differences.extend(
                    _find_differences(left[key], right[key], child_prefix)
                )
        return differences

    if isinstance(left, list):
        differences = []
        max_len = max(len(left), len(right))
        for index in range(max_len):
            child_prefix = f"{prefix}[{index}]"
            if index >= len(left):
                differences.append(
                    {"path": child_prefix, "left": None, "right": right[index]}
                )
            elif index >= len(right):
                differences.append(
                    {"path": child_prefix, "left": left[index], "right": None}
                )
            else:
                differences.extend(
                    _find_differences(left[index], right[index], child_prefix)
                )
        return differences

    if left != right:
        return [{"path": prefix or "$", "left": left, "right": right}]
    return []


def _group_by(records: list[ExportRecord], key_name: str) -> list[dict[str, Any]]:
    buckets: dict[str, list[ExportRecord]] = {}
    for record in records:
        key = getattr(record, key_name)
        buckets.setdefault(key, []).append(record)

    return [
        {"hash": key, "paths": [record.path for record in group]}
        for key, group in buckets.items()
        if len(group) > 1
    ]


def _json_equivalence(records: list[ExportRecord]) -> list[dict[str, Any]]:
    buckets: dict[str, list[ExportRecord]] = {}
    for record in records:
        if record.suffix == ".json" and record.payload is not None:
            buckets.setdefault(_message_signature(record.payload), []).append(record)

    groups: list[dict[str, Any]] = []
    for signature, group in buckets.items():
        if len(group) < 2:
            continue

        pairwise_differences = []
        for left_index, left in enumerate(group):
            for right in group[left_index + 1 :]:
                pairwise_differences.append(
                    {
                        "left": left.path,
                        "right": right.path,
                        "differences": _find_differences(left.payload, right.payload),
                    }
                )

        groups.append(
            {
                "relation_type": "json_message_equivalent",
                "signature": hashlib.sha256(signature.encode()).hexdigest(),
                "paths": [record.path for record in group],
                "content_identical_but_raw_distinct": len(
                    {record.raw_hash for record in group}
                )
                > 1,
                "pairwise_differences": pairwise_differences,
            }
        )

    return groups


def _markdown_equivalence(records: list[ExportRecord]) -> list[dict[str, Any]]:
    buckets: dict[str, list[ExportRecord]] = {}
    for record in records:
        if record.suffix == ".md":
            normalized = normalize_markdown(record.raw)
            key = hashlib.sha256(normalized.encode()).hexdigest()
            buckets.setdefault(key, []).append(record)

    return [
        {
            "relation_type": "markdown_normalized_equivalent",
            "signature": key,
            "paths": [record.path for record in group],
        }
        for key, group in buckets.items()
        if len(group) > 1
    ]


def _json_prefix_relations(records: list[ExportRecord]) -> list[dict[str, Any]]:
    json_records = [
        record
        for record in records
        if record.suffix == ".json" and record.payload is not None
    ]
    relations: list[dict[str, Any]] = []

    for source in json_records:
        source_messages = source.payload.get("messages", [])
        for target in json_records:
            if source.path == target.path:
                continue
            target_messages = target.payload.get("messages", [])
            if _is_prefix(source_messages, target_messages):
                relations.append(
                    {
                        "source_path": source.path,
                        "target_path": target.path,
                        "source_message_count": len(source_messages),
                        "target_message_count": len(target_messages),
                    }
                )

    return relations


def analyze_exports(paths: list[Path | str]) -> dict[str, Any]:
    records = [_load_record(Path(path)) for path in paths]
    exact_duplicates = _group_by(records, "raw_hash")

    return {
        "export_count": len(records),
        "paths": [record.path for record in records],
        "relationships": {
            "exact_duplicates": exact_duplicates,
            "content_equivalence": _json_equivalence(records)
            + _markdown_equivalence(records),
            "json_prefix_relations": _json_prefix_relations(records),
        },
    }


def _render_report(manifest: dict[str, Any]) -> str:
    relationships = manifest["relationships"]
    lines = [
        "# Export Diff Report",
        "",
        f"Exports analyzed: {manifest['export_count']}",
        "",
        f"Exact duplicate groups: {len(relationships['exact_duplicates'])}",
        f"Content equivalence groups: {len(relationships['content_equivalence'])}",
        f"JSON prefix relations: {len(relationships['json_prefix_relations'])}",
        "",
    ]
    return "\n".join(lines)


def write_outputs(
    manifest: dict[str, Any],
    report_path: Path | str,
    manifest_path: Path | str,
) -> None:
    report = Path(report_path)
    manifest_file = Path(manifest_path)
    report.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(_render_report(manifest), encoding="utf-8")
    manifest_file.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze exported thread files.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--report-path", type=Path, required=True)
    parser.add_argument("--manifest-path", type=Path, required=True)
    args = parser.parse_args(argv)

    manifest = analyze_exports(args.paths)
    write_outputs(manifest, args.report_path, args.manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

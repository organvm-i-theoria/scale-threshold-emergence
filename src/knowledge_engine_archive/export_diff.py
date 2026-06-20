from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


def normalize_markdown(text: str) -> str:
    """Normalize Markdown enough to compare export-equivalent files."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip() + "\n"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _read_record(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    suffix = path.suffix.lower()
    record: dict[str, Any] = {
        "path": str(path),
        "suffix": suffix,
        "raw_hash": _sha256_bytes(raw),
        "size_bytes": len(raw),
    }

    if suffix == ".json":
        payload = json.loads(raw.decode("utf-8"))
        messages = payload.get("messages", [])
        record.update(
            {
                "kind": "json",
                "payload": payload,
                "messages": messages,
                "message_count": len(messages),
                "message_hash": hashlib.sha256(
                    _canonical_json(messages).encode("utf-8")
                ).hexdigest(),
            }
        )
    elif suffix in {".md", ".markdown"}:
        text = raw.decode("utf-8")
        record.update(
            {
                "kind": "markdown",
                "text": text,
                "normalized_hash": hashlib.sha256(
                    normalize_markdown(text).encode("utf-8")
                ).hexdigest(),
            }
        )
    else:
        record["kind"] = "other"

    return record


def _group_by(records: list[dict[str, Any]], key: str) -> list[list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if key in record:
            groups.setdefault(str(record[key]), []).append(record)
    return [group for group in groups.values() if len(group) > 1]


def _diff_json(left: Any, right: Any, path: str = "") -> list[dict[str, Any]]:
    if left == right:
        return []

    if isinstance(left, dict) and isinstance(right, dict):
        differences: list[dict[str, Any]] = []
        for key in sorted(set(left) | set(right)):
            child_path = f"{path}.{key}" if path else str(key)
            if key not in left:
                differences.append(
                    {"path": child_path, "left": None, "right": right[key]}
                )
            elif key not in right:
                differences.append(
                    {"path": child_path, "left": left[key], "right": None}
                )
            else:
                differences.extend(_diff_json(left[key], right[key], child_path))
        return differences

    if isinstance(left, list) and isinstance(right, list) and len(left) == len(right):
        differences = []
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences.extend(_diff_json(left_item, right_item, f"{path}[{index}]"))
        return differences

    return [{"path": path or "$", "left": left, "right": right}]


def _json_message_equivalence(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups = []
    for group in _group_by(records, "message_hash"):
        pairwise_differences = []
        for left, right in itertools.combinations(group, 2):
            pairwise_differences.append(
                {
                    "left": left["path"],
                    "right": right["path"],
                    "differences": _diff_json(left["payload"], right["payload"]),
                }
            )

        groups.append(
            {
                "relation_type": "json_message_equivalent",
                "paths": [record["path"] for record in group],
                "message_count": group[0]["message_count"],
                "content_identical_but_raw_distinct": (
                    len({record["raw_hash"] for record in group}) > 1
                ),
                "pairwise_differences": pairwise_differences,
            }
        )
    return groups


def _markdown_equivalence(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = []
    for group in _group_by(records, "normalized_hash"):
        groups.append(
            {
                "relation_type": "markdown_normalized_equivalent",
                "paths": [record["path"] for record in group],
                "content_identical_but_raw_distinct": (
                    len({record["raw_hash"] for record in group}) > 1
                ),
            }
        )
    return groups


def _is_prefix(shorter: list[Any], longer: list[Any]) -> bool:
    return len(shorter) < len(longer) and longer[: len(shorter)] == shorter


def _json_prefix_relations(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    relations = []
    json_records = [record for record in records if record["kind"] == "json"]
    for left, right in itertools.permutations(json_records, 2):
        if _is_prefix(left["messages"], right["messages"]):
            relations.append(
                {
                    "relation_type": "json_message_prefix",
                    "source_path": left["path"],
                    "target_path": right["path"],
                    "source_message_count": left["message_count"],
                    "target_message_count": right["message_count"],
                }
            )
    return relations


def analyze_exports(paths: list[Path]) -> dict[str, Any]:
    records = [_read_record(Path(path)) for path in paths]

    exact_duplicates = [
        {
            "relation_type": "exact_duplicate",
            "paths": [record["path"] for record in group],
            "raw_hash": group[0]["raw_hash"],
        }
        for group in _group_by(records, "raw_hash")
    ]

    content_equivalence = []
    content_equivalence.extend(_json_message_equivalence(records))
    content_equivalence.extend(_markdown_equivalence(records))

    return {
        "exports": [
            {
                "path": record["path"],
                "kind": record["kind"],
                "size_bytes": record["size_bytes"],
            }
            for record in records
        ],
        "relationships": {
            "exact_duplicates": exact_duplicates,
            "content_equivalence": content_equivalence,
            "json_prefix_relations": _json_prefix_relations(records),
        },
    }


def _render_report(manifest: dict[str, Any]) -> str:
    relationships = manifest["relationships"]
    return "\n".join(
        [
            "# Export Diff Report",
            "",
            f"Exports analyzed: {len(manifest['exports'])}",
            f"Exact duplicate groups: {len(relationships['exact_duplicates'])}",
            f"Equivalence groups: {len(relationships['content_equivalence'])}",
            f"JSON prefix relations: {len(relationships['json_prefix_relations'])}",
            "",
        ]
    )


def write_outputs(
    manifest: dict[str, Any],
    report_path: Path,
    manifest_path: Path,
) -> None:
    report_path = Path(report_path)
    manifest_path = Path(manifest_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    report_path.write_text(_render_report(manifest), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--report-path", required=True, type=Path)
    parser.add_argument("--manifest-path", required=True, type=Path)
    args = parser.parse_args()

    manifest = analyze_exports(args.paths)
    write_outputs(
        manifest,
        report_path=args.report_path,
        manifest_path=args.manifest_path,
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Iterable


def normalize_markdown(content: str) -> str:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    normalized = "\n".join(line.rstrip() for line in lines).strip()
    return f"{normalized}\n" if normalized else ""


def analyze_exports(paths: Iterable[Path]) -> dict[str, object]:
    records = [_read_export(Path(path)) for path in paths]
    json_records = [record for record in records if record["kind"] == "json_export"]
    markdown_records = [
        record for record in records if record["kind"] == "markdown_export"
    ]

    return {
        "generated_at": _utc_now(),
        "source_paths": [str(record["path"]) for record in records],
        "inventory": {
            "json": [_inventory_json(record) for record in json_records],
            "markdown": [_inventory_markdown(record) for record in markdown_records],
        },
        "relationships": {
            "exact_duplicates": _exact_duplicates(records),
            "content_equivalence": [
                *_json_message_equivalence(json_records),
                *_markdown_normalized_equivalence(markdown_records),
            ],
            "json_prefix_relations": _json_prefix_relations(json_records),
        },
    }


def write_outputs(
    manifest: dict[str, object], report_path: Path, manifest_path: Path
) -> None:
    report_path = Path(report_path)
    manifest_path = Path(manifest_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    report_path.write_text(_render_report(manifest, manifest_path), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(prog="knowledge_engine_archive.export_diff")
    parser.add_argument("--report-path", required=True, type=Path)
    parser.add_argument("--manifest-path", required=True, type=Path)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    manifest = analyze_exports(args.paths)
    write_outputs(
        manifest,
        report_path=args.report_path,
        manifest_path=args.manifest_path,
    )
    print(json.dumps({"status": "pass", "compared": len(args.paths)}, sort_keys=True))


def _read_export(path: Path) -> dict[str, object]:
    raw_bytes = path.read_bytes()
    raw_text = raw_bytes.decode("utf-8")
    raw_sha256 = _sha256_bytes(raw_bytes)
    suffix = path.suffix.lower()

    if suffix == ".json":
        parsed = json.loads(raw_text)
        messages = parsed.get("messages", []) if isinstance(parsed, dict) else []
        if not isinstance(messages, list):
            messages = []
        return {
            "kind": "json_export",
            "path": path,
            "family": _family_name(path),
            "raw_sha256": raw_sha256,
            "parsed": parsed,
            "messages": messages,
            "message_sha256": _sha256_json(messages),
            "message_count": len(messages),
        }

    normalized = normalize_markdown(raw_text)
    return {
        "kind": "markdown_export",
        "path": path,
        "family": _family_name(path),
        "raw_sha256": raw_sha256,
        "normalized_sha256": _sha256_text(normalized),
        "line_count": len(raw_text.splitlines()),
    }


def _inventory_json(record: dict[str, object]) -> dict[str, object]:
    parsed = record["parsed"]
    metadata = parsed.get("metadata", {}) if isinstance(parsed, dict) else {}
    dates = metadata.get("dates", {}) if isinstance(metadata, dict) else {}
    return {
        "path": str(record["path"]),
        "file": Path(str(record["path"])).name,
        "family": record["family"],
        "message_count": record["message_count"],
        "raw_sha256": record["raw_sha256"],
        "message_sha256": record["message_sha256"],
        "updated": dates.get("updated") if isinstance(dates, dict) else None,
        "exported": dates.get("exported") if isinstance(dates, dict) else None,
    }


def _inventory_markdown(record: dict[str, object]) -> dict[str, object]:
    return {
        "path": str(record["path"]),
        "file": Path(str(record["path"])).name,
        "family": record["family"],
        "line_count": record["line_count"],
        "raw_sha256": record["raw_sha256"],
        "normalized_sha256": record["normalized_sha256"],
    }


def _exact_duplicates(records: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[dict[str, object]]] = {}
    for record in records:
        key = (str(record["kind"]), str(record["raw_sha256"]))
        groups.setdefault(key, []).append(record)

    duplicates: list[dict[str, object]] = []
    for (kind, raw_hash), group in sorted(groups.items(), key=lambda item: item[0]):
        if len(group) < 2:
            continue
        duplicates.append(
            {
                "kind": kind,
                "raw_sha256": raw_hash,
                "paths": [str(record["path"]) for record in group],
            }
        )
    return duplicates


def _json_message_equivalence(
    records: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = {}
    for record in records:
        groups.setdefault(str(record["message_sha256"]), []).append(record)

    equivalences: list[dict[str, object]] = []
    for message_hash, group in sorted(groups.items()):
        if len(group) < 2:
            continue
        raw_hashes = {record["raw_sha256"] for record in group}
        pairwise_differences = []
        for left, right in combinations(group, 2):
            differences = _diff_values(left["parsed"], right["parsed"])
            if differences:
                pairwise_differences.append(
                    {
                        "left_path": str(left["path"]),
                        "right_path": str(right["path"]),
                        "differences": differences,
                    }
                )
        equivalences.append(
            {
                "relation_type": "json_message_equivalent",
                "message_sha256": message_hash,
                "paths": [str(record["path"]) for record in group],
                "content_identical_but_raw_distinct": len(raw_hashes) > 1,
                "pairwise_differences": pairwise_differences,
            }
        )
    return equivalences


def _markdown_normalized_equivalence(
    records: list[dict[str, object]],
) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = {}
    for record in records:
        groups.setdefault(str(record["normalized_sha256"]), []).append(record)

    equivalences: list[dict[str, object]] = []
    for normalized_hash, group in sorted(groups.items()):
        if len(group) < 2:
            continue
        equivalences.append(
            {
                "relation_type": "markdown_normalized_equivalent",
                "normalized_sha256": normalized_hash,
                "paths": [str(record["path"]) for record in group],
            }
        )
    return equivalences


def _json_prefix_relations(records: list[dict[str, object]]) -> list[dict[str, object]]:
    relations: list[dict[str, object]] = []
    for source, target in combinations(records, 2):
        relation = _prefix_relation(source, target)
        if relation is not None:
            relations.append(relation)
            continue
        relation = _prefix_relation(target, source)
        if relation is not None:
            relations.append(relation)
    return relations


def _prefix_relation(
    source: dict[str, object], target: dict[str, object]
) -> dict[str, object] | None:
    source_messages = source["messages"]
    target_messages = target["messages"]
    if not isinstance(source_messages, list) or not isinstance(target_messages, list):
        return None
    if len(source_messages) >= len(target_messages):
        return None
    if target_messages[: len(source_messages)] != source_messages:
        return None

    added_messages = target_messages[len(source_messages) :]
    first_added = added_messages[0] if added_messages else {}
    preview = ""
    if isinstance(first_added, dict):
        preview = str(first_added.get("say", ""))[:120]

    return {
        "source_path": str(source["path"]),
        "target_path": str(target["path"]),
        "source_message_count": len(source_messages),
        "target_message_count": len(target_messages),
        "added_message_count": len(added_messages),
        "first_added_message_preview": preview,
    }


def _diff_values(
    left: object, right: object, path: str = ""
) -> list[dict[str, object]]:
    if type(left) is not type(right):
        return [{"path": path or "$", "left": left, "right": right}]

    if isinstance(left, dict):
        differences: list[dict[str, object]] = []
        keys = sorted(set(left) | set(right))
        for key in keys:
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
                differences.extend(_diff_values(left[key], right[key], child_path))
        return differences

    if isinstance(left, list):
        differences = []
        max_length = max(len(left), len(right))
        for index in range(max_length):
            child_path = f"{path}[{index}]"
            if index >= len(left):
                differences.append(
                    {"path": child_path, "left": None, "right": right[index]}
                )
            elif index >= len(right):
                differences.append(
                    {"path": child_path, "left": left[index], "right": None}
                )
            else:
                differences.extend(_diff_values(left[index], right[index], child_path))
        return differences

    if left != right:
        return [{"path": path or "$", "left": left, "right": right}]
    return []


def _render_report(manifest: dict[str, object], manifest_path: Path) -> str:
    inventory = manifest.get("inventory", {})
    relationships = manifest.get("relationships", {})
    json_inventory = inventory.get("json", []) if isinstance(inventory, dict) else []
    markdown_inventory = (
        inventory.get("markdown", []) if isinstance(inventory, dict) else []
    )
    exact_duplicates = (
        relationships.get("exact_duplicates", [])
        if isinstance(relationships, dict)
        else []
    )
    equivalences = (
        relationships.get("content_equivalence", [])
        if isinstance(relationships, dict)
        else []
    )
    prefix_relations = (
        relationships.get("json_prefix_relations", [])
        if isinstance(relationships, dict)
        else []
    )

    lines = [
        "# Export Diff Report",
        "",
        f"Generated at: `{manifest.get('generated_at', _utc_now())}`",
        "",
        "## Scope",
        "",
        f"- Compared `{len(manifest.get('source_paths', []))}` exports.",
        f"- JSON exports: `{len(json_inventory)}`",
        f"- Markdown exports: `{len(markdown_inventory)}`",
        f"- Machine-readable manifest: `{manifest_path}`",
        "",
        "## Inventory",
        "",
        "### JSON",
        "",
        "| File | Family | Messages | Raw SHA-256 | Message SHA-256 | Updated | Exported |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for item in json_inventory:
        lines.append(
            "| `{file}` | `{family}` | {message_count} | `{raw}` | `{message}` | `{updated}` | `{exported}` |".format(
                file=item["file"],
                family=item["family"],
                message_count=item["message_count"],
                raw=str(item["raw_sha256"])[:12],
                message=str(item["message_sha256"])[:12],
                updated=item.get("updated") or "",
                exported=item.get("exported") or "",
            )
        )

    lines.extend(
        [
            "",
            "### Markdown",
            "",
            "| File | Family | Lines | Raw SHA-256 | Normalized SHA-256 |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for item in markdown_inventory:
        lines.append(
            "| `{file}` | `{family}` | {line_count} | `{raw}` | `{normalized}` |".format(
                file=item["file"],
                family=item["family"],
                line_count=item["line_count"],
                raw=str(item["raw_sha256"])[:12],
                normalized=str(item["normalized_sha256"])[:12],
            )
        )

    lines.extend(["", "## Exact Duplicates", ""])
    if exact_duplicates:
        for duplicate in exact_duplicates:
            lines.append(
                f"- `{duplicate['kind']}` exact duplicate set on raw hash `{str(duplicate['raw_sha256'])[:12]}`:"
            )
            for path in duplicate["paths"]:
                lines.append(f"  - `{path}`")
    else:
        lines.append("- None")

    lines.extend(["", "## Content Equivalence", ""])
    if equivalences:
        for equivalence in equivalences:
            basis = equivalence.get("message_sha256") or equivalence.get(
                "normalized_sha256"
            )
            lines.append(
                f"- `{equivalence['relation_type']}` on `{str(basis)[:12]}` across `{len(equivalence['paths'])}` files."
            )
            for path in equivalence["paths"]:
                lines.append(f"  - `{path}`")
            if equivalence.get("content_identical_but_raw_distinct"):
                lines.append(
                    "  - Raw bytes differ even though the comparison basis matches."
                )
    else:
        lines.append("- None")

    lines.extend(["", "## JSON Prefix Lineage", ""])
    if prefix_relations:
        for relation in prefix_relations:
            lines.append(
                "- `{source}` is an exact message prefix of `{target}` ({source_count} -> {target_count} messages).".format(
                    source=Path(str(relation["source_path"])).name,
                    target=Path(str(relation["target_path"])).name,
                    source_count=relation["source_message_count"],
                    target_count=relation["target_message_count"],
                )
            )
            if relation.get("first_added_message_preview"):
                lines.append(
                    f"  - Added messages: `{relation['added_message_count']}`; first added message preview: `{relation['first_added_message_preview']}`"
                )
    else:
        lines.append("- None")

    lines.extend(["", "## Source Paths", ""])
    for path in manifest.get("source_paths", []):
        lines.append(f"- `{path}`")

    return "\n".join(lines) + "\n"


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _sha256_text(content: str) -> str:
    return _sha256_bytes(content.encode("utf-8"))


def _sha256_json(value: object) -> str:
    canonical = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return _sha256_text(canonical)


def _family_name(path: Path) -> str:
    stem = re.sub(r"\s+\(\d+\)$", "", path.stem)
    stem = re.sub(r"^ChatGPT-", "", stem)
    family = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return family or "unknown"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


if __name__ == "__main__":
    main()

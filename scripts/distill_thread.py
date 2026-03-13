#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

PROJECT_ROOT = Path(os.environ["PROJECT_ROOT"])
RAW_DIR = PROJECT_ROOT / "ingestion" / "raw_threads"
NORM_DIR = PROJECT_ROOT / "ingestion" / "normalized_threads"
MANIFEST_DIR = PROJECT_ROOT / "manifest"
DOCS_DIR = PROJECT_ROOT / "docs"
RESEARCH_DIR = PROJECT_ROOT / "research"
GRAPH_DIR = PROJECT_ROOT / "knowledge_graph"

NORM_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

SECTION_TARGETS = {
    "primitive canon": DOCS_DIR / "primitive_canon.md",
    "module library": DOCS_DIR / "module_library.md",
    "threshold atlas": DOCS_DIR / "threshold_atlas.md",
    "mechanism registry": DOCS_DIR / "mechanism_registry.md",
    "computational patterns": DOCS_DIR / "computational_patterns.md",
    "universe_engine_kernel_spec_v0": DOCS_DIR / "kernel_spec.md",
    "module_api_spec_v1": DOCS_DIR / "module_api.md",
    "world_instance_schema_v1": DOCS_DIR / "world_instance_schema.md",
    "research_dashboard_v1": RESEARCH_DIR / "dashboards" / "research_dashboard.md",
    "mechanism extraction template": RESEARCH_DIR / "indexes" / "mechanism_extraction_template.md",
    "core reading library": RESEARCH_DIR / "indexes" / "core_reading_library.md",
    "thread manifest": MANIFEST_DIR / "thread_manifest.md",
}

PATTERNS = {
    "primitive": r"\bPR-\d{3}\b",
    "module": r"\bM-\d{2}\b",
    "threshold": r"\bTP-\d{2}\b",
    "mechanism": r"\bMECH-\d{3}\b",
    "glossary": r"\bGL-\d{3}\b",
    "thread": r"\bTH-\d{3}\b",
}

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"

def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "_", value)
    return value.strip("_")

def split_headings(text: str) -> List[Tuple[str, str]]:
    matches = list(re.finditer(r"^(#{1,3})\s+(.+)$", text, flags=re.MULTILINE))
    if not matches:
        return [("full_thread", text)]
    sections = []
    for i, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip() + "\n"
        sections.append((title, body))
    return sections

def infer_title_from_prompt(prompt: str, idx: int) -> str:
    first = prompt.strip().splitlines()[0].strip()
    if not first:
        return f"Thread Segment {idx:03d}"
    first = re.sub(r"\s+", " ", first)
    if len(first) > 80:
        first = first[:77] + "..."
    return first

def pair_user_assistant_blocks(text: str) -> List[Dict[str, str]]:
    """
    Expects transcripts roughly in this form:
    User:
    ...
    Assistant:
    ...
    Falls back to paragraph chunking if markers are absent.
    """
    user_re = re.compile(r"(?im)^user\s*:\s*$")
    asst_re = re.compile(r"(?im)^assistant\s*:\s*$")

    user_positions = [m.start() for m in user_re.finditer(text)]
    asst_positions = [m.start() for m in asst_re.finditer(text)]

    if not user_positions or not asst_positions:
        return [{
            "id": "TH-001",
            "title": "Full Thread Capture",
            "prompt": "Full imported thread",
            "response": text.strip()
        }]

    markers = []
    for m in user_re.finditer(text):
        markers.append((m.start(), "user", m.end()))
    for m in asst_re.finditer(text):
        markers.append((m.start(), "assistant", m.end()))
    markers.sort(key=lambda x: x[0])

    blocks = []
    current_user = None
    pair_index = 1

    for i, (_, role, content_start) in enumerate(markers):
        content_end = markers[i + 1][0] if i + 1 < len(markers) else len(text)
        content = text[content_start:content_end].strip()

        if role == "user":
            current_user = content
        elif role == "assistant" and current_user is not None:
            title = infer_title_from_prompt(current_user, pair_index)
            blocks.append({
                "id": f"TH-{pair_index:03d}",
                "title": title,
                "prompt": current_user,
                "response": content
            })
            pair_index += 1
            current_user = None

    if not blocks:
        return [{
            "id": "TH-001",
            "title": "Full Thread Capture",
            "prompt": "Full imported thread",
            "response": text.strip()
        }]
    return blocks

def write_manifest(pairs: List[Dict[str, str]], out_path: Path) -> None:
    lines = [
        "---",
        "id: thread_manifest_v1",
        "title: Thread Manifest",
        "type: archive-manifest",
        "status: active",
        "version: 1",
        "---",
        "",
        "# Thread Manifest",
        "",
    ]
    for pair in pairs:
        summary = pair["response"].strip().splitlines()[0].strip() if pair["response"].strip() else ""
        if len(summary) > 120:
            summary = summary[:117] + "..."
        lines.extend([
            f"## {pair['id']} — {pair['title']}",
            "",
            "### Prompt",
            "",
            pair["prompt"].strip(),
            "",
            "### Response Summary",
            "",
            summary,
            "",
        ])
    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

def append_or_replace_section(target_path: Path, section_title: str, content: str) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if not target_path.exists():
        target_path.write_text(content.strip() + "\n", encoding="utf-8")
        return

    existing = target_path.read_text(encoding="utf-8")
    heading_re = re.compile(
        rf"(?ms)^#\s+{re.escape(section_title)}\s*$.*?(?=^#\s+|\Z)"
    )
    if heading_re.search(existing):
        updated = heading_re.sub(content.strip() + "\n", existing)
        target_path.write_text(updated, encoding="utf-8")
    else:
        target_path.write_text(existing.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")

def route_sections(sections: List[Tuple[str, str]]) -> List[Dict[str, str]]:
    routed = []
    for title, body in sections:
        title_key = slugify(title)
        matched = None
        for key, path in SECTION_TARGETS.items():
            if key == title_key or key in title_key or title_key in key:
                matched = path
                break
        if matched:
            append_or_replace_section(matched, title, body)
            routed.append({
                "title": title,
                "path": str(matched.relative_to(PROJECT_ROOT))
            })
    return routed

def build_graph() -> None:
    doc_dirs = [
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "research",
        PROJECT_ROOT / "manifest",
        PROJECT_ROOT / "engine",
    ]
    nodes = {}
    edges = []

    def add_node(node_id: str, node_type: str) -> None:
        if node_id not in nodes:
            nodes[node_id] = {"id": node_id, "type": node_type}

    for doc_dir in doc_dirs:
        if not doc_dir.exists():
            continue
        for path in doc_dir.rglob("*.md"):
            doc_id = str(path.relative_to(PROJECT_ROOT))
            add_node(doc_id, "document")
            text = path.read_text(encoding="utf-8")
            for node_type, pattern in PATTERNS.items():
                for match in sorted(set(re.findall(pattern, text))):
                    add_node(match, node_type)
                    edges.append({
                        "source": doc_id,
                        "target": match,
                        "relation": "mentions"
                    })

    out_path = GRAPH_DIR / "graph_database.json"
    out_path.write_text(json.dumps({
        "nodes": list(nodes.values()),
        "edges": edges
    }, indent=2), encoding="utf-8")

def write_distillation_report(source_path: Path, pairs: List[Dict[str, str]], routed: List[Dict[str, str]]) -> None:
    report_path = MANIFEST_DIR / f"{source_path.stem}_distillation_report.md"
    lines = [
        "---",
        f"id: {source_path.stem}_distillation_report",
        "title: Distillation Report",
        "type: archive-report",
        "status: active",
        "version: 1",
        "---",
        "",
        "# Distillation Report",
        "",
        f"## Source",
        "",
        str(source_path.relative_to(PROJECT_ROOT)),
        "",
        "## Pair Count",
        "",
        str(len(pairs)),
        "",
        "## Routed Sections",
        "",
    ]
    if routed:
        for item in routed:
            lines.append(f"- {item['title']} → `{item['path']}`")
    else:
        lines.append("No routable sections detected.")
    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")

def process_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    normalized = normalize_text(raw)

    norm_path = NORM_DIR / path.name
    norm_path.write_text(normalized, encoding="utf-8")

    pairs = pair_user_assistant_blocks(normalized)
    manifest_path = MANIFEST_DIR / f"{path.stem}_thread_manifest.md"
    write_manifest(pairs, manifest_path)

    sections = split_headings(normalized)
    routed = route_sections(sections)

    write_distillation_report(path, pairs, routed)

def main() -> None:
    files = sorted([p for p in RAW_DIR.glob("*") if p.is_file()])
    if not files:
        raise SystemExit(f"No raw thread files found in: {RAW_DIR}")

    for path in files:
        process_file(path)

    build_graph()
    print("Thread distillation complete.")

if __name__ == "__main__":
    main()

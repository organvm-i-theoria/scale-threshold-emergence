#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path


PROJECT_ROOT = Path(os.environ["PROJECT_ROOT"])
DOC_DIRS = [
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "research",
    PROJECT_ROOT / "manifest",
    PROJECT_ROOT / "engine",
    PROJECT_ROOT / "atlas",
    PROJECT_ROOT / "governance",
    PROJECT_ROOT / "organvm_bridge",
]
OUT_FILE = PROJECT_ROOT / "knowledge_graph" / "graph_database.json"

PATTERNS = {
    "primitive": r"\bPR-\d{3}\b",
    "module": r"\bM-\d{2}\b",
    "threshold": r"\bTP-\d{2}\b",
    "mechanism": r"\bMECH-\d{3}\b",
    "glossary": r"\bGL-\d{3}\b",
    "thread": r"\bTH-\d{3}\b",
}


def main() -> None:
    nodes: dict[str, dict[str, str]] = {}
    edges: list[dict[str, str]] = []

    def add_node(node_id: str, node_type: str) -> None:
        if node_id not in nodes:
            nodes[node_id] = {"id": node_id, "type": node_type}

    for doc_dir in DOC_DIRS:
        if not doc_dir.exists():
            continue
        for path in doc_dir.rglob("*.md"):
            doc_id = str(path.relative_to(PROJECT_ROOT))
            add_node(doc_id, "document")
            text = path.read_text(encoding="utf-8")
            for node_type, pattern in PATTERNS.items():
                for match in sorted(set(re.findall(pattern, text))):
                    add_node(match, node_type)
                    edges.append(
                        {
                            "source": doc_id,
                            "target": match,
                            "relation": "mentions",
                        }
                    )

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps({"nodes": list(nodes.values()), "edges": edges}, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {OUT_FILE}")


if __name__ == "__main__":
    main()

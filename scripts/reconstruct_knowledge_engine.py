#!/usr/bin/env python3
"""
Knowledge Engine Repository Reconstruction Script

This script reconstructs the knowledge-engine repository from a ChatGPT transcript,
extracting all thread pairs, artifacts, and generating proper manifests.
"""

import json
import hashlib
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configuration
REPO_ROOT = Path("/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine")
SOURCE_FILE = (
    REPO_ROOT
    / "source_artifacts/raw/MASTER_transcript.json"
)


def compute_sha256(content: str) -> str:
    """Compute SHA256 hash of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_transcript() -> Dict[str, Any]:
    """Load the source transcript JSON."""
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_title_from_response(response: str, max_len: int = 50) -> str:
    """Extract a title slug from the response content."""
    # Look for common artifact introduction patterns
    patterns = [
        r"^(#{1,3}\s+(.+))",  # Markdown headers
        r"^([A-Z_]+\s+v\d+)",  # ALL_CAPS v1 style titles
        r"^Below is (.+?)\.",
    ]

    for pattern in patterns:
        match = re.match(pattern, response.strip(), re.MULTILINE)
        if match:
            title = match.group(1) if match.lastindex == 1 else match.group(2)
            title = re.sub(r"[#*]", "", title).strip()[:max_len]
            return title.replace(" ", "-").replace("/", "-").replace("\\", "-")

    # Fallback: first significant line
    lines = [
        l.strip()
        for l in response.strip().split("\n")
        if l.strip() and len(l.strip()) > 10
    ]
    if lines:
        return lines[0][:max_len].replace(" ", "-").replace("/", "-").replace("\\", "-")

    return "untitled"


def create_thread_pairs(messages: List[Dict]) -> List[Dict]:
    """Extract thread pairs from messages using proper Prompt->Response pairing."""
    pairs = []
    pair_id = 1
    i = 0
    
    while i < len(messages):
        # Find a Prompt
        while i < len(messages) and messages[i].get("role") != "Prompt":
            i += 1
        
        if i >= len(messages):
            break
        
        prompt_idx = i
        prompt_content = messages[i].get("say", "")
        
        # Find the next Response after this Prompt
        j = i + 1
        while j < len(messages) and messages[j].get("role") != "Response":
            j += 1
        
        if j >= len(messages):
            break  # No response for this prompt
        
        response_content = messages[j].get("say", "")
        
        pair = {
            "pair_id": f"TH-{pair_id:03d}",
            "pair_number": pair_id,
            "prompt_message_id": f"MSG-{prompt_idx + 1:03d}",
            "response_message_id": f"MSG-{j + 1:03d}",
            "prompt_sha256": compute_sha256(prompt_content),
            "response_sha256": compute_sha256(response_content),
            "title": extract_title_from_response(response_content),
            "prompt": prompt_content,
            "response": response_content,
            "source_indexes": [prompt_idx, j],
        }

        pairs.append(pair)
        pair_id += 1
        i = j + 1  # Move past this response

    return pairs


def extract_artifacts_from_response(pair: Dict) -> List[Dict]:
    """Extract named artifacts from a response."""
    artifacts = []
    response = pair["response"]
    pair_id = pair["pair_id"]

    # Known artifact patterns
    artifact_patterns = [
        (r"(Phase-?1?\s+Research\s+Matrix)", "research_matrix"),
        (r"(Research\s+Atlas)", "research_atlas"),
        (r"(Reading[_-]and[_-]Synthesis\s+Protocol)", "reading_protocol"),
        (r"(Phase-?1?\s+Master\s+Index)", "master_index"),
        (r"(Phase-?1?\s+Dependency\s+Graph)", "dependency_graph"),
        (r"(Kernel\s+Ontology\s+Charter)", "kernel_charter"),
        (r"(Primitive\s+Discovery\s+Registry)", "primitive_registry"),
        (r"(UNIVERSE_ENGINE_KERNEL_SPEC_v\d+)", "kernel_spec"),
        (r"(MODULE_API_SPEC_v\d+)", "module_api_spec"),
        (r"(WORLD_INSTANCE_SCHEMA_v\d+)", "world_instance_schema"),
        (r"(RESEARCH_DASHBOARD_v\d+)", "research_dashboard"),
        (r"(Threshold\s+Package\s+Library)", "threshold_library"),
        (r"(Mechanism\s+Registry)", "mechanism_registry"),
        (r"(Primitive\s+Canon)", "primitive_canon"),
        (r"(Lane\s+Governance\s+Charter)", "lane_governance"),
        (r"(Research\s+Pipeline)", "research_pipeline"),
        (r"(Phase-?2?\s+Deep\s+Research\s+Charter)", "phase2_charter"),
        (r"(Research\s+Lane\s+Syllabus)", "research_syllabus"),
        (r"(12\s+Mechanism\s+Families)", "mechanism_families"),
        (r"(Universal\s+Systems\s+Map)", "universal_systems_map"),
        (r"(Universal\s+Primitive\s+Graph)", "primitive_graph"),
        (r"(Transition\s+Atlas)", "transition_atlas"),
        (r"(Cross[_-]Lane\s+Primitive\s+Matrix)", "primitive_matrix"),
        (r"(Primitive\s+Interaction\s+Map)", "primitive_interaction"),
        (r"(Glossary\s+Draft\s+Pack)", "glossary_pack"),
    ]

    artifact_id = 1
    pair_num = pair["pair_number"]
    for pattern, artifact_type in artifact_patterns:
        matches = re.finditer(pattern, response, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            artifact_name = match.group(1)
            artifacts.append(
                {
                    "artifact_id": f"ART-{pair_num:03d}-{artifact_id:03d}",
                    "source_pair_id": pair["pair_id"],
                    "name": artifact_name,
                    "type": artifact_type,
                    "title": artifact_name,
                    "content": response,  # Full response as artifact content
                }
            )
            artifact_id += 1

    return artifacts


def create_thread_pair_file(pair: Dict, output_dir: Path) -> Path:
    """Create a markdown file for a thread pair."""
    filename = f"{pair['pair_id']}-{pair['title']}.md"
    filepath = output_dir / filename

    content = f"""---
pair_id: {pair["pair_id"]}
pair_number: {pair["pair_number"]}
title: "{pair["title"]}"
prompt_message_id: {pair["prompt_message_id"]}
response_message_id: {pair["response_message_id"]}
source_indexes:
  - {pair["source_indexes"][0]}
  - {pair["source_indexes"][1]}
pair_sha256: {pair["prompt_sha256"][:16]}...{pair["response_sha256"][:16]}
generated_at: {datetime.utcnow().isoformat()}Z
---

# {pair["pair_id"]} — {pair["title"]}

## Prompt

{pair["prompt"]}

## Response

{pair["response"]}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def main():
    """Main reconstruction function."""
    print("=" * 60)
    print("Knowledge Engine Repository Reconstruction")
    print("=" * 60)

    # Load transcript
    print(f"\n[1/6] Loading transcript from {SOURCE_FILE}...")
    transcript = load_transcript()
    messages = transcript.get("messages", [])
    print(f"      Found {len(messages)} messages")

    # Extract thread pairs
    print(f"\n[2/6] Extracting thread pairs...")
    pairs = create_thread_pairs(messages)
    print(f"      Extracted {len(pairs)} thread pairs")

    # Create thread pair directory
    thread_pairs_dir = REPO_ROOT / "research" / "thread_pairs"
    thread_pairs_dir.mkdir(parents=True, exist_ok=True)

    # Write thread pair files
    print(f"\n[3/6] Writing thread pair files...")
    for pair in pairs:
        create_thread_pair_file(pair, thread_pairs_dir)
    print(f"      Wrote {len(pairs)} thread pair files")

    # Extract artifacts
    print(f"\n[4/6] Extracting artifacts...")
    all_artifacts = []
    for pair in pairs:
        artifacts = extract_artifacts_from_response(pair)
        all_artifacts.extend(artifacts)
    print(f"      Found {len(all_artifacts)} artifact references")

    # Generate manifests
    print(f"\n[5/6] Generating manifests...")

    # Chat pair manifest
    chat_pair_manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_file": str(SOURCE_FILE),
        "source_sha256": compute_sha256(json.dumps(transcript)),
        "total_pairs": len(pairs),
        "pairs": [
            {
                "pair_id": p["pair_id"],
                "pair_number": p["pair_number"],
                "title": p["title"],
                "prompt_sha256": p["prompt_sha256"],
                "response_sha256": p["response_sha256"],
            }
            for p in pairs
        ],
    }

    manifest_path = REPO_ROOT / "manifest" / "chat_pair_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(chat_pair_manifest, f, indent=2)
    print(f"      Written chat_pair_manifest.json")

    # Integrity manifest
    integrity_manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source_sha256": compute_sha256(json.dumps(transcript)),
        "message_count": len(messages),
        "pair_count": len(pairs),
        "messages": [
            {
                "message_id": f"MSG-{i + 1:03d}",
                "index": i,
                "role": msg.get("role"),
                "sha256": compute_sha256(msg.get("say", "")),
                "char_count": len(msg.get("say", "")),
            }
            for i, msg in enumerate(messages)
        ],
    }

    integrity_path = REPO_ROOT / "manifest" / "integrity_manifest.json"
    with open(integrity_path, "w") as f:
        json.dump(integrity_manifest, f, indent=2)
    print(f"      Written integrity_manifest.json")

    # Artifact manifest
    artifact_manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_artifacts": len(all_artifacts),
        "artifacts": all_artifacts,
    }

    artifact_path = REPO_ROOT / "manifest" / "artifact_manifest.json"
    with open(artifact_path, "w") as f:
        json.dump(artifact_manifest, f, indent=2)
    print(f"      Written artifact_manifest.json")

    print(f"\n[6/6] Reconstruction complete!")
    print(f"      Thread pairs: {len(pairs)}")
    print(f"      Artifacts found: {len(all_artifacts)}")
    print(f"      Manifests generated: 3")
    print("=" * 60)


if __name__ == "__main__":
    main()

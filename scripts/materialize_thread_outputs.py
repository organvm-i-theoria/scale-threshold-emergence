#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ENV_TARGET_ROOTS = {
    "PROJECT_ROOT": Path(),
    "DOCS_DIR": Path("docs"),
    "RESEARCH_DIR": Path("research"),
    "GRAPH_DIR": Path("knowledge_graph"),
    "ENGINE_DIR": Path("engine"),
    "EXPERIMENTS_DIR": Path("experiments"),
    "MANIFEST_DIR": Path("manifest"),
    "DATA_DIR": Path("data"),
    "SCRIPTS_DIR": Path("scripts"),
    "INGEST_DIR": Path("ingestion"),
    "LIBRARY_DIR": Path("library"),
    "HANDOFF_DIR": Path("handoff"),
    "GOVERNANCE_DIR": Path("governance"),
    "ATLAS_DIR": Path("atlas"),
    "ORGANVM_DIR": Path("organvm_bridge"),
}

SEED_TARGETS = {
    ".env.example",
    "mkdocs.yml",
    "handoff/ai_handoff_prompt.md",
    "experiments/experiment_log.md",
    "research/reports/annotated_bibliography.md",
    "knowledge_graph/graph_schema.md",
    "governance/change_proposal_registry.md",
    "engine/runtime/process_node_schema.md",
    "engine/runtime/parameter_system_spec.md",
    "engine/runtime/law_profile_spec.md",
    "engine/runtime/runtime_scheduler_spec.md",
    "engine/runtime/provenance_logging_spec.md",
}

ARTIFACT_TARGETS = {
    "docs/primitive_canon.md": "engine/primitives/ART-038-primitive-canon-v1.md",
    "docs/module_library.md": "atlas/artifacts/ART-019-system-architecture-seed-modules.md",
    "docs/threshold_atlas.md": "engine/thresholds/ART-022-transition-atlas.md",
    "docs/mechanism_registry.md": "engine/mechanisms/ART-039-mechanism-registry-v1.md",
    "docs/computational_patterns.md": "governance/artifacts/ART-042-not-object-types-not-domain-specific-subsystems-patterns.md",
    "docs/kernel_spec.md": "engine/runtime/ART-043-universe-engine-kernel-spec-v0.md",
    "docs/module_api.md": "engine/modules/ART-044-module-api-spec-v1.md",
    "docs/world_instance_schema.md": "engine/worlds/ART-045-world-instance-schema-v1.md",
    "docs/three_pillar_model.md": "atlas/artifacts/ART-064-the-three-pillars-as-knowledge-engines.md",
    "research/dashboards/research_dashboard.md": "engine/mechanisms/ART-046-research-dashboard-v1.md",
    "research/indexes/core_reading_library.md": "organvm_bridge/artifacts/ART-047-below-is-the-phase-1-launch-reading-set-30-texts.md",
    "research/indexes/mechanism_extraction_template.md": "engine/mechanisms/ART-048-mechanism-extraction-template-v1.md",
    "research/indexes/research_pipeline.md": "atlas/artifacts/ART-058-below-is-the-research-pipeline-r0-r6-that-operationalizes-the-entire-research-phase.md",
    "research/indexes/lane_governance_charter.md": "governance/artifacts/ART-060-lane-governance-charter-v1.md",
    "atlas/organvm_system_atlas.md": "atlas/artifacts/ART-076-the-single-most-stabilizing-repository-that-organvm-does-not-yet-clearly-have-is-something-like.md",
    "organvm_bridge/theoria_integration_brief.md": "organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md",
    "governance/reflexive_change_governance.md": "organvm_bridge/artifacts/ART-071-the-core-principle.md",
}

SECOND_RING_REQUIRED_PATHS = {
    "research/open_problems/open_problem_register.md",
    "governance/primitive_revision_protocol.md",
    "governance/mechanism_review_process.md",
    "governance/threshold_review_cycle.md",
    "governance/annual_framework_review.md",
    "organvm_bridge/knowledge_supply_chain.md",
    "atlas/repo_index.json",
    "atlas/dependency_graph.md",
    "atlas/promotion_state_dashboard.md",
    "knowledge_graph/graph_query_library.md",
    "manifest/distillation_report.md",
    "engine/runtime/mechanism_pack_spec.md",
    "engine/runtime/cross_scale_coupling_spec.md",
    "docs/public_research_archive.md",
    "docs/technical_whitepaper_01.md",
    "docs/simulation_demo_01.md",
    "docs/creative_output_trace_template.md",
}

NORMALIZE_THREAD_SCRIPT = """#!/usr/bin/env python3
import os
import re
from pathlib import Path


PROJECT_ROOT = Path(os.environ["PROJECT_ROOT"])
RAW_DIR = PROJECT_ROOT / "ingestion" / "raw_threads"
OUT_DIR = PROJECT_ROOT / "ingestion" / "normalized_threads"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(text: str) -> str:
    text = text.replace("\\r\\n", "\\n").replace("\\r", "\\n")
    text = re.sub(r"\\n{3,}", "\\n\\n", text)
    text = re.sub(r"[ \\t]+$", "", text, flags=re.MULTILINE)
    return text.strip() + "\\n"


def main() -> None:
    for path in RAW_DIR.glob("*"):
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        normalized = normalize_text(raw)
        out_path = OUT_DIR / path.name
        out_path.write_text(normalized, encoding="utf-8")
        print(f"normalized: {out_path}")


if __name__ == "__main__":
    main()
"""

BUILD_GRAPH_SCRIPT = """#!/usr/bin/env python3
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
    "primitive": r"\\bPR-\\d{3}\\b",
    "module": r"\\bM-\\d{2}\\b",
    "threshold": r"\\bTP-\\d{2}\\b",
    "mechanism": r"\\bMECH-\\d{3}\\b",
    "glossary": r"\\bGL-\\d{3}\\b",
    "thread": r"\\bTH-\\d{3}\\b",
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
    OUT_FILE.write_text(json.dumps({"nodes": list(nodes.values()), "edges": edges}, indent=2) + "\\n", encoding="utf-8")
    print(f"wrote: {OUT_FILE}")


if __name__ == "__main__":
    main()
"""

RUN_DISTILL_SCRIPT = """#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ROOT:?Set PROJECT_ROOT first}"

python3 "${PROJECT_ROOT}/scripts/normalize_thread.py"
python3 "${PROJECT_ROOT}/scripts/distill_thread.py"
python3 "${PROJECT_ROOT}/scripts/build_graph.py"

echo "Distillation and graph build complete."
"""

INIT_GIT_SCRIPT = """#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ROOT:?Set PROJECT_ROOT first}"

cd "${PROJECT_ROOT}"

if [ ! -d .git ]; then
  git init
fi

git add .
git commit -m "bootstrap universe engine research repository v2" || true
"""

BOOTSTRAP_SCRIPT = """#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

python3 "${SCRIPT_DIR}/materialize_thread_outputs.py" --repo-root "${PROJECT_ROOT}"
printf "Materialized thread-defined outputs in: %s\\n" "${PROJECT_ROOT}"
"""


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def extract_response_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    marker = "\n## Response\n\n"
    if marker not in text:
        raise ValueError(f"Response marker not found in {path}")
    body = text.split(marker, 1)[1].lstrip()
    lines = body.splitlines()
    if lines and re.fullmatch(r"Thought for \d+s", lines[0].strip()):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines).rstrip() + "\n"


def parse_seed_blocks(response_body: str) -> dict[str, str]:
    pattern = re.compile(
        r'^cat > "\$\{(?P<var>[A-Z_]+)\}/(?P<rel>[^"]+)" <<\'EOF\'\n(?P<content>.*?)(?=^EOF$)',
        re.MULTILINE | re.DOTALL,
    )
    blocks: dict[str, str] = {}
    for match in pattern.finditer(response_body):
        env_var = match.group("var")
        rel_path = match.group("rel")
        if env_var not in ENV_TARGET_ROOTS:
            continue
        target = ENV_TARGET_ROOTS[env_var] / rel_path
        blocks[str(target)] = match.group("content").rstrip() + "\n"
    return blocks


def extract_distill_script(response_body: str) -> str:
    match = re.search(
        r"^#!/usr/bin/env python3\n.*?(?=^Save this runner too as:)",
        response_body,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError("Could not extract distill_thread.py from TH-051 response")
    return match.group(0).rstrip() + "\n"


def render_markdown_document(
    *,
    doc_id: str,
    title: str,
    doc_type: str,
    status: str,
    source_artifacts: list[str],
    body: str,
) -> str:
    source_lines = "\n".join(f"  - {artifact}" for artifact in source_artifacts)
    return (
        "---\n"
        f"id: {doc_id}\n"
        f"title: {json.dumps(title)}\n"
        f"type: {doc_type}\n"
        f"status: {status}\n"
        "version: 1\n"
        "source_artifacts:\n"
        f"{source_lines}\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{body.rstrip()}\n"
    )


def render_placeholder_document(
    *,
    doc_id: str,
    title: str,
    doc_type: str,
    purpose: str,
    source_artifacts: list[str],
) -> str:
    body = (
        f"Purpose: {purpose}\n\n"
        "Status: placeholder\n\n"
        "This artifact was named in the close-out inventory but was not fully drafted in the source thread.\n\n"
        "Suggested next sections:\n\n"
        "- Purpose and boundary\n"
        "- Required inputs\n"
        "- Canonical structure\n"
        "- Provenance and integrity requirements\n"
        "- Open decisions\n"
    )
    return render_markdown_document(
        doc_id=doc_id,
        title=title,
        doc_type=doc_type,
        status="placeholder",
        source_artifacts=source_artifacts,
        body=body,
    )


def build_second_ring_documents(repo_root: Path) -> dict[str, dict[str, Any]]:
    materialized_from = "manifest/artifacts/ART-077-a-updated-automated-repository-generator-script.md"
    second_ring: dict[str, dict[str, Any]] = {}

    second_ring["research/open_problems/open_problem_register.md"] = {
        "mode": "derived_from_research_dashboard",
        "source_artifacts": [
            "engine/mechanisms/ART-046-research-dashboard-v1.md",
            "governance/artifacts/ART-037-below-is-the-realistic-assessment.md",
        ],
        "content": render_markdown_document(
            doc_id="open_problem_register_v1",
            title="Open Problem Register",
            doc_type="research-register",
            status="derived_from_thread",
            source_artifacts=[
                "engine/mechanisms/ART-046-research-dashboard-v1.md",
                "governance/artifacts/ART-037-below-is-the-realistic-assessment.md",
            ],
            body=(
                "The research dashboard explicitly names the open problem register as one of the six major sections in the live program view.\n\n"
                "Every research report should add open problems so unresolved questions become first-class tracked objects rather than buried prose.\n\n"
                "Required fields:\n\n"
                "| Field | Meaning |\n"
                "| --- | --- |\n"
                "| open_problem_id | Stable identifier |\n"
                "| source_artifact_id | Reading, note, report, or mechanism that surfaced the problem |\n"
                "| lane | Research lane or threshold package affected |\n"
                "| description | The unresolved question in atomic form |\n"
                "| blocking_scope | What downstream artifact or experiment is blocked |\n"
                "| next_evidence | What reading, dataset, or experiment would reduce uncertainty |\n"
                "| status | open / active / deferred / retired |\n\n"
                "Operational rule:\n\n"
                "- Every synthesis report should emit zero or more open problem records.\n"
                "- Open problems stay linked to provenance and should feed the dashboard, lane tracker, and future mechanism work.\n"
            ),
        ),
    }

    second_ring["governance/primitive_revision_protocol.md"] = {
        "mode": "derived_from_primitive_canon",
        "source_artifacts": [
            "docs/primitive_canon.md",
            "governance/artifacts/ART-035-research-institute-operating-model.md",
        ],
        "content": render_markdown_document(
            doc_id="primitive_revision_protocol_v1",
            title="Primitive Revision Protocol",
            doc_type="governance-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "docs/primitive_canon.md",
                "governance/artifacts/ART-035-research-institute-operating-model.md",
            ],
            body=(
                "Primitive definitions should change only rarely and only through formal revision.\n\n"
                "Primitive revisions require:\n\n"
                "- proposal\n"
                "- literature justification\n"
                "- cross-lane review\n"
                "- version update\n\n"
                "Review cadence:\n\n"
                "- The institute performs periodic framework revision, including yearly review of the primitive set.\n"
                "- Structural revisions happen more slowly than ordinary knowledge updates.\n\n"
                "Adoption rule:\n\n"
                "- A primitive proposal remains pending until cross-lane review confirms that the change improves coherence rather than introducing vocabulary drift.\n"
                "- Accepted revisions advance the canon version (`Primitive Canon v1`, `Primitive Canon v2`, and so on).\n"
            ),
        ),
    }

    second_ring["governance/mechanism_review_process.md"] = {
        "mode": "derived_from_mechanism_discipline_protocol",
        "source_artifacts": [
            "governance/artifacts/ART-056-preventing-that-outcome-requires-a-mechanism-discipline-protocol-before-the-literature-review-begins.md"
        ],
        "content": render_markdown_document(
            doc_id="mechanism_review_process_v1",
            title="Mechanism Review Process",
            doc_type="governance-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "governance/artifacts/ART-056-preventing-that-outcome-requires-a-mechanism-discipline-protocol-before-the-literature-review-begins.md"
            ],
            body=(
                "The mechanism review process is the registry admission path that prevents mechanism explosion.\n\n"
                "Control flow:\n\n"
                "candidate mechanism\n"
                "→ normalization\n"
                "→ primitive mapping\n"
                "→ merge test\n"
                "→ threshold placement\n"
                "→ registry admission\n\n"
                "Admission rules:\n\n"
                "- A mechanism must be a reproducible process that transforms inputs into outputs through identifiable steps.\n"
                "- It must map cleanly to the primitive canon.\n"
                "- It must pass the merge test so variants do not inflate the registry.\n"
                "- It must anchor to a threshold transition.\n"
                "- It must satisfy the evidence gate or remain in the speculative pool.\n\n"
                "Expected outcome:\n\n"
                "- With discipline, the registry stabilizes around 40–80 core mechanisms.\n"
                "- Without discipline, it drifts toward hundreds of loosely defined entries and becomes unusable.\n"
            ),
        ),
    }

    second_ring["governance/threshold_review_cycle.md"] = {
        "mode": "derived_from_threshold_packages",
        "source_artifacts": [
            "engine/thresholds/ART-023-threshold-package-library.md",
            "governance/artifacts/ART-035-research-institute-operating-model.md",
        ],
        "content": render_markdown_document(
            doc_id="threshold_review_cycle_v1",
            title="Threshold Review Cycle",
            doc_type="governance-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "engine/thresholds/ART-023-threshold-package-library.md",
                "governance/artifacts/ART-035-research-institute-operating-model.md",
            ],
            body=(
                "Threshold packages are reusable transition schemas, but they also carry revision norms and must be reviewed as the research program matures.\n\n"
                "Minimum review cadence:\n\n"
                "- Yearly framework review includes threshold definitions.\n"
                "- Earlier review is triggered when a lane produces contradictory mechanism evidence or repeated collapse conditions.\n\n"
                "Review checklist:\n\n"
                "- Reconfirm the lower-order and higher-order regimes.\n"
                "- Verify enabling primitives and activating modules still match the canon.\n"
                "- Re-evaluate stabilization and collapse conditions.\n"
                "- Record whether the package remains descriptive only or is ready to become a design pattern for simulation.\n"
            ),
        ),
    }

    second_ring["governance/annual_framework_review.md"] = {
        "mode": "derived_from_research_institute_model",
        "source_artifacts": [
            "governance/artifacts/ART-035-research-institute-operating-model.md"
        ],
        "content": render_markdown_document(
            doc_id="annual_framework_review_v1",
            title="Annual Framework Review",
            doc_type="governance-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "governance/artifacts/ART-035-research-institute-operating-model.md"
            ],
            body=(
                "The annual framework review is the slow-cycle structural audit for the research institute.\n\n"
                "Every year the institute reviews:\n\n"
                "- primitive set\n"
                "- module architecture\n"
                "- threshold definitions\n\n"
                "The goal is not continuous redesign. The goal is to allow deliberate structural change without locking the software and research program into premature assumptions.\n\n"
                "Practical implementation rhythm:\n\n"
                "- weekly reading sessions\n"
                "- monthly synthesis drafts\n"
                "- quarterly research reports\n"
                "- annual framework revision\n"
            ),
        ),
    }

    second_ring["organvm_bridge/knowledge_supply_chain.md"] = {
        "mode": "derived_from_organvm_integration",
        "source_artifacts": [
            "organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md"
        ],
        "content": render_markdown_document(
            doc_id="knowledge_supply_chain_v1",
            title="Knowledge Supply Chain",
            doc_type="integration-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md"
            ],
            body=(
                "The missing automation layer identified in the thread is the knowledge supply chain that moves discoveries from Theoria into Poiesis and then into Ergon.\n\n"
                "Canonical flow:\n\n"
                "Theoria\n"
                "↓\n"
                "Poiesis\n"
                "↓\n"
                "Ergon\n\n"
                "Governance organs orchestrate the flow. The research system strengthens organvm by turning discoveries into portable artifacts, simulation demonstrations, and product-ready downstream knowledge without introducing back-edges.\n"
            ),
        ),
    }

    second_ring["atlas/dependency_graph.md"] = {
        "mode": "derived_from_organvm_design_brief",
        "source_artifacts": [
            "organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md",
            "organvm_bridge/artifacts/ART-070-design-brief.md",
        ],
        "content": render_markdown_document(
            doc_id="dependency_graph_v1",
            title="Dependency Graph",
            doc_type="atlas-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md",
                "organvm_bridge/artifacts/ART-070-design-brief.md",
            ],
            body=(
                "The organism uses a directed dependency graph with strict flow constraints.\n\n"
                "Primary production flow:\n\n"
                "- Theory (I) → Art (II) → Commerce (III)\n\n"
                "Governance organs operate laterally and coordinate orchestration, publication, community, distribution, and meta-mapping without introducing circular dependencies.\n\n"
                "Architectural law:\n\n"
                "- No back-edges exist in the dependency graph.\n"
                "- Commerce cannot reach back into Art for runtime dependencies.\n"
                "- Art cannot reach back into Theory.\n"
            ),
        ),
    }

    second_ring["atlas/promotion_state_dashboard.md"] = {
        "mode": "derived_from_organvm_design_brief",
        "source_artifacts": [
            "organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md"
        ],
        "content": render_markdown_document(
            doc_id="promotion_state_dashboard_v1",
            title="Promotion State Dashboard",
            doc_type="atlas-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md"
            ],
            body=(
                "Promotion is a state machine. Repositories move through explicit states rather than ad hoc upgrades.\n\n"
                "Canonical states:\n\n"
                "- LOCAL\n"
                "- CANDIDATE\n"
                "- PUBLIC_PROCESS\n"
                "- GRADUATED\n"
                "- ARCHIVED\n\n"
                "Dashboard purpose:\n\n"
                "- show current state per repository\n"
                "- track promotion criteria and blockers\n"
                "- keep the organism legible at portfolio scale\n"
            ),
        ),
    }

    second_ring["engine/runtime/mechanism_pack_spec.md"] = {
        "mode": "derived_from_kernel_spec",
        "source_artifacts": ["docs/kernel_spec.md"],
        "content": render_markdown_document(
            doc_id="mechanism_pack_spec_v1",
            title="Mechanism Pack Spec",
            doc_type="technical-spec",
            status="derived_from_thread",
            source_artifacts=["docs/kernel_spec.md"],
            body=(
                "A mechanism pack is how literature becomes executable theory.\n\n"
                "Required fields:\n\n"
                "| Field | Meaning |\n"
                "| --- | --- |\n"
                "| mechanism_pack_id | implementation ID |\n"
                "| source_mechanism_id | canonical registry linkage |\n"
                "| target_threshold_id | threshold served |\n"
                "| required_modules | module dependencies |\n"
                "| required_primitives | conceptual dependencies |\n"
                "| law_profile_compatibility | which worlds can host it |\n"
                "| parameter_defaults | default settings |\n"
                "| runtime_operators | executable behaviors |\n"
                "| evidence_note | empirical or theoretical basis |\n"
                "| revision_status | provisional / stable / deprecated |\n\n"
                "Comparative modeling rule:\n\n"
                "- A single threshold can host multiple competing mechanism packs so the engine remains a research instrument rather than a single locked interpretation.\n"
            ),
        ),
    }

    second_ring["engine/runtime/cross_scale_coupling_spec.md"] = {
        "mode": "derived_from_universe_engine_architecture",
        "source_artifacts": [
            "governance/artifacts/ART-036-universe-engine-computational-architecture.md"
        ],
        "content": render_markdown_document(
            doc_id="cross_scale_coupling_spec_v1",
            title="Cross-Scale Coupling Spec",
            doc_type="technical-spec",
            status="derived_from_thread",
            source_artifacts=[
                "governance/artifacts/ART-036-universe-engine-computational-architecture.md"
            ],
            body=(
                "Each pattern class in the universe engine requires explicit cross-scale coupling rules.\n\n"
                "Pattern-level requirements:\n\n"
                "- identity conditions\n"
                "- stability conditions\n"
                "- transition rules\n"
                "- interaction surfaces\n"
                "- decay / mutation rules\n"
                "- cross-scale coupling rules\n\n"
                "Scale layer:\n\n"
                "- micro\n"
                "- meso\n"
                "- macro\n"
                "- meta\n\n"
                "The same module may behave differently at different scales even when the formal logic is homologous. Coupling rules therefore have to declare how behavior translates across scale boundaries.\n"
            ),
        ),
    }

    second_ring["docs/public_research_archive.md"] = {
        "mode": "derived_from_research_institute_model",
        "source_artifacts": [
            "governance/artifacts/ART-035-research-institute-operating-model.md"
        ],
        "content": render_markdown_document(
            doc_id="public_research_archive_v1",
            title="Public Research Archive",
            doc_type="public-artifact",
            status="derived_from_thread",
            source_artifacts=[
                "governance/artifacts/ART-035-research-institute-operating-model.md"
            ],
            body=(
                "The thread names the public research archive as one of the three long-term outputs of the institute alongside the theory framework and the simulation system.\n\n"
                "Purpose:\n\n"
                "- preserve structured public-facing releases of readings, notes, reports, and mechanism work\n"
                "- make the evolving framework visible without sacrificing provenance\n"
                "- strengthen the theory and simulation layers through transparent publication\n"
            ),
        ),
    }

    second_ring["knowledge_graph/graph_query_library.md"] = {
        "mode": "seeded_from_graph_schema",
        "source_artifacts": [
            "knowledge_graph/graph_schema.md",
            "knowledge_graph/graph_database.json",
        ],
        "content": render_markdown_document(
            doc_id="graph_query_library_v1",
            title="Graph Query Library",
            doc_type="graph-spec",
            status="seeded",
            source_artifacts=[
                "knowledge_graph/graph_schema.md",
                "knowledge_graph/graph_database.json",
            ],
            body=(
                "This library standardizes recurring graph queries over the reconstructed thread graph.\n\n"
                "Seed query set:\n\n"
                "1. Show all documents that mention a given primitive ID.\n"
                "2. Show all documents that mention a given mechanism ID.\n"
                "3. Trace every thread pair that fed a given canonical document.\n"
                "4. List threshold IDs referenced by a given module or runtime spec.\n"
                "5. Show governance artifacts that mention versioning, review, or revision.\n"
            ),
        ),
    }

    second_ring["docs/technical_whitepaper_01.md"] = {
        "mode": "placeholder_from_close_out_inventory",
        "source_artifacts": [materialized_from],
        "content": render_placeholder_document(
            doc_id="technical_whitepaper_01_v1",
            title="Technical Whitepaper 01",
            doc_type="public-artifact",
            purpose="First scholarly output packaging the theory, simulation, and provenance model for public review.",
            source_artifacts=[materialized_from],
        ),
    }

    second_ring["docs/simulation_demo_01.md"] = {
        "mode": "placeholder_from_close_out_inventory",
        "source_artifacts": [materialized_from],
        "content": render_placeholder_document(
            doc_id="simulation_demo_01_v1",
            title="Simulation Demo 01",
            doc_type="public-artifact",
            purpose="First demonstration artifact linking mechanism packs, runtime parameters, and evaluation traces.",
            source_artifacts=[materialized_from],
        ),
    }

    second_ring["docs/creative_output_trace_template.md"] = {
        "mode": "placeholder_from_close_out_inventory",
        "source_artifacts": [materialized_from],
        "content": render_placeholder_document(
            doc_id="creative_output_trace_template_v1",
            title="Creative Output Trace Template",
            doc_type="public-artifact",
            purpose="Trace template for connecting creative outputs back to mechanisms, models, and provenance.",
            source_artifacts=[materialized_from],
        ),
    }

    repo_index = build_repo_index(repo_root)
    second_ring["atlas/repo_index.json"] = {
        "mode": "derived_from_repo_tree",
        "source_artifacts": ["manifest/materialized_outputs_manifest.json"],
        "content": json.dumps(repo_index, indent=2) + "\n",
    }

    second_ring["manifest/distillation_report.md"] = {
        "mode": "derived_from_manifests",
        "source_artifacts": [
            "manifest/thread_manifest.json",
            "manifest/pair_manifest.json",
            "manifest/artifact_manifest.json",
            "manifest/materialized_outputs_manifest.json",
        ],
        "content": build_distillation_report(repo_root, second_ring),
    }

    return second_ring


def build_repo_index(repo_root: Path) -> dict[str, Any]:
    top_level_dirs = sorted(path.name for path in repo_root.iterdir() if path.is_dir() and not path.name.startswith("."))
    markdown_files = list(repo_root.rglob("*.md"))
    json_files = list(repo_root.rglob("*.json"))
    script_files = list((repo_root / "scripts").glob("*")) if (repo_root / "scripts").exists() else []
    return {
        "id": "repo_index_v1",
        "title": "Repository Index",
        "repo_root": str(repo_root),
        "top_level_directories": top_level_dirs,
        "counts": {
            "markdown_files": len(markdown_files),
            "json_files": len(json_files),
            "script_entries": len([path for path in script_files if path.is_file()]),
        },
    }


def build_distillation_report(repo_root: Path, second_ring: dict[str, dict[str, Any]]) -> str:
    thread_manifest = json.loads((repo_root / "manifest/thread_manifest.json").read_text(encoding="utf-8"))
    pair_manifest = json.loads((repo_root / "manifest/pair_manifest.json").read_text(encoding="utf-8"))
    artifact_manifest = json.loads((repo_root / "manifest/artifact_manifest.json").read_text(encoding="utf-8"))
    artifact_count = (
        artifact_manifest["total_artifacts"] if isinstance(artifact_manifest, dict) else len(artifact_manifest)
    )
    materialized_path = repo_root / "manifest/materialized_outputs_manifest.json"
    if materialized_path.exists():
        existing_materialized = json.loads(materialized_path.read_text(encoding="utf-8"))
        prior_materialized_count = existing_materialized["materialized_count"]
    else:
        prior_materialized_count = 0

    body = (
        f"Generated from the authoritative source thread: `{thread_manifest['source_path']}`.\n\n"
        "Current distillation state:\n\n"
        f"- thread title: {thread_manifest['title']}\n"
        f"- prompt-response pairs: {len(pair_manifest)}\n"
        f"- extracted artifact records: {artifact_count}\n"
        f"- prior materialized outputs: {prior_materialized_count}\n"
        f"- second-ring outputs materialized in this pass: {len(SECOND_RING_REQUIRED_PATHS)}\n\n"
        "This report exists to bridge the raw archival layer and the runnable repository layer. It records that the close-out pack's first-ring canonical files are already present and that the second-ring follow-on artifacts were promoted into explicit files in this pass.\n"
    )
    return render_markdown_document(
        doc_id="distillation_report_v1",
        title="Distillation Report",
        doc_type="archive-manifest",
        status="active",
        source_artifacts=[
            "manifest/thread_manifest.json",
            "manifest/pair_manifest.json",
            "manifest/artifact_manifest.json",
            "manifest/materialized_outputs_manifest.json",
        ],
        body=body,
    )


def write_file(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    status = "updated" if path.exists() else "created"
    path.write_text(content, encoding="utf-8")
    return status


def build_thread_manifest_md(repo_root: Path) -> str:
    pair_manifest = json.loads((repo_root / "manifest/pair_manifest.json").read_text(encoding="utf-8"))
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
        "| Pair ID | Title | Pair Path |",
        "| --- | --- | --- |",
    ]
    for pair in pair_manifest:
        lines.append(f"| {pair['pair_id']} | {pair['title']} | `{pair['pair_path']}` |")
    return "\n".join(lines) + "\n"


def build_graph_database(repo_root: Path) -> str:
    nodes = json.loads((repo_root / "knowledge_graph/nodes.json").read_text(encoding="utf-8"))
    edges = json.loads((repo_root / "knowledge_graph/edges.json").read_text(encoding="utf-8"))
    return json.dumps({"nodes": nodes, "edges": edges}, indent=2) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Materialize the thread-defined canonical file layer.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    art077 = repo_root / "manifest/artifacts/ART-077-a-updated-automated-repository-generator-script.md"
    th051 = repo_root / "ingestion/artifacts/ART-051-below-is-the-thread-distiller-script-that-takes-a-raw-chatgpt-transcript-and-turns-it-into-seeded-repository-artifacts.md"
    seed_blocks = parse_seed_blocks(extract_response_body(art077))

    manifest_entries: list[dict[str, Any]] = []

    for rel_path in sorted(SEED_TARGETS):
        if rel_path not in seed_blocks:
            raise ValueError(f"Seed block not found for {rel_path}")
        status = write_file(repo_root / rel_path, seed_blocks[rel_path])
        manifest_entries.append(
            {
                "target_path": rel_path,
                "mode": "seed_block_from_art077",
                "source_artifacts": [str(art077.relative_to(repo_root))],
                "status": status,
            }
        )

    for rel_path, artifact_rel in sorted(ARTIFACT_TARGETS.items()):
        source_path = repo_root / artifact_rel
        status = write_file(repo_root / rel_path, extract_response_body(source_path))
        manifest_entries.append(
            {
                "target_path": rel_path,
                "mode": "full_response_overlay",
                "source_artifacts": [artifact_rel],
                "status": status,
            }
        )

    script_targets = {
        "scripts/normalize_thread.py": NORMALIZE_THREAD_SCRIPT,
        "scripts/build_graph.py": BUILD_GRAPH_SCRIPT,
        "scripts/distill_thread.py": extract_distill_script(extract_response_body(th051)),
        "scripts/run_distill.sh": RUN_DISTILL_SCRIPT,
        "scripts/init_git.sh": INIT_GIT_SCRIPT,
        "scripts/bootstrap_universe_repo_v2.sh": BOOTSTRAP_SCRIPT,
    }

    for rel_path, content in script_targets.items():
        status = write_file(repo_root / rel_path, content)
        manifest_entries.append(
            {
                "target_path": rel_path,
                "mode": "script_materialization",
                "source_artifacts": [
                    str(th051.relative_to(repo_root)) if rel_path.endswith("distill_thread.py") else str(art077.relative_to(repo_root))
                ],
                "status": status,
            }
        )

    for rel_path in [
        "data",
        "library",
        "handoff",
        "experiments/sandbox",
        "research/dashboards",
        "research/indexes",
        "research/reports",
        "research/reading_notes",
        "research/mechanism_extractions",
        "research/lanes",
        "research/open_problems",
        "ingestion/raw_threads",
        "ingestion/normalized_threads",
        "ingestion/manifests",
        "ingestion/logs",
    ]:
        (repo_root / rel_path).mkdir(parents=True, exist_ok=True)

    status = write_file(repo_root / "manifest/thread_manifest.md", build_thread_manifest_md(repo_root))
    manifest_entries.append(
        {
            "target_path": "manifest/thread_manifest.md",
            "mode": "derived_from_pair_manifest",
            "source_artifacts": ["manifest/pair_manifest.json"],
            "status": status,
        }
    )

    status = write_file(repo_root / "knowledge_graph/graph_database.json", build_graph_database(repo_root))
    manifest_entries.append(
        {
            "target_path": "knowledge_graph/graph_database.json",
            "mode": "derived_from_nodes_and_edges",
            "source_artifacts": ["knowledge_graph/nodes.json", "knowledge_graph/edges.json"],
            "status": status,
        }
    )

    second_ring_documents = build_second_ring_documents(repo_root)
    for rel_path, payload in sorted(second_ring_documents.items()):
        status = write_file(repo_root / rel_path, payload["content"])
        manifest_entries.append(
            {
                "target_path": rel_path,
                "mode": payload["mode"],
                "source_artifacts": payload["source_artifacts"],
                "status": status,
            }
        )

    second_ring_manifest = {
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "required_count": len(SECOND_RING_REQUIRED_PATHS),
        "materialized_count": len(second_ring_documents),
        "fully_materialized": sorted(second_ring_documents),
    }
    status = write_file(
        repo_root / "manifest/second_ring_artifacts_manifest.json",
        json.dumps(second_ring_manifest, indent=2) + "\n",
    )
    manifest_entries.append(
        {
            "target_path": "manifest/second_ring_artifacts_manifest.json",
            "mode": "derived_from_second_ring_materialization",
            "source_artifacts": sorted(second_ring_documents),
            "status": status,
        }
    )

    for rel_path in [
        "scripts/normalize_thread.py",
        "scripts/build_graph.py",
        "scripts/distill_thread.py",
        "scripts/run_distill.sh",
        "scripts/init_git.sh",
        "scripts/bootstrap_universe_repo_v2.sh",
    ]:
        path = repo_root / rel_path
        path.chmod(0o755)

    materialized_manifest = {
        "generated_at": utc_now(),
        "repo_root": str(repo_root),
        "materialized_count": len(manifest_entries),
        "entries": manifest_entries,
    }
    write_file(
        repo_root / "manifest/materialized_outputs_manifest.json",
        json.dumps(materialized_manifest, indent=2) + "\n",
    )

    print(json.dumps({"status": "pass", "materialized_count": len(manifest_entries)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

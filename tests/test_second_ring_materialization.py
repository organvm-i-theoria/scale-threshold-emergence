from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_second_ring_manifest_covers_required_files() -> None:
    manifest = json.loads(
        (REPO_ROOT / "manifest/second_ring_artifacts_manifest.json").read_text(
            encoding="utf-8"
        )
    )

    expected = {
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

    assert manifest["required_count"] == len(expected)
    assert set(manifest["fully_materialized"]) == expected


def test_second_ring_documents_include_expected_seed_content() -> None:
    mechanism_pack = (REPO_ROOT / "engine/runtime/mechanism_pack_spec.md").read_text(
        encoding="utf-8"
    )
    assert (
        "A mechanism pack is how literature becomes executable theory."
        in mechanism_pack
    )

    knowledge_supply_chain = (
        REPO_ROOT / "organvm_bridge/knowledge_supply_chain.md"
    ).read_text(encoding="utf-8")
    assert "Theoria" in knowledge_supply_chain
    assert "Poiesis" in knowledge_supply_chain
    assert "Ergon" in knowledge_supply_chain

    whitepaper = (REPO_ROOT / "docs/technical_whitepaper_01.md").read_text(
        encoding="utf-8"
    )
    assert "status:" in whitepaper.lower()

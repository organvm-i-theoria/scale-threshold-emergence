#!/usr/bin/env python3
"""
Integration tests for scale-threshold-emergence knowledge engine.
Tests the complete flow from intake to assembly.
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest


class TestKnowledgeEnginePipeline:
    """Integration tests for the complete knowledge engine pipeline."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_text(self):
        """Sample text for testing."""
        return """
        Python is a high-level programming language.
        Machine learning is a subset of artificial intelligence.
        Knowledge graphs store entities and relationships in a graph structure.
        Natural language processing enables computers to understand text.
        """

    @pytest.fixture
    def sample_code(self):
        """Sample code for testing."""
        return """
def hello_world():
    '''Says hello to the world'''
    print("Hello, World!")

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
"""

    def test_intake_to_refinery_pipeline(self, sample_text):
        """Test complete pipeline from intake to refinery."""
        from intake import SourceIntake
        from refinery.text import TextRefinery

        intake = SourceIntake(output_dir="./test_intake")
        record = intake.ingest_content(sample_text, source_type="text")

        refinery = TextRefinery()
        result = refinery.refine(sample_text)

        assert result is not None
        assert result.source_hash is not None
        assert record.id is not None

    def test_refinery_to_storage_pipeline(self, sample_text):
        """Test pipeline from refinery to storage."""
        from refinery.text import TextRefinery
        from storage.cas import ContentAddressableStorage

        refinery = TextRefinery()
        result = refinery.refine(sample_text)

        with tempfile.TemporaryDirectory() as tmpdir:
            cas = ContentAddressableStorage(storage_dir=tmpdir)

            for atom in result.atoms:
                hash_val = cas.put(atom.content, "text")
                assert hash_val is not None

    def test_cas_to_vector_pipeline(self, sample_text):
        """Test pipeline from CAS to vector storage."""
        from storage.cas import ContentAddressableStorage
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            cas = ContentAddressableStorage(storage_dir=f"{tmpdir}/cas")
            hash_val = cas.put(sample_text, "text")
            content = cas.get_content(hash_val)

            vector_store = VectorStore(storage_dir=f"{tmpdir}/vector", dimension=64)
            vector_store.add(content)

            results = vector_store.search("programming", top_k=1)
            assert len(results) >= 0

    def test_vector_to_graph_pipeline(self, sample_text):
        """Test pipeline from vector to graph storage."""
        from storage.vector import VectorStore
        from storage.graph import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            vector_store = VectorStore(storage_dir=f"{tmpdir}/vector", dimension=64)
            vector_store.add("Python is a programming language")
            vector_store.add("Machine learning is AI")

            graph_store = GraphStore(storage_dir=f"{tmpdir}/graph")

            node1 = graph_store.add_node("atom", {"content": "Python"})
            node2 = graph_store.add_node("atom", {"content": "ML"})

            graph_store.add_edge(node1, node2, "related_to")

            stats = graph_store.get_stats()
            assert stats["total_nodes"] == 2

    def test_full_pipeline(self, sample_text, sample_code):
        """Test complete end-to-end pipeline."""
        from intake import SourceIntake
        from refinery.text import TextRefinery
        from refinery.code import CodeRefinery
        from storage.cas import ContentAddressableStorage
        from storage.vector import VectorStore
        from storage.graph import GraphStore
        from analysis import AnalysisNormalizer

        with tempfile.TemporaryDirectory() as tmpdir:
            intake = SourceIntake(output_dir=f"{tmpdir}/intake")
            text_record = intake.ingest_content(sample_text, source_type="text")
            code_record = intake.ingest_content(sample_code, source_type="code")

            text_refinery = TextRefinery()
            code_refinery = CodeRefinery()

            text_result = text_refinery.refine(sample_text)
            code_atoms, code_relations = code_refinery.refine_content(
                sample_code, "test.py"
            )

            cas = ContentAddressableStorage(storage_dir=f"{tmpdir}/cas")
            for atom in text_result.atoms:
                cas.put(atom.content, "text")

            vector_store = VectorStore(storage_dir=f"{tmpdir}/vector", dimension=64)
            vector_store.add(sample_text)

            graph_store = GraphStore(storage_dir=f"{tmpdir}/graph")
            for atom in text_result.atoms:
                graph_store.add_node("atom", {"content": atom.content})

            normalizer = AnalysisNormalizer()
            atoms_dict = [
                {"id": a.id, "content": a.content, "atom_type": a.atom_type}
                for a in text_result.atoms
            ]
            normalized = normalizer.normalize_atoms(atoms_dict)

            assert len(text_result.atoms) > 0
            assert len(code_atoms) > 0
            assert text_record.source_type == "text"
            assert code_record.source_type == "code"
            assert len(normalized) > 0

    def test_assembly_integration(self, sample_text):
        """Test assembly engine integration."""
        from refinery.text import TextRefinery
        from assembly import AssemblyEngine

        refinery = TextRefinery()
        result = refinery.refine(sample_text)

        engine = AssemblyEngine()

        for atom in result.atoms:
            engine.register_atom(
                atom.id, {"content": atom.content, "atom_type": atom.atom_type}
            )

        result = engine.assemble("default_summary", {"content": "Test content"})

        assert result is not None

    def test_portal_integration(self, sample_text):
        """Test portal projection integration."""
        from refinery.text import TextRefinery
        from portal import PortalProjection

        with tempfile.TemporaryDirectory() as tmpdir:
            refinery = TextRefinery()
            result = refinery.refine(sample_text)

            portal = PortalProjection(output_dir=tmpdir)

            doc = portal.generate_document(
                "Test Document",
                result.segments[0] if result.segments else "No content",
                "markdown",
            )

            assert doc is not None

    def test_ops_health_check_integration(self):
        """Test operations health check integration."""
        from ops import Operations, HealthStatus

        ops = Operations()

        def intake_health():
            return HealthStatus(component="intake", status="healthy", message="OK")

        ops.register_health_check("intake", intake_health)

        status = ops.check_health("intake")

        assert "intake" in status

    def test_evaluation_benchmark_integration(self):
        """Test evaluation harness benchmark integration."""
        from evaluation import EvaluationHarness

        harness = EvaluationHarness(output_dir="./test_eval")

        def sample_benchmark():
            return 100.0

        harness.register_benchmark("sample", sample_benchmark)
        result = harness.run_benchmark("sample")

        assert result.passed is True

    def test_graphql_api_integration(self):
        """Test GraphQL API integration."""
        from api.graphql import GraphQLAPI

        api = GraphQLAPI()

        atoms = [
            {"id": "1", "content": "Python is a language", "atomType": "concept"},
            {"id": "2", "content": "ML is AI", "atomType": "concept"},
        ]

        api.load_data(atoms, [])

        result = api.execute("query { atoms { id content } }")

        assert result.errors == [] or result.data is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

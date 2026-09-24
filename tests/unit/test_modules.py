#!/usr/bin/env python3
"""
Unit tests for scale-threshold-emergence modules.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest


class TestIntakeModule:
    """Tests for Source Intake module."""

    def test_intake_source_intake_class(self):
        """Test SourceIntake class exists and can be instantiated."""
        from intake import SourceIntake

        intake = SourceIntake(output_dir="./test_data/intake")
        assert intake is not None
        assert intake.encoding == "utf-8"

    def test_intake_normalize_encoding(self):
        """Test encoding normalization."""
        from intake import SourceIntake

        intake = SourceIntake()

        content = "Hello\r\nWorld\r"
        normalized = intake._normalize_encoding(content)
        assert "\r" not in normalized

    def test_intake_compute_hash(self):
        """Test hash computation."""
        from intake import SourceIntake

        intake = SourceIntake()

        hash1 = intake._compute_hash("test content")
        hash2 = intake._compute_hash("test content")
        hash3 = intake._compute_hash("different content")

        assert hash1 == hash2
        assert hash1 != hash3

    def test_intake_detect_format(self):
        """Test format detection."""
        from intake import SourceIntake

        intake = SourceIntake()

        assert intake._detect_format("[Assistant]: Hello") == "claude"
        assert intake._detect_format("Response: Hello") == "chatgpt"
        assert intake._detect_format("Just some text") == "unknown"

    def test_intake_ingest_content(self):
        """Test content ingestion."""
        from intake import SourceIntake

        intake = SourceIntake(output_dir="./test_data/intake")

        record = intake.ingest_content("Test content", source_type="text")

        assert record.id is not None
        assert record.source_type == "text"
        assert record.content == "Test content"
        assert record.hash != ""

    def test_intake_queued_count(self):
        """Test queue count."""
        from intake import SourceIntake

        intake = SourceIntake(output_dir="./test_data/intake")

        assert intake.get_queued_count() == 0
        intake.ingest_content("Test 1")
        assert intake.get_queued_count() == 1
        intake.ingest_content("Test 2")
        assert intake.get_queued_count() == 2


class TestRefineryTextModule:
    """Tests for Text Refinery module."""

    def test_text_refinery_class(self):
        """Test TextRefinery class exists."""
        from refinery.text import TextRefinery

        refinery = TextRefinery()
        assert refinery is not None

    def test_text_refinery_compute_hash(self):
        """Test hash computation."""
        from refinery.text import TextRefinery

        refinery = TextRefinery()

        hash1 = refinery._compute_hash("test")
        hash2 = refinery._compute_hash("test")

        assert hash1 == hash2

    def test_text_refinery_segment_text(self):
        """Test text segmentation."""
        from refinery.text import TextRefinery

        refinery = TextRefinery()

        text = "This is first sentence. This is second sentence. This is third."
        segments = refinery._segment_text(text)

        assert len(segments) > 0

    def test_text_refinery_refine(self):
        """Test text refinement."""
        from refinery.text import TextRefinery

        refinery = TextRefinery()

        result = refinery.refine("Python is a programming language.")

        assert result.source_hash is not None
        assert result.atoms is not None


class TestRefineryCodeModule:
    """Tests for Code Refinery module."""

    def test_code_refinery_class(self):
        """Test CodeRefinery class exists."""
        from refinery.code import CodeRefinery

        refinery = CodeRefinery()
        assert refinery is not None
        assert "python" in refinery.supported_languages

    def test_code_refinery_detect_language(self):
        """Test language detection."""
        from refinery.code import CodeRefinery

        refinery = CodeRefinery()

        assert refinery._detect_language("test.py") == "python"
        assert refinery._detect_language("test.js") == "javascript"
        assert refinery._detect_language("test.ts") == "typescript"
        assert refinery._detect_language("test.go") == "go"
        assert refinery._detect_language("test.rs") == "rust"

    def test_code_refinery_extract_python(self):
        """Test Python code extraction."""
        from refinery.code import CodeRefinery

        refinery = CodeRefinery()

        code = """
def hello_world():
    '''Says hello'''
    print("Hello, World!")
    
class MyClass:
    pass
"""
        atoms, relations = refinery.refine_content(code, "test.py")

        assert len(atoms) > 0

    def test_code_refinery_extract_go(self):
        """Test Go code extraction."""
        from refinery.code import CodeRefinery

        refinery = CodeRefinery()

        code = """
package main

func main() {
    fmt.Println("Hello")
}

type MyStruct struct {
    Name string
}
"""
        atoms, relations = refinery.refine_content(code, "test.go")

        assert len(atoms) > 0


class TestStorageCASModule:
    """Tests for Content-Addressable Storage module."""

    def test_cas_class(self):
        """Test ContentAddressableStorage class exists."""
        from storage.cas import ContentAddressableStorage

        with tempfile.TemporaryDirectory() as tmpdir:
            cas = ContentAddressableStorage(storage_dir=tmpdir)
            assert cas is not None

    def test_cas_put_get(self):
        """Test put and get operations."""
        from storage.cas import ContentAddressableStorage

        with tempfile.TemporaryDirectory() as tmpdir:
            cas = ContentAddressableStorage(storage_dir=tmpdir)

            hash_val = cas.put("test content", "text")

            assert hash_val is not None
            assert cas.exists(hash_val)

            obj = cas.get(hash_val)
            assert obj is not None
            assert obj.content == "test content"

    def test_cas_verify(self):
        """Test content verification."""
        from storage.cas import ContentAddressableStorage

        with tempfile.TemporaryDirectory() as tmpdir:
            cas = ContentAddressableStorage(storage_dir=tmpdir)

            hash_val = cas.put("test content", "text")

            assert cas.verify(hash_val, "test content") is True
            assert cas.verify(hash_val, "wrong content") is False

    def test_cas_deduplication(self):
        """Test deduplication."""
        from storage.cas import ContentAddressableStorage

        with tempfile.TemporaryDirectory() as tmpdir:
            cas = ContentAddressableStorage(storage_dir=tmpdir)

            hash1 = cas.put("test content", "text")
            hash2 = cas.put("test content", "text")

            assert hash1 == hash2

    def test_cas_stats(self):
        """Test statistics."""
        from storage.cas import ContentAddressableStorage

        with tempfile.TemporaryDirectory() as tmpdir:
            cas = ContentAddressableStorage(storage_dir=tmpdir)

            cas.put("content 1", "text")
            cas.put("content 2", "text")

            stats = cas.get_stats()

            assert stats["total_objects"] == 2


class TestStorageVectorModule:
    """Tests for Vector Storage module."""

    def test_vector_class(self):
        """Test VectorStore class exists."""
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(storage_dir=tmpdir, dimension=64)
            assert store is not None
            assert store.dimension == 64

    def test_vector_add(self):
        """Test adding vectors."""
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(storage_dir=tmpdir, dimension=64)

            entry_id = store.add("test content")

            assert entry_id is not None

    def test_vector_search(self):
        """Test vector search."""
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(storage_dir=tmpdir, dimension=64)

            store.add("Python is a programming language")
            store.add("JavaScript is for web development")
            store.add("Rust is a systems programming language")

            results = store.search("programming", top_k=2)

            assert len(results) <= 2

    def test_vector_stats(self):
        """Test statistics."""
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(storage_dir=tmpdir, dimension=64)

            store.add("content 1")
            store.add("content 2")

            stats = store.get_stats()

            assert stats["total_entries"] == 2

    def test_vector_add_with_vector_dimension_mismatch(self):
        """Test adding a vector with wrong dimension raises ValueError and leaves store unchanged."""
        import json
        from pathlib import Path
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(storage_dir=tmpdir, dimension=64)

            assert len(store.entries) == 0
            index_path = Path(tmpdir) / "index.json"

            with pytest.raises(ValueError, match="expected 64, got 2") as exc_info:
                store.add_with_vector("bad", [1.0, 0.0])

            assert "64" in str(exc_info.value)
            assert "2" in str(exc_info.value)
            assert len(store.entries) == 0
            if index_path.exists():
                data = json.loads(index_path.read_text("utf-8"))
                assert len(data.get("entries", {})) == 0

    def test_vector_search_by_vector_dimension_mismatch(self):
        """Test searching with wrong dimension query vector raises ValueError."""
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(storage_dir=tmpdir, dimension=64)
            store.add_with_vector("good", [1.0] + [0.0] * 63)

            with pytest.raises(ValueError, match="expected 64, got 2") as exc_info:
                store.search_by_vector([1.0, 0.0])

            assert "64" in str(exc_info.value)
            assert "2" in str(exc_info.value)

    def test_vector_add_and_search_by_vector_valid_dimension(self):
        """Test valid same-dimension vectors normalize, store, and search correctly."""
        from storage.vector import VectorStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(storage_dir=tmpdir, dimension=64)

            v1 = [2.0] + [0.0] * 63
            entry_id1 = store.add_with_vector("content1", v1)
            stored1 = store.get(entry_id1)
            assert stored1 is not None
            assert stored1.vector[0] == pytest.approx(1.0)

            zero_vec = [0.0] * 64
            entry_id2 = store.add_with_vector("zero_content", zero_vec)
            stored2 = store.get(entry_id2)
            assert stored2 is not None
            assert stored2.vector == zero_vec

            query_vec = [1.0] + [0.0] * 63
            results = store.search_by_vector(query_vec, top_k=10)
            assert len(results) == 2
            assert results[0][0] == entry_id1
            assert results[0][1] == pytest.approx(1.0)


class TestStorageGraphModule:
    """Tests for Graph Storage module."""

    def test_graph_class(self):
        """Test GraphStore class exists."""
        from storage.graph import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(storage_dir=tmpdir)
            assert store is not None

    def test_graph_add_node(self):
        """Test adding nodes."""
        from storage.graph import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(storage_dir=tmpdir)

            node_id = store.add_node("atom", {"content": "test"})

            assert node_id is not None
            assert store.get_node(node_id) is not None

    def test_graph_add_edge(self):
        """Test adding edges."""
        from storage.graph import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(storage_dir=tmpdir)

            node1 = store.add_node("atom", {"content": "node1"})
            node2 = store.add_node("atom", {"content": "node2"})

            edge_id = store.add_edge(node1, node2, "related_to")

            assert edge_id is not None

    def test_graph_find_by_label(self):
        """Test finding nodes by label."""
        from storage.graph import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(storage_dir=tmpdir)

            store.add_node("concept", {"name": "AI"})
            store.add_node("concept", {"name": "ML"})
            store.add_node("entity", {"name": "Python"})

            concepts = store.find_nodes_by_label("concept")

            assert len(concepts) == 2

    def test_graph_neighbors(self):
        """Test finding neighbors."""
        from storage.graph import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(storage_dir=tmpdir)

            node1 = store.add_node("atom", {"content": "node1"})
            node2 = store.add_node("atom", {"content": "node2"})

            store.add_edge(node1, node2, "related_to")

            neighbors = store.get_neighbors(node1)

            assert len(neighbors) > 0

    def test_graph_stats(self):
        """Test statistics."""
        from storage.graph import GraphStore

        with tempfile.TemporaryDirectory() as tmpdir:
            store = GraphStore(storage_dir=tmpdir)

            store.add_node("atom", {"content": "test"})
            store.add_node("atom", {"content": "test2"})

            stats = store.get_stats()

            assert stats["total_nodes"] == 2


class TestAnalysisModule:
    """Tests for Analysis Normalization module."""

    def test_analysis_class(self):
        """Test AnalysisNormalizer class exists."""
        from analysis import AnalysisNormalizer

        normalizer = AnalysisNormalizer()
        assert normalizer is not None

    def test_analysis_canonicalize(self):
        """Test canonicalization."""
        from analysis import AnalysisNormalizer

        normalizer = AnalysisNormalizer()

        canonical = normalizer._canonicalize("  Hello World!  ")

        assert canonical == "hello world"

    def test_analysis_validate_schema(self):
        """Test schema validation."""
        from analysis import AnalysisNormalizer

        normalizer = AnalysisNormalizer()

        valid_atom = {"id": "1", "content": "test", "atom_type": "concept"}
        result = normalizer._validate_schema(valid_atom)

        assert result.valid is True

    def test_analysis_normalize_atom(self):
        """Test atom normalization."""
        from analysis import AnalysisNormalizer

        normalizer = AnalysisNormalizer()

        atom = {"id": "1", "content": "Test Content", "atom_type": "concept"}
        result = normalizer.normalize_atom(atom)

        assert result.id == "1"
        assert result.canonical_form == "test content"

    def test_analysis_merge_duplicates(self):
        """Test duplicate merging."""
        from analysis import AnalysisNormalizer

        normalizer = AnalysisNormalizer()

        atoms = [
            {"id": "1", "content": "test", "atom_type": "concept"},
            {"id": "2", "content": "test", "atom_type": "concept"},
        ]

        results = normalizer.merge_duplicates(atoms)

        assert len(results) == 1
        assert len(results[0].merged_from) == 2


class TestAssemblyModule:
    """Tests for Assembly Engine module."""

    def test_assembly_class(self):
        """Test AssemblyEngine class exists."""
        from assembly import AssemblyEngine

        engine = AssemblyEngine()
        assert engine is not None

    def test_assembly_register_atom(self):
        """Test atom registration."""
        from assembly import AssemblyEngine

        engine = AssemblyEngine()

        engine.register_atom(
            "atom1", {"content": "Test content", "atom_type": "concept"}
        )

        assert "atom1" in engine.atom_registry

    def test_assembly_assemble(self):
        """Test assembly."""
        from assembly import AssemblyEngine

        engine = AssemblyEngine()

        result = engine.assemble("default_summary", {"content": "Test summary"})

        assert result.output == "Summary: Test summary"

    def test_assembly_templates(self):
        """Test template listing."""
        from assembly import AssemblyEngine

        engine = AssemblyEngine()

        templates = engine.list_templates()

        assert len(templates) > 0

    def test_assembly_stats(self):
        """Test statistics."""
        from assembly import AssemblyEngine

        engine = AssemblyEngine()

        engine.register_atom("atom1", {"content": "test"})

        stats = engine.get_stats()

        assert stats["registered_atoms"] == 1


class TestPortalModule:
    """Tests for Portal Projection module."""

    def test_portal_class(self):
        """Test PortalProjection class exists."""
        from portal import PortalProjection

        with tempfile.TemporaryDirectory() as tmpdir:
            portal = PortalProjection(output_dir=tmpdir)
            assert portal is not None

    def test_portal_create_view(self):
        """Test view creation."""
        from portal import PortalProjection

        with tempfile.TemporaryDirectory() as tmpdir:
            portal = PortalProjection(output_dir=tmpdir)

            view = portal.create_view("Test View", "list")

            assert view.id is not None
            assert view.name == "Test View"

    def test_portal_generate_document(self):
        """Test document generation."""
        from portal import PortalProjection

        with tempfile.TemporaryDirectory() as tmpdir:
            portal = PortalProjection(output_dir=tmpdir)

            doc = portal.generate_document("Test Doc", "# Content", "markdown")

            assert doc.id is not None
            assert doc.title == "Test Doc"

    def test_portal_export_atoms(self):
        """Test atom export."""
        from portal import PortalProjection

        with tempfile.TemporaryDirectory() as tmpdir:
            portal = PortalProjection(output_dir=tmpdir)

            atoms = [{"id": "1", "content": "test"}]

            json_export = portal.export_atoms(atoms, "json")

            assert "1" in json_export

            csv_export = portal.export_atoms([{"id": "1", "content": "a,b"}], "csv")

            assert csv_export == "id,content\n1,a;b\n"


class TestOpsModule:
    """Tests for Operations module."""

    def test_ops_class(self):
        """Test Operations class exists."""
        from ops import Operations

        ops = Operations()
        assert ops is not None

    def test_ops_health_check(self):
        """Test health checks."""
        from ops import Operations, HealthStatus

        ops = Operations()

        def sample_health_check():
            return HealthStatus(component="test", status="healthy", message="OK")

        ops.register_health_check("test", sample_health_check)

        status = ops.check_health("test")

        assert "test" in status
        assert status["test"].status == "healthy"

    def test_ops_metrics(self):
        """Test metrics recording."""
        from ops import Operations

        ops = Operations()

        ops.record_metric("test.metric", 42.0, "count")

        metrics = ops.get_metrics("test.metric")

        assert len(metrics) == 1
        assert metrics[0].value == 42.0

    def test_ops_alerts(self):
        """Test alert creation."""
        from ops import Operations

        ops = Operations()

        alert = ops.create_alert("warning", "Test alert", "component")

        assert alert.id is not None
        assert alert.severity == "warning"

    def test_ops_uptime(self):
        """Test uptime tracking."""
        from ops import Operations

        ops = Operations()

        uptime = ops.get_uptime()

        assert uptime >= 0


class TestEvaluationModule:
    """Tests for Evaluation Harness module."""

    def test_eval_class(self):
        """Test EvaluationHarness class exists."""
        from evaluation import EvaluationHarness

        with tempfile.TemporaryDirectory() as tmpdir:
            harness = EvaluationHarness(output_dir=tmpdir)
            assert harness is not None

    def test_eval_register_benchmark(self):
        """Test benchmark registration."""
        from evaluation import EvaluationHarness

        with tempfile.TemporaryDirectory() as tmpdir:
            harness = EvaluationHarness(output_dir=tmpdir)

            def sample_benchmark():
                return 100.0

            harness.register_benchmark("test", sample_benchmark)

            assert "test" in harness.benchmarks

    def test_eval_run_benchmark(self):
        """Test benchmark running."""
        from evaluation import EvaluationHarness

        with tempfile.TemporaryDirectory() as tmpdir:
            harness = EvaluationHarness(output_dir=tmpdir)

            def sample_benchmark():
                return 100.0

            harness.register_benchmark("test", sample_benchmark)

            result = harness.run_benchmark("test")

            assert result.name == "test"
            assert result.passed is True

    def test_eval_validate(self):
        """Test validation."""
        from evaluation import EvaluationHarness

        with tempfile.TemporaryDirectory() as tmpdir:
            harness = EvaluationHarness(output_dir=tmpdir)

            harness.register_gold_fixture("test_fixture", {"key": "value"})

            result = harness.validate("test_fixture", {"key": "value"})

            assert result.passed is True

    def test_eval_generate_report(self):
        """Test report generation."""
        from evaluation import EvaluationHarness

        with tempfile.TemporaryDirectory() as tmpdir:
            harness = EvaluationHarness(output_dir=tmpdir)

            def sample_benchmark():
                return 100.0

            harness.register_benchmark("test", sample_benchmark)

            results = harness.run_all_benchmarks()
            report = harness.generate_report(benchmarks=results)

            assert report.id is not None
            assert len(report.benchmarks) == 1


class TestGraphQLModule:
    """Tests for GraphQL API module."""

    def test_graphql_class(self):
        """Test GraphQLAPI class exists."""
        from api.graphql import GraphQLAPI

        api = GraphQLAPI()
        assert api is not None

    def test_graphql_schema(self):
        """Test schema generation."""
        from api.graphql import GraphQLAPI

        api = GraphQLAPI()

        schema = api.get_schema()

        assert "type Atom" in schema
        assert "type Query" in schema

    def test_graphql_load_data(self):
        """Test data loading."""
        from api.graphql import GraphQLAPI

        api = GraphQLAPI()

        atoms = [{"id": "1", "content": "test", "atomType": "concept"}]
        relations = []

        api.load_data(atoms, relations)

        assert len(api.data["atoms"]) == 1

    def test_graphql_execute_query(self):
        """Test query execution."""
        from api.graphql import GraphQLAPI

        api = GraphQLAPI()

        api.load_data([{"id": "1", "content": "test"}], [])

        result = api.execute("query { atoms { id content } }")

        assert result.errors == [] or result.data is not None

    def test_graphql_mutations(self):
        """Test mutations."""
        from api.graphql import GraphQLAPI

        api = GraphQLAPI()

        result = api.execute(
            'mutation { createAtom(id: "new", content: "test") { id content } }'
        )

        assert result.errors == []
        assert len(api.data["atoms"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

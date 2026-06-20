from __future__ import annotations

import textwrap

import pytest

from refinery.code import CodeAtom, CodeRefinery


def atoms_by_name(atoms):
    return {atom.name: atom for atom in atoms}


class TestCodeRefineryExtraction:
    def test_python_refinement_extracts_metadata_and_relations(self) -> None:
        refinery = CodeRefinery()
        code = textwrap.dedent(
            '''
            import math

            class Parser(BaseParser):
                pass

            def build_parser():
                """Create a parser with a numeric guard."""
                math.sqrt(4)
                return Parser()
            '''
        ).strip()

        atoms, relations = refinery.refine_content(code, "pipeline.py")

        by_name = atoms_by_name(atoms)
        assert set(by_name) == {"math", "Parser", "build_parser"}

        function = by_name["build_parser"]
        assert function.atom_type == "function"
        assert function.language == "python"
        assert function.line_start == 6
        assert function.documentation == "Create a parser with a numeric guard."
        assert 'math.sqrt(4)' in function.content
        assert function.provenance == {
            "source": "function_pattern",
            "source_path": "pipeline.py",
        }

        klass = by_name["Parser"]
        assert klass.atom_type == "class"
        assert klass.documentation == "Extends: BaseParser"

        imported = by_name["math"]
        assert imported.atom_type == "import"
        assert imported.content == "import math"

        relation_types = {relation.relation_type for relation in relations}
        assert relation_types == {"imports", "defines"}
        assert all(relation.source_id == function.id for relation in relations)
        assert {relation.target_id for relation in relations} == {
            imported.id,
            klass.id,
        }

    def test_javascript_extracts_class_inheritance(self) -> None:
        refinery = CodeRefinery()
        code = textwrap.dedent(
            """
            import { BaseController } from "./base";

            class DashboardController extends BaseController {
              render() {
                return null;
              }
            }
            """
        ).strip()

        atoms, relations = refinery.refine_content(code, "dashboard.js")

        assert relations == []
        assert len(atoms) == 1
        atom = atoms[0]
        assert atom.name == "DashboardController"
        assert atom.atom_type == "class"
        assert atom.language == "javascript"
        assert atom.line_start == 3
        assert atom.documentation == "Extends: BaseController"
        assert atom.provenance["source_path"] == "dashboard.js"

    def test_typescript_extracts_class_and_interface(self) -> None:
        refinery = CodeRefinery()
        code = textwrap.dedent(
            """
            class Repository extends BaseRepository {
              find(id: string): RecordData {
                return { id };
              }
            }

            interface RecordData {
              id: string;
            }
            """
        ).strip()

        atoms, relations = refinery.refine_content(code, "repository.ts")

        assert relations == []
        by_name = atoms_by_name(atoms)
        assert set(by_name) == {"Repository", "RecordData"}
        assert by_name["Repository"].atom_type == "class"
        assert by_name["Repository"].documentation == "Extends: BaseRepository"
        assert by_name["RecordData"].atom_type == "interface"
        assert by_name["RecordData"].language == "typescript"
        assert by_name["RecordData"].line_start == 7

    def test_go_extracts_receiver_functions_and_types(self) -> None:
        refinery = CodeRefinery()
        code = textwrap.dedent(
            """
            package runtime

            type Engine struct {
                Name string
            }

            func (e *Engine) Run() {
            }

            func NewEngine() *Engine {
                return &Engine{}
            }
            """
        ).strip()

        atoms, relations = refinery.refine_content(code, "engine.go")

        assert relations == []
        by_name = atoms_by_name(atoms)
        assert set(by_name) == {"Engine", "Run", "NewEngine"}
        assert by_name["Engine"].atom_type == "type"
        assert by_name["Run"].documentation == "Receiver: e"
        assert by_name["NewEngine"].atom_type == "function"
        assert all(atom.language == "go" for atom in atoms)

    def test_rust_extracts_generic_function_struct_and_trait(self) -> None:
        refinery = CodeRefinery()
        code = textwrap.dedent(
            """
            pub struct Engine {
                name: String,
            }

            pub trait Runnable {
                fn run(&self);
            }

            pub fn build<T>() -> Engine {
                Engine { name: String::new() }
            }
            """
        ).strip()

        atoms, relations = refinery.refine_content(code, "engine.rs")

        assert relations == []
        by_name = atoms_by_name(atoms)
        assert set(by_name) == {"Engine", "Runnable", "build"}
        assert by_name["Engine"].atom_type == "struct"
        assert by_name["Runnable"].atom_type == "trait"
        assert by_name["build"].atom_type == "function"
        assert all(atom.language == "rust" for atom in atoms)

    def test_unsupported_language_returns_empty_results(self) -> None:
        refinery = CodeRefinery()

        atoms, relations = refinery.refine_content("public class Demo {}", "Demo.java")

        assert atoms == []
        assert relations == []


class TestCodeRefineryFileOperations:
    def test_refine_file_reads_content_and_preserves_source_path(
        self, tmp_path
    ) -> None:
        refinery = CodeRefinery()
        source = tmp_path / "module.py"
        source.write_text(
            textwrap.dedent(
                """
                def load():
                    return "ok"
                """
            ).strip(),
            encoding="utf-8",
        )

        atoms, relations = refinery.refine_file(str(source))

        assert relations == []
        assert [atom.name for atom in atoms] == ["load"]
        assert atoms[0].provenance["source_path"] == str(source)

    def test_refine_file_raises_for_missing_path(self, tmp_path) -> None:
        refinery = CodeRefinery()

        with pytest.raises(FileNotFoundError, match="File not found"):
            refinery.refine_file(str(tmp_path / "missing.py"))

    def test_refine_directory_processes_matching_files_only(self, tmp_path) -> None:
        refinery = CodeRefinery()
        first = tmp_path / "first.py"
        second = tmp_path / "second.py"
        ignored = tmp_path / "notes.txt"
        first.write_text("def alpha():\n    return 1\n", encoding="utf-8")
        second.write_text("class Beta:\n    pass\n", encoding="utf-8")
        ignored.write_text("def ignored():\n    return 0\n", encoding="utf-8")

        results = refinery.refine_directory(str(tmp_path), pattern="*.py")

        assert set(results) == {str(first), str(second)}
        assert [atom.name for atom in results[str(first)][0]] == ["alpha"]
        assert [atom.name for atom in results[str(second)][0]] == ["Beta"]

    def test_refine_directory_reports_file_errors(
        self, tmp_path, monkeypatch, capsys
    ) -> None:
        refinery = CodeRefinery()
        source = tmp_path / "broken.py"
        source.write_text("def broken():\n    return None\n", encoding="utf-8")

        def raise_for_file(filepath: str):
            raise ValueError(f"cannot parse {filepath}")

        monkeypatch.setattr(refinery, "refine_file", raise_for_file)

        assert refinery.refine_directory(str(tmp_path), pattern="*.py") == {}
        assert "Error processing" in capsys.readouterr().out


def test_code_atom_defaults_are_initialized() -> None:
    atom = CodeAtom(
        id="code_1",
        name="load",
        content="def load(): pass",
        atom_type="function",
        language="python",
        line_start=1,
        line_end=1,
    )

    assert atom.relations == []
    assert atom.provenance == {}
    assert atom.created_at

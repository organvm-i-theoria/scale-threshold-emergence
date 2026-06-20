#!/usr/bin/env python3
"""
Code Refinery
=============
Extracts atomic units from code files.

Features:
- Parse programming languages
- Extract functions, classes, imports
- Identify code relations
- Generate code atoms
- Link to documentation
"""

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class CodeAtom:
    """Represents an atomic unit of code knowledge."""

    id: str
    name: str
    content: str
    atom_type: str  # function, class, import, variable, module
    language: str
    line_start: int
    line_end: int
    documentation: str = ""
    relations: list = field(default_factory=list)
    provenance: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CodeRelation:
    """Represents a relation between code atoms."""

    id: str
    source_id: str
    target_id: str
    relation_type: str  # imports, calls, defines, extends, implements
    confidence: float = 1.0


LANGUAGE_PATTERNS = {
    "python": {
        "function": re.compile(
            r"^(\s*)def\s+(\w+)\s*\((.*?)\)(?:\s*->\s*(.*?))?:", re.MULTILINE
        ),
        "class": re.compile(r"^class\s+(\w+)(?:\((.*?)\))?:", re.MULTILINE),
        "import": re.compile(
            r"^(?:from\s+(\S+)\s+)?import\s+(.+?)(?:\s+as\s+\w+)?$", re.MULTILINE
        ),
        "docstring": re.compile(r'"""(.*?)"""', re.DOTALL),
    },
    "javascript": {
        "function": re.compile(
            r"(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*:\s*(?:async\s*)?\()",
            re.MULTILINE,
        ),
        "class": re.compile(r"class\s+(\w+)(?:\s+extends\s+(\w+))?", re.MULTILINE),
        "import": re.compile(
            r'import\s+(?:\{([^}]+)\}|\*\s+as\s+(\w+)|(\w+))\s+from\s+[\'"]([^\'"]+)[\'"]',
            re.MULTILINE,
        ),
    },
    "typescript": {
        "function": re.compile(
            r"(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*\([^)]*\)(?:\s*:\s*[\w\[\]]+)?\s*\{)",
            re.MULTILINE,
        ),
        "class": re.compile(
            r"class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+(\w+))?",
            re.MULTILINE,
        ),
        "interface": re.compile(r"interface\s+(\w+)(?:\s*\{)?", re.MULTILINE),
        "import": re.compile(
            r'import\s+(?:\{([^}]+)\}|\*\s+as\s+(\w+)|(\w+))\s+from\s+[\'"]([^\'"]+)[\'"]',
            re.MULTILINE,
        ),
    },
    "go": {
        "function": re.compile(
            r"^func\s+(?:\((\w+)\s+\*?\w+\)\s+)?(\w+)\s*\(", re.MULTILINE
        ),
        "type": re.compile(r"^type\s+(\w+)\s+(?:struct|interface)", re.MULTILINE),
        "import": re.compile(r"import\s+(?:\(([^)]+)\)|\"([^\"]+)\")", re.MULTILINE),
    },
    "rust": {
        "function": re.compile(r"^(?:pub\s+)?fn\s+(\w+)\s*<[^>]*>?\s*\(", re.MULTILINE),
        "struct": re.compile(r"^(?:pub\s+)?struct\s+(\w+)", re.MULTILINE),
        "trait": re.compile(r"^(?:pub\s+)?trait\s+(\w+)", re.MULTILINE),
        "impl": re.compile(
            r"^(?:pub\s+)?impl(?:\s+<[^>]+>)?\s+(?:(\w+)\s+for\s+)?(\w+)", re.MULTILINE
        ),
        "use": re.compile(r"^use\s+(.+?)(?:\s+as\s+\w+)?;", re.MULTILINE),
    },
}


class CodeRefinery:
    """Extracts atomic units from code files."""

    def __init__(self):
        self.min_atom_length = 2
        self.supported_languages = list(LANGUAGE_PATTERNS.keys())

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def _detect_language(self, filepath: str) -> str:
        """Detect programming language from file extension."""
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".cs": "csharp",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
        }

        ext = Path(filepath).suffix.lower()
        return ext_map.get(ext, "unknown")

    def _extract_python_atoms(self, content: str) -> list[CodeAtom]:
        """Extract code atoms from Python content."""
        atoms = []
        lines = content.split("\n")
        patterns = LANGUAGE_PATTERNS["python"]

        for match in patterns["function"].finditer(content):
            name = match.group(2)
            start_line = content[: match.start()].count("\n") + 1

            end_line = start_line
            for i in range(start_line, len(lines)):
                if lines[i] and not lines[i][0].isspace():
                    if i > start_line:
                        end_line = i
                        break
                end_line = i + 1

            func_content = "\n".join(lines[start_line - 1 : end_line])

            docstring = ""
            doc_match = patterns["docstring"].search(func_content)
            if doc_match:
                docstring = doc_match.group(1).strip()

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=func_content,
                    atom_type="function",
                    language="python",
                    line_start=start_line,
                    line_end=end_line,
                    documentation=docstring,
                    provenance={"source": "function_pattern"},
                )
            )

        for match in patterns["class"].finditer(content):
            name = match.group(1)
            inherits = match.group(2) or ""
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="class",
                    language="python",
                    line_start=start_line,
                    line_end=start_line,
                    documentation=f"Extends: {inherits}" if inherits else "",
                    provenance={"source": "class_pattern"},
                )
            )

        for match in patterns["import"].finditer(content):
            module = match.group(1) or match.group(2)
            if module:
                start_line = content[: match.start()].count("\n") + 1
                atom_id = f"code_{self._compute_hash(module)[:12]}"
                atoms.append(
                    CodeAtom(
                        id=atom_id,
                        name=module,
                        content=match.group(0),
                        atom_type="import",
                        language="python",
                        line_start=start_line,
                        line_end=start_line,
                        provenance={"source": "import_pattern"},
                    )
                )

        return atoms

    def _extract_javascript_atoms(self, content: str) -> list[CodeAtom]:
        """Extract code atoms from JavaScript content."""
        atoms = []
        patterns = LANGUAGE_PATTERNS["javascript"]

        for match in patterns["class"].finditer(content):
            name = match.group(1)
            extends = match.group(2) or ""
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="class",
                    language="javascript",
                    line_start=start_line,
                    line_end=start_line,
                    documentation=f"Extends: {extends}" if extends else "",
                    provenance={"source": "class_pattern"},
                )
            )

        return atoms

    def _extract_typescript_atoms(self, content: str) -> list[CodeAtom]:
        """Extract code atoms from TypeScript content."""
        atoms = []
        atoms.extend(self._extract_javascript_atoms(content))

        patterns = LANGUAGE_PATTERNS["typescript"]

        for match in patterns["interface"].finditer(content):
            name = match.group(1)
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="interface",
                    language="typescript",
                    line_start=start_line,
                    line_end=start_line,
                    provenance={"source": "interface_pattern"},
                )
            )

        return atoms

    def _extract_go_atoms(self, content: str) -> list[CodeAtom]:
        """Extract code atoms from Go content."""
        atoms = []
        patterns = LANGUAGE_PATTERNS["go"]

        for match in patterns["function"].finditer(content):
            receiver = match.group(1) or ""
            name = match.group(2)
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="function",
                    language="go",
                    line_start=start_line,
                    line_end=start_line,
                    documentation=f"Receiver: {receiver}" if receiver else "",
                    provenance={"source": "function_pattern"},
                )
            )

        for match in patterns["type"].finditer(content):
            name = match.group(1)
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="type",
                    language="go",
                    line_start=start_line,
                    line_end=start_line,
                    provenance={"source": "type_pattern"},
                )
            )

        return atoms

    def _extract_rust_atoms(self, content: str) -> list[CodeAtom]:
        """Extract code atoms from Rust content."""
        atoms = []
        patterns = LANGUAGE_PATTERNS["rust"]

        for match in patterns["function"].finditer(content):
            name = match.group(1)
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="function",
                    language="rust",
                    line_start=start_line,
                    line_end=start_line,
                    provenance={"source": "function_pattern"},
                )
            )

        for match in patterns["struct"].finditer(content):
            name = match.group(1)
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="struct",
                    language="rust",
                    line_start=start_line,
                    line_end=start_line,
                    provenance={"source": "struct_pattern"},
                )
            )

        for match in patterns["trait"].finditer(content):
            name = match.group(1)
            start_line = content[: match.start()].count("\n") + 1

            atom_id = f"code_{self._compute_hash(name + content[:50])[:12]}"
            atoms.append(
                CodeAtom(
                    id=atom_id,
                    name=name,
                    content=match.group(0),
                    atom_type="trait",
                    language="rust",
                    line_start=start_line,
                    line_end=start_line,
                    provenance={"source": "trait_pattern"},
                )
            )

        return atoms

    def _identify_code_relations(self, atoms: list[CodeAtom]) -> list[CodeRelation]:
        """Identify relations between code atoms."""
        relations = []

        imports = [a for a in atoms if a.atom_type == "import"]
        functions = [a for a in atoms if a.atom_type == "function"]
        classes = [a for a in atoms if a.atom_type == "class"]

        for imp in imports:
            for func in functions:
                if func.content and imp.name in func.content:
                    rel_id = f"rel_{self._compute_hash(imp.id + func.id)[:12]}"
                    relations.append(
                        CodeRelation(
                            id=rel_id,
                            source_id=func.id,
                            target_id=imp.id,
                            relation_type="imports",
                            confidence=0.9,
                        )
                    )

        for cls in classes:
            for func in functions:
                if func.content and cls.name in func.content:
                    rel_id = f"rel_{self._compute_hash(cls.id + func.id)[:12]}"
                    relations.append(
                        CodeRelation(
                            id=rel_id,
                            source_id=func.id,
                            target_id=cls.id,
                            relation_type="defines",
                            confidence=0.8,
                        )
                    )

        return relations

    def refine_file(self, filepath: str) -> tuple[list[CodeAtom], list[CodeRelation]]:
        """
        Extract code atoms from a file.

        Args:
            filepath: Path to the code file

        Returns:
            Tuple of (atoms, relations)
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        content = path.read_text(encoding="utf-8")
        return self.refine_content(content, str(path))

    def refine_content(
        self, content: str, source_path: str = ""
    ) -> tuple[list[CodeAtom], list[CodeRelation]]:
        """
        Extract code atoms from content.

        Args:
            content: Code content
            source_path: Optional source path

        Returns:
            Tuple of (atoms, relations)
        """
        language = self._detect_language(source_path)

        if language == "python":
            atoms = self._extract_python_atoms(content)
        elif language == "javascript":
            atoms = self._extract_javascript_atoms(content)
        elif language == "typescript":
            atoms = self._extract_typescript_atoms(content)
        elif language == "go":
            atoms = self._extract_go_atoms(content)
        elif language == "rust":
            atoms = self._extract_rust_atoms(content)
        else:
            atoms = []

        for atom in atoms:
            atom.provenance["source_path"] = source_path

        relations = self._identify_code_relations(atoms)

        return atoms, relations

    def refine_directory(self, dirpath: str, pattern: str = "*.py") -> dict:
        """
        Extract code atoms from all matching files in a directory.

        Args:
            dirpath: Path to directory
            pattern: Glob pattern for files

        Returns:
            Dictionary mapping file paths to (atoms, relations) tuples
        """
        path = Path(dirpath)
        results = {}

        for filepath in path.glob(pattern):
            try:
                atoms, relations = self.refine_file(str(filepath))
                results[str(filepath)] = (atoms, relations)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

        return results

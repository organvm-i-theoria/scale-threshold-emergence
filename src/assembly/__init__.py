#!/usr/bin/env python3
"""
Assembly Engine
===============
Assembles atoms into higher-level outputs.

Features:
- Template processing
- Atom substitution
- Relation traversal
- Output generation
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class AssemblyTemplate:
    """Represents an assembly template."""

    id: str
    name: str
    template: str
    required_vars: list = field(default_factory=list)
    description: str = ""


@dataclass
class AssemblyResult:
    """Result of assembly operation."""

    output: str
    template_id: str
    variables_used: dict = field(default_factory=dict)
    atoms_referenced: list = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class AssemblyEngine:
    """Assembles atoms into higher-level outputs."""

    def __init__(self):
        self.templates: dict[str, AssemblyTemplate] = {}
        self.atom_registry: dict[str, dict] = {}
        self._register_default_templates()

    def _register_default_templates(self):
        """Register default templates."""
        self.register_template(
            AssemblyTemplate(
                id="default_summary",
                name="Summary",
                template="Summary: {content}",
                required_vars=["content"],
                description="Basic summary template",
            )
        )

        self.register_template(
            AssemblyTemplate(
                id="default_explanation",
                name="Explanation",
                template="## {title}\n\n{content}\n\n### Key Points\n{points}",
                required_vars=["title", "content", "points"],
                description="Explanation with key points",
            )
        )

        self.register_template(
            AssemblyTemplate(
                id="default_report",
                name="Report",
                template="# {title}\n\n**Date**: {date}\n\n## Summary\n{summary}\n\n## Details\n{details}\n\n## Conclusion\n{conclusion}",
                required_vars=["title", "date", "summary", "details", "conclusion"],
                description="Full report template",
            )
        )

    def register_template(self, template: AssemblyTemplate):
        """Register a template."""
        self.templates[template.id] = template

    def register_atom(self, atom_id: str, atom_data: dict):
        """Register an atom for assembly."""
        self.atom_registry[atom_id] = atom_data

    def register_atoms(self, atoms: list[dict]):
        """Register multiple atoms."""
        for atom in atoms:
            atom_id = atom.get("id", "")
            if atom_id:
                self.atom_registry[atom_id] = atom

    def _extract_variables(self, template: str) -> list[str]:
        """Extract variable names from template."""
        pattern = re.compile(r"\{(\w+)\}")
        return pattern.findall(template)

    def _substitute_variables(self, template: str, variables: dict[str, Any]) -> str:
        """Substitute variables in template."""
        result = template

        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"

            if isinstance(var_value, list):
                value_str = "\n".join(f"- {item}" for item in var_value)
            elif isinstance(var_value, dict):
                value_str = "\n".join(f"{k}: {v}" for k, v in var_value.items())
            else:
                value_str = str(var_value)

            result = result.replace(placeholder, value_str)

        return result

    def _resolve_atom_reference(self, ref: str) -> Optional[str]:
        """Resolve atom reference to content."""
        if ref in self.atom_registry:
            return self.atom_registry[ref].get("content", "")

        for atom_id, atom_data in self.atom_registry.items():
            if atom_data.get("name") == ref:
                return atom_data.get("content", "")

        return None

    def assemble(
        self, template_id: str, variables: dict[str, Any], auto_resolve: bool = True
    ) -> AssemblyResult:
        """
        Assemble output from template and variables.

        Args:
            template_id: Template ID
            variables: Variables to substitute
            auto_resolve: Automatically resolve atom references

        Returns:
            AssemblyResult
        """
        if template_id not in self.templates:
            raise ValueError(f"Template not found: {template_id}")

        template = self.templates[template_id]

        resolved_vars = variables.copy()
        atoms_referenced = []

        if auto_resolve:
            for var_name, var_value in variables.items():
                if isinstance(var_value, str) and var_value.startswith("@"):
                    atom_ref = var_value[1:]
                    content = self._resolve_atom_reference(atom_ref)
                    if content:
                        resolved_vars[var_name] = content
                        atoms_referenced.append(atom_ref)

        output = self._substitute_variables(template.template, resolved_vars)

        return AssemblyResult(
            output=output,
            template_id=template_id,
            variables_used=resolved_vars,
            atoms_referenced=atoms_referenced,
        )

    def assemble_with_atoms(
        self,
        template_id: str,
        atom_ids: list[str],
        additional_vars: Optional[dict] = None,
    ) -> AssemblyResult:
        """
        Assemble output using atoms.

        Args:
            template_id: Template ID
            atom_ids: List of atom IDs to include
            additional_vars: Additional variables

        Returns:
            AssemblyResult
        """
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")

        variables = additional_vars or {}
        atoms_referenced = []

        for var_name in template.required_vars:
            if var_name not in variables:
                for atom_id in atom_ids:
                    atom = self.atom_registry.get(atom_id, {})
                    if atom.get("atom_type") == var_name or atom.get("name"):
                        variables[var_name] = atom.get("content", "")
                        atoms_referenced.append(atom_id)
                        break

        variables.setdefault(
            "content",
            "\n\n".join(
                self.atom_registry.get(aid, {}).get("content", "") for aid in atom_ids
            ),
        )

        return self.assemble(template_id, variables, auto_resolve=False)

    def get_template(self, template_id: str) -> Optional[AssemblyTemplate]:
        """Get template by ID."""
        return self.templates.get(template_id)

    def list_templates(self) -> list[AssemblyTemplate]:
        """List all registered templates."""
        return list(self.templates.values())

    def get_stats(self) -> dict:
        """Get assembly engine statistics."""
        return {
            "total_templates": len(self.templates),
            "registered_atoms": len(self.atom_registry),
            "template_ids": list(self.templates.keys()),
        }

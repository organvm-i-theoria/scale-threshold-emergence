#!/usr/bin/env python3
"""
Portal Projection
================
Projects knowledge into different views.

Features:
- Workspace views
- Document generation
- Trace generation
- Export formats
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class WorkspaceView:
    """Represents a workspace view."""

    id: str
    name: str
    view_type: str  # timeline, graph, list, tree
    filters: dict = field(default_factory=dict)
    layout: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GeneratedDocument:
    """Represents a generated document."""

    id: str
    title: str
    content: str
    format: str  # markdown, html, pdf, json
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class PortalProjection:
    """Projects knowledge into different views."""

    def __init__(self, output_dir: str = "./data/portal"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.views: dict[str, WorkspaceView] = {}
        self.documents: dict[str, GeneratedDocument] = {}
        self._register_default_views()

    def _register_default_views(self):
        """Register default workspace views."""
        self.register_view(
            WorkspaceView(
                id="timeline",
                name="Timeline View",
                view_type="timeline",
                layout={"columns": ["date", "content", "source"]},
            )
        )

        self.register_view(
            WorkspaceView(
                id="graph",
                name="Graph View",
                view_type="graph",
                layout={"layout": "force-directed"},
            )
        )

        self.register_view(
            WorkspaceView(
                id="list",
                name="List View",
                view_type="list",
                layout={"sort_by": "date", "order": "desc"},
            )
        )

    def register_view(self, view: WorkspaceView):
        """Register a workspace view."""
        self.views[view.id] = view

    def create_view(
        self,
        name: str,
        view_type: str,
        filters: Optional[dict] = None,
        layout: Optional[dict] = None,
    ) -> WorkspaceView:
        """
        Create a new workspace view.

        Args:
            name: View name
            view_type: Type of view
            filters: View filters
            layout: View layout

        Returns:
            WorkspaceView
        """
        view_id = f"view_{len(self.views)}"

        view = WorkspaceView(
            id=view_id,
            name=name,
            view_type=view_type,
            filters=filters or {},
            layout=layout or {},
        )

        self.views[view_id] = view
        return view

    def generate_document(
        self,
        title: str,
        content: str,
        format: str = "markdown",
        metadata: Optional[dict] = None,
    ) -> GeneratedDocument:
        """
        Generate a document.

        Args:
            title: Document title
            content: Document content
            format: Document format
            metadata: Document metadata

        Returns:
            GeneratedDocument
        """
        doc_id = f"doc_{len(self.documents)}"

        document = GeneratedDocument(
            id=doc_id,
            title=title,
            content=content,
            format=format,
            metadata=metadata or {},
        )

        self.documents[doc_id] = document
        return document

    def save_document(self, document: GeneratedDocument) -> str:
        """Save document to file."""
        ext = {"markdown": "md", "html": "html", "json": "json", "pdf": "pdf"}.get(
            document.format, "txt"
        )

        output_path = self.output_dir / f"{document.id}.{ext}"
        output_path.write_text(document.content, encoding="utf-8")

        return str(output_path)

    def generate_trace(self, atom_id: str, provenance: dict) -> str:
        """
        Generate a trace for an atom.

        Args:
            atom_id: Atom ID
            provenance: Provenance data

        Returns:
            Trace in markdown format
        """
        trace = f"# Trace for {atom_id}\n\n"
        trace += f"**Generated**: {datetime.now().isoformat()}\n\n"

        trace += "## Provenance\n\n"
        for key, value in provenance.items():
            trace += f"- **{key}**: {value}\n"

        return trace

    def export_atoms(self, atoms: list[dict], format: str = "json") -> str:
        """
        Export atoms to specified format.

        Args:
            atoms: List of atoms
            format: Export format

        Returns:
            Exported content
        """
        if format == "json":
            return json.dumps(atoms, indent=2)

        elif format == "markdown":
            md = "# Atoms Export\n\n"
            for atom in atoms:
                md += f"## {atom.get('id', 'unknown')}\n\n"
                md += f"**Type**: {atom.get('atom_type', 'unknown')}\n\n"
                md += f"{atom.get('content', '')}\n\n"
                md += "---\n\n"
            return md

        elif format == "csv":
            if not atoms:
                return ""

            headers = list(atoms[0].keys())
            csv = ",".join(headers) + "\n"

            for atom in atoms:
                values = [
                    str(atom.get(header, "")).replace(",", ";") for header in headers
                ]
                csv += ",".join(values) + "\n"

            return csv

        return str(atoms)

    def get_view(self, view_id: str) -> Optional[WorkspaceView]:
        """Get view by ID."""
        return self.views.get(view_id)

    def get_document(self, doc_id: str) -> Optional[GeneratedDocument]:
        """Get document by ID."""
        return self.documents.get(doc_id)

    def list_views(self) -> list[WorkspaceView]:
        """List all views."""
        return list(self.views.values())

    def list_documents(self) -> list[GeneratedDocument]:
        """List all documents."""
        return list(self.documents.values())

    def get_stats(self) -> dict:
        """Get portal statistics."""
        return {
            "total_views": len(self.views),
            "total_documents": len(self.documents),
            "view_types": list(set(v.view_type for v in self.views.values())),
            "export_formats": ["json", "markdown", "csv"],
        }

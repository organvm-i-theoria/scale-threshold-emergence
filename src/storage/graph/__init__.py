#!/usr/bin/env python3
"""
Graph Storage
=============
Stores atoms and relations in a graph database.

Features:
- Store atoms as nodes
- Store relations as edges
- Support querying by type
- Support path queries
- Maintain provenance
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class GraphNode:
    """Represents a node in the graph (an atom)."""

    id: str
    label: str
    properties: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GraphEdge:
    """Represents an edge in the graph (a relation)."""

    id: str
    source_id: str
    target_id: str
    relation_type: str
    properties: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class GraphStore:
    """Stores atoms and relations in a graph structure."""

    def __init__(self, storage_dir: str = "./data/graph"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.nodes: dict[str, GraphNode] = {}
        self.edges: dict[str, GraphEdge] = {}
        self._load_index()

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _load_index(self):
        """Load the graph index."""
        index_path = self.storage_dir / "index.json"
        if index_path.exists():
            try:
                data = json.loads(index_path.read_text("utf-8"))
                for node_id, node_data in data.get("nodes", {}).items():
                    self.nodes[node_id] = GraphNode(**node_data)
                for edge_id, edge_data in data.get("edges", {}).items():
                    self.edges[edge_id] = GraphEdge(**edge_data)
            except Exception as e:
                print(f"Error loading index: {e}")

    def _save_index(self):
        """Save the graph index."""
        index_path = self.storage_dir / "index.json"
        data = {
            "nodes": {
                node_id: {
                    "id": node.id,
                    "label": node.label,
                    "properties": node.properties,
                    "created_at": node.created_at,
                }
                for node_id, node in self.nodes.items()
            },
            "edges": {
                edge_id: {
                    "id": edge.id,
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "relation_type": edge.relation_type,
                    "properties": edge.properties,
                    "created_at": edge.created_at,
                }
                for edge_id, edge in self.edges.items()
            },
        }
        index_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add_node(
        self,
        label: str,
        properties: Optional[dict] = None,
        node_id: Optional[str] = None,
    ) -> str:
        """
        Add a node to the graph.

        Args:
            label: Node label (e.g., 'atom', 'concept')
            properties: Node properties
            node_id: Optional node ID (generated if not provided)

        Returns:
            Node ID
        """
        if node_id is None:
            node_id = f"node_{self._compute_hash(label + str(properties))[:12]}"

        if node_id in self.nodes:
            return node_id

        node = GraphNode(id=node_id, label=label, properties=properties or {})

        self.nodes[node_id] = node
        self._save_index()

        return node_id

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        properties: Optional[dict] = None,
        edge_id: Optional[str] = None,
    ) -> str:
        """
        Add an edge to the graph.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            relation_type: Type of relation
            properties: Edge properties
            edge_id: Optional edge ID

        Returns:
            Edge ID
        """
        if source_id not in self.nodes:
            raise ValueError(f"Source node not found: {source_id}")
        if target_id not in self.nodes:
            raise ValueError(f"Target node not found: {target_id}")

        if edge_id is None:
            edge_id = (
                f"edge_{self._compute_hash(source_id + target_id + relation_type)[:12]}"
            )

        if edge_id in self.edges:
            return edge_id

        edge = GraphEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            properties=properties or {},
        )

        self.edges[edge_id] = edge
        self._save_index()

        return edge_id

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get node by ID."""
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        """Get edge by ID."""
        return self.edges.get(edge_id)

    def find_nodes_by_label(self, label: str) -> list[GraphNode]:
        """Find nodes by label."""
        return [node for node in self.nodes.values() if node.label == label]

    def find_nodes_by_property(self, key: str, value: any) -> list[GraphNode]:
        """Find nodes by property value."""
        return [
            node for node in self.nodes.values() if node.properties.get(key) == value
        ]

    def find_edges_by_type(self, relation_type: str) -> list[GraphEdge]:
        """Find edges by relation type."""
        return [
            edge for edge in self.edges.values() if edge.relation_type == relation_type
        ]

    def get_neighbors(
        self, node_id: str, relation_type: Optional[str] = None
    ) -> list[tuple[GraphNode, GraphEdge]]:
        """
        Get neighboring nodes.

        Args:
            node_id: Node ID
            relation_type: Optional filter by relation type

        Returns:
            List of (neighbor_node, edge) tuples
        """
        neighbors = []

        for edge in self.edges.values():
            if edge.source_id == node_id:
                neighbor = self.nodes.get(edge.target_id)
                if neighbor:
                    if relation_type is None or edge.relation_type == relation_type:
                        neighbors.append((neighbor, edge))
            elif edge.target_id == node_id:
                neighbor = self.nodes.get(edge.source_id)
                if neighbor:
                    if relation_type is None or edge.relation_type == relation_type:
                        neighbors.append((neighbor, edge))

        return neighbors

    def find_paths(
        self, source_id: str, target_id: str, max_depth: int = 3
    ) -> list[list[str]]:
        """
        Find paths between two nodes.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            max_depth: Maximum path depth

        Returns:
            List of paths (each path is a list of node IDs)
        """
        paths = []

        def dfs(current: str, target: str, visited: set, path: list):
            if current == target:
                paths.append(path.copy())
                return

            if len(path) >= max_depth:
                return

            visited.add(current)

            for edge in self.edges.values():
                next_node = None
                if edge.source_id == current and edge.target_id not in visited:
                    next_node = edge.target_id
                elif edge.target_id == current and edge.source_id not in visited:
                    next_node = edge.source_id

                if next_node:
                    path.append(next_node)
                    dfs(next_node, target, visited, path)
                    path.pop()

            visited.remove(current)

        dfs(source_id, target_id, set(), [source_id])
        return paths

    def delete_node(self, node_id: str) -> bool:
        """Delete node and all connected edges."""
        if node_id not in self.nodes:
            return False

        edges_to_delete = [
            eid
            for eid, edge in self.edges.items()
            if edge.source_id == node_id or edge.target_id == node_id
        ]

        for edge_id in edges_to_delete:
            del self.edges[edge_id]

        del self.nodes[node_id]
        self._save_index()

        return True

    def delete_edge(self, edge_id: str) -> bool:
        """Delete edge by ID."""
        if edge_id in self.edges:
            del self.edges[edge_id]
            self._save_index()
            return True
        return False

    def get_stats(self) -> dict:
        """Get graph statistics."""
        relation_counts = {}
        for edge in self.edges.values():
            relation_counts[edge.relation_type] = (
                relation_counts.get(edge.relation_type, 0) + 1
            )

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "relation_types": relation_counts,
            "node_labels": list(set(node.label for node in self.nodes.values())),
        }

    def clear(self):
        """Clear all nodes and edges."""
        self.nodes.clear()
        self.edges.clear()
        self._save_index()

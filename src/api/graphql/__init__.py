#!/usr/bin/env python3
"""
GraphQL API
===========
Provides GraphQL interface for querying atoms.

Features:
- Implement schema
- CRUD operations
- Search queries
- Pagination
- Error handling
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class GraphQLQuery:
    """Represents a GraphQL query."""

    query: str
    variables: dict = field(default_factory=dict)
    operation_name: Optional[str] = None


@dataclass
class GraphQLResult:
    """Represents a GraphQL result."""

    data: Optional[dict] = None
    errors: list = field(default_factory=list)


class GraphQLSchema:
    """GraphQL schema definition."""

    def __init__(self):
        self.types: dict[str, dict] = {}
        self.queries: dict[str, callable] = {}
        self.mutations: dict[str, callable] = {}
        self.resolvers: dict[str, callable] = {}

        self._register_default_schema()

    def _register_default_schema(self):
        """Register default GraphQL schema."""
        self.types["Atom"] = {
            "id": "ID!",
            "content": "String!",
            "atomType": "String",
            "confidence": "Float",
            "metadata": "JSON",
        }

        self.types["Relation"] = {
            "id": "ID!",
            "sourceId": "ID!",
            "targetId": "ID!",
            "relationType": "String!",
            "confidence": "Float",
        }

        self.types["Query"] = {
            "atoms": "[Atom]",
            "atom": "Atom",
            "relations": "[Relation]",
            "search": "[Atom]",
        }

    def register_query(self, name: str, resolver: callable):
        """Register a query resolver."""
        self.queries[name] = resolver

    def register_mutation(self, name: str, resolver: callable):
        """Register a mutation resolver."""
        self.mutations[name] = resolver

    def register_resolver(self, field_path: str, resolver: callable):
        """Register a field resolver."""
        self.resolvers[field_path] = resolver

    def get_schemaSDL(self) -> str:
        """Get GraphQL schema as SDL."""
        sdl = ""

        for type_name, fields in self.types.items():
            sdl += f"type {type_name} {{\n"
            for field_name, field_type in fields.items():
                sdl += f"  {field_name}: {field_type}\n"
            sdl += "}}\n\n"

        if self.queries:
            sdl += "type Query {\n"
            for q_name, q_type in self.queries.items():
                sdl += f"  {q_name}: {q_type}\n"
            sdl += "}\n\n"

        if self.mutations:
            sdl += "type Mutation {\n"
            for m_name, m_type in self.mutations.items():
                sdl += f"  {m_name}: {m_type}\n"
            sdl += "}\n\n"

        return sdl


class GraphQLAPI:
    """Provides GraphQL interface for querying atoms."""

    def __init__(self):
        self.schema = GraphQLSchema()
        self.data: dict[str, list[dict]] = {"atoms": [], "relations": []}
        self.page_size = 20

        self._register_default_resolvers()

    def _register_default_resolvers(self):
        """Register default resolvers."""
        self.schema.register_query("atoms", self._resolve_atoms)
        self.schema.register_query("atom", self._resolve_atom)
        self.schema.register_query("relations", self._resolve_relations)
        self.schema.register_query("search", self._resolve_search)

        self.schema.register_mutation("createAtom", self._mutate_create_atom)
        self.schema.register_mutation("updateAtom", self._mutate_update_atom)
        self.schema.register_mutation("deleteAtom", self._mutate_delete_atom)

    def load_data(self, atoms: list[dict], relations: list[dict]):
        """Load data into the API."""
        self.data["atoms"] = atoms
        self.data["relations"] = relations

    def _resolve_atoms(self, info: dict, **kwargs) -> list[dict]:
        """Resolve atoms query."""
        atoms = self.data.get("atoms", [])

        offset = kwargs.get("offset", 0)
        first = kwargs.get("first", self.page_size)

        return atoms[offset : offset + first]

    def _resolve_atom(self, info: dict, **kwargs) -> Optional[dict]:
        """Resolve single atom query."""
        atom_id = kwargs.get("id")
        if not atom_id:
            return None

        for atom in self.data.get("atoms", []):
            if atom.get("id") == atom_id:
                return atom

        return None

    def _resolve_relations(self, info: dict, **kwargs) -> list[dict]:
        """Resolve relations query."""
        relations = self.data.get("relations", [])

        source_id = kwargs.get("sourceId")
        target_id = kwargs.get("targetId")

        if source_id:
            relations = [r for r in relations if r.get("sourceId") == source_id]
        if target_id:
            relations = [r for r in relations if r.get("targetId") == target_id]

        return relations

    def _resolve_search(self, info: dict, **kwargs) -> list[dict]:
        """Resolve search query."""
        query = kwargs.get("query", "").lower()
        if not query:
            return []

        results = []
        for atom in self.data.get("atoms", []):
            content = atom.get("content", "").lower()
            if query in content:
                results.append(atom)

        return results

    def _mutate_create_atom(self, info: dict, **kwargs) -> dict:
        """Create atom mutation."""
        atom = {
            "id": kwargs.get("id", f"atom_{len(self.data['atoms'])}"),
            "content": kwargs.get("content", ""),
            "atomType": kwargs.get("atomType", "unknown"),
            "confidence": kwargs.get("confidence", 1.0),
            "metadata": kwargs.get("metadata", {}),
            "createdAt": datetime.now().isoformat(),
        }

        self.data["atoms"].append(atom)
        return atom

    def _mutate_update_atom(self, info: dict, **kwargs) -> Optional[dict]:
        """Update atom mutation."""
        atom_id = kwargs.get("id")

        for i, atom in enumerate(self.data["atoms"]):
            if atom.get("id") == atom_id:
                atom.update(kwargs)
                self.data["atoms"][i] = atom
                return atom

        return None

    def _mutate_delete_atom(self, info: dict, **kwargs) -> bool:
        """Delete atom mutation."""
        atom_id = kwargs.get("id")

        for i, atom in enumerate(self.data["atoms"]):
            if atom.get("id") == atom_id:
                del self.data["atoms"][i]
                return True

        return False

    def execute(self, query: str, variables: Optional[dict] = None) -> GraphQLResult:
        """
        Execute a GraphQL query.

        Args:
            query: GraphQL query string
            variables: Query variables

        Returns:
            GraphQLResult
        """
        variables = variables or {}

        try:
            parsed = self._parse_query(query)

            if not parsed:
                return GraphQLResult(
                    errors=[{"message": "Invalid query", "locations": []}]
                )

            operation_type = parsed.get("type")
            operation_name = parsed.get("name")
            selections = parsed.get("selections", [])

            if operation_type == "query":
                data = self._execute_query(selections, variables)
                return GraphQLResult(data=data)

            elif operation_type == "mutation":
                data = self._execute_mutation(selections, variables)
                return GraphQLResult(data=data)

            else:
                return GraphQLResult(
                    errors=[{"message": "Unknown operation type", "locations": []}]
                )

        except Exception as e:
            return GraphQLResult(errors=[{"message": str(e), "locations": []}])

    def _parse_query(self, query: str) -> Optional[dict]:
        """Simple query parser."""
        query = query.strip()

        if query.startswith("query"):
            op_type = "query"
        elif query.startswith("mutation"):
            op_type = "mutation"
        else:
            op_type = "query"

        selections = []

        import re

        pattern = r"(\w+)(?:\(([^)]+)\))?"
        for match in re.finditer(pattern, query):
            field_name = match.group(1)
            if field_name in ["query", "mutation", "{", "}", "fragment"]:
                continue
            selections.append({"name": field_name})

        return {"type": op_type, "selections": selections}

    def _execute_query(self, selections: list[dict], variables: dict) -> dict:
        """Execute query selections."""
        result = {}

        for selection in selections:
            name = selection.get("name")

            if name in self.schema.queries:
                resolver = self.schema.queries[name]
                result[name] = resolver(info={}, **{k: v for k, v in variables.items()})
            elif name in self.data:
                result[name] = self.data[name]

        return result

    def _execute_mutation(self, selections: list[dict], variables: dict) -> dict:
        """Execute mutation selections."""
        result = {}

        for selection in selections:
            name = selection.get("name")

            if name in self.schema.mutations:
                resolver = self.schema.mutations[name]
                result[name] = resolver(info={}, **{k: v for k, v in variables.items()})

        return result

    def get_schema(self) -> str:
        """Get GraphQL schema SDL."""
        return self.schema.get_schemaSDL()

    def get_stats(self) -> dict:
        """Get API statistics."""
        return {
            "total_atoms": len(self.data.get("atoms", [])),
            "total_relations": len(self.data.get("relations", [])),
            "queries": list(self.schema.queries.keys()),
            "mutations": list(self.schema.mutations.keys()),
        }

#!/usr/bin/env python3
"""
Vector Storage
===============
Stores embeddings for semantic retrieval.

Features:
- Generate embeddings for atoms
- Store in vector database
- Support similarity search
- Support hybrid queries
"""

import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class VectorEntry:
    """Represents a vector entry with metadata."""

    id: str
    vector: list[float]
    content: str
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class VectorStore:
    """Stores embeddings for semantic retrieval using local FAISS-like implementation."""

    def __init__(self, storage_dir: str = "./data/vector", dimension: int = 384):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.dimension = dimension
        self.entries: dict[str, VectorEntry] = {}
        self._load_index()

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _load_index(self):
        """Load the vector index."""
        index_path = self.storage_dir / "index.json"
        if index_path.exists():
            try:
                data = json.loads(index_path.read_text("utf-8"))
                dimension = data.get("dimension", self.dimension)
                self.dimension = dimension
                for entry_id, entry_data in data.get("entries", {}).items():
                    self.entries[entry_id] = VectorEntry(**entry_data)
            except Exception as e:
                print(f"Error loading index: {e}")

    def _save_index(self):
        """Save the vector index."""
        index_path = self.storage_dir / "index.json"
        data = {
            "dimension": self.dimension,
            "entries": {
                entry_id: {
                    "id": entry.id,
                    "vector": entry.vector,
                    "content": entry.content,
                    "metadata": entry.metadata,
                    "created_at": entry.created_at,
                }
                for entry_id, entry in self.entries.items()
            },
        }
        index_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _normalize(self, vector: list[float]) -> list[float]:
        """Normalize vector to unit length."""
        magnitude = math.sqrt(sum(x * x for x in vector))
        if magnitude == 0:
            return vector
        return [x / magnitude for x in vector]

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        return dot_product

    def _generate_embedding(self, content: str) -> list[float]:
        """Generate a simple embedding for content (placeholder - use actual embeddings in production)."""
        content_hash = self._compute_hash(content)

        seed = int(content_hash[:8], 16)

        import random

        random.seed(seed)

        vector = [random.gauss(0, 1) for _ in range(self.dimension)]

        return self._normalize(vector)

    def add(self, content: str, metadata: Optional[dict] = None) -> str:
        """
        Add content to the vector store.

        Args:
            content: Text content to embed
            metadata: Optional metadata

        Returns:
            Entry ID
        """
        entry_id = self._compute_hash(content)[:16]

        if entry_id in self.entries:
            return entry_id

        vector = self._generate_embedding(content)

        entry = VectorEntry(
            id=entry_id, vector=vector, content=content, metadata=metadata or {}
        )

        self.entries[entry_id] = entry
        self._save_index()

        return entry_id

    def add_with_vector(
        self, content: str, vector: list[float], metadata: Optional[dict] = None
    ) -> str:
        """
        Add content with pre-computed vector.

        Args:
            content: Text content
            vector: Pre-computed embedding vector
            metadata: Optional metadata

        Returns:
            Entry ID
        """
        entry_id = self._compute_hash(content)[:16]

        if entry_id in self.entries:
            return entry_id

        vector = self._normalize(vector)

        entry = VectorEntry(
            id=entry_id, vector=vector, content=content, metadata=metadata or {}
        )

        self.entries[entry_id] = entry
        self._save_index()

        return entry_id

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float, str]]:
        """
        Search for similar content.

        Args:
            query: Query text
            top_k: Number of results to return

        Returns:
            List of (entry_id, score, content) tuples
        """
        query_vector = self._generate_embedding(query)

        similarities = []
        for entry_id, entry in self.entries.items():
            score = self._cosine_similarity(query_vector, entry.vector)
            similarities.append((entry_id, score, entry.content))

        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def search_by_vector(
        self, vector: list[float], top_k: int = 10
    ) -> list[tuple[str, float, str]]:
        """
        Search by vector.

        Args:
            vector: Query vector
            top_k: Number of results to return

        Returns:
            List of (entry_id, score, content) tuples
        """
        query_vector = self._normalize(vector)

        similarities = []
        for entry_id, entry in self.entries.items():
            score = self._cosine_similarity(query_vector, entry.vector)
            similarities.append((entry_id, score, entry.content))

        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def get(self, entry_id: str) -> Optional[VectorEntry]:
        """Get entry by ID."""
        return self.entries.get(entry_id)

    def delete(self, entry_id: str) -> bool:
        """Delete entry by ID."""
        if entry_id in self.entries:
            del self.entries[entry_id]
            self._save_index()
            return True
        return False

    def get_stats(self) -> dict:
        """Get storage statistics."""
        return {
            "total_entries": len(self.entries),
            "dimension": self.dimension,
            "storage_size_bytes": sum(
                len(json.dumps(e.vector).encode("utf-8")) + len(e.content)
                for e in self.entries.values()
            ),
        }

    def clear(self):
        """Clear all entries."""
        self.entries.clear()
        self._save_index()

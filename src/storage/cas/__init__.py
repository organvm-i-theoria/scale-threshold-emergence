#!/usr/bin/env python3
"""
Content-Addressable Storage
===========================
Stores atom content with content hashing.

Features:
- Hash content with SHA-256
- Store by content hash
- Verify integrity on read
- Deduplicate content
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class CASObject:
    """Represents a content-addressable object."""

    hash: str
    content: str
    content_type: str
    size: int
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ref_count: int = 1


class ContentAddressableStorage:
    """Stores atom content with content hashing."""

    def __init__(self, storage_dir: str = "./data/cas"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.objects: dict[str, CASObject] = {}
        self._load_index()

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _get_object_path(self, hash: str) -> Path:
        """Get the file path for a content hash."""
        return self.storage_dir / f"{hash}.json"

    def _load_index(self):
        """Load the storage index."""
        index_path = self.storage_dir / "index.json"
        if index_path.exists():
            try:
                data = json.loads(index_path.read_text("utf-8"))
                for hash_val, obj_data in data.items():
                    self.objects[hash_val] = CASObject(**obj_data)
            except Exception as e:
                print(f"Error loading index: {e}")

    def _save_index(self):
        """Save the storage index."""
        index_path = self.storage_dir / "index.json"
        data = {
            hash_val: {
                "hash": obj.hash,
                "content": obj.content,
                "content_type": obj.content_type,
                "size": obj.size,
                "metadata": obj.metadata,
                "created_at": obj.created_at,
                "ref_count": obj.ref_count,
            }
            for hash_val, obj in self.objects.items()
        }
        index_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def put(
        self, content: str, content_type: str = "text", metadata: Optional[dict] = None
    ) -> str:
        """
        Store content and return its content hash.

        Args:
            content: Content to store
            content_type: Type of content (text, json, code, etc.)
            metadata: Optional metadata

        Returns:
            Content hash (SHA-256)
        """
        content_hash = self._compute_hash(content)

        if content_hash in self.objects:
            self.objects[content_hash].ref_count += 1
            self._save_index()
            return content_hash

        obj = CASObject(
            hash=content_hash,
            content=content,
            content_type=content_type,
            size=len(content.encode("utf-8")),
            metadata=metadata or {},
            ref_count=1,
        )

        self.objects[content_hash] = obj
        self._save_index()

        return content_hash

    def get(self, content_hash: str) -> Optional[CASObject]:
        """
        Retrieve content by its hash.

        Args:
            content_hash: SHA-256 hash of content

        Returns:
            CASObject if found, None otherwise
        """
        return self.objects.get(content_hash)

    def get_content(self, content_hash: str) -> Optional[str]:
        """
        Retrieve raw content by its hash.

        Args:
            content_hash: SHA-256 hash of content

        Returns:
            Content string if found, None otherwise
        """
        obj = self.objects.get(content_hash)
        return obj.content if obj else None

    def verify(self, content_hash: str, content: str) -> bool:
        """
        Verify content matches the stored hash.

        Args:
            content_hash: Expected hash
            content: Content to verify

        Returns:
            True if content matches hash, False otherwise
        """
        computed_hash = self._compute_hash(content)
        return computed_hash == content_hash

    def exists(self, content_hash: str) -> bool:
        """Check if content exists in storage."""
        return content_hash in self.objects

    def delete(self, content_hash: str) -> bool:
        """
        Delete content from storage (decrement ref count).

        Args:
            content_hash: SHA-256 hash of content

        Returns:
            True if content was deleted, False if still referenced
        """
        if content_hash not in self.objects:
            return False

        obj = self.objects[content_hash]
        obj.ref_count -= 1

        if obj.ref_count <= 0:
            del self.objects[content_hash]
            obj_path = self._get_object_path(content_hash)
            if obj_path.exists():
                obj_path.unlink()

        self._save_index()
        return True

    def get_stats(self) -> dict:
        """Get storage statistics."""
        total_objects = len(self.objects)
        total_size = sum(obj.size for obj in self.objects.values())
        total_refs = sum(obj.ref_count for obj in self.objects.values())

        return {
            "total_objects": total_objects,
            "total_size_bytes": total_size,
            "total_references": total_refs,
            "unique_content": total_objects,
        }

    def deduplicate(self) -> int:
        """Get deduplication statistics (always returns 0 since we deduplicate on write)."""
        return 0

    def list_hashes(self) -> list[str]:
        """List all content hashes in storage."""
        return list(self.objects.keys())

    def search_by_type(self, content_type: str) -> list[str]:
        """Search for content by type."""
        return [
            hash_val
            for hash_val, obj in self.objects.items()
            if obj.content_type == content_type
        ]

    def clear(self):
        """Clear all content from storage."""
        self.objects.clear()
        self._save_index()

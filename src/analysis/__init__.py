#!/usr/bin/env python3
"""
Analysis Normalization
======================
Normalizes and validates extracted atoms.

Features:
- Apply canonicalization rules
- Validate against schemas
- Resolve aliases
- Merge duplicate atoms
"""

import hashlib
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NormalizedAtom:
    """Represents a normalized atom."""

    id: str
    canonical_form: str
    atom_type: str
    aliases: list = field(default_factory=list)
    merged_from: list = field(default_factory=list)
    confidence: float = 1.0
    validation_errors: list = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of validation."""

    valid: bool
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


class AnalysisNormalizer:
    """Normalizes and validates extracted atoms."""

    def __init__(self, controlled_vocabulary: Optional[dict] = None):
        self.vocabulary = controlled_vocabulary or {}
        self.alias_map: dict[str, str] = {}
        self.canonical_forms: dict[str, str] = {}
        self.min_confidence = 0.5

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _canonicalize(self, text: str) -> str:
        """Apply canonicalization rules to text."""
        canonical = text.lower().strip()

        canonical = re.sub(r"[^\w\s]", "", canonical)

        canonical = re.sub(r"\s+", " ", canonical)

        return canonical

    def _validate_schema(self, atom: dict) -> ValidationResult:
        """Validate atom against schema."""
        errors = []
        warnings = []

        required_fields = ["id", "content", "atom_type"]
        for required_field in required_fields:
            if required_field not in atom:
                errors.append(f"Missing required field: {required_field}")

        if "content" in atom:
            if len(atom["content"]) < 2:
                errors.append("Content too short")
            if len(atom["content"]) > 1000:
                warnings.append("Content very long - may need review")

        if "atom_type" in atom:
            valid_types = [
                "concept",
                "entity",
                "relation",
                "statement",
                "function",
                "class",
                "import",
            ]
            if atom["atom_type"] not in valid_types:
                warnings.append(f"Unknown atom type: {atom['atom_type']}")

        return ValidationResult(
            valid=len(errors) == 0, errors=errors, warnings=warnings
        )

    def add_alias(self, alias: str, canonical: str):
        """Add an alias mapping."""
        alias_canonical = self._canonicalize(alias)
        canonical_form = self._canonicalize(canonical)

        self.alias_map[alias_canonical] = canonical_form

    def resolve_alias(self, text: str) -> str:
        """Resolve alias to canonical form."""
        canonical = self._canonicalize(text)
        return self.alias_map.get(canonical, text)

    def normalize_atom(self, atom: dict) -> NormalizedAtom:
        """
        Normalize a single atom.

        Args:
            atom: Atom dictionary with 'id', 'content', 'atom_type', etc.

        Returns:
            NormalizedAtom
        """
        validation = self._validate_schema(atom)

        canonical_form = self._canonicalize(atom.get("content", ""))

        if canonical_form in self.canonical_forms:
            existing_id = self.canonical_forms[canonical_form]
            return NormalizedAtom(
                id=atom.get("id", ""),
                canonical_form=canonical_form,
                atom_type=atom.get("atom_type", "unknown"),
                aliases=[atom.get("content", "")],
                merged_from=[existing_id],
                confidence=0.9,
                validation_errors=validation.errors,
            )

        self.canonical_forms[canonical_form] = atom.get("id", "")

        vocab_terms = []
        for category, terms in self.vocabulary.items():
            for term in terms:
                if term.lower() in canonical_form:
                    vocab_terms.append(f"{category}:{term}")

        confidence = 1.0
        if vocab_terms:
            confidence = min(1.0, confidence + 0.1)

        if validation.warnings:
            confidence -= 0.1

        return NormalizedAtom(
            id=atom.get("id", ""),
            canonical_form=canonical_form,
            atom_type=atom.get("atom_type", "unknown"),
            aliases=[],
            merged_from=[],
            confidence=max(self.min_confidence, confidence),
            validation_errors=validation.errors,
        )

    def normalize_atoms(self, atoms: list[dict]) -> list[NormalizedAtom]:
        """
        Normalize multiple atoms.

        Args:
            atoms: List of atom dictionaries

        Returns:
            List of NormalizedAtoms
        """
        normalized = []

        for atom in atoms:
            norm_atom = self.normalize_atom(atom)
            normalized.append(norm_atom)

        return normalized

    def merge_duplicates(self, atoms: list[dict]) -> list[NormalizedAtom]:
        """
        Merge duplicate atoms.

        Args:
            atoms: List of atom dictionaries

        Returns:
            List of NormalizedAtoms with duplicates merged
        """
        hash_map: dict[str, list[dict]] = {}

        for atom in atoms:
            content_hash = self._compute_hash(atom.get("content", ""))
            if content_hash not in hash_map:
                hash_map[content_hash] = []
            hash_map[content_hash].append(atom)

        merged = []
        for content_hash, atom_group in hash_map.items():
            if len(atom_group) == 1:
                merged.append(self.normalize_atom(atom_group[0]))
            else:
                primary = atom_group[0]
                merged_ids = [a.get("id", "") for a in atom_group]

                norm_atom = self.normalize_atom(primary)
                norm_atom.merged_from = merged_ids
                norm_atom.confidence = min(1.0, 0.9 + (len(atom_group) - 1) * 0.05)

                merged.append(norm_atom)

        return merged

    def get_stats(self) -> dict:
        """Get normalization statistics."""
        return {
            "canonical_forms": len(self.canonical_forms),
            "aliases": len(self.alias_map),
            "vocabulary_categories": len(self.vocabulary),
        }

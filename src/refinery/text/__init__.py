#!/usr/bin/env python3
"""
Text Refinery
==============
Transforms raw text into atomic knowledge units.

Features:
- Segment text into logical units
- Extract concepts as text atoms
- Identify relations between atoms
- Apply controlled vocabulary
- Assign provenance and confidence
"""

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TextAtom:
    """Represents an atomic unit of text knowledge."""

    id: str
    content: str
    atom_type: str  # concept, entity, relation, statement
    confidence: float = 1.0
    provenance: dict = field(default_factory=dict)
    vocabulary_terms: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TextRelation:
    """Represents a relation between text atoms."""

    id: str
    source_id: str
    target_id: str
    relation_type: str  # isa, part_of, related_to, causes, etc.
    confidence: float = 1.0
    provenance: dict = field(default_factory=dict)


@dataclass
class RefinedText:
    """Represents refined text with extracted atoms and relations."""

    source_hash: str
    atoms: list = field(default_factory=list)
    relations: list = field(default_factory=list)
    segments: list = field(default_factory=list)
    vocabulary: dict = field(default_factory=dict)


class TextRefinery:
    """Transforms raw text into atomic knowledge units."""

    CONCEPT_PATTERNS = {
        "definition": re.compile(
            r"\b(\w+(?:\s+\w+)?)\s+is\s+(?:a|an|the)\s+(.+?)(?:\.|$)", re.IGNORECASE
        ),
        "term": re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b"),
        "process": re.compile(r"\b(\w+ing)\s+(?:the\s+)?(\w+)(?:\.|$)", re.IGNORECASE),
    }

    RELATION_PATTERNS = {
        "isa": re.compile(r"\b(\w+)\s+is\s+(?:a|an)\s+(\w+)", re.IGNORECASE),
        "part_of": re.compile(
            r"\b(\w+)\s+is\s+(?:part of|part of the)\s+(\w+)", re.IGNORECASE
        ),
        "related_to": re.compile(r"\b(\w+)\s+(?:and|with)\s+(\w+)", re.IGNORECASE),
        "causes": re.compile(r"\b(\w+)\s+causes\s+(?:that\s+)?(\w+)", re.IGNORECASE),
    }

    def __init__(self, controlled_vocabulary: Optional[dict] = None):
        self.vocabulary = controlled_vocabulary or {}
        self.min_confidence = 0.5
        self.min_atom_length = 3
        self.max_atom_length = 500

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()

    def _segment_text(self, text: str) -> list[str]:
        """Segment text into logical units."""
        segments = []

        paragraph_split = re.split(r"\n\s*\n", text)
        for para in paragraph_split:
            para = para.strip()
            if not para:
                continue

            sentences = re.split(r"(?<=[.!?])\s+", para)
            current_segment = []

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue

                current_segment.append(sentence)

                if len(" ".join(current_segment)) > 200:
                    segments.append(" ".join(current_segment))
                    current_segment = []

            if current_segment:
                segments.append(" ".join(current_segment))

        return segments

    def _extract_concepts(self, text: str, source_hash: str) -> list[TextAtom]:
        """Extract concepts as text atoms."""
        atoms = []

        for match in self.CONCEPT_PATTERNS["definition"].finditer(text):
            term = match.group(1).strip()
            definition = match.group(2).strip()

            if self.min_atom_length <= len(term) <= self.max_atom_length:
                atom_id = f"atom_{self._compute_hash(term + source_hash)[:12]}"
                atoms.append(
                    TextAtom(
                        id=atom_id,
                        content=f"{term}: {definition}",
                        atom_type="concept",
                        confidence=0.9,
                        provenance={
                            "source": "definition_pattern",
                            "match": match.group(0),
                        },
                        vocabulary_terms=self._match_vocabulary(term),
                    )
                )

        for match in self.CONCEPT_PATTERNS["term"].finditer(text):
            term = match.group(0).strip()

            if term.lower() in [a.content for a in atoms]:
                continue

            if self.min_atom_length <= len(term) <= self.max_atom_length:
                atom_id = f"atom_{self._compute_hash(term + source_hash)[:12]}"
                atoms.append(
                    TextAtom(
                        id=atom_id,
                        content=term,
                        atom_type="entity",
                        confidence=0.7,
                        provenance={"source": "term_pattern"},
                        vocabulary_terms=self._match_vocabulary(term),
                    )
                )

        return atoms

    def _extract_statements(self, text: str, source_hash: str) -> list[TextAtom]:
        """Extract statements as text atoms."""
        atoms = []

        sentences = re.split(r"(?<=[.!?])\s+", text)
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            if self.min_atom_length <= len(sentence) <= self.max_atom_length:
                atom_id = f"atom_{self._compute_hash(sentence + source_hash)[:12]}"
                atoms.append(
                    TextAtom(
                        id=atom_id,
                        content=sentence,
                        atom_type="statement",
                        confidence=0.8,
                        provenance={"source": "sentence", "index": i},
                    )
                )

        return atoms

    def _identify_relations(
        self, atoms: list[TextAtom], source_hash: str
    ) -> list[TextRelation]:
        """Identify relations between atoms."""
        relations = []
        content_map = {atom.content.lower(): atom.id for atom in atoms}

        for rel_type, pattern in self.RELATION_PATTERNS.items():
            for match in pattern.finditer(" ".join(a.content for a in atoms)):
                source = match.group(1).lower()
                target = match.group(2).lower()

                if source in content_map and target in content_map:
                    rel_id = (
                        f"rel_{self._compute_hash(source + target + source_hash)[:12]}"
                    )
                    relations.append(
                        TextRelation(
                            id=rel_id,
                            source_id=content_map[source],
                            target_id=content_map[target],
                            relation_type=rel_type,
                            confidence=0.8,
                            provenance={"pattern": rel_type},
                        )
                    )

        return relations

    def _match_vocabulary(self, term: str) -> list[str]:
        """Match term against controlled vocabulary."""
        matches = []
        term_lower = term.lower()

        for category, terms in self.vocabulary.items():
            for vocab_term in terms:
                if vocab_term.lower() in term_lower or term_lower in vocab_term.lower():
                    matches.append(f"{category}:{vocab_term}")

        return matches

    def refine(
        self, text: str, source_provenance: Optional[dict] = None
    ) -> RefinedText:
        """
        Transform raw text into atomic knowledge units.

        Args:
            text: Raw text to refine
            source_provenance: Optional provenance info for the source

        Returns:
            RefinedText with atoms and relations
        """
        source_hash = self._compute_hash(text)

        segments = self._segment_text(text)

        atoms = []
        atoms.extend(self._extract_concepts(text, source_hash))
        atoms.extend(self._extract_statements(text, source_hash))

        for atom in atoms:
            if source_provenance:
                atom.provenance.update(source_provenance)

        relations = self._identify_relations(atoms, source_hash)

        return RefinedText(
            source_hash=source_hash,
            atoms=atoms,
            relations=relations,
            segments=segments,
            vocabulary=self.vocabulary,
        )

    def refine_batch(
        self, texts: list[tuple[str, Optional[dict]]]
    ) -> list[RefinedText]:
        """
        Refine multiple texts.

        Args:
            texts: List of (text, provenance) tuples

        Returns:
            List of RefinedText objects
        """
        results = []
        for text, provenance in texts:
            result = self.refine(text, provenance)
            results.append(result)
        return results

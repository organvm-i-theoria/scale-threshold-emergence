---
id: uaks_v1_retrieval_scoring_spec_20260311
title: Retrieval Scoring Specification
type: technical-spec
status: drafted_in_chat
version: 1
---

# Retrieval Scoring Specification

## Purpose

Defines how atoms are scored and ranked during retrieval.

## Scoring Components

### Vector Similarity
- Cosine similarity between query and atom embeddings
- Range: 0.0 to 1.0

### Trust Weight
- Multiplier based on atom trust level (T0-T4)
- Range: 0.1 to 1.0

### Recency Factor
- Boost for recently modified atoms
- Decay over time

### Relation Bonus
- Boost for atoms connected to matched atoms

## Final Score Calculation

```
score = (vector_similarity * 0.5) + 
        (trust_weight * 0.3) + 
        (recency_bonus * 0.1) +
        (relation_bonus * 0.1)
```

## TODO Implementation

```python
# src/retrieval/scoring.py

class RetrievalScorer:
    """Computes relevance scores for retrieved atoms."""
    
    def score(self, query: Query, atoms: list[Atom]) -> list[tuple[Atom, float]]:
        # TODO: Implement
        pass
```

## Acceptance Criteria

- [ ] Scores range 0.0-1.0
- [ ] Perfect match scores > 0.8
- [ ] Trust affects ranking
- [ ] Relations boost related atoms

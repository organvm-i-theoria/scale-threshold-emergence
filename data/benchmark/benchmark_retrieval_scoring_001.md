---
id: benchmark_retrieval_001
type: benchmark
category: retrieval_scoring
status: active
version: 1
source: synthetic
---

# Benchmark: Retrieval Scoring

This benchmark tests the retrieval scoring algorithm for atomic knowledge units.

## Query

```
"mechanism for phase transitions in complex systems"
```

## Corpus (Text Atoms)

| Atom ID | Content | Vector (simplified) |
|---------|---------|---------------------|
| TA-001 | phase transition | [0.9, 0.1, 0.3] |
| TA-002 | complex systems | [0.2, 0.8, 0.5] |
| TA-003 | quantum mechanics | [0.7, 0.2, 0.1] |
| TA-004 | biological evolution | [0.1, 0.6, 0.8] |
| TA-005 | emergence | [0.5, 0.5, 0.6] |
| TA-006 | thermodynamics | [0.6, 0.3, 0.2] |

## Expected Rankings

| Rank | Atom ID | Score (cosine) | Reasoning |
|------|---------|----------------|-----------|
| 1 | TA-001 | 0.85+ | "phase transition" in query |
| 2 | TA-002 | 0.70+ | "complex systems" in query |
| 3 | TA-005 | 0.55+ | related to both terms |
| 4 | TA-006 | 0.40+ | thermodynamics relates to phase |
| 5 | TA-004 | 0.30+ | biological systems show emergence |
| 6 | TA-003 | 0.15+ | distant - quantum not in query |

## Validation Criteria

- [ ] Top-3 results include TA-001, TA-002, TA-005
- [ ] Scores decrease monotonically
- [ ] No negative scores
- [ ] Perfect match scores > 0.8

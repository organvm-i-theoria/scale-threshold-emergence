---
id: uaks_v1_evaluation_pack_A_20260311
title: Evaluation Pack A - Benchmarks
type: evaluation-artifact
status: drafted_in_chat
version: 1
---

# Evaluation Pack A: Benchmarks

## Purpose

Defines benchmark tests for system evaluation.

## Benchmark Categories

### Extraction Benchmarks

| ID | Name | Metric | Target |
|----|------|--------|--------|
| B001 | Text atom extraction | Precision | > 0.95 |
| B002 | Code atom extraction | Recall | > 0.90 |
| B003 | Relation extraction | F1 | > 0.85 |

### Retrieval Benchmarks

| ID | Name | Metric | Target |
|----|------|--------|--------|
| B010 | Top-1 accuracy | Accuracy | > 0.80 |
| B011 | Top-10 recall | Recall | > 0.95 |
| B012 | Latency | P99 | < 200ms |

## Running Benchmarks

```bash
pytest tests/evaluation/test_benchmarks.py -v
```

## Gold Fixtures

See `data/gold/` for canonical test cases.

## Acceptance Criteria

- [ ] All benchmarks defined
- [ ] Gold fixtures created
- [ ] Test runner working
- [ ] Targets achievable

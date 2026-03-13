---
id: benchmark_textatom_001
type: benchmark
category: text_atom_extraction
status: active
version: 1
source: synthetic
---

# Benchmark: Text Atom Extraction

This benchmark tests the ability to extract atomic text units from unstructured research notes.

## Input

```
Research note: The theory of everything applies to multiple domains of reality.
From physics to biology to cognition. Each domain has distinct emergence patterns.
The fundamental layer is physics, which constrains chemistry, which enables biology.
```

## Expected Output (Text Atoms)

| Atom ID | Content | Type | Source Range |
|---------|---------|------|--------------|
| TA-001 | theory of everything | concept | 0-21 |
| TA-002 | multiple domains | concept | 22-38 |
| TA-003 | physics | domain | 45-52 |
| TA-004 | biology | domain | 60-67 |
| TA-005 | cognition | domain | 72-80 |
| TA-006 | emergence patterns | concept | 82-99 |
| TA-007 | fundamental layer | concept | 107-122 |
| TA-008 | constrains | relation | 130-140 |
| TA-009 | enables | relation | 153-160 |

## Validation Criteria

- [ ] All domains extracted
- [ ] All relations identified
- [ ] Source ranges accurate
- [ ] No spurious atoms

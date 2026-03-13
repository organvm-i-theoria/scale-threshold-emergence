---
id: gold_primitive_001
type: gold_fixture
category: primitive
status: canonical
version: 1
---

# Gold Fixture: Primitive Atom

This is the canonical form for a primitive atom in the system.

## Atom Record

```json
{
  "atom_id": "PRIM-001",
  "atom_type": "primitive",
  "name": "process",
  "definition": "A primitive denoting continuous transformation or action in a system",
  "category": "process_primitive",
  "provenance": {
    "source": "primitive_canon_v1",
    "extracted_from": "research/thread_pairs/TH-049-Thought-for-45s.md",
    "confidence": 0.95
  },
  "relations": [
    {"target": "state", "type": "transforms_to"},
    {"target": "constraint", "type": "bounded_by"},
    {"target": "event", "type": "generates"}
  ],
  "metadata": {
    "created_at": "2026-03-11T00:00:00Z",
    "version": 1,
    "status": "stable"
  }
}
```

## Validation Rules

- atom_id MUST match pattern `^PRIM-\d{3}$`
- atom_type MUST be "primitive"
- name MUST be non-empty string
- provenance MUST include source reference
- relations MUST be valid target atoms

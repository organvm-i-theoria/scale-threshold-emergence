---
id: gold_module_001
type: gold_fixture
category: module
status: canonical
version: 1
---

# Gold Fixture: Module Atom

This is the canonical form for a module atom in the system.

## Atom Record

```json
{
  "atom_id": "MOD-001",
  "atom_type": "module",
  "name": "cosmological_module",
  "scale": "universal",
  "definition": "A module representing the universal cosmological substrate",
  "parameters": [
    {"name": "expansion_rate", "type": "float", "unit": "m/s"},
    {"name": "matter_density", "type": "float", "unit": "kg/m^3"},
    {"name": "dark_energy_fraction", "type": "float", "range": [0, 1]}
  ],
  "couplings": [
    {"target": "MOD-002", "type": "constrains", "direction": "upward"},
    {"target": "PRIM-001", "type": "implements", "direction": "instantiates"}
  ],
  "provenance": {
    "source": "module_library_v1",
    "extracted_from": "research/thread_pairs/TH-049-Thought-for-45s.md",
    "confidence": 0.88
  },
  "metadata": {
    "created_at": "2026-03-11T00:00:00Z",
    "version": 1,
    "status": "draft"
  }
}
```

## Validation Rules

- atom_id MUST match pattern `^MOD-\d{3}$`
- atom_type MUST be "module"
- scale MUST be from valid scale list (subatomic...universal)
- parameters MUST each have name, type, and unit/range
- couplings MUST reference valid atom IDs

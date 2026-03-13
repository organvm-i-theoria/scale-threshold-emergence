---
id: gold_mechanism_001
type: gold_fixture
category: mechanism
status: canonical
version: 1
---

# Gold Fixture: Mechanism Atom

This is the canonical form for a mechanism atom in the system.

## Atom Record

```json
{
  "atom_id": "MECH-001",
  "atom_type": "mechanism",
  "name": "feedback_regulation",
  "family": "control_systems",
  "definition": "A mechanism where system output feeds back to influence future behavior",
  "input_types": ["signal", "state"],
  "output_types": ["control_action", "parameter_adjustment"],
  "scale_applicability": ["molecular", "biological", "social", "civilizational"],
  "provenance": {
    "source": "mechanism_registry_v1",
    "extracted_from": "research/thread_pairs/TH-049-Thought-for-45s.md",
    "confidence": 0.92
  },
  "related_primitives": [
    "signal", "constraint", "state", "attractor"
  ],
  "examples": [
    "thermostat regulation",
    "hormone feedback loops",
    "market price signals",
    "cultural norms reinforcement"
  ],
  "metadata": {
    "created_at": "2026-03-11T00:00:00Z",
    "version": 1,
    "status": "stable"
  }
}
```

## Validation Rules

- atom_id MUST match pattern `^MECH-\d{3}$`
- atom_type MUST be "mechanism"
- family MUST be from approved mechanism families list
- scale_applicability MUST include at least one valid scale
- related_primitives MUST reference valid primitive IDs

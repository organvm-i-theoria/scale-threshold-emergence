---
id: uaks_v1_text_refinery_spec_20260311
title: Text Refinery Specification
type: technical-spec
status: drafted_in_chat
version: 1
---

# Text Refinery Specification

## Purpose

The text refinery transforms raw textual input into atomic knowledge units.

## Processing Stages

### Stage 1: Segmentation
- Split input into logical segments
- Identify paragraph boundaries
- Detect section headers

### Stage 2: Atom Extraction
- Extract concepts as text atoms
- Identify relations between atoms
- Tag atoms with types

### Stage 3: Normalization
- Standardize terminology
- Apply controlled vocabulary
- Resolve aliases

### Stage 4: Provenance Assignment
- Record source location
- Assign confidence scores
- Link to parent atoms

## TODO Implementation

```python
# src/refinery/text/refinery.py

class TextRefinery:
    """Transforms text into atomic knowledge units."""
    
    def process(self, text: str, source: Provenance) -> list[TextAtom]:
        # TODO: Implement
        pass
```

## Acceptance Criteria

- [ ] Segmentation handles nested structures
- [ ] Atom extraction identifies 95%+ of concepts
- [ ] Normalization uses controlled vocabulary
- [ ] Provenance fully tracked

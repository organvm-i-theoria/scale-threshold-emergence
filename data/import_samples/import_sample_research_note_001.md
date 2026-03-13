---
id: import_sample_001
type: import_bundle
category: research_note
status: sample
version: 1
---

# Import Sample: Research Note

This is a sample research note that can be imported into the knowledge engine.

## Source

```markdown
# Research Note: Emergence in Complex Systems

## Key Concept
Emergence is the phenomenon where complex patterns arise from simple rules.

## Levels of Emergence
1. Weak emergence: predictable from lower levels
2. Strong emergence: not predictable, novel properties

## Examples
- Temperature (statistical emergence from particle motion)
- Consciousness (strong emergence from neural activity)
- Markets (emergent from individual economic actors)

## Related Mechanisms
- Feedback regulation
- Attractor dynamics
- Network effects

## References
- Philip Anderson (1972): "More Is Different"
- John Holland (1995): "Hidden Order"
```

## Expected Processing

When imported, this note should produce:
- 3-5 text atoms for key concepts
- 2-3 mechanism references
- 1 module reference (neural_network)
- Relations between atoms based on semantic connections

## Import Metadata

```json
{
  "import_id": "IMP-001",
  "source_type": "markdown",
  "content_hash": "sha256:abc123...",
  "extracted_at": "2026-03-12T00:00:00Z",
  "expected_atoms": 8,
  "expected_relations": 6
}
```

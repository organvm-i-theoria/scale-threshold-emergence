---
id: mechanism_pack_spec_v1
title: "Mechanism Pack Spec"
type: technical-spec
status: derived_from_thread
version: 1
source_artifacts:
  - docs/kernel_spec.md
---

# Mechanism Pack Spec

A mechanism pack is how literature becomes executable theory.

Required fields:

| Field | Meaning |
| --- | --- |
| mechanism_pack_id | implementation ID |
| source_mechanism_id | canonical registry linkage |
| target_threshold_id | threshold served |
| required_modules | module dependencies |
| required_primitives | conceptual dependencies |
| law_profile_compatibility | which worlds can host it |
| parameter_defaults | default settings |
| runtime_operators | executable behaviors |
| evidence_note | empirical or theoretical basis |
| revision_status | provisional / stable / deprecated |

Comparative modeling rule:

- A single threshold can host multiple competing mechanism packs so the engine remains a research instrument rather than a single locked interpretation.

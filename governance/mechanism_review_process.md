---
id: mechanism_review_process_v1
title: "Mechanism Review Process"
type: governance-artifact
status: derived_from_thread
version: 1
source_artifacts:
  - governance/artifacts/ART-056-preventing-that-outcome-requires-a-mechanism-discipline-protocol-before-the-literature-review-begins.md
---

# Mechanism Review Process

The mechanism review process is the registry admission path that prevents mechanism explosion.

Control flow:

candidate mechanism
→ normalization
→ primitive mapping
→ merge test
→ threshold placement
→ registry admission

Admission rules:

- A mechanism must be a reproducible process that transforms inputs into outputs through identifiable steps.
- It must map cleanly to the primitive canon.
- It must pass the merge test so variants do not inflate the registry.
- It must anchor to a threshold transition.
- It must satisfy the evidence gate or remain in the speculative pool.

Expected outcome:

- With discipline, the registry stabilizes around 40–80 core mechanisms.
- Without discipline, it drifts toward hundreds of loosely defined entries and becomes unusable.

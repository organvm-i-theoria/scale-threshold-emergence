---
id: open_problem_register_v1
title: "Open Problem Register"
type: research-register
status: derived_from_thread
version: 1
source_artifacts:
  - engine/mechanisms/ART-046-research-dashboard-v1.md
  - governance/artifacts/ART-037-below-is-the-realistic-assessment.md
---

# Open Problem Register

The research dashboard explicitly names the open problem register as one of the six major sections in the live program view.

Every research report should add open problems so unresolved questions become first-class tracked objects rather than buried prose.

Required fields:

| Field | Meaning |
| --- | --- |
| open_problem_id | Stable identifier |
| source_artifact_id | Reading, note, report, or mechanism that surfaced the problem |
| lane | Research lane or threshold package affected |
| description | The unresolved question in atomic form |
| blocking_scope | What downstream artifact or experiment is blocked |
| next_evidence | What reading, dataset, or experiment would reduce uncertainty |
| status | open / active / deferred / retired |

Operational rule:

- Every synthesis report should emit zero or more open problem records.
- Open problems stay linked to provenance and should feed the dashboard, lane tracker, and future mechanism work.

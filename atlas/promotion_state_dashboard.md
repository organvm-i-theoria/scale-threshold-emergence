---
id: promotion_state_dashboard_v1
title: "Promotion State Dashboard"
type: atlas-artifact
status: derived_from_thread
version: 1
source_artifacts:
  - organvm_bridge/artifacts/ART-069-below-is-the-clean-integration.md
---

# Promotion State Dashboard

Promotion is a state machine. Repositories move through explicit states rather than ad hoc upgrades.

Canonical states:

- LOCAL
- CANDIDATE
- PUBLIC_PROCESS
- GRADUATED
- ARCHIVED

Dashboard purpose:

- show current state per repository
- track promotion criteria and blockers
- keep the organism legible at portfolio scale

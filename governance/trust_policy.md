---
id: governance_trust_policy_v1
title: Trust Policy
type: governance-artifact
status: draft
version: 1
---

# Trust Policy

This document defines the trust levels for atoms and their sources.

## Trust Levels

| Level | Name | Description | Requirements |
|-------|------|-------------|--------------|
| T0 | Untrusted | No verification | None |
| T1 | Low Trust | Basic provenance | Source identified |
| T2 | Medium Trust | Verified source | Peer review complete |
| T3 | High Trust | Canonical | Multiple verifications |
| T4 | Absolute Trust | Gold standard | Formal proof |

## Trust Propagation

- Atoms inherit trust from their source
- Derived atoms cannot exceed source trust level
- Trust can decrease but not increase without verification

## Source Trust Mapping

| Source Type | Default Trust |
|-------------|---------------|
| Chat transcript | T1 |
| Research note | T1 |
| Published paper | T2 |
| Gold fixture | T4 |
| Benchmark | T3 |

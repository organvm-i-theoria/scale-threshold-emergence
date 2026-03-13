# Release Controls

Status: IMPLEMENTATION PENDING

## Version State Machine

```
┌─────────┐    deploy    ┌─────────┐    promote    ┌─────────┐
│ DRAFT   │─────────────▶│ STAGING │───────────────▶│ RELEASED│
└─────────┘              └─────────┘              └─────────┘
     ▲                        │                        │
     │                        │                        │
     └────────────────────────┴────────────────────────┘
                       rollback
```

## States

| State | Description | Who Can Transition |
|-------|-------------|-------------------|
| DRAFT | Initial creation | Author |
| STAGING | Ready for review | Author → Reviewer |
| RELEASED | Production ready | Reviewer → Release Manager |
| DEPRECATED | Superseded | Release Manager |
| ARCHIVED | No longer active | System |

## Release Triggers

### Automatic

- All benchmarks passing (>90%)
- Integrity check passing (100%)
- Documentation complete

### Manual

- Security review signed off
- Performance benchmarks met
- Stakeholder approval

## Rollback Procedure

```bash
# Quick rollback to previous version
./scripts/rollback.sh --version PREVIOUS

# Verify rollback
./scripts/verify_rollback.sh
```

## Access Control

| Action | Author | Reviewer | Release Manager |
|--------|--------|----------|-----------------|
| Create | ✓ | | |
| Edit | ✓ | | |
| Stage | ✓ | ✓ | |
| Release | | | ✓ |
| Deprecate | | | ✓ |
| Rollback | | | ✓ |

## Implementation

See `src/ops/release.py` for implementation.

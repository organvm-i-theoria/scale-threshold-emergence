# scale-threshold-emergence

Research framework for studying threshold transitions across scales — from chemistry to life to mind to society to reflexive knowledge systems.

## Status

**Phase**: Foundation → Infrastructure Completion  
**Omega Progress**: ~15% complete (see [there-and-back-again.md](./there-and-back-again.md))

## Overview

This repository implements a systematic approach to researching emergence across five fundamental thresholds:

| Threshold | Domain Transition | Lane |
|-----------|------------------|------|
| TP-05 | Chemistry → Biology | R2-01 |
| TP-06 | Biology → Mind | R2-02 |
| TP-07 | Mind → Society | R2-03 |
| TP-08 | Society → Symbolic | R2-04 |
| TP-09 | Symbolic → Reflexive | R2-05 |

## Architecture

```
scale-threshold-emergence/
├── atlas/                    # Research maps, lane definitions
├── docs/                     # Governance, specifications, artifacts
├── engine/                   # Runtime kernel, mechanisms, modules
│   ├── runtime/             # Kernel, scheduler, parameters
│   ├── mechanisms/           # Mechanism registry
│   ├── modules/             # Module API specifications
│   ├── primitives/          # Primitive canon
│   ├── thresholds/          # Threshold definitions
│   └── worlds/              # World instance schemas
├── governance/              # Lane charters, policies
├── knowledge_graph/          # Graph schema, queries, data
├── manifest/                # Thread manifests, integrity reports
├── research/                # Research operations
│   ├── dashboards/          # Program state tracking
│   ├── indexes/             # Templates, pipelines
│   ├── lanes/              # Individual lane charters/queues
│   ├── reading_notes/       # Literature notes
│   ├── mechanism_extractions/  # Extracted mechanisms
│   ├── reports/            # Synthesis outputs
│   └── thread_pairs/       # Original conversation pairs
├── scripts/                 # Automation
│   ├── academic/            # Academic API clients
│   └── academic_mcp/        # MCP server
├── src/                     # Knowledge engine archive
└── handoff/                # AI handoff prompts
```

## Quick Start

### 1. Check Pipeline Status

```bash
python scripts/pipeline.py status
```

### 2. Find Academic Papers

```bash
python scripts/pipeline.py find-reading "origin of life energy"
python scripts/pipeline.py find-reading "Nick Lane Vital Question"
```

### 3. Fetch Paper Metadata

```bash
python scripts/pipeline.py fetch-paper "DOI:10.xxx"
python scripts/pipeline.py fetch-paper "arxiv:xxxxx"
```

### 4. Advance Research

```bash
# Advance lane to next stage
python scripts/pipeline.py advance R2-01

# Add reading to queue
python scripts/pipeline.py add-reading R2-01 R201-004

# Extract mechanism
python scripts/pipeline.py extract-mechanism 001
```

## Current Lanes

### R2-01: Origin of Life (Chemistry → Biology)

- **Status**: Charter created, reading in progress
- **Reading Queue**: 11 core texts planned
- **Current**: R201-001 (Energy Flow in Biology) — awaiting source

### R2-02 through R2-05

- **Status**: Not yet launched
- **Waiting on**: R2-01 completion for methodology refinement

## Research Pipeline (R0-R6)

| Stage | Name | Status |
|-------|------|--------|
| R0 | Orientation | ✅ Complete |
| R1 | Source Acquisition | ✅ Complete |
| R2 | Structured Reading | 🔄 In Progress |
| R3 | Mechanism Extraction | 🔄 In Progress |
| R4 | Mechanism Integration | ⏳ Pending |
| R5 | Simulation Translation | ⏳ Pending |
| R6 | Theoretical Synthesis | ⏳ Pending |

## Academic API Suite

Built-in access to academic paper databases:

- **Semantic Scholar**: 200M+ papers (rate-limited without API key)
- **arXiv**: Physics, math, CS preprints
- **PubMed**: Life sciences literature

### Getting an API Key (Optional)

1. Sign up at [semanticscholar.org](https://www.semanticscholar.org/api)
2. Set environment variable:
   ```bash
   export SEMANTIC_SCHOLAR_API_KEY="your-key"
   ```

## MCP Integration

To expose academic tools to Claude:

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "academic": {
      "command": "python3",
      "args": ["-m", "academic_mcp"],
      "cwd": "/path/to/scale-threshold-emergence/scripts"
    }
  }
}
```

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Active Lanes | 1/5 | 5/5 |
| Mechanisms Identified | 0 | 50+ |
| Mechanisms Admitted | 0 | 20+ |
| Modules Implemented | 0 | 20+ |
| Simulations Run | 0 | 10+ |

## Documentation

- **[there-and-back-again.md](./there-and-back-again.md)** — Full roadmap to Omega
- **[research/dashboards/research_dashboard_operational.md](./research/dashboards/research_dashboard_operational.md)** — Live program state
- **[engine/runtime/ART-043-universe-engine-kernel-spec-v0.md](./engine/runtime/ART-043-universe-engine-kernel-spec-v0.md)** — Engine kernel spec

## Source

Original conversation: `/Users/4jp/Workspace/meta-organvm/materia-collider/genesis/ChatGPT-Branch · Theory of Everything Domains (1).json`

## License

This is a research framework. Artifacts and code are provided as-is for research purposes.

---

*Path to Omega: ~52 milestones*
*Last updated: 2026-03-13*

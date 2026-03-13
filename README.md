# knowledge-engine

Theoria-native archival and knowledge-engine repository for preserving, normalizing,
and structuring ChatGPT research threads without semantic loss.

This repository has three operating layers:

1. `ingestion/` keeps the raw export, normalized transcript, and run logs.
2. `research/thread_pairs/` preserves the authoritative prompt-response order.
3. The root artifact directories (`docs/`, `research/`, `knowledge_graph/`,
   `engine/`, `governance/`, `atlas/`, `organvm_bridge/`, `manifest/`) hold
   categorized standalone markdown artifacts generated from the source thread.

The initial source thread is:

`/Users/4jp/Workspace/meta-organvm/materia-collider/genesis/ChatGPT-Branch · Theory of Everything Domains (1).json`

## Commands

```bash
PYTHONPATH=src python -m knowledge_engine_archive archive \
  --source "/Users/4jp/Workspace/meta-organvm/materia-collider/genesis/ChatGPT-Branch · Theory of Everything Domains (1).json" \
  --repo-root "/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine"

PYTHONPATH=src python -m knowledge_engine_archive verify \
  --repo-root "/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine"

PYTHONPATH=src python -m knowledge_engine_archive.export_diff \
  --report-path "/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine/docs/2026-03-11-export-diff-report.md" \
  --manifest-path "/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine/manifest/2026-03-11-export-diff-manifest.json" \
  "/Users/4jp/Downloads/ChatGPT-Branch · Theory of Everything Domains.json" \
  "/Users/4jp/Downloads/ChatGPT-Branch · Theory of Everything Domains (1).json"

scripts/run_export_diff.sh

pytest
```

# Build `knowledge-engine` from the ChatGPT thread export

## Summary

- Create a new nested repo at `/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine` as a Theoria-native knowledge-engine archive, with `atlas/` and `organvm_bridge/` included as supporting subtrees.
- Treat `/Users/4jp/Workspace/meta-organvm/materia-collider/genesis/ChatGPT-Branch · Theory of Everything Domains (1).json` as the sole authoritative source.
- Use "verbatim with wrappers" preservation: allow YAML/front matter, deterministic IDs, filenames, manifests, and provenance notes, but do not rewrite substantive source content.

## Implementation Changes

- Bootstrap the repo with these root directories: `docs/`, `research/`, `knowledge_graph/`, `engine/`, `experiments/`, `manifest/`, `governance/`, `atlas/`, `organvm_bridge/`, `ingestion/`.
- Normalize the JSON into an ordered canonical transcript without semantic rewriting:
  - Preserve the source file byte-for-byte in `ingestion/raw/`.
  - Generate normalized JSON and Markdown transcript views in `ingestion/normalized/`.
  - Use deterministic pair IDs `TH-001` through `TH-077`.
  - Store one file per pair in `research/thread_pairs/TH-###-*.md`.
  - Preserve the empty response in pair 25 exactly as empty content.
- Generate manifests in `manifest/`:
  - `thread_manifest.json`
  - `pair_manifest.json`
  - `artifact_manifest.json`
  - `integrity_manifest.json`
- Extract each pair into a categorized standalone artifact document under the primary family directory while retaining the pair files as the canonical ordered transcript.
- Build a machine-readable graph in `knowledge_graph/` linking thread, pair, artifact, family, and directory nodes.
- Produce `manifest/INTEGRITY_REPORT.md` and `manifest/INTEGRITY_REPORT.json`.

## Defaults

- Repo identity: Theoria knowledge engine.
- Repo name: `knowledge-engine`.
- No semantic rewriting beyond metadata wrappers.


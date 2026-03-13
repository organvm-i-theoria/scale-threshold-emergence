---
id: graph_query_library_v1
title: "Graph Query Library"
type: graph-spec
status: seeded
version: 1
source_artifacts:
  - knowledge_graph/graph_schema.md
  - knowledge_graph/graph_database.json
---

# Graph Query Library

This library standardizes recurring graph queries over the reconstructed thread graph.

Seed query set:

1. Show all documents that mention a given primitive ID.
2. Show all documents that mention a given mechanism ID.
3. Trace every thread pair that fed a given canonical document.
4. List threshold IDs referenced by a given module or runtime spec.
5. Show governance artifacts that mention versioning, review, or revision.

# Knowledge Engine Materialization Repair

Date: 2026-03-11
Project: /Users/4jp/Workspace/organvm-i-theoria/knowledge-engine

## Problem

The repository preserved the thread as archival artifacts, but it did not materialize the thread's own canonical output layer:

- canonical docs like `docs/primitive_canon.md`
- runtime/spec files like `engine/runtime/process_node_schema.md`
- operational files like `research/dashboards/research_dashboard.md`
- handoff / graph / manifest convenience files
- the thread-distillation helper scripts described in the close-out pack

## Repair

1. Add a materializer script that reads the preserved artifact docs.
2. Use the final generator artifact as the seed source for placeholder/canonical paths.
3. Overlay fuller drafted artifact content where the thread produced it elsewhere.
4. Generate a provenance manifest for the materialized file set.
5. Run the materializer and verify the expected canonical files now exist.

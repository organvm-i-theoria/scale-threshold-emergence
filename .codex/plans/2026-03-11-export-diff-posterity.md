# Export Diff Posterity Plan

Date: 2026-03-11
Project: /Users/4jp/Workspace/organvm-i-theoria/knowledge-engine

## Goal

Preserve a durable comparison of the ChatGPT JSON and Markdown export variants in Downloads, so the lineage and duplication state of the exports is inspectable later without re-running ad hoc shell commands.

## Steps

1. Add a reusable export-comparison module to `knowledge_engine_archive`.
2. Add tests covering duplicate detection, message-equivalent JSON exports, and prefix lineage.
3. Run the comparator against the user-specified export set.
4. Save a Markdown report under `docs/` and a machine-readable manifest under `manifest/`.
5. Run `pytest` and confirm the generated posterity artifacts exist.

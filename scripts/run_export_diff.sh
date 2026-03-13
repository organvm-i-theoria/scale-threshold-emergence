#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine}"
REPORT_PATH="${2:-$REPO_ROOT/docs/2026-03-11-export-diff-report.md}"
MANIFEST_PATH="${3:-$REPO_ROOT/manifest/2026-03-11-export-diff-manifest.json}"

PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" \
  python3 -m knowledge_engine_archive.export_diff \
    --report-path "$REPORT_PATH" \
    --manifest-path "$MANIFEST_PATH" \
    "/Users/4jp/Downloads/ChatGPT-Branch · Theory of Everything Domains.json" \
    "/Users/4jp/Downloads/ChatGPT-Atomic Knowledge Assembler.json" \
    "/Users/4jp/Downloads/ChatGPT-Branch · Atomic Knowledge Assembler (1).json" \
    "/Users/4jp/Downloads/ChatGPT-Branch · Atomic Knowledge Assembler.json" \
    "/Users/4jp/Downloads/ChatGPT-Branch · Branch · Theory of Everything Domains.json" \
    "/Users/4jp/Downloads/ChatGPT-Branch · Theory of Everything Domains (2).json" \
    "/Users/4jp/Downloads/ChatGPT-Theory of Everything Domains.json" \
    "/Users/4jp/Downloads/Branch-·-Branch-·-Theory-of-Everything-Domains.md" \
    "/Users/4jp/Downloads/Atomic-Knowledge-Assembler.md" \
    "/Users/4jp/Downloads/Branch-·-Theory-of-Everything-Domains (1).md" \
    "/Users/4jp/Downloads/Branch-·-Theory-of-Everything-Domains.md" \
    "/Users/4jp/Downloads/Branch-·-Atomic-Knowledge-Assembler (1).md" \
    "/Users/4jp/Downloads/Branch-·-Atomic-Knowledge-Assembler.md" \
    "/Users/4jp/Downloads/Theory-of-Everything-Domains.md" \
    "/Users/4jp/Downloads/ChatGPT-Branch · Theory of Everything Domains (1).json"

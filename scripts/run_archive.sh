#!/usr/bin/env bash
set -euo pipefail

SOURCE_PATH="${1:-/Users/4jp/Workspace/meta-organvm/materia-collider/genesis/ChatGPT-Branch · Theory of Everything Domains (1).json}"
REPO_ROOT="${2:-/Users/4jp/Workspace/organvm-i-theoria/knowledge-engine}"

PYTHONPATH="$REPO_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" \
  python -m knowledge_engine_archive archive --source "$SOURCE_PATH" --repo-root "$REPO_ROOT"

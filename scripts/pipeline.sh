#!/usr/bin/env bash
# Research Pipeline Wrapper
# Usage: ./pipeline.sh <command> [args...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

python3 scripts/pipeline.py "$@"

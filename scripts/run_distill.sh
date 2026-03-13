#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ROOT:?Set PROJECT_ROOT first}"

python3 "${PROJECT_ROOT}/scripts/normalize_thread.py"
python3 "${PROJECT_ROOT}/scripts/distill_thread.py"
python3 "${PROJECT_ROOT}/scripts/build_graph.py"

echo "Distillation and graph build complete."

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

python3 "${SCRIPT_DIR}/materialize_thread_outputs.py" --repo-root "${PROJECT_ROOT}"
printf "Materialized thread-defined outputs in: %s\n" "${PROJECT_ROOT}"

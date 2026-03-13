#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ROOT:?Set PROJECT_ROOT first}"

cd "${PROJECT_ROOT}"

if [ ! -d .git ]; then
  git init
fi

git add .
git commit -m "bootstrap universe engine research repository v2" || true

#!/usr/bin/env bash
#
# Knowledge Engine Repository Bootstrap Script
#
# This script reconstructs the knowledge-engine repository from the source transcript.
# Run from the repository root.
#
# Usage:
#   ./scripts/bootstrap_knowledge_engine.sh
#
# Requirements:
#   - Python 3.8+
#   - jq (optional, for JSON processing)
#

set -euo pipefail

# Configuration
REPO_ROOT="${REPO_ROOT:-$PWD}"
SOURCE_TRANSCRIPT="${1:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
check_dependencies() {
  log_info "Checking dependencies..."

  if ! command -v python3 &>/dev/null; then
    log_error "Python 3 is required but not installed."
    exit 1
  fi

  log_info "Dependencies OK"
}

# Setup directory structure
setup_directories() {
  log_info "Setting up directory structure..."

  mkdir -p "$REPO_ROOT/source_artifacts/raw"
  mkdir -p "$REPO_ROOT/source_artifacts/chat_pairs"
  mkdir -p "$REPO_ROOT/source_artifacts/normalized"
  mkdir -p "$REPO_ROOT/research/thread_pairs"
  mkdir -p "$REPO_ROOT/research/artifacts"
  mkdir -p "$REPO_ROOT/research/dashboards"
  mkdir -p "$REPO_ROOT/research/indexes"
  mkdir -p "$REPO_ROOT/research/lanes"
  mkdir -p "$REPO_ROOT/research/mechanism_extractions"
  mkdir -p "$REPO_ROOT/research/open_problems"
  mkdir -p "$REPO_ROOT/research/reading_notes"
  mkdir -p "$REPO_ROOT/research/reports"
  mkdir -p "$REPO_ROOT/knowledge_graph"
  mkdir -p "$REPO_ROOT/engine"
  mkdir -p "$REPO_ROOT/governance"
  mkdir -p "$REPO_ROOT/atlas"
  mkdir -p "$REPO_ROOT/organvm_bridge"
  mkdir -p "$REPO_ROOT/manifest"
  mkdir -p "$REPO_ROOT/ingestion/artifacts"
  mkdir -p "$REPO_ROOT/ingestion/logs"
  mkdir -p "$REPO_ROOT/ingestion/manifests"
  mkdir -p "$REPO_ROOT/ingestion/normalized"
  mkdir -p "$REPO_ROOT/ingestion/normalized_threads"
  mkdir -p "$REPO_ROOT/ingestion/raw"
  mkdir -p "$REPO_ROOT/ingestion/raw_threads"
  mkdir -p "$REPO_ROOT/docs"
  mkdir -p "$REPO_ROOT/scripts"
  mkdir -p "$REPO_ROOT/tests/benchmark"
  mkdir -p "$REPO_ROOT/tests/gold"
  mkdir -p "$REPO_ROOT/tests/unit"
  mkdir -p "$REPO_ROOT/data/benchmark"
  mkdir -p "$REPO_ROOT/data/gold"
  mkdir -p "$REPO_ROOT/data/import_samples"
  mkdir -p "$REPO_ROOT/data/projections"
  mkdir -p "$REPO_ROOT/handoff"
  mkdir -p "$REPO_ROOT/ecosystem"
  mkdir -p "$REPO_ROOT/ecosystem/intelligence/content"
  mkdir -p "$REPO_ROOT/ecosystem/intelligence/delivery"
  mkdir -p "$REPO_ROOT/ecosystem/pillar-dna"
  mkdir -p "$REPO_ROOT/ecosystem/snapshots/content"
  mkdir -p "$REPO_ROOT/ecosystem/snapshots/delivery"

  log_info "Directory structure created"
}

# Run reconstruction script
run_reconstruction() {
  log_info "Running reconstruction script..."

  cd "$REPO_ROOT"

  if [ -f "$REPO_ROOT/scripts/reconstruct_knowledge_engine.py" ]; then
    python3 "$REPO_ROOT/scripts/reconstruct_knowledge_engine.py"
  else
    log_warn "Reconstruction script not found, skipping..."
  fi
}

# Verify reconstruction
verify_reconstruction() {
  log_info "Verifying reconstruction..."

  local pair_count
  pair_count=$(find "$REPO_ROOT/research/thread_pairs" -name "TH-*.md" 2>/dev/null | wc -l)

  log_info "Thread pairs created: $pair_count"

  if [ "$pair_count" -gt 0 ]; then
    log_info "Verification PASSED"
    return 0
  else
    log_error "Verification FAILED - no thread pairs found"
    return 1
  fi
}

# Main execution
main() {
  echo "========================================"
  echo "Knowledge Engine Repository Bootstrap"
  echo "========================================"
  echo ""

  check_dependencies
  setup_directories
  run_reconstruction
  verify_reconstruction

  echo ""
  echo "========================================"
  log_info "Bootstrap complete!"
  echo "========================================"
}

main "$@"

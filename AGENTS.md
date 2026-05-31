# AGENTS.md - Agentic Coding Guidelines

This file provides guidance for AI coding agents operating in the scale-threshold-emergence repository.

## Project Overview

**scale-threshold-emergence** is a research framework for studying threshold transitions across scales - from chemistry to life to mind to society to reflexive knowledge systems. It implements a systematic approach to researching emergence across five fundamental thresholds.

## Build, Test, and Development Commands

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run unit tests only
python -m pytest tests/unit/ -v

# Run integration tests only
python -m pytest tests/integration/ -v

# Run a specific test file
python -m pytest tests/unit/test_modules.py -v

# Run a single test class
python -m pytest tests/unit/test_modules.py::TestIntakeModule -v

# Run a single test method
python -m pytest tests/unit/test_modules.py::TestIntakeModule::test_intake_ingest_content -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Run tests matching a pattern
python -m pytest -k "test_intake" -v
```

### Running the Pipeline

```bash
# Check pipeline status
python scripts/pipeline.py status

# Find academic papers
python scripts/pipeline.py find-reading "origin of life"
python scripts/pipeline.py find-reading "Nick Lane Vital Question"

# Fetch paper metadata
python scripts/pipeline.py fetch-paper "DOI:10.xxx"
python scripts/pipeline.py fetch-paper "arxiv:xxxxx"

# Advance research lane
python scripts/pipeline.py advance R2-01

# Add reading to queue
python scripts/pipeline.py add-reading R2-01 R201-004

# Extract mechanism
python scripts/pipeline.py extract-mechanism 001
```

### Code Quality

```bash
# Install dependencies
pip install requests pytest pytest-cov

# Lint with ruff
ruff check src/
ruff format src/
```

## Code Style Guidelines

### Python Conventions

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 88 characters (ruff default)
- **Encoding**: UTF-8

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Modules/Packages | snake_case | `source_intake`, `text_refinery` |
| Classes | PascalCase | `SourceIntake`, `TextRefinery` |
| Functions/Methods | snake_case | `def ingest_content()`, `def refine()` |
| Variables | snake_case | `atom_id`, `content_hash` |
| Constants | UPPER_SNAKE_CASE | `MAX_LENGTH`, `DEFAULT_ENCODING` |

### Import Organization

```python
# Standard library
import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# Third-party packages
try:
    import nltk
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

# Local imports
from .module import ClassName
from ..package import function
```

### Type Hints

Use type hints throughout. Avoid `Any` when possible.

```python
def process_atoms(atoms: list[dict]) -> list[str]:
    results: list[str] = []
    return results
```

### Error Handling

- Use specific exception types
- Never use bare `except:`
- Use context managers

```python
try:
    result = process_content(content)
except ValueError as e:
    logger.error(f"Invalid content: {e}")
    raise

with open(filepath, 'r') as f:
    content = f.read()
```

## Project Structure

```
scale-threshold-emergence/
├── src/                    # Knowledge engine modules (12 modules)
│   ├── intake/            # Source intake
│   ├── refinery/           # Text and code refining
│   │   ├── text/
│   │   └── code/
│   ├── storage/            # Storage backends
│   │   ├── cas/           # Content-addressable storage
│   │   ├── vector/        # Vector storage
│   │   └── graph/         # Graph storage
│   ├── analysis/           # Analysis normalization
│   ├── assembly/           # Assembly engine
│   ├── portal/             # Portal projection
│   ├── ops/                # Operations/monitoring
│   ├── evaluation/          # Evaluation harness
│   └── api/graphql/        # GraphQL API
├── scripts/                # Automation and CLI
│   ├── pipeline.py         # Main pipeline
│   ├── academic/           # Academic paper APIs
│   └── academic_mcp/       # MCP server
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── docs/                   # Documentation
├── .github/workflows/     # CI/CD
├── pyproject.toml         # Project config
└── README.md
```

## Testing Guidelines

### Test File Organization

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test classes `Test*` and test methods `test_*`

```python
class TestIntakeModule:
    """Tests for Source Intake module."""

    def test_intake_ingest_content(self):
        """Test content ingestion."""
        ...
```

### Assertions

Use descriptive assertions with clear error messages:

```python
assert result.id is not None, "Atom ID should be generated"
assert len(atoms) > 0, "Should extract at least one atom"
```

## Commit Conventions

Use Conventional Commits:

| Prefix | Use For |
|--------|---------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `docs:` | Documentation |
| `chore:` | Maintenance, refactoring |
| `ci:` | CI/CD changes |
| `test:` | Test changes |
| `research:` | Research-related changes |

```bash
git commit -m "feat: add intake module for chat transcripts"
git commit -m "fix: resolve vector search error"
git commit -m "docs: update README"
```

## Security Best Practices

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive config
- Add secrets to `.gitignore`

---

*Last updated: 2026-03-14*

<!-- ORGANVM:AUTO:START -->
## Agent Context (auto-generated — do not edit)

This repo participates in the **ORGAN-I (Theory)** swarm.

### Active Subscriptions
- *No active event subscriptions*

### Production Responsibilities
- *No production responsibilities*

### External Dependencies
- *No external dependencies*

### Governance Constraints
- Adhere to unidirectional flow: I→II→III
- Never commit secrets or credentials

*Last synced: 2026-05-23T00:26:31Z*
<!-- ORGANVM:AUTO:END -->

---
id: benchmark_codeatom_001
type: benchmark
category: code_atom_extraction
status: active
version: 1
source: synthetic
---

# Benchmark: Code Atom Extraction

This benchmark tests the ability to extract atomic code units from script files.

## Input (Python)

```python
#!/usr/bin/env python3
import os
import re
from pathlib import Path

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    return text.strip()

def extract_atoms(text: str) -> list:
    atoms = []
    # Parse atoms from text
    for line in text.splitlines():
        if line.strip():
            atoms.append({"content": line.strip()})
    return atoms
```

## Expected Output (Code Atoms)

| Atom ID | Content | Type | Function |
|---------|---------|------|----------|
| CA-001 | import os | import | top-level |
| CA-002 | import re | import | top-level |
| CA-003 | from pathlib import Path | import | top-level |
| CA-004 | normalize_text | function | definition |
| CA-005 | text.replace | method | call |
| CA-006 | text.strip | method | call |
| CA-007 | extract_atoms | function | definition |
| CA-008 | for line in... | iteration | control |

## Validation Criteria

- [ ] All imports identified
- [ ] All function definitions captured
- [ ] Method calls within functions tracked
- [ ] Control flow atoms identified

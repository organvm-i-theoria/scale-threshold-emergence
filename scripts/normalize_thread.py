#!/usr/bin/env python3
import os
import re
from pathlib import Path


PROJECT_ROOT = Path(os.environ["PROJECT_ROOT"])
RAW_DIR = PROJECT_ROOT / "ingestion" / "raw_threads"
OUT_DIR = PROJECT_ROOT / "ingestion" / "normalized_threads"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip() + "\n"


def main() -> None:
    for path in RAW_DIR.glob("*"):
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        normalized = normalize_text(raw)
        out_path = OUT_DIR / path.name
        out_path.write_text(normalized, encoding="utf-8")
        print(f"normalized: {out_path}")


if __name__ == "__main__":
    main()

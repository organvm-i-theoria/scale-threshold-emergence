from __future__ import annotations

import argparse
import json
from pathlib import Path

from .archive import archive_thread, verify_repo


def main() -> None:
    parser = argparse.ArgumentParser(prog="knowledge_engine_archive")
    subparsers = parser.add_subparsers(dest="command", required=True)

    archive_parser = subparsers.add_parser("archive")
    archive_parser.add_argument("--source", required=True, type=Path)
    archive_parser.add_argument("--repo-root", required=True, type=Path)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--repo-root", required=True, type=Path)

    args = parser.parse_args()

    if args.command == "archive":
        result = archive_thread(source_path=args.source, repo_root=args.repo_root)
    else:
        result = verify_repo(args.repo_root)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse

from .archive import main as archive_main


def main() -> int:
    parser = argparse.ArgumentParser(prog="knowledge_engine_archive")
    subparsers = parser.add_subparsers(dest="command", required=True)

    archive_parser = subparsers.add_parser("archive")
    archive_parser.add_argument("--source", required=True)
    archive_parser.add_argument("--repo-root", required=True)

    args = parser.parse_args()
    if args.command == "archive":
        return archive_main(["--source", args.source, "--repo-root", args.repo_root])

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

"""Archive and export-diff utilities for the knowledge engine."""

__all__ = [
    "analyze_exports",
    "archive_thread",
    "derive_title",
    "normalize_markdown",
    "verify_repo",
    "write_outputs",
]


def __getattr__(name: str) -> object:
    if name in {"archive_thread", "derive_title", "verify_repo"}:
        from . import archive

        return getattr(archive, name)

    if name in {"analyze_exports", "normalize_markdown", "write_outputs"}:
        from . import export_diff

        return getattr(export_diff, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

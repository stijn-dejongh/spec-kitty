"""Guard test: ensure deprecated .kittify/memory/constitution.md path is not used.

Scans docs/ and architecture/ for the deprecated path and fails if any
non-historical references are found.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

DEPRECATED_PATH = ".kittify/memory/constitution.md"

# Directories to scan for the deprecated path
SCAN_DIRS = [
    REPO_ROOT / "docs",
    REPO_ROOT / "architecture",
]

# Files explicitly allowed to mention the deprecated path (historical context)
EXCEPTIONS: set[str] = set()


def _find_deprecated_references() -> list[tuple[str, int, str]]:
    """Return (file, line_number, line_text) tuples containing the deprecated path."""
    hits: list[tuple[str, int, str]] = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for md_file in sorted(scan_dir.rglob("*.md")):
            rel = str(md_file.relative_to(REPO_ROOT))
            if rel in EXCEPTIONS:
                continue
            for i, line in enumerate(md_file.read_text().splitlines(), start=1):
                if DEPRECATED_PATH in line:
                    hits.append((rel, i, line.strip()))
    return hits


def test_no_deprecated_constitution_path():
    """No docs or architecture files should reference the deprecated path."""
    hits = _find_deprecated_references()
    if hits:
        report = "\n".join(
            f"  {path}:{lineno}: {text}" for path, lineno, text in hits
        )
        pytest.fail(
            f"Found {len(hits)} reference(s) to deprecated "
            f"'{DEPRECATED_PATH}':\n{report}\n\n"
            f"Use '.kittify/constitution/constitution.md' instead, "
            f"or add the file to EXCEPTIONS if the reference is historical."
        )

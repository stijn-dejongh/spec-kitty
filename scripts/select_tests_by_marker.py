#!/usr/bin/env python3
"""Select test files containing a given pytest marker.

Pytest's ``-m`` filtering happens after collection, which means separate jobs
still import the full test tree. This helper builds a file list up front so CI
lanes only collect the files relevant to their marker.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


def _file_uses_marker(path: Path, marker: str) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        if node.attr != marker:
            continue
        base = node.value
        if isinstance(base, ast.Attribute) and base.attr == "mark":
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("marker", help="pytest marker name to select")
    parser.add_argument(
        "--root",
        default="tests",
        help="Test root directory to scan (default: tests)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        return 0

    matches: list[str] = []
    for path in sorted(root.rglob("test_*.py")):
        if _file_uses_marker(path, args.marker):
            matches.append(path.as_posix())

    sys.stdout.write("\n".join(matches))
    if matches:
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

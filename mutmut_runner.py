#!/usr/bin/env python3
"""
Wrapper script for mutmut pytest runner that ensures full package is available.
This script is called by mutmut with pytest arguments.
"""
import sys
import shutil
from pathlib import Path

def setup_environment():
    """Ensure non-mutated package files are available in mutants directory."""
    # We're being called from the main repo, but tests run in mutants/
    mutants_dir = Path.cwd() / "mutants"
    
    if not mutants_dir.exists():
        return  # Nothing to do if mutants doesn't exist yet
    
    src_dir = Path.cwd() / "src" / "specify_cli"
    mutants_src = mutants_dir / "src" / "specify_cli"
    
    if not mutants_src.exists():
        return  # Nothing to setup
    
    # Files and directories being mutated (already in mutants/)
    mutated_items = {"status", "glossary"}
    
    # Copy everything else from specify_cli that's not already there
    for item in src_dir.iterdir():
        if item.name not in mutated_items:
            dest = mutants_src / item.name
            if not dest.exists():  # Only copy if not already there
                if item.is_file():
                    shutil.copy2(item, dest)
                elif item.is_dir() and not item.name.startswith("__pycache__"):
                    shutil.copytree(item, dest)

def main():
    """Setup environment and run pytest."""
    setup_environment()
    
    # Now run pytest with the provided arguments
    import pytest
    sys.exit(pytest.main(sys.argv[1:]))

if __name__ == "__main__":
    main()

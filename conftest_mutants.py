"""
Conftest for mutants directory - ensures full package is available.
This file will be copied to mutants/conftest.py by mutmut.
"""
import sys
import shutil
from pathlib import Path

def pytest_configure(config):
    """Setup hook called before test collection."""
    # Check if we're in the mutants directory
    cwd = Path.cwd()
    if cwd.name != "mutants":
        return  # Not in mutants, nothing to do
    
    # Setup the full package structure
    repo_root = cwd.parent
    src_dir = repo_root / "src" / "specify_cli"
    mutants_src = cwd / "src" / "specify_cli"
    
    if not mutants_src.exists() or not src_dir.exists():
        return
    
    # Files and directories being mutated (already in mutants/)
    mutated_items = {"status", "glossary"}
    
    # Copy everything else from specify_cli that's not already there
    for item in src_dir.iterdir():
        if item.name not in mutated_items:
            dest = mutants_src / item.name
            if not dest.exists():  # Only copy if not already there
                try:
                    if item.is_file():
                        shutil.copy2(item, dest)
                    elif item.is_dir() and not item.name.startswith("__pycache__"):
                        shutil.copytree(item, dest)
                except Exception as e:
                    # Log but don't fail
                    print(f"Warning: Could not copy {item.name}: {e}")

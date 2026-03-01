#!/usr/bin/env python3
"""
Setup script to prepare the mutants directory for mutation testing.
Copies non-mutated parts of the package to mutants/src to ensure imports work.
"""
import shutil
from pathlib import Path

def setup_mutants_environment():
    """Copy non-mutated package files to mutants directory."""
    repo_root = Path(__file__).parent
    mutants_dir = repo_root / "mutants"
    
    # Only run if mutants directory exists
    if not mutants_dir.exists():
        print("mutants/ directory doesn't exist yet")
        return
    
    src_dir = repo_root / "src" / "specify_cli"
    mutants_src = mutants_dir / "src" / "specify_cli"
    
    # Ensure the mutants src directory exists
    mutants_src.mkdir(parents=True, exist_ok=True)
    
    # Files and directories being mutated (will already be in mutants/)
    mutated_items = {"status", "glossary"}
    
    # Copy everything else from specify_cli
    for item in src_dir.iterdir():
        if item.name not in mutated_items:
            dest = mutants_src / item.name
            if item.is_file():
                shutil.copy2(item, dest)
                print(f"Copied {item.name}")
            elif item.is_dir() and not item.name.startswith("__pycache__"):
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                print(f"Copied directory {item.name}")
    
    print(f"\nSetup complete! Non-mutated package files copied to {mutants_src}")

if __name__ == "__main__":
    setup_mutants_environment()

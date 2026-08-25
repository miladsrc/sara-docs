#!/usr/bin/env python
"""Load Sara's knowledge into a new environment.

Usage:
  python load_sara.py [--check] [--load-memory] [--load-config] [--load-skills]

Options:
  --check         Check if Sara's files are already loaded
  --load-memory   Load Sara's memory file
  --load-config   Load Sara's configuration
  --load-skills   Load Sara's skills

If no options are specified, all will be loaded.
"""
import os
import shutil
import sys
from pathlib import Path

# Source directory (where this script is located)
SOURCE_DIR = Path(__file__).parent.parent

# Target directories
TARGET_MEMORY = Path.home() / ".config" / "opencode" / "memory"
TARGET_CONFIG = Path.home() / ".config" / "opencode"
TARGET_SKILLS = Path.home() / ".config" / "opencode" / "skills"


def check_sara():
    """Check if Sara's files are already loaded."""
    print("Checking Sara's files...")
    
    memory_file = TARGET_MEMORY / "sara.md"
    config_file = TARGET_CONFIG / "AGENTS.md"
    skills_dir = TARGET_SKILLS / "read-terminals"
    
    checks = [
        ("Memory file", memory_file.exists()),
        ("Config file", config_file.exists()),
        ("Skills directory", skills_dir.exists()),
    ]
    
    all_ok = True
    for name, exists in checks:
        status = "✓" if exists else "✗"
        print(f"  {status} {name}")
        if not exists:
            all_ok = False
    
    if all_ok:
        print("\nAll Sara files are already loaded!")
    else:
        print("\nSome files are missing. Use --load-memory, --load-config, or --load-skills to load them.")
    
    return all_ok


def load_memory():
    """Load Sara's memory file."""
    print("Loading Sara's memory...")
    
    source = SOURCE_DIR / "memory" / "sara.md"
    target = TARGET_MEMORY / "sara.md"
    
    if not source.exists():
        print(f"  Error: Source file not found: {source}")
        return False
    
    # Create target directory if it doesn't exist
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy file
    shutil.copy2(source, target)
    print(f"  Copied: {source} -> {target}")
    return True


def load_config():
    """Load Sara's configuration."""
    print("Loading Sara's configuration...")
    
    source = SOURCE_DIR / "config" / "AGENTS.md"
    target = TARGET_CONFIG / "AGENTS.md"
    
    if not source.exists():
        print(f"  Error: Source file not found: {source}")
        return False
    
    # Copy file
    shutil.copy2(source, target)
    print(f"  Copied: {source} -> {target}")
    return True


def load_skills():
    """Load Sara's skills."""
    print("Loading Sara's skills...")
    
    source_dir = SOURCE_DIR / "skills" / "read-terminals"
    target_dir = TARGET_SKILLS / "read-terminals"
    
    if not source_dir.exists():
        print(f"  Error: Source directory not found: {source_dir}")
        return False
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files
    for file in source_dir.glob("*"):
        if file.is_file():
            target = target_dir / file.name
            shutil.copy2(file, target)
            print(f"  Copied: {file} -> {target}")
    
    return True


def main():
    args = sys.argv[1:]
    
    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0)
    
    if "--check" in args:
        check_sara()
        sys.exit(0)
    
    success = True
    
    if "--load-memory" in args or (not any(a.startswith("--") for a in args)):
        if not load_memory():
            success = False
    
    if "--load-config" in args or (not any(a.startswith("--") for a in args)):
        if not load_config():
            success = False
    
    if "--load-skills" in args or (not any(a.startswith("--") for a in args)):
        if not load_skills():
            success = False
    
    if success:
        print("\nSara's knowledge loaded successfully!")
        print("Restart opencode to apply changes.")
    else:
        print("\nSome files failed to load.")
        sys.exit(1)


if __name__ == "__main__":
    main()

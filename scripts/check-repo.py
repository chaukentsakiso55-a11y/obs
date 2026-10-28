#!/usr/bin/env python3
"""Quick repo health check. Catch missing stuff before the ISO build does."""
from pathlib import Path
import ast
import sys

ROOT=Path(__file__).resolve().parents[1]
NEEDED=[
 "README.md",
 "scripts/stage.sh",
 "scripts/build-iso.sh",
 "config/hooks/live/010-obsidian.hook.chroot",
 "config/package-lists/obsidian.list.chroot",
 "obsidian/shell.py",
 "obsidian/eden.py",
 "obsidian/eden_runtime.py",
 "obsidian/security_events.py",
 "tools/obs.py",
 ".github/workflows/build-iso.yml",
 ".github/workflows/python-tests.yml",
]
issues=[]
for item in NEEDED:
    path=ROOT/item
    if not path.is_file():
        issues.append("Missing: "+item)
for folder in ("obsidian","tools","tests"):
    for path in (ROOT/folder).glob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
        except SyntaxError as error:
            issues.append(f"Python syntax: {path.relative_to(ROOT)}:{error.lineno} {error.msg}")
packages=(ROOT/"config/package-lists/obsidian.list.chroot")
if packages.is_file():
    contents=packages.read_text()
    for required in ("xfce4-terminal","xfce4-taskmanager","python3","gcc","g++","nodejs","rustc"):
        if required not in contents.splitlines():
            issues.append("Missing ISO dependency: "+required)
if issues:
    print("Repo check failed:")
    for issue in issues:print(" -",issue)
    sys.exit(1)
print("Repo check passed: expected files, Python syntax and core packages found.")

#!/usr/bin/env python3
"""
Find all references to "Paul's Computer", "Paul's COMPUTER", or similar phrasing.
"""
import os
import re

PAT = re.compile(r"Paul['’]s\s+Computer", re.IGNORECASE)

IGNORE_DIRS = {".git", ".venv", "node_modules", "build"}
EXTENSIONS = {".md", ".json", ".html", ".js", ".mjs", ".c", ".h", ".py", ".sh", ".txt"}

matches = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    for file in files:
        _, ext = os.path.splitext(file)
        if ext.lower() in EXTENSIONS or file in {"README", "LICENSE", "Makefile"}:
            path = os.path.join(root, file)
            if "find_pauls_computer.py" in path:
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, 1):
                        m = PAT.search(line)
                        if m:
                            matches.append((path, line_no, line.strip()))
            except Exception:
                pass

print(f"Found {len(matches)} occurrences:")
for path, line_no, line in matches:
    print(f"{path}:{line_no}: {line}")

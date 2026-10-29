#!/usr/bin/env python3
"""
Find all meta-references across all repo text files.
"""

import os
import re

PATTERNS = [
    re.compile(r"tim\s+(?:and|&)\s+eric", re.IGNORECASE),
    re.compile(r"\bsketch\b", re.IGNORECASE),
    re.compile(r"\bparody\b", re.IGNORECASE),
    re.compile(r"\bsatire\b", re.IGNORECASE),
    re.compile(r"\bcomedy\b", re.IGNORECASE),
    re.compile(r"adult\s+swim", re.IGNORECASE),
    re.compile(r"awesome\s+show", re.IGNORECASE),
    re.compile(r"\brudd\b", re.IGNORECASE),
    re.compile(r"\bwareheim\b", re.IGNORECASE),
    re.compile(r"\bheidecker\b", re.IGNORECASE),
    re.compile(r"\btribute\b", re.IGNORECASE),
    re.compile(r"\bfan-", re.IGNORECASE),
    re.compile(r"documentary\s+footage", re.IGNORECASE),
]

IGNORE_DIRS = {".git", ".venv", "node_modules", "build"}
EXTENSIONS = {".md", ".json", ".html", ".js", ".mjs", ".c", ".h", ".py", ".sh", ".txt"}

matches = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    for file in files:
        _, ext = os.path.splitext(file)
        if ext.lower() in EXTENSIONS or file in {"README", "LICENSE", "Makefile"}:
            path = os.path.join(root, file)
            if "find_meta_refs.py" in path:
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, 1):
                        for p in PATTERNS:
                            m = p.search(line)
                            if m:
                                matches.append((path, line_no, line.strip(), m.group(0)))
                                break
            except Exception as e:
                pass

print(f"Found {len(matches)} occurrences:")
for path, line_no, line, matched in matches:
    print(f"{path}:{line_no} [{matched}]: {line}")

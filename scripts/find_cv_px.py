#!/usr/bin/env python3
import os

print("Searching for cv_px in codebase...")
for root, dirs, files in os.walk("."):
    if any(x in root for x in [".venv", ".git", "build"]):
        continue
    for f in files:
        p = os.path.join(root, f)
        try:
            with open(p, "r", errors="ignore") as fh:
                txt = fh.read()
                if "cv_px" in txt:
                    print(f"Found in {p}")
        except Exception:
            pass

#!/usr/bin/env python3
import os

print("Searching repo files (excluding .venv, .git, build)...")
for root, dirs, files in os.walk("."):
    if any(x in root for x in [".venv", ".git", "build", "__pycache__"]):
        continue
    for f in files:
        p = os.path.join(root, f)
        try:
            with open(p, "r", errors="ignore") as fh:
                content = fh.read()
                matches = []
                for kw in ["uboot", "spl", "recovery", "oct-", "oct+", "0x02000120"]:
                    if kw in content.lower():
                        matches.append(kw)
                if matches:
                    print(f"  {p}: matched {matches}")
        except Exception:
            pass

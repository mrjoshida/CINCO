#!/usr/bin/env python3
import os

print("Searching for uboot and recovery references...")
for root, dirs, files in os.walk("."):
    # skip .git
    if ".git" in root or "build" in root:
        continue
    for f in files:
        if f.endswith((".c", ".h", ".py", ".md", ".sh", ".S", ".s")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", errors="ignore") as fh:
                    content = fh.read()
                    if "uboot" in content.lower() or "recovery" in content.lower() or "spl" in content.lower():
                        print(f"Found in {p}")
            except Exception as e:
                pass

#!/usr/bin/env python3
import subprocess

print("=== GIT STATUS ===")
subprocess.run(["git", "status", "-s"])

print("\n=== GIT DIFF STAT ===")
subprocess.run(["git", "diff", "--stat"])

print("\n=== CHECKING IF LOADER OR SDK FILES WERE MODIFIED ===")
r = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True)
for f in r.stdout.splitlines():
    print("  Modified:", f)

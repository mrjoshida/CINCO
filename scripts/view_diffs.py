#!/usr/bin/env python3
import subprocess

print("=== GIT DIFF FOR TRACKED FILES ===")
subprocess.run(["git", "diff", "tools/build.py", "firmware/src/audio.c", "firmware/src/felucca.c", "firmware/src/usb.c"])

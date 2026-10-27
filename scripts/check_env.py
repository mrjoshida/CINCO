#!/usr/bin/env python3
import os
import shutil
import subprocess

print("JIELI_TOOLCHAIN env:", os.environ.get("JIELI_TOOLCHAIN"))
print("docker path:", shutil.which("docker"))
if shutil.which("docker"):
    try:
        r = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=3)
        print("docker info returncode:", r.returncode)
    except Exception as e:
        print("docker check error:", e)

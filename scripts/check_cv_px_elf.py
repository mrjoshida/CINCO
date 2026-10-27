#!/usr/bin/env python3
import os
import subprocess

tc_dir = os.path.expanduser("~/.jieli/toolchain")

cmd = [
    "docker", "run", "--rm", "--platform", "linux/amd64",
    "-v", f"{os.getcwd()}:/work",
    "-v", f"{tc_dir}:/opt/jieli:ro",
    "-w", "/work",
    "debian:bookworm-slim",
    "/opt/jieli/pi32v2/bin/nm", "build/felucca.elf"
]
r = subprocess.run(cmd, capture_output=True, text=True)
found = False
for line in r.stdout.splitlines():
    if "cv_px" in line:
        print("Found cv_px in ELF:", line)
        found = True

if not found:
    print("CONFIRMED: cv_px is NOT present in build/felucca.elf! (Stock canvas was eliminated in Cinco 2.5)")

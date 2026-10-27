#!/usr/bin/env python3
import os
import subprocess

tc_dir = os.path.expanduser("~/.jieli/toolchain")

# Run nm with line numbers / filenames if possible or grep nm
cmd = [
    "docker", "run", "--rm", "--platform", "linux/amd64",
    "-v", f"{os.getcwd()}:/work",
    "-v", f"{tc_dir}:/opt/jieli:ro",
    "-w", "/work",
    "debian:bookworm-slim",
    "/opt/jieli/pi32v2/bin/nm", "-l", "build/felucca.elf"
]
r = subprocess.run(cmd, capture_output=True, text=True)
for line in r.stdout.splitlines():
    if "cv_px" in line or "cv_" in line:
        print(line)

# Also check build/ directory for any .o files
print("\nChecking object files in build/:")
for f in os.listdir("build"):
    if f.endswith(".o"):
        cmd_o = [
            "docker", "run", "--rm", "--platform", "linux/amd64",
            "-v", f"{os.getcwd()}:/work",
            "-v", f"{tc_dir}:/opt/jieli:ro",
            "-w", "/work",
            "debian:bookworm-slim",
            "/opt/jieli/pi32v2/bin/nm", f"build/{f}"
        ]
        r_o = subprocess.run(cmd_o, capture_output=True, text=True)
        if "cv_px" in r_o.stdout:
            print(f"  build/{f} defines/uses cv_px!")

#!/usr/bin/env python3
import os
import subprocess

tc_dir = os.path.expanduser("~/.jieli/toolchain")
print("Toolchain pi32v2/bin contents:")
bin_dir = os.path.join(tc_dir, "pi32v2", "bin")
if os.path.exists(bin_dir):
    print(os.listdir(bin_dir))

common_bin = os.path.join(tc_dir, "common", "bin")
if os.path.exists(common_bin):
    print("common/bin contents:", os.listdir(common_bin))

# Try running objdump via docker
cmd = [
    "docker", "run", "--rm", "--platform", "linux/amd64",
    "-v", f"{os.getcwd()}:/work",
    "-v", f"{tc_dir}:/opt/jieli:ro",
    "-w", "/work",
    "debian:bookworm-slim",
    "/opt/jieli/pi32v2/bin/objdump", "--version"
]
print("\nTesting docker execution with objdump:")
r = subprocess.run(cmd, capture_output=True, text=True)
print("Returncode:", r.returncode)
print("Stdout:", r.stdout.strip())
print("Stderr:", r.stderr.strip())

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
    "/opt/jieli/pi32v2/bin/objdump", "-d", "build/felucca.elf"
]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
for i in range(40):
    line = proc.stdout.readline()
    print(line, end="")
proc.terminate()

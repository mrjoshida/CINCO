#!/usr/bin/env python3
import os
import subprocess

tc_dir = os.path.expanduser("~/.jieli/toolchain")

def run_in_docker(args):
    cmd = [
        "docker", "run", "--rm", "--platform", "linux/amd64",
        "-v", f"{os.getcwd()}:/work",
        "-v", f"{tc_dir}:/opt/jieli:ro",
        "-w", "/work",
        "debian:bookworm-slim",
    ] + args
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return r.stdout

print("=== CHECKING ENTRY POINT AND STACKS IN ELF ===")
nm_out = run_in_docker(["/opt/jieli/pi32v2/bin/nm", "-n", "build/felucca.elf"])

for target in ["_start", "fm1_cstart", "main", "_ustack_top", "_sstack_top", "_c1_ustack", "_c1_sstack", "_c1_ustack_top", "_c1_sstack_top"]:
    found = False
    for line in nm_out.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[2] == target:
            print(f"  {parts[0]} {parts[1]} {parts[2]}")
            found = True
    if not found:
        print(f"  NOT FOUND: {target}")

print("\n=== DISASSEMBLING _start ===")
dis_start = run_in_docker(["/opt/jieli/pi32v2/bin/objdump", "-d", "-j", ".text", "build/felucca.elf"])
start_lines = []
capturing = False
for line in dis_start.splitlines():
    if "_start:" in line:
        capturing = True
    elif capturing and line.endswith(":") and not "_start" in line:
        break
    if capturing:
        start_lines.append(line)

print("\n".join(start_lines[:25]))

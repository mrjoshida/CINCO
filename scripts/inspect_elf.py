#!/usr/bin/env python3
import os
import subprocess
import sys

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
        print("Error running:", args)
        print("Stderr:", r.stderr)
        sys.exit(r.returncode)
    return r.stdout

print("=== INSPECTING ELF HEADERS AND SECTIONS ===")
out = run_in_docker(["/opt/jieli/pi32v2/bin/objdump", "-h", "build/felucca.elf"])
print(out)

print("=== INSPECTING RAM_TEXT SYMBOLS ===")
nm_out = run_in_docker(["/opt/jieli/pi32v2/bin/nm", "-n", "build/felucca.elf"])
ram_symbols = []
for line in nm_out.splitlines():
    parts = line.split()
    if len(parts) >= 3:
        addr = int(parts[0], 16)
        sym_type = parts[1]
        name = parts[2]
        # Check if in RAM address range (0x01C00000 - 0x01FFFFFF)
        if 0x01C00000 <= addr < 0x02000000:
            ram_symbols.append((addr, sym_type, name))

print(f"Total RAM symbols found: {len(ram_symbols)}")
for s in ram_symbols[:30]:
    print(f"  {s[0]:08x} {s[1]} {s[2]}")

print("\n=== DISASSEMBLING .ram_text ===")
dis_out = run_in_docker(["/opt/jieli/pi32v2/bin/objdump", "-d", "-j", ".ram_text", "build/felucca.elf"])
print(f".ram_text disassembly length: {len(dis_out.splitlines())} lines")
# Write disassembly to a file for complete analysis
with open("build/ram_text_disasm.txt", "w") as f:
    f.write(dis_out)
print("Wrote build/ram_text_disasm.txt")

#!/usr/bin/env python3
import re

with open("build/ram_text_disasm.txt") as f:
    text = f.read()

# Pattern for pi32v2 disassembly lines
# e.g.:   1c00010:	12 34 56 78 	call 0x02001000
# or:     1c00010:	12 34 	calla r1
call_re = re.compile(r"^\s*([0-9a-f]+):\s+([0-9a-f\s]+)\t(\w+)\s*(.*)$", re.MULTILINE)

calls = []
all_insts = []
for m in call_re.finditer(text):
    addr_str, hex_code, op, args = m.groups()
    addr = int(addr_str, 16)
    all_insts.append((addr, op, args.strip()))
    if "call" in op or "jmp" in op or "b" in op:
        calls.append((addr, op, args.strip()))

print(f"Total instructions in .ram_text: {len(all_insts)}")
print(f"Total branches/calls in .ram_text: {len(calls)}")

print("\nAll branches and calls:")
flash_targets = []
for addr, op, args in calls:
    print(f"  {addr:08x}: {op:10s} {args}")
    # Check if target contains hex address
    hex_addrs = re.findall(r"0x[0-9a-fA-F]+", args)
    for h in hex_addrs:
        val = int(h, 16)
        if 0x02000000 <= val < 0x08000000:
            flash_targets.append((addr, op, args, val))

if flash_targets:
    print("\nCRITICAL ALERT: FOUND FLASH CALLS IN .ram_text:")
    for addr, op, args, val in flash_targets:
        print(f"  CRITICAL: at {addr:08x} -> {op} {args} (target: 0x{val:08x})")
else:
    print("\nVERIFIED: ZERO calls/branches to flash (0x02xxxxxx) found in .ram_text!")

#!/usr/bin/env python3
import re

with open("build/ram_text_disasm.txt") as f:
    lines = f.readlines()

print(f"Total lines in disassembly: {len(lines)}")

call_instructions = []
goto_instructions = []
flash_references = []
all_destinations = []

for idx, line in enumerate(lines):
    line_clean = line.strip()
    if not line_clean or line_clean.startswith("build/") or line_clean.startswith("Disassembly"):
        continue
    if line_clean.endswith(":"):
        # label
        continue
    
    # Check for calls
    if re.search(r"\bcall\b", line_clean) or re.search(r"\bcalla\b", line_clean):
        call_instructions.append((idx + 1, line_clean))
        
    # Check for gotos
    if "goto" in line_clean:
        goto_instructions.append((idx + 1, line_clean))

    # Check for flash address pattern (0x02xxxxxx or 20xxxxx)
    # Note: XIP starts at 0x02000000 to 0x08000000
    m_hex = re.findall(r"0x([0-9a-fA-F]{7,8})", line_clean)
    for h in m_hex:
        val = int(h, 16)
        if 0x02000000 <= val < 0x08000000:
            flash_references.append((idx + 1, line_clean, val))
            
    # Check for target labels like <symbol+offset : 2xxxxxx >
    m_tgt = re.findall(r":\s*([0-9a-fA-F]{6,8})\s*>", line_clean)
    for h in m_tgt:
        val = int(h, 16)
        all_destinations.append((idx + 1, line_clean, val))
        if 0x02000000 <= val < 0x08000000:
            flash_references.append((idx + 1, line_clean, val))

print(f"Call instructions count: {len(call_instructions)}")
for line_no, c in call_instructions:
    print(f"  Line {line_no}: {c}")

print(f"\nGoto instructions count: {len(goto_instructions)}")

print(f"\nFlash references count (0x02xxxxxx): {len(flash_references)}")
for line_no, c, val in flash_references:
    print(f"  Line {line_no}: 0x{val:08x} -> {c}")

# Check all destinations to ensure they are within SRAM (.ram_text: 0x01c00000 - 0x01c00b6c)
outside_ram_text = []
for line_no, c, val in all_destinations:
    if not (0x01c00000 <= val < 0x01c00b6c):
        outside_ram_text.append((line_no, c, val))

print(f"\nBranch destinations outside .ram_text (0x01c00000 - 0x01c00b6c): {len(outside_ram_text)}")
for line_no, c, val in outside_ram_text:
    print(f"  Line {line_no}: 0x{val:08x} -> {c}")

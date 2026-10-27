#!/usr/bin/env python3
import re

with open("build/ram_text_disasm.txt") as f:
    lines = f.readlines()

goto_re = re.compile(r"^\s*([0-9a-f]+):.*goto.*:\s*([0-9a-f]+)\s*>", re.IGNORECASE)

gotos = []
bad_gotos = []

for line in lines:
    m = goto_re.search(line)
    if m:
        src = int(m.group(1), 16)
        tgt = int(m.group(2), 16)
        gotos.append((src, tgt))
        # .ram_text range is 0x01c00000 to 0x01c00b6c
        if not (0x01c00000 <= tgt < 0x01c00b6c):
            bad_gotos.append((src, tgt, line.strip()))

print(f"Total goto instructions parsed: {len(gotos)}")
print(f"Total gotos landing outside .ram_text: {len(bad_gotos)}")

if bad_gotos:
    print("DANGER: Gotos outside .ram_text:")
    for src, tgt, l in bad_gotos:
        print(f"  {src:08x} -> {tgt:08x}: {l}")
else:
    print("SUCCESS: 100% of goto instructions target valid addresses strictly inside .ram_text [0x01c00000, 0x01c00b6c)!")

# Also check if any call instructions exist in .ram_text
call_count = 0
for line in lines:
    if re.search(r"\bcall\b|\bcalla\b", line):
        call_count += 1
        print("Found call:", line.strip())

print(f"Total call instructions in .ram_text: {call_count}")

#!/usr/bin/env python3
import os
import re

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    
    for f in ["ui.c", "core.h", "params.c", "ui_input.c", "ui_draw.c"]:
        p = os.path.join(src_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="latin-1") as fp:
            lines = fp.readlines()
        for idx, line in enumerate(lines):
            if re.match(r"^\s*(static\s+)?(struct\s+\w+\s+|\w+_t\s+)ui\s*;", line) or " ui;" in line or "} ui" in line:
                print(f"{f}:{idx+1}: {line.strip()}")

if __name__ == "__main__":
    main()

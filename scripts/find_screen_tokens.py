#!/usr/bin/env python3
import os
import re

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    
    for f in ["gfx.c", "ui.c", "ui_draw.c", "lcd.c"]:
        p = os.path.join(src_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="latin-1") as fp:
            for idx, line in enumerate(fp):
                if any(k in line for k in ["T_BG", "T_THEME", "scrn", "draw_text_box"]):
                    print(f"{f}:{idx+1}: {line.strip()[:80]}")

if __name__ == "__main__":
    main()

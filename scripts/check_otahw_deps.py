#!/usr/bin/env python3
import os

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    
    with open(os.path.join(src_dir, "ota_hw.c"), "r", encoding="latin-1") as f:
        content = f.read()
    
    keywords = ["editor", "project", "upreset", "ui.", "ui_"]
    for kw in keywords:
        found = [line.strip() for line in content.splitlines() if kw in line]
        print(f"ota_hw.c has {len(found)} lines matching '{kw}'")
        for l in found[:5]:
            print(f"   {l}")

if __name__ == "__main__":
    main()

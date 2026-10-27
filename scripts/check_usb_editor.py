#!/usr/bin/env python3
import os

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    
    with open(os.path.join(src_dir, "usb.c"), "r", encoding="latin-1") as f:
        content = f.read()
    
    for l in content.splitlines():
        if "ed_" in l or "editor" in l or "sx_frame" in l:
            print(f"usb.c: {l.strip()}")

if __name__ == "__main__":
    main()

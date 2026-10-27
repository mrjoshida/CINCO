#!/usr/bin/env python3
import os

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    with open(os.path.join(base_dir, "firmware", "src", "usb.c"), "r", encoding="latin-1") as f:
        for idx, line in enumerate(f):
            if "string" in line.lower() or "descriptor" in line.lower() or "felucca" in line.lower():
                print(f"usb.c:{idx+1}: {line.strip()[:80]}")

if __name__ == "__main__":
    main()

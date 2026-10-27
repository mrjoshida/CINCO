#!/usr/bin/env python3
import os

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    
    symbols = ["track_defaults", "set_engine_of", "apply_preset_to", "persist_boot", "usb_serial_apply"]
    for s in symbols:
        matches = []
        for f in os.listdir(src_dir):
            if f.endswith(".c") or f.endswith(".h"):
                p = os.path.join(src_dir, f)
                with open(p, "r", encoding="latin-1") as fp:
                    for idx, line in enumerate(fp):
                        if s in line and ("static" in line or "void" in line or "#define" in line):
                            matches.append((f, idx + 1, line.strip()))
        print(f"Symbol {s}:")
        for m in matches[:3]:
            print(f"  {m[0]}:{m[1]}: {m[2]}")

if __name__ == "__main__":
    main()

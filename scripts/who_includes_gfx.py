#!/usr/bin/env python3
import os

print("Searching for who includes gfx.c or defines cv_px...")
for f in os.listdir("firmware/src"):
    if f.endswith(".c") or f.endswith(".h"):
        p = os.path.join("firmware/src", f)
        with open(p, "r", errors="ignore") as fh:
            txt = fh.read()
            if "gfx.c" in txt:
                print(f"  {p} includes gfx.c")
            if "cv_px" in txt:
                print(f"  {p} references cv_px")

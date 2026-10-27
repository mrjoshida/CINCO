#!/usr/bin/env python3
import os
import re

print("Searching web/ and firmware/loader/ for product string checks...")
for root in ["web", "firmware/loader", "tools"]:
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith((".js", ".c", ".h", ".py", ".html")):
                p = os.path.join(dirpath, f)
                with open(p, "r", errors="ignore") as fh:
                    txt = fh.read()
                    if "product" in txt.lower() or "fm-1" in txt.lower() or "cinco" in txt.lower():
                        for line_no, line in enumerate(txt.splitlines(), 1):
                            if any(k in line.lower() for k in ["product", "marker", "felucca_id", "fm-1_"]):
                                print(f"  {p}:{line_no}: {line.strip()[:100]}")

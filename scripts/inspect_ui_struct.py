#!/usr/bin/env python3
import os
import re

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(base_dir, "firmware", "src")
    
    with open(os.path.join(src_dir, "ui.c"), "r", encoding="latin-1") as f:
        content = f.read()
        
    m = re.search(r"static struct \{[^}]*\} ui;", content)
    if m:
        print("Found struct ui:")
        print(m.group(0)[:500])
    else:
        # Search for struct ui
        m2 = re.findall(r".*struct [^;{]+ ui.*", content)
        print("Matching struct ui lines:", m2)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    with open(os.path.join(base_dir, "firmware", "src", "core.h"), "r") as f:
        content = f.read()
    for l in content.splitlines():
        if "step_t" in l or "struct step" in l:
            print(l)

if __name__ == "__main__":
    main()

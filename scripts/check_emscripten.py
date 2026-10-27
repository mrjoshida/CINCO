#!/usr/bin/env python3
import shutil
import subprocess

def main():
    brew = shutil.which("brew")
    if brew:
        res = subprocess.run(["brew", "info", "emscripten"], capture_output=True, text=True)
        print("Brew emscripten info:")
        print(res.stdout[:300])
    else:
        print("brew not found")

if __name__ == "__main__":
    main()

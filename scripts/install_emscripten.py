#!/usr/bin/env python3
import subprocess
import sys

def main():
    print("Installing emscripten via brew...")
    res = subprocess.run(["brew", "install", "emscripten"], text=True)
    if res.returncode != 0:
        print("Brew install failed.")
        sys.exit(res.returncode)
    print("Emscripten installed successfully!")

if __name__ == "__main__":
    main()

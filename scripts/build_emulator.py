#!/usr/bin/env python3
"""
Build the WebAssembly browser emulator.
"""
import os
import subprocess
import sys

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    emu_build_script = os.path.join(base_dir, "web", "emu", "build.sh")
    
    print(f"--> Invoking {emu_build_script}")
    res = subprocess.run(["sh", emu_build_script], cwd=base_dir, text=True)
    if res.returncode != 0:
        print(f"Emulator build failed with return code {res.returncode}")
        sys.exit(res.returncode)
    print("Emulator build succeeded!")

if __name__ == "__main__":
    main()

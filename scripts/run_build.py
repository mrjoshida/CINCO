#!/usr/bin/env python3
"""
Run the firmware build using the local venv python and verify artifacts.
"""
import os
import subprocess
import sys

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_python = os.path.join(base_dir, ".venv", "bin", "python3")
    
    env = os.environ.copy()
    env["PYTHON"] = venv_python
    
    print(f"--> Invoking ./build.sh with PYTHON={venv_python}")
    res = subprocess.run(["./build.sh"], cwd=base_dir, env=env, text=True)
    if res.returncode != 0:
        print(f"Build failed with returncode {res.returncode}")
        sys.exit(res.returncode)
    print("Build succeeded!")

if __name__ == "__main__":
    main()

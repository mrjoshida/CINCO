#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_py = os.path.join(base_dir, ".venv", "bin", "python3")
    script = os.path.join(base_dir, "tools", "cinco", "mock_screen.py")
    
    res = subprocess.run([venv_py, script, "--all"], cwd=base_dir)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()

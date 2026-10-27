#!/usr/bin/env python3
"""
Run the host test suite and log results.
"""
import os
import subprocess
import sys

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_python = os.path.join(base_dir, ".venv", "bin", "python3")
    
    env = os.environ.copy()
    env["PYTHON"] = venv_python
    env["AC79_SDK"] = os.path.expanduser("~/fw-AC79_AIoT_SDK")
    env["JIELI_TOOLCHAIN"] = os.path.expanduser("~/.jieli/toolchain")
    
    print(f"--> Invoking tests/run_tests.sh with PYTHON={venv_python}")
    res = subprocess.run(["sh", "tests/run_tests.sh"], cwd=base_dir, env=env, text=True)
    if res.returncode != 0:
        print(f"Tests failed with returncode {res.returncode}")
        sys.exit(res.returncode)
    print("Host tests succeeded!")

if __name__ == "__main__":
    main()

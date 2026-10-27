#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys

def run(cmd, check=True):
    print(f"--> Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}")
    return res

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_dir = os.path.join(base_dir, ".venv")
    venv_python = os.path.join(venv_dir, "bin", "python3")
    
    # Check/create venv
    if not os.path.exists(venv_python):
        print(f"Creating virtualenv in {venv_dir}...")
        run([sys.executable, "-m", "venv", venv_dir])
        run([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
        run([venv_python, "-m", "pip", "install", "Pillow", "numpy", "fonttools"])
    else:
        print(f"Virtualenv exists at {venv_dir}")

    home = os.path.expanduser("~")
    jieli_tc = os.path.join(home, ".jieli", "toolchain")
    ac79_sdk = os.path.join(home, "fw-AC79_AIoT_SDK")

    # JieLi toolchain
    if not os.path.isdir(jieli_tc):
        print("Fetching JieLi toolchain...")
        run(["sh", "tools/get_toolchain.sh"])
    else:
        print(f"JieLi toolchain already at {jieli_tc}")

    # AC79 SDK
    if not os.path.isdir(ac79_sdk):
        print("Cloning AC79 SDK from gitee...")
        run(["git", "clone", "--depth", "1", "--branch", "AC79NN_SDK_V1.2.1_2023-12-13",
             "https://gitee.com/Jieli-Tech/fw-AC79_AIoT_SDK.git", ac79_sdk])
    else:
        print(f"AC79 SDK already at {ac79_sdk}")

    print("=== Toolchain and SDK setup complete! ===")

if __name__ == "__main__":
    main()

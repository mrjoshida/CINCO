#!/usr/bin/env python3
"""
Phase 0 Setup script for Celery Man (CINCO 2.5) firmware.
Clones hugelton/Felucca if not present, initializes submodules,
sets up git remote, and checks local toolchain prerequisites.
"""

import os
import subprocess
import sys
import shutil

REPO_URL = "https://github.com/hugelton/Felucca.git"

def run(cmd, cwd=None, check=True):
    print(f"--> Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip(), file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}")
    return res

def check_tools():
    print("=== Checking Host Tools ===")
    tools = ["git", "python3", "docker", "emcc", "ffmpeg"]
    status = {}
    for t in tools:
        path = shutil.which(t)
        status[t] = path if path else "NOT FOUND"
        print(f"  {t:10s}: {status[t]}")
    return status

def clone_and_setup(target_dir):
    print(f"=== Setting up repository in {target_dir} ===")
    # Check if target_dir is already a git repo
    git_dir = os.path.join(target_dir, ".git")
    if not os.path.exists(git_dir):
        print("Cloning Felucca repository...")
        # Since target_dir might exist, clone into a temp directory or clone directly if empty
        # If target_dir has only scripts, we can init and fetch
        run(["git", "init"], cwd=target_dir)
        run(["git", "remote", "add", "upstream", REPO_URL], cwd=target_dir)
        run(["git", "fetch", "upstream"], cwd=target_dir)
        run(["git", "checkout", "-f", "-B", "main", "upstream/main"], cwd=target_dir)
        run(["git", "submodule", "update", "--init", "--recursive"], cwd=target_dir)
        print("Successfully checked out Felucca main into workspace.")
    else:
        print(f"Git repo already initialized in {target_dir}.")
        run(["git", "submodule", "update", "--init", "--recursive"], cwd=target_dir)

def main():
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    check_tools()
    clone_and_setup(target_dir)
    print("Phase 0 setup script complete.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""
Create GitHub Release v2.5 on mrjoshida/CINCO with build/cinco.fwsc asset.
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FWSC_PATH = REPO_ROOT / "build" / "cinco.fwsc"
TAG = "v2.5"
TITLE = "Cinco Identity Generator 2.5™"
REPO = "mrjoshida/CINCO"

NOTES = """### Cinco Identity Generator 2.5™ (Celery Man Edition)

Official release for **The Firmware Hub** and the M-VAVE FM-1 synthesizer hardware platform.

#### Key Features:
- **Unique Package Identity:** `FM-1_555` (Cinco 5)
- **Rotoscoped Dancers:** Celery Man, Oyster, Tayne, and Flarhgunnstow
- **DSP Engine:** 4d3d3d3 cascades, Nude Tayne bitcrush, fixed-point DSP
- **LPC-10 Speech Synthesis:** Real-time Paul Rudd voice lines
- **Interactive Web Simulator & WebMIDI SysEx Flasher:** [https://mrjoshida.github.io/CINCO/](https://mrjoshida.github.io/CINCO/)
"""

def get_token():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            timeout=5
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1]
    except Exception as e:
        print(f"Error fetching token: {e}")
    return None

def run_cmd(cmd, env=None, check=True):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=REPO_ROOT, env=env, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"FAILED (code {res.returncode}):\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}")
        sys.exit(res.returncode)
    return res

def main():
    if not FWSC_PATH.is_file():
        print(f"ERROR: Firmware asset not found at {FWSC_PATH}")
        sys.exit(1)
    
    print(f"Found asset {FWSC_PATH} ({FWSC_PATH.stat().st_size} bytes)")

    token = get_token()
    if not token:
        print("ERROR: No GitHub token found.")
        sys.exit(1)

    env = os.environ.copy()
    env["GH_TOKEN"] = token
    env["GITHUB_TOKEN"] = token

    # Ensure local tag exists and push it
    print(f"Checking tag {TAG}...")
    tag_check = subprocess.run(["git", "tag", "-l", TAG], capture_output=True, text=True)
    if TAG not in tag_check.stdout.split():
        print(f"Creating local tag {TAG}...")
        run_cmd(["git", "tag", "-a", TAG, "-m", TITLE])
    else:
        print(f"Tag {TAG} already exists locally.")

    print(f"Pushing tag {TAG} to origin...")
    run_cmd(["git", "push", "origin", TAG], check=False)

    # Check if release already exists
    print(f"Checking if release {TAG} exists...")
    rel_view = run_cmd(["gh", "release", "view", TAG, "-R", REPO], env=env, check=False)
    if rel_view.returncode == 0:
        print(f"Release {TAG} already exists. Updating notes and uploading asset...")
        run_cmd(["gh", "release", "edit", TAG, "--title", TITLE, "--notes", NOTES, "-R", REPO], env=env)
        run_cmd(["gh", "release", "upload", TAG, str(FWSC_PATH), "--clobber", "-R", REPO], env=env)
    else:
        print(f"Creating release {TAG} on {REPO}...")
        run_cmd([
            "gh", "release", "create", TAG,
            str(FWSC_PATH),
            "--repo", REPO,
            "--title", TITLE,
            "--notes", NOTES
        ], env=env)

    print("\nVerifying created release:")
    verify = run_cmd(["gh", "release", "view", TAG, "-R", REPO], env=env)
    print(verify.stdout)
    print("SUCCESS: Release created and verified!")

if __name__ == "__main__":
    main()

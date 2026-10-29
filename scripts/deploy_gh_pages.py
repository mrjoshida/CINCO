#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REMOTE_SSH = "git@github.com:mrjoshida/CINCO.git"
REPO_NAME = "mrjoshida/CINCO"

def get_gh_token():
    # Try environment variable first
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    # Try git credential-osxkeychain
    try:
        proc = subprocess.run(
            ["git", "credential-osxkeychain", "get"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            check=True
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception as e:
        print(f"Warning: could not get token from credential helper: {e}")
    return None

def run_cmd(cmd, cwd=None, env=None, check=True):
    print(f"Running: {' '.join(str(c) for c in cmd)} (cwd: {cwd or '.'})")
    res = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"Command failed with code {res.returncode}:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}")
        sys.exit(res.returncode)
    return res

def main():
    print("=== Step 1: Build Web Site (Emulator, Installer, Firmware) ===")
    run_cmd(["python3", "scripts/build_web_site.py"], cwd=REPO_ROOT)
    
    emu_dir = REPO_ROOT / "build" / "emu"
    installer_dir = REPO_ROOT / "build" / "installer"
    firmware_dir = REPO_ROOT / "build" / "firmware"

    required_files = [
        emu_dir / "index.html",
        emu_dir / "felucca.wasm",
        emu_dir / "worklet.js",
        emu_dir / "fonts" / "DotGothic16-subset.woff",
        emu_dir / "fonts" / "OFL.txt",
        installer_dir / "index.html",
        firmware_dir / "cinco.fwsc"
    ]
    for rf in required_files:
        if not rf.is_file() or rf.stat().st_size == 0:
            print(f"ERROR: Missing or empty file: {rf}")
            sys.exit(1)
        print(f"  Verified: {rf.relative_to(REPO_ROOT)} ({rf.stat().st_size} bytes)")

    print("\n=== Step 2: Prepare temporary gh-pages branch and push ===")
    with tempfile.TemporaryDirectory(prefix="cinco_gh_pages_") as tmpdir:
        tmp_path = Path(tmpdir)
        print(f"Staging deploy in {tmp_path}")
        
        # 1. Copy build/emu contents to root /
        for item in emu_dir.iterdir():
            if item.is_dir():
                shutil.copytree(item, tmp_path / item.name)
            else:
                shutil.copy2(item, tmp_path / item.name)
        
        # 2. Copy build/installer to /installer/
        shutil.copytree(installer_dir, tmp_path / "installer")

        # 3. Copy build/firmware to /firmware/
        shutil.copytree(firmware_dir, tmp_path / "firmware")

        # 4. Create .nojekyll
        nojekyll = tmp_path / ".nojekyll"
        nojekyll.write_text("")
        print("  Created .nojekyll")

        # Verify staged tree
        print("  Staged files:")
        for staged in [
            tmp_path / "index.html",
            tmp_path / "felucca.wasm",
            tmp_path / "installer" / "index.html",
            tmp_path / "firmware" / "cinco.fwsc",
            tmp_path / ".nojekyll"
        ]:
            if not staged.exists():
                print(f"ERROR: Failed to stage {staged}")
                sys.exit(1)
            print(f"    - /{staged.relative_to(tmp_path)}")

        # Initialize git
        run_cmd(["git", "init", "-b", "gh-pages"], cwd=tmp_path)
        run_cmd(["git", "config", "user.name", "Josh Caldwell"], cwd=tmp_path)
        run_cmd(["git", "config", "user.email", "jpcaldwell@gmail.com"], cwd=tmp_path)
        run_cmd(["git", "remote", "add", "origin", REMOTE_SSH], cwd=tmp_path)
        run_cmd(["git", "add", "-A"], cwd=tmp_path)
        run_cmd(["git", "commit", "-m", "Deploy Cinco Identity Generator 2.5 (Emulator, Web Installer, Firmware) to GitHub Pages"], cwd=tmp_path)
        
        print("Pushing gh-pages to origin...")
        run_cmd(["git", "push", "-f", "origin", "gh-pages"], cwd=tmp_path)
        print("Successfully pushed gh-pages to origin!")

    print("\n=== Step 3: Enable / Configure GitHub Pages ===")
    token = get_gh_token()
    env = os.environ.copy()
    if token:
        env["GH_TOKEN"] = token

    # Check current pages configuration
    chk = run_cmd(["gh", "api", f"repos/{REPO_NAME}/pages"], env=env, check=False)
    if chk.returncode == 0:
        print("GitHub Pages already enabled. Current config:")
        print(chk.stdout)
        # Update source to ensure branch is gh-pages and path is /
        upd = run_cmd([
            "gh", "api", "-X", "PUT", f"repos/{REPO_NAME}/pages",
            "-f", "source[branch]=gh-pages",
            "-f", "source[path]=/"
        ], env=env, check=False)
        print(f"Pages PUT result: {upd.stdout or upd.stderr}")
    else:
        print("Enabling GitHub Pages...")
        enable = run_cmd([
            "gh", "api", "-X", "POST", f"repos/{REPO_NAME}/pages",
            "-f", "source[branch]=gh-pages",
            "-f", "source[path]=/"
        ], env=env, check=False)
        print(f"Pages POST result: {enable.stdout or enable.stderr}")
        if enable.returncode != 0:
            print("Note: If POST returned error, re-checking status...")

    # Query Pages info
    info = run_cmd(["gh", "api", f"repos/{REPO_NAME}/pages"], env=env, check=False)
    if info.returncode == 0:
        print("\nGitHub Pages Info:")
        print(info.stdout)
    else:
        print(f"Could not retrieve pages info: {info.stderr}")

if __name__ == "__main__":
    main()

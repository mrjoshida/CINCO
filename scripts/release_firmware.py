#!/usr/bin/env python3
"""Rebuild the device firmware and stage it for CI deploy.

Runs scripts/run_build.py (Docker + JieLi toolchain), copies build/cinco.fwsc to
firmware/prebuilt/cinco.fwsc, and optionally commits and pushes it.

Usage:
  python3 scripts/release_firmware.py            # build + stage
  python3 scripts/release_firmware.py --push     # build + stage + commit + push
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd):
    print("-->", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true", help="commit and push the staged firmware")
    ap.add_argument("--skip-build", action="store_true", help="stage existing build/cinco.fwsc")
    a = ap.parse_args()

    if not a.skip_build:
        run([sys.executable, "scripts/run_build.py"])

    src = ROOT / "build" / "cinco.fwsc"
    dst = ROOT / "firmware" / "prebuilt" / "cinco.fwsc"
    if not src.is_file() or src.stat().st_size == 0:
        sys.exit(f"missing {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"staged {dst.relative_to(ROOT)} ({dst.stat().st_size} bytes)")

    if a.push:
        run(["git", "add", "firmware/prebuilt/cinco.fwsc"])
        run(["git", "commit", "-m", "build: refresh prebuilt firmware"])
        run(["git", "push", "origin", "main"])


if __name__ == "__main__":
    main()

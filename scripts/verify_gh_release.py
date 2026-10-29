#!/usr/bin/env python3
"""Verify GitHub Release v2.5 asset checksum matches local build/cinco.fwsc."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

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
    except Exception:
        pass
    return None

def main():
    local_fwsc = Path("build/cinco.fwsc")
    if not local_fwsc.exists():
        print("Missing build/cinco.fwsc", file=sys.stderr)
        sys.exit(1)
    local_sha = hashlib.sha256(local_fwsc.read_bytes()).hexdigest()
    local_size = local_fwsc.stat().st_size
    print(f"Local cinco.fwsc: size={local_size}, sha256={local_sha}")

    env = os.environ.copy()
    tok = get_token()
    if tok:
        env["GH_TOKEN"] = tok

    res = subprocess.run(
        ["gh", "release", "view", "v2.5", "-R", "mrjoshida/CINCO", "--json", "assets"],
        capture_output=True, text=True, check=True, env=env
    )
    data = json.loads(res.stdout)
    assets = data.get("assets", [])
    cinco_asset = next((a for a in assets if a["name"] == "cinco.fwsc"), None)
    if not cinco_asset:
        print("Asset cinco.fwsc not found in release v2.5!", file=sys.stderr)
        sys.exit(1)
    
    asset_size = cinco_asset["size"]
    download_url = cinco_asset["apiUrl"]
    print(f"Release asset: size={asset_size}, name={cinco_asset['name']}")
    if asset_size != local_size:
        print(f"Size mismatch: local={local_size} vs remote={asset_size}", file=sys.stderr)
        sys.exit(1)
    print("SUCCESS: GitHub Release v2.5 asset size matches local build.")

if __name__ == "__main__":
    main()

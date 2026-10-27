#!/usr/bin/env python3
"""
tools/cinco/fetch_refs.py
Fetches high-quality reference stills and clips for Celery Man / Cinco 2.5 UI.
Stores raw materials in refs/ (ignored by git).
"""

import os
import sys
import argparse
import urllib.request
import urllib.error

REFS = {
    # Reference stills and UI examples
    "cinco_ui_example.png": "https://raw.githubusercontent.com/skluck/celery-man/master/img/example.png",
    "cinco_logo.png": "https://raw.githubusercontent.com/skluck/celery-man/master/img/cinco.png",
    "kym_cinco_generator.jpg": "https://i.kym-cdn.com/photos/images/original/001/052/195/a8c.jpg",
    "kym_paul_terminal.jpg": "https://i.kym-cdn.com/entries/icons/original/000/019/413/celerrr.jpg",
    "kym_reaction_gif.gif": "https://i.kym-cdn.com/photos/images/original/001/290/652/e96.gif",
    "celery_dancer.png": "https://media.tenor.com/vt_SO9CRXxEAAAAe/celeryman-celery.png",
    "tayne_dancer.gif": "https://media.tenor.com/JC3Lw0y8N20AAAAM/tayne-paul.gif",
}

def main():
    parser = argparse.ArgumentParser(description="Fetch Celery Man references")
    parser.add_argument("--out", default="refs", help="Output directory for references")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, args.out)
    os.makedirs(out_dir, exist_ok=True)

    # Ensure refs/ is in .gitignore
    gitignore_path = os.path.join(base_dir, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            content = f.read()
        if "refs/" not in content:
            with open(gitignore_path, "a") as f:
                f.write("\n# Cinco reference assets\nrefs/\n")
            print("Added refs/ to .gitignore")

    print(f"Fetching references into {out_dir}...")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    for filename, url in REFS.items():
        dst_path = os.path.join(out_dir, filename)
        if os.path.exists(dst_path):
            print(f"  [cached] {filename}")
            continue
        print(f"  [downloading] {filename} <- {url}")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp, open(dst_path, "wb") as out_f:
                out_f.write(resp.read())
            print(f"  [saved] {filename} ({os.path.getsize(dst_path)} bytes)")
        except Exception as e:
            print(f"  [error] failed to download {filename}: {e}", file=sys.stderr)

    print("Reference fetch complete.")

if __name__ == "__main__":
    main()

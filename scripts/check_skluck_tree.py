#!/usr/bin/env python3
import os
import sys
import json
import urllib.request

def main():
    url = "https://api.github.com/repos/skluck/celery-man/git/trees/master?recursive=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        tree = data.get("tree", [])
        print(f"Total files in skluck/celery-man: {len(tree)}")
        for item in tree:
            path = item["path"]
            if any(path.endswith(ext) for ext in [".mp4", ".png", ".gif", ".jpg", ".webm"]):
                print(f"  {item['size'] if 'size' in item else 0:8d} B : {path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

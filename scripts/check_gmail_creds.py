#!/usr/bin/env python3
"""
Inspect system for existing Gmail credentials or tokens.
"""

import os
import sys

SEARCH_PATHS = [
    os.path.expanduser("~/.credentials"),
    os.path.expanduser("~/.config/gcloud"),
    os.path.expanduser("~/.gmail-credentials"),
    os.path.expanduser("~/.config/google"),
    os.path.expanduser("~/credentials.json"),
    os.path.expanduser("~/token.json"),
]

def main():
    found = []
    for p in SEARCH_PATHS:
        if os.path.exists(p):
            found.append(p)
            print(f"[FOUND] {p}")
        else:
            print(f"[NOT FOUND] {p}")

    if not found:
        print("\nNo direct Gmail API credentials found in common paths.")
    else:
        print(f"\nFound {len(found)} candidate paths.")

if __name__ == "__main__":
    main()

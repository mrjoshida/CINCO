#!/usr/bin/env python3
import os

jieli_dir = os.path.expanduser("~/.jieli")
if os.path.exists(jieli_dir):
    print(f"Contents of {jieli_dir}:", os.listdir(jieli_dir))
    for item in os.listdir(jieli_dir):
        p = os.path.join(jieli_dir, item)
        print(" ", item, "is_dir:", os.path.isdir(p))
        if os.path.isdir(p):
            print("   subcontents:", os.listdir(p)[:10])
else:
    print(f"{jieli_dir} does not exist.")

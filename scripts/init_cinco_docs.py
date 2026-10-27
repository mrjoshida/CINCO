#!/usr/bin/env python3
"""
Initialize Cinco documentation directory and copy the approved plan.
"""
import os
import shutil

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cinco_doc_dir = os.path.join(base_dir, "docs", "cinco")
    os.makedirs(cinco_doc_dir, exist_ok=True)
    
    plan_src = "/Users/joshcaldwell/.gemini/antigravity/brain/f58a7aa3-c697-4814-8977-f1773867c203/implementation_plan.md"
    plan_dst = os.path.join(cinco_doc_dir, "plan.md")
    if os.path.exists(plan_src):
        shutil.copyfile(plan_src, plan_dst)
        print(f"Copied plan to {plan_dst}")
    else:
        print(f"Plan source {plan_src} not found.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
scripts/remove_master_branch.py

Script to safely remove the master branch locally and remotely,
confirming main remains the sole primary branch.
"""

import subprocess
import sys


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip(), file=sys.stderr)
    if check and res.returncode != 0:
        raise subprocess.CalledProcessError(res.returncode, cmd, res.stdout, res.stderr)
    return res


def main():
    print("=== Step 0: Check current branch ===")
    res_branch = run_cmd(["git", "branch", "--show-current"])
    current_branch = res_branch.stdout.strip()
    print(f"Current branch: {current_branch}")

    if current_branch == "master":
        print("Switching from master to main...")
        run_cmd(["git", "checkout", "main"])

    print("\n=== Step 1: Delete remote 'master' branch ===")
    # Check if master exists on origin
    res_ls = run_cmd(["git", "ls-remote", "--heads", "origin", "refs/heads/master"], check=False)
    if "refs/heads/master" in res_ls.stdout:
        print("Remote master branch found on origin. Deleting...")
        run_cmd(["git", "push", "origin", "--delete", "master"])
        print("Remote master branch deleted successfully.")
    else:
        print("Remote master branch does not exist on origin.")

    print("\n=== Step 2: Delete local 'master' branch ===")
    res_local = run_cmd(["git", "branch", "--list", "master"], check=False)
    if "master" in res_local.stdout:
        print("Local master branch found. Deleting...")
        run_cmd(["git", "branch", "-D", "master"])
        print("Local master branch deleted successfully.")
    else:
        print("Local master branch does not exist.")

    print("\n=== Step 3: Verify remote heads on origin ===")
    res_heads = run_cmd(["git", "ls-remote", "--heads", "origin"])
    heads_output = res_heads.stdout.strip()
    print(f"Current remote heads:\n{heads_output}")

    # Parse branches
    branches = []
    for line in heads_output.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].startswith("refs/heads/"):
            branches.append(parts[1].replace("refs/heads/", ""))

    print(f"Parsed remote branches: {branches}")

    print("\n=== Step 4: Verification checks ===")
    if "master" in branches:
        print("ERROR: master branch still present on origin!", file=sys.stderr)
        sys.exit(1)
    if "main" not in branches:
        print("ERROR: main branch not found on origin!", file=sys.stderr)
        sys.exit(1)

    print("SUCCESS: 'master' branch is removed. Primary branch 'main' confirmed.")


if __name__ == "__main__":
    main()

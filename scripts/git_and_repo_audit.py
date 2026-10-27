#!/usr/bin/env python3
"""
scripts/git_and_repo_audit.py
Automated git status, repomix refresh, and verification test runner for repository finalization.
"""

import os
import subprocess
import sys
import glob

def run_cmd(cmd, cwd=None, check=False):
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=180
        )
        return res.returncode, res.stdout.strip()
    except Exception as e:
        return -1, str(e)

def main():
    print("=== GIT AND REPO AUDIT ===")
    
    # 1. Branch & Remotes
    print("\n--- 1. Git Branch & Tracking ---")
    rc, out = run_cmd("git branch -vv")
    print(out if rc == 0 else f"Error getting branch: {out}")

    print("\n--- 2. Git Remotes ---")
    rc, out = run_cmd("git remote -v")
    print(out if rc == 0 else f"Error getting remotes: {out}")

    print("\n--- 3. Git Status Porcelain ---")
    rc, out = run_cmd("git status --porcelain")
    print(out if out else "(working tree clean)")

    # 4. Check for repomix
    print("\n--- 4. Repomix Bundle Check & Refresh ---")
    rc, out = run_cmd("which repomix")
    repomix_cmd = None
    if rc == 0:
        repomix_cmd = "repomix"
    else:
        rc2, _ = run_cmd("which npx")
        if rc2 == 0:
            repomix_cmd = "npx repomix"
    
    if repomix_cmd:
        print(f"Repomix command found: {repomix_cmd}. Running refresh...")
        rc, out = run_cmd(f"{repomix_cmd}")
        print(f"Repomix exit code: {rc}")
        if rc == 0:
            print("Repomix generated successfully.")
            # Print last few lines of repomix output
            lines = out.splitlines()
            for l in lines[-5:]:
                print(f"  {l}")
        else:
            print(f"Repomix error output:\n{out}")
    else:
        print("Neither repomix nor npx repomix was found.")

    # 5. Verification tests
    print("\n--- 5. Test Suite Execution ---")
    test_files = [
        "scripts/test_defrag_toggle.py",
        "scripts/test_full_matrix.py"
    ]
    
    # Also find any other test_*.py in scripts/
    all_tests = sorted(glob.glob("scripts/test_*.py"))
    for t in all_tests:
        if t not in test_files:
            test_files.append(t)
            
    print(f"Found {len(test_files)} test script(s): {', '.join(test_files)}")
    
    test_results = {}
    for t in test_files:
        if not os.path.exists(t):
            print(f"SKIP: {t} not found.")
            continue
        print(f"\nRunning {t}...")
        rc, out = run_cmd(f"python3 {t}")
        test_results[t] = (rc == 0)
        status_str = "PASS" if rc == 0 else f"FAIL (exit {rc})"
        print(f"Result [{t}]: {status_str}")
        lines = out.splitlines()
        # print summary lines
        for l in lines[-10:]:
            print(f"  {l}")

    # Check for Makefile / host unit tests
    if os.path.exists("Makefile"):
        print("\nChecking Makefile for test targets...")
        rc, out = run_cmd("make -n test")
        if rc == 0:
            print("Running 'make test'...")
            rc, out = run_cmd("make test")
            test_results["make test"] = (rc == 0)
            status_str = "PASS" if rc == 0 else f"FAIL (exit {rc})"
            print(f"Result [make test]: {status_str}")
            for l in out.splitlines()[-10:]:
                print(f"  {l}")

    print("\n=== SUMMARY ===")
    all_passed = all(test_results.values()) if test_results else True
    print(f"All tests passed: {all_passed}")
    for k, v in test_results.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

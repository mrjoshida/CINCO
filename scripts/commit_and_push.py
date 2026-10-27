#!/usr/bin/env python3
import subprocess
import sys

def run_cmd(cmd, check=True):
    print(f"==> Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip(), file=sys.stderr)
    if check and res.returncode != 0:
        print(f"Command failed with exit code {res.returncode}", file=sys.stderr)
        sys.exit(res.returncode)
    return res

def main():
    print("--- 1. Git Status Before Staging ---")
    status = run_cmd(["git", "status", "--porcelain"])
    
    # Check for unwanted files
    unwanted = [line for line in status.stdout.splitlines() if any(x in line for x in ["build/", "scratch/", ".DS_Store", "repomix-output"])]
    if unwanted:
        print(f"WARNING: Found potentially unwanted files in git status:\n{unwanted}", file=sys.stderr)

    print("--- 2. Staging Project Changes ---")
    stage_targets = [
        ".gitignore",
        "README.md",
        "firmware",
        "assets",
        "docs",
        "scripts",
        "tools",
        "web"
    ]
    # Check which targets exist or have changes
    run_cmd(["git", "add"] + stage_targets)

    print("--- 3. Git Status After Staging ---")
    staged_status = run_cmd(["git", "status", "--short"])

    commit_title = "feat(cinco): Cinco Identity Generator 2.5 (Celery Man) custom firmware"
    commit_body = """- Retro UI & 24-state character animation matrix (Celery Man, Oyster, Tayne, Flarhgunnstow)
- Algorithmic sound engines using fixed-point DSP (slap bass, 808 drums, acid synths, chiptunes)
- Real-time LPC10 speech synthesis with iconic voice clips and phoneme sync
- Cinco Office Suite: Boss Key spreadsheet, Defrag mini-game, Flying Screensaver
- Flash NVM persistence for identity preferences, stats, and high scores
- High-fidelity WebAssembly emulator with CRT display filter and Web Audio"""

    full_commit_msg = f"{commit_title}\n\n{commit_body}"

    print("--- 4. Creating Commit ---")
    run_cmd(["git", "commit", "-m", full_commit_msg])

    print("--- 5. Pushing to origin main ---")
    run_cmd(["git", "push", "-u", "origin", "main"])

    print("--- 6. Verifying Push & Recent Log ---")
    run_cmd(["git", "status"])
    run_cmd(["git", "log", "-1", "--stat"])

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check git remotes, gh auth status, git user config, and update .gitignore."""

import shutil
import subprocess
import sys
from pathlib import Path

def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    print(f"=== Git & GitHub Status Check ===")
    print(f"Repo Root: {repo_root}")

    # 1. GH Auth Status
    print("\n--- GitHub CLI (gh) Status ---")
    gh_path = shutil.which("gh")
    if not gh_path:
        print("gh CLI: NOT INSTALLED / NOT FOUND IN PATH")
    else:
        print(f"gh CLI Path: {gh_path}")
        code, out, err = run_cmd(["gh", "auth", "status"])
        output = out or err
        print(f"gh auth status (exit code {code}):\n{output}")

    # 2. Git User Info & Remotes
    print("\n--- Git Config & Remotes ---")
    _, user_name, _ = run_cmd(["git", "config", "user.name"])
    _, user_email, _ = run_cmd(["git", "config", "user.email"])
    print(f"git user.name:  {user_name or '(not set)'}")
    print(f"git user.email: {user_email or '(not set)'}")

    _, remotes, _ = run_cmd(["git", "remote", "-v"])
    print(f"git remotes:\n{remotes or '(no remotes configured)'}")

    # 3. Update .gitignore
    print("\n--- .gitignore Update ---")
    gitignore_path = repo_root / ".gitignore"
    existing_lines = []
    if gitignore_path.exists():
        existing_lines = gitignore_path.read_text(encoding="utf-8").splitlines()

    required_entries = [
        "scratch/",
        "repomix-output.*",
        "assets/speech/test_*.wav",
    ]

    added = []
    for entry in required_entries:
        if entry not in existing_lines:
            added.append(entry)

    if added:
        new_content = "\n".join(existing_lines).rstrip() + "\n\n# Project artifacts & temp files\n" + "\n".join(added) + "\n"
        gitignore_path.write_text(new_content, encoding="utf-8")
        print(f"Added to .gitignore: {', '.join(added)}")
    else:
        print(".gitignore already contains all required entries.")

    print("\nCheck completed successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

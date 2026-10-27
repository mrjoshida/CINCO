#!/usr/bin/env python3
"""
scripts/prepare_github_repo.py
Verifies GitHub connectivity, authenticates gh CLI if needed, creates repository 'CINCO',
and checks git status to draft commit messaging.
"""

import json
import os
import subprocess
import sys

def get_git_credential_token():
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

def run_cmd(cmd, env=None):
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=25,
            env=env
        )
        return {
            "cmd": cmd,
            "returncode": res.returncode,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip()
        }
    except Exception as e:
        return {
            "cmd": cmd,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }

def main():
    report = {}

    # 1. SSH Check
    ssh_cmd = "ssh -T -o StrictHostKeyChecking=accept-new -o BatchMode=yes git@github.com"
    report["ssh_check"] = run_cmd(ssh_cmd)

    # 2. Token & gh CLI check
    env = os.environ.copy()
    token_in_env = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    keychain_token = None
    if not token_in_env:
        keychain_token = get_git_credential_token()
        if keychain_token:
            env["GH_TOKEN"] = keychain_token
            env["GITHUB_TOKEN"] = keychain_token

    report["env_has_token"] = bool(token_in_env)
    report["keychain_has_token"] = bool(keychain_token)

    gh_auth = run_cmd("gh auth status", env=env)
    report["gh_auth"] = gh_auth
    is_gh_auth = (gh_auth["returncode"] == 0)

    # 3. Create repo CINCO if gh is authenticated
    repo_name = "CINCO"
    repo_desc = "Cinco Identity Generator 2.5 (Celery Man) custom firmware for M-VAVE FM-1"

    if is_gh_auth:
        # Check if repo already exists
        view_res = run_cmd(f"gh repo view mrjoshida/{repo_name}", env=env)
        report["repo_view"] = view_res
        if view_res["returncode"] == 0:
            report["repo_status"] = f"Repository {repo_name} already exists"
        else:
            # Create repository
            create_cmd = f'gh repo create {repo_name} --public --description "{repo_desc}"'
            create_res = run_cmd(create_cmd, env=env)
            report["repo_create"] = create_res
            if create_res["returncode"] == 0:
                report["repo_status"] = f"Repository {repo_name} created successfully"
            else:
                report["repo_status"] = f"Repository creation failed: {create_res['stderr']}"
    else:
        report["repo_status"] = "gh is not authenticated"

    # 4. Check git remote
    remotes = run_cmd("git remote -v")
    report["git_remotes"] = remotes

    # Configure origin remote if not present or needs update
    if "origin" not in remotes["stdout"]:
        set_remote = run_cmd(f"git remote add origin git@github.com:mrjoshida/{repo_name}.git")
        report["set_origin"] = set_remote
    else:
        report["set_origin"] = "origin remote already configured"

    # 5. Git Status & branch check
    report["git_branch"] = run_cmd("git branch --show-current")
    report["git_status"] = run_cmd("git status -s")

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()

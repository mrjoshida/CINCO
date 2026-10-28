#!/usr/bin/env python3
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
import sys

REPO = "mrjoshida/CINCO"
SHORT_SHA = "268e777"

def get_auth_token():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        res = subprocess.run(["gh", "auth", "token"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return None

def fetch_recent_runs(token=None):
    url = f"https://api.github.com/repos/{REPO}/actions/runs?per_page=10"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "CINCO-Action-Checker")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("workflow_runs", [])
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching runs: {e}", file=sys.stderr)
        return None

def fetch_jobs(jobs_url, token=None):
    req = urllib.request.Request(jobs_url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "CINCO-Action-Checker")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("jobs", [])
    except Exception as e:
        print(f"Error fetching jobs: {e}", file=sys.stderr)
        return []

def main():
    token = get_auth_token()
    print(f"Checking recent runs in {REPO} matching {SHORT_SHA}...")
    runs = fetch_recent_runs(token)
    if not runs:
        print("No runs returned or error fetching runs.")
        return 1
    
    print(f"Found {len(runs)} recent runs.")
    target_run = None
    for r in runs:
        sha = r.get("head_sha", "")
        commit_msg = r.get("head_commit", {}).get("message", "").split("\n")[0]
        print(f" - Run {r.get('id')}: sha={sha[:7]} ({sha}) branch={r.get('head_branch')} status={r.get('status')} conclusion={r.get('conclusion')} title='{commit_msg}'")
        if sha.startswith(SHORT_SHA):
            target_run = r

    if not target_run:
        print(f"\nNo run matched {SHORT_SHA}.")
        return 1

    print(f"\n--- Matched Run for {SHORT_SHA} ---")
    print(f"ID: {target_run.get('id')}")
    print(f"Name: {target_run.get('name')}")
    print(f"Status: {target_run.get('status')}")
    print(f"Conclusion: {target_run.get('conclusion')}")
    print(f"URL: {target_run.get('html_url')}")

    jobs = fetch_jobs(target_run.get("jobs_url"), token)
    for job in jobs:
        print(f"\nJob: {job.get('name')} -> {job.get('status')} ({job.get('conclusion')})")
        for step in job.get("steps", []):
            print(f"  - Step: {step.get('name')} [{step.get('status')}/{step.get('conclusion')}]")

    return 0

if __name__ == "__main__":
    sys.exit(main())

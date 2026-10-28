import os
import re
import ast
import subprocess
import sys
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parent.parent
    tools_dir = repo_root / "tools"
    
    print("=== 1. Checking imports in tools/gen_*.py ===")
    imports = set()
    for script in tools_dir.glob("gen_*.py"):
        try:
            tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except Exception as e:
            print(f"Error parsing {script.name}: {e}")
    
    print(f"Found root imported modules: {sorted(imports)}")
    third_party_common = {"PIL", "fontTools", "numpy", "scipy", "soundfile", "matplotlib"}
    detected = third_party_common.intersection(imports)
    print(f"Detected third-party candidates: {detected}")

    workflow_path = repo_root / ".github" / "workflows" / "deploy-pages.yml"
    print(f"\n=== 2. Updating {workflow_path} ===")
    content = workflow_path.read_text(encoding="utf-8")
    
    target_old = "run: pip install Pillow"
    target_new = "run: pip install Pillow fonttools numpy"
    
    if target_old in content:
        content = content.replace(target_old, target_new)
        workflow_path.write_text(content, encoding="utf-8")
        print(f"Successfully replaced '{target_old}' with '{target_new}'")
    elif target_new in content:
        print(f"Workflow already contains '{target_new}'")
    else:
        print(f"Error: Could not find '{target_old}' in {workflow_path}")
        sys.exit(1)

    print("\n=== 3. Staging and Committing ===")
    subprocess.run(["git", "add", str(workflow_path)], cwd=repo_root, check=True)
    
    diff_res = subprocess.run(["git", "diff", "--staged"], cwd=repo_root, capture_output=True, text=True)
    print("Staged diff:")
    print(diff_res.stdout)
    
    commit_msg = "ci: add fonttools and numpy dependencies to deploy-pages workflow"
    # Check if there is anything to commit
    status_res = subprocess.run(["git", "status", "--porcelain", str(workflow_path)], cwd=repo_root, capture_output=True, text=True)
    if status_res.stdout.strip():
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_root, check=True)
        print("Committed successfully.")
    else:
        print("No changes to commit (already committed?).")

    print("\n=== 4. Pushing to origin main ===")
    subprocess.run(["git", "push", "origin", "main"], cwd=repo_root, check=True)
    print("Pushed successfully.")

    print("\n=== 5. Checking GitHub Actions status ===")
    gh_res = subprocess.run(["gh", "run", "list", "--limit", "3"], cwd=repo_root, capture_output=True, text=True)
    print("GitHub Actions runs:")
    print(gh_res.stdout)
    if gh_res.stderr:
        print("Stderr:", gh_res.stderr)

if __name__ == "__main__":
    main()

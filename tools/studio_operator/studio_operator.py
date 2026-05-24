from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import REQUIRED_FILES, built_place_path, ensure_logs_dir, find_studio_exe, find_windows, get_rojo_command, plugin_path, run_command
from git_manager import (
    commit,
    create_branch,
    ensure_git_repo,
    ensure_gitignore,
    get_current_branch,
    get_head_commit,
    has_changes,
    show_summary,
    stage_safe_files,
)
from github_manager import check_auth, check_gh, check_remote, create_pr, push_branch
from operator_state import add_report, load_state, save_state, update_status
from studio_flow import run_flow


def run_git_pr_workflow() -> dict[str, str | bool | list[str]]:
    state = load_state()
    report: dict[str, str | bool | list[str]] = {
        "git_repo_initialized": False,
        "branch_name": "operator/studio-automation-v4",
        "commit_hash": "",
        "remote_origin": False,
        "pr_created": False,
        "manual_next_steps": [],
    }

    report["git_repo_initialized"] = ensure_git_repo()
    report["gitignore_present"] = ensure_gitignore()

    create_branch(report["branch_name"])  # type: ignore[arg-type]
    ok_stage, staged_paths = stage_safe_files()
    report["staged_paths"] = staged_paths

    if ok_stage and has_changes():
        ok_commit, commit_output = commit("Add Studio Operator v4 automation")
        report["commit_output"] = commit_output
        if ok_commit:
            report["commit_hash"] = get_head_commit()
    else:
        report["commit_output"] = "No safe changes to commit."

    gh_ok, gh_output = check_gh()
    auth_ok, auth_output = check_auth() if gh_ok else (False, "gh not installed")
    remote_ok, remote_output = check_remote()
    report["gh_available"] = gh_ok
    report["gh_auth_ok"] = auth_ok
    report["remote_origin"] = remote_ok
    report["gh_auth_output"] = auth_output
    report["remote_output"] = remote_output

    if report["commit_hash"] and gh_ok and auth_ok and remote_ok and not has_changes():
        push_ok, push_output = push_branch(report["branch_name"])  # type: ignore[arg-type]
        report["push_output"] = push_output
        if push_ok:
            pr_ok, pr_output = create_pr(
                "Add Studio Operator v4 automation",
                "This PR adds safe stateful Roblox Studio automation, cleanup, and git/GitHub workflows.",
                "main",
            )
            report["pr_created"] = pr_ok
            report["pr_output"] = pr_output
    else:
        next_steps: list[str] = []
        if not gh_ok:
            next_steps.append("Install GitHub CLI or ensure `gh` is in PATH.")
        if gh_ok and not auth_ok:
            next_steps.append("Run `gh auth login`.")
        if not remote_ok:
            next_steps.append("Add `origin` manually with `git remote add origin <repo-url>`.")
        if has_changes():
            next_steps.append("Working tree is not clean after commit workflow.")
        report["manual_next_steps"] = next_steps

    update_status(state, "GIT_PR_WORKFLOW_COMPLETED")
    save_state(state)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Studio Operator entrypoint")
    parser.add_argument("--click-mode", choices=("off", "cautious"), default="off")
    parser.add_argument("--action", choices=("report", "git-pr"), default="report")
    args = parser.parse_args()

    if args.action == "git-pr":
        result = run_git_pr_workflow()
        print(f"git_repo_initialized={result['git_repo_initialized']}")
        print(f"branch_name={result['branch_name']}")
        print(f"commit_hash={result['commit_hash']}")
        print(f"remote_origin={result['remote_origin']}")
        print(f"pr_created={result['pr_created']}")
        if result.get("manual_next_steps"):
            for step in result["manual_next_steps"]:  # type: ignore[index]
                print(f"next_step={step}")
        return 0

    result = run_flow("status", args.click_mode)
    print(f"Flow report written to: {result['report_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

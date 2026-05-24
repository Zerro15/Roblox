from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]

if str(SCRIPT_DIR) not in sys.path:
	sys.path.insert(0, str(SCRIPT_DIR))

from common import built_place_path, run_command


def gh_json(arguments: list[str]) -> tuple[bool, Any, str]:
	ok, output = run_command(["gh", *arguments], cwd=PROJECT_ROOT)
	if not ok:
		return False, None, output

	try:
		return True, json.loads(output or "null"), output
	except json.JSONDecodeError as exc:
		return False, None, f"Failed to parse JSON output: {exc}"


def git_status_short() -> str:
	ok, output = run_command(["git", "status", "--short"], cwd=PROJECT_ROOT)
	return output if ok else output


def current_branch() -> str:
	ok, output = run_command(["git", "branch", "--show-current"], cwd=PROJECT_ROOT)
	return output.strip() if ok else ""


def remote_url() -> str:
	ok, output = run_command(["git", "remote", "get-url", "origin"], cwd=PROJECT_ROOT)
	return output.strip() if ok else ""


def gh_auth_ok() -> tuple[bool, str]:
	return run_command(["gh", "auth", "status"], cwd=PROJECT_ROOT)


def list_open_prs() -> tuple[bool, list[dict[str, Any]], str]:
	ok, data, output = gh_json(
		[
			"pr",
			"list",
			"--state",
			"open",
			"--json",
			"number,title,headRefName,baseRefName,isDraft,mergeable,url",
		]
	)
	return ok, data or [], output


def get_pr_info(pr_number: int) -> tuple[bool, dict[str, Any] | None, str]:
	return gh_json(
		[
			"pr",
			"view",
			str(pr_number),
			"--json",
			"number,title,headRefName,baseRefName,isDraft,mergeable,mergeStateStatus,url,isCrossRepository",
		]
	)


def print_pr_list(prs: list[dict[str, Any]]) -> None:
	if not prs:
		print("Open PRs: none")
		return

	print("Open PRs:")
	for pr in prs:
		print(
			f"- #{pr['number']} {pr['title']} | head={pr['headRefName']} | "
			f"base={pr['baseRefName']} | draft={pr['isDraft']} | mergeable={pr['mergeable']} | {pr['url']}"
		)


def ensure_clean_worktree() -> tuple[bool, str]:
	status = git_status_short()
	if status.strip():
		return False, status
	return True, ""


def run_build_check() -> tuple[bool, str]:
	ok, output = run_command(
		[
			"powershell",
			"-NoProfile",
			"-ExecutionPolicy",
			"Bypass",
			"-File",
			str(PROJECT_ROOT / "scripts" / "build_place.ps1"),
		],
		cwd=PROJECT_ROOT,
	)
	if not ok:
		return False, output

	place_path = built_place_path()
	if not place_path.exists():
		return False, f"Build finished but output was not found: {place_path}"

	return True, output


def check_gh_checks(pr_number: int) -> tuple[bool, str]:
	ok, output = run_command(["gh", "pr", "checks", str(pr_number)], cwd=PROJECT_ROOT)
	lowered = output.lower()
	if ok:
		return True, output
	if "no checks reported" in lowered or "no checks" in lowered:
		return True, output
	return False, output


def run_check(pr_number: int) -> tuple[bool, dict[str, Any]]:
	report: dict[str, Any] = {"pr_number": pr_number}

	auth_ok, auth_output = gh_auth_ok()
	report["gh_auth_output"] = auth_output
	if not auth_ok:
		report["error"] = "gh auth status failed."
		return False, report

	clean, status_output = ensure_clean_worktree()
	report["git_status"] = status_output
	if not clean:
		report["error"] = "Working tree is dirty."
		return False, report

	ok, pr_info, pr_output = get_pr_info(pr_number)
	report["pr_output"] = pr_output
	report["pr_info"] = pr_info
	if not ok or not pr_info:
		report["error"] = "Unable to read PR details."
		return False, report

	if pr_info.get("baseRefName") != "main":
		report["error"] = "PR base is not main."
		return False, report

	if pr_info.get("isDraft"):
		report["error"] = "PR is still a draft."
		return False, report

	if pr_info.get("isCrossRepository"):
		report["error"] = "PR is cross-repository."
		return False, report

	if pr_info.get("mergeable") == "CONFLICTING":
		report["error"] = "PR has merge conflicts."
		return False, report

	build_ok, build_output = run_build_check()
	report["build_output"] = build_output
	report["build_path"] = str(built_place_path())
	if not build_ok:
		report["error"] = "Build check failed."
		return False, report

	clean_after_build, status_after_build = ensure_clean_worktree()
	report["git_status_after_build"] = status_after_build
	if not clean_after_build:
		report["error"] = "Working tree became dirty after build."
		return False, report

	checks_ok, checks_output = check_gh_checks(pr_number)
	report["checks_output"] = checks_output
	if not checks_ok:
		report["error"] = "GitHub checks are failing."
		return False, report

	report["result"] = "ok"
	return True, report


def print_check_report(success: bool, report: dict[str, Any]) -> None:
	pr_info = report.get("pr_info") or {}
	if pr_info:
		print(
			f"PR #{pr_info.get('number')} {pr_info.get('title')} | "
			f"head={pr_info.get('headRefName')} | base={pr_info.get('baseRefName')} | "
			f"draft={pr_info.get('isDraft')} | mergeable={pr_info.get('mergeable')} | "
			f"mergeStateStatus={pr_info.get('mergeStateStatus')} | {pr_info.get('url')}"
		)

	print(f"Build path: {report.get('build_path', built_place_path())}")
	if report.get("checks_output"):
		print("GitHub checks:")
		print(report["checks_output"])

	if success:
		print("Check result: OK")
	else:
		print(f"Check result: FAILED - {report.get('error', 'Unknown error')}")
		if report.get("git_status"):
			print("Git status:")
			print(report["git_status"])


def merge_pr(pr_number: int) -> int:
	success, report = run_check(pr_number)
	print_check_report(success, report)
	if not success:
		return 1

	ok, output = run_command(
		["gh", "pr", "merge", str(pr_number), "--squash", "--delete-branch"],
		cwd=PROJECT_ROOT,
	)
	if not ok:
		print(output)
		return 1

	print(output)

	ok_checkout, checkout_output = run_command(["git", "checkout", "main"], cwd=PROJECT_ROOT)
	if not ok_checkout:
		print(checkout_output)
		return 1

	ok_pull, pull_output = run_command(["git", "pull", "origin", "main"], cwd=PROJECT_ROOT)
	print(checkout_output)
	print(pull_output)
	return 0 if ok_pull else 1


def merge_latest() -> int:
	ok, prs, output = list_open_prs()
	if not ok:
		print(output)
		return 1

	if not prs:
		print("No open PRs found.")
		return 1

	if len(prs) > 1:
		print("Multiple open PRs found. Choose a PR number explicitly:")
		print_pr_list(prs)
		return 1

	return merge_pr(int(prs[0]["number"]))


def status_mode() -> int:
	print(f"Current branch: {current_branch()}")
	status = git_status_short()
	print("Git status:")
	print(status if status else "clean")

	print(f"Remote origin: {remote_url() or 'missing'}")

	auth_ok, auth_output = gh_auth_ok()
	print("gh auth status:")
	print(auth_output)
	if not auth_ok:
		return 1

	ok, prs, output = list_open_prs()
	if not ok:
		print(output)
		return 1

	print_pr_list(prs)
	return 0


def main() -> int:
	parser = argparse.ArgumentParser(description="Safe PR merge manager")
	parser.add_argument("--mode", choices=("status", "check", "merge", "merge-latest"), required=True)
	parser.add_argument("--pr", type=int)
	args = parser.parse_args()

	if args.mode == "status":
		return status_mode()
	if args.mode == "merge-latest":
		return merge_latest()

	if args.pr is None:
		print("--pr is required for check and merge modes.")
		return 1

	if args.mode == "check":
		success, report = run_check(args.pr)
		print_check_report(success, report)
		return 0 if success else 1

	if args.mode == "merge":
		return merge_pr(args.pr)

	return 1


if __name__ == "__main__":
	raise SystemExit(main())

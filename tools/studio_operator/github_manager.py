from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _run(command: list[str]) -> tuple[bool, str]:
    import subprocess

    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part).strip()
    return completed.returncode == 0, output


def check_gh() -> tuple[bool, str]:
    return _run(["gh", "--version"])


def check_auth() -> tuple[bool, str]:
    return _run(["gh", "auth", "status"])


def check_remote() -> tuple[bool, str]:
    ok, output = _run(["git", "remote", "get-url", "origin"])
    return ok, output


def create_remote_if_requested() -> tuple[bool, str]:
    return False, "Remote creation is intentionally manual."


def push_branch(branch: str) -> tuple[bool, str]:
    return _run(["git", "push", "-u", "origin", branch])


def create_pr(title: str, body: str, base: str) -> tuple[bool, str]:
    return _run(["gh", "pr", "create", "--title", title, "--body", body, "--base", base])

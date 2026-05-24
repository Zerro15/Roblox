from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _run_git(args: list[str]) -> tuple[bool, str]:
    import subprocess

    completed = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part).strip()
    return completed.returncode == 0, output


def ensure_git_repo() -> bool:
    if (PROJECT_ROOT / ".git").exists():
        return True
    ok, _ = _run_git(["init", "."])
    return ok and (PROJECT_ROOT / ".git").exists()


def ensure_gitignore() -> bool:
    return (PROJECT_ROOT / ".gitignore").exists()


def git_status() -> str:
    _, output = _run_git(["status", "--short"])
    return output


def has_changes() -> bool:
    return bool(git_status().strip())


def get_current_branch() -> str:
    ok, output = _run_git(["branch", "--show-current"])
    return output if ok and output else "master"


def create_branch(branch_name: str) -> tuple[bool, str]:
    current = get_current_branch()
    if current == branch_name:
        return True, current
    ok, output = _run_git(["checkout", "-B", branch_name])
    return ok, output


def _ensure_local_identity() -> None:
    ok_name, name = _run_git(["config", "--local", "user.name"])
    ok_email, email = _run_git(["config", "--local", "user.email"])
    if not ok_name or not name:
        _run_git(["config", "--local", "user.name", "Bogdan Mashenin"])
    if not ok_email or not email:
        _run_git(["config", "--local", "user.email", "bogdan2008mashenin@gmail.com"])


def stage_safe_files() -> tuple[bool, list[str]]:
    _ensure_local_identity()
    ok, output = _run_git(["status", "--porcelain"])
    if not ok:
        return False, []

    paths: list[str] = []
    for line in output.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        normalized = path.replace("\\", "/")
        if normalized.startswith(".venv") or normalized.startswith("build/") or normalized.startswith("logs/screenshots/"):
            continue
        if normalized.startswith("logs/") and normalized != "logs/.gitkeep":
            continue
        if normalized.endswith(".rbxlx") or normalized.endswith(".rbxl"):
            continue
        if normalized.startswith(".env") or "/.env" in normalized:
            continue
        paths.append(path)

    if not paths:
        return True, []

    _run_git(["add", "--"] + paths)
    return True, paths


def commit(message: str) -> tuple[bool, str]:
    if not has_changes():
        return False, "No changes to commit."
    ok, output = _run_git(["commit", "-m", message])
    return ok, output


def show_summary() -> str:
    _, output = _run_git(["status", "--short"])
    return output


def get_head_commit() -> str:
    ok, output = _run_git(["rev-parse", "HEAD"])
    return output if ok else ""

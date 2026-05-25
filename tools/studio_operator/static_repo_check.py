from __future__ import annotations

import fnmatch
import os
import py_compile
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
TOOLS_DIR = PROJECT_ROOT / "tools" / "studio_operator"

REQUIRED_FILES = [
    PROJECT_ROOT / "scripts" / "pipeline_smoke_test.ps1",
    PROJECT_ROOT / "scripts" / "demo_evidence_report.ps1",
    TOOLS_DIR / "pipeline_smoke_test.py",
    TOOLS_DIR / "demo_evidence_report.py",
    TOOLS_DIR / "demo_test_player.py",
    TOOLS_DIR / "demo_autofix_loop.py",
    TOOLS_DIR / "roblox_logs.py",
    TOOLS_DIR / "inspect_place_structure.py",
]

FORBIDDEN_TRACKED_RULES = [
    ("logs/**", {"logs/.gitkeep"}),
    ("logs/recordings/**", set()),
    ("logs/screenshots/**", set()),
    ("build/*.rbxlx", set()),
    ("*.mp4", set()),
    ("*.avi", set()),
    ("*.mov", set()),
    ("*.mkv", set()),
    ("agentrouter-*.csv", set()),
    ("claude-agentrouter-*.csv", set()),
    (".env", set()),
    (".venv/**", set()),
]


def compile_python_files() -> None:
    python_files = sorted(TOOLS_DIR.glob("*.py"))
    if not python_files:
        raise RuntimeError(f"No Python files found in {TOOLS_DIR}")

    for path in python_files:
        py_compile.compile(str(path), doraise=True)


def check_required_files() -> None:
    missing = [str(path.relative_to(PROJECT_ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise RuntimeError("Missing required files:\n- " + "\n- ".join(missing))


def tracked_files() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git ls-files failed")

    return [line.strip().replace("\\", "/") for line in completed.stdout.splitlines() if line.strip()]


def is_forbidden(path: str) -> bool:
    for pattern, allowed in FORBIDDEN_TRACKED_RULES:
        if path in allowed:
            continue

        if fnmatch.fnmatch(path, pattern):
            return True

        # `fnmatch` does not treat `logs/**` as matching `logs/foo` on every platform,
        # so keep a simple prefix fallback for directory-shaped patterns.
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            if path.startswith(prefix) and path not in allowed:
                return True

    return False


def check_forbidden_tracked_files() -> None:
    forbidden = sorted(path for path in tracked_files() if is_forbidden(path))
    if forbidden:
        raise RuntimeError("Forbidden tracked artifacts found:\n- " + "\n- ".join(forbidden))


def main() -> int:
    os.chdir(PROJECT_ROOT)

    compile_python_files()
    check_required_files()
    check_forbidden_tracked_files()

    print("Static repository checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

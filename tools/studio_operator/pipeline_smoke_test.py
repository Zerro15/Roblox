"""Pipeline smoke test: validates demo/runtime pipeline infrastructure.

Checks build tools, required files, existing logs/reports/videos,
and produces logs/pipeline_smoke_report.md with pass/fail per check.

Does NOT launch Roblox Studio. Does NOT fake results.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"
BUILD_DIR = PROJECT_ROOT / "build"
RECORDINGS_DIR = LOGS_DIR / "recordings"
REPORT_PATH = LOGS_DIR / "pipeline_smoke_report.md"


def _run(command: list[str], timeout: int = 30) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        output = (result.stdout.strip() + "\n" + result.stderr.strip()).strip()
        return result.returncode == 0, output
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)


def _git_info() -> dict[str, str]:
    info: dict[str, str] = {}
    ok, branch = _run(["git", "branch", "--show-current"])
    info["branch"] = branch.strip() if ok else "unknown"
    ok, sha = _run(["git", "rev-parse", "--short", "HEAD"])
    info["commit"] = sha.strip() if ok else "unknown"
    ok, msg = _run(["git", "log", "-1", "--format=%s"])
    info["message"] = msg.strip() if ok else "unknown"
    return info


class Check:
    def __init__(self, name: str, passed: bool, detail: str = ""):
        self.name = name
        self.passed = passed
        self.detail = detail


def check_required_files() -> list[Check]:
    required = [
        "default.project.json",
        "src/server/Main.server.lua",
        "src/client/Main.client.lua",
        "src/server/services/DemoDiagnosticsService.lua",
        "src/server/services/RuntimeService.lua",
        "src/server/services/MapService.lua",
        "src/server/services/WaveService.lua",
        "src/server/services/PlayerSpawnService.lua",
        "src/server/BridgeClient.server.lua",
        "scripts/build_place.ps1",
        "scripts/run_demo_assisted_auto_play_30s.ps1",
        "scripts/demo_autofix_loop.ps1",
        "tools/studio_operator/demo_test_player.py",
        "tools/studio_operator/demo_autofix_loop.py",
        "tools/studio_operator/roblox_logs.py",
    ]
    checks: list[Check] = []
    for rel in required:
        p = PROJECT_ROOT / rel.replace("/", "\\")
        checks.append(Check(f"file:{rel}", p.exists(), str(p)))
    return checks


def check_rojo() -> Check:
    ok, out = _run(["rojo", "--version"])
    if ok:
        return Check("rojo_available", True, out.split("\n")[0])
    # fallback
    import os
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Rojo" / "rojo.exe"
    if local.exists():
        return Check("rojo_available", True, str(local))
    return Check("rojo_available", False, "rojo not found in PATH or LOCALAPPDATA")


def check_build() -> Check:
    ok, out = _run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ".\\scripts\\build_place.ps1"],
        timeout=60,
    )
    place = BUILD_DIR / "game.rbxlx"
    if ok and place.exists():
        size_mb = place.stat().st_size / (1024 * 1024)
        return Check("rojo_build", True, f"{place} ({size_mb:.2f} MB)")
    return Check("rojo_build", False, out[-500:])


def check_venv() -> Check:
    venv = PROJECT_ROOT / ".venv_studio_operator"
    if venv.exists():
        py = venv / "Scripts" / "python.exe"
        return Check("venv_exists", py.exists(), str(py) if py.exists() else "python.exe missing inside venv")
    return Check("venv_exists", False, "No .venv_studio_operator directory")


def check_demo_report() -> Check:
    report = LOGS_DIR / "demo_test_report.md"
    if report.exists():
        mtime = datetime.fromtimestamp(report.stat().st_mtime).isoformat()
        return Check("demo_report_exists", True, f"modified {mtime}")
    return Check("demo_report_exists", False, "logs/demo_test_report.md not found")


def check_marker_report() -> Check:
    report = LOGS_DIR / "roblox_latest_markers.md"
    meta = LOGS_DIR / "roblox_latest_markers.json"
    if not report.exists():
        return Check("marker_report", False, "logs/roblox_latest_markers.md not found")
    project_count = 0
    if meta.exists():
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
            project_count = int(data.get("project_markers_count", 0))
        except (OSError, ValueError):
            pass
    return Check("marker_report", True, f"project_markers_count={project_count}")


def check_recordings() -> Check:
    if not RECORDINGS_DIR.exists():
        return Check("recordings", False, "logs/recordings/ not found")
    mp4s = sorted(RECORDINGS_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not mp4s:
        return Check("recordings", False, "No .mp4 files in logs/recordings/")
    latest = mp4s[0]
    size_mb = latest.stat().st_size / (1024 * 1024)
    mtime = datetime.fromtimestamp(latest.stat().st_mtime).isoformat()
    return Check("recordings", True, f"{latest.name} ({size_mb:.2f} MB, {mtime})")


def check_server_markers_in_logs() -> Check:
    """Check whether server-side markers are present in any Roblox log."""
    roblox_logs_dir = Path.home() / "AppData" / "Local" / "Roblox" / "logs"
    if not roblox_logs_dir.exists():
        return Check("server_markers", False, "Roblox logs dir not found")

    server_markers = ["[Server boot]", "[DemoDiagnostics]", "[WaveService]", "[RuntimeService]"]
    all_logs = sorted(roblox_logs_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)[:12]
    found: list[str] = []
    for log_file in all_logs:
        try:
            text = log_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for marker in server_markers:
            if marker in text and marker not in found:
                found.append(marker)

    if found:
        return Check("server_markers", True, f"Found in Roblox logs: {', '.join(found)}")
    return Check(
        "server_markers",
        False,
        f"None of {server_markers} found in {len(all_logs)} recent logs. "
        "Server markers are not currently observed in the automated Studio run.",
    )


def generate_report(checks: list[Check], git_info: dict[str, str]) -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().isoformat()
    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    all_pass = passed == total

    lines = [
        "# Pipeline Smoke Test Report",
        "",
        f"- timestamp: `{now}`",
        f"- branch: `{git_info['branch']}`",
        f"- commit: `{git_info['commit']}`",
        f"- commit_message: `{git_info['message']}`",
        f"- result: `{'PASS' if all_pass else 'FAIL'}`",
        f"- checks_passed: `{passed}/{total}`",
        "",
        "## Checks",
        "",
    ]

    for check in checks:
        icon = "✅" if check.passed else "❌"
        lines.append(f"- {icon} **{check.name}**: `{'PASS' if check.passed else 'FAIL'}` — {check.detail}")

    lines.extend([
        "",
        "## Commands Run",
        "- `rojo --version`",
        "- `powershell -ExecutionPolicy Bypass -File .\\scripts\\build_place.ps1`",
        "- `git branch --show-current && git rev-parse --short HEAD`",
        "",
        "## Manual Steps Still Required",
        "",
        "The following steps cannot be automated from terminal and require Roblox Studio:",
        "",
        "1. **Open Studio**: `build/game.rbxlx` must be opened in Roblox Studio",
        "2. **Press F5**: Enter Play mode (automated via `run_demo_assisted_auto_play_30s.ps1`",
        "   but requires Studio window to be foreground)",
        "3. **Verify Output logs**: Check Studio Output panel for `[Server boot]`,",
        "   `[DemoDiagnostics]`, `[WaveService]`, `[EnemyService]`, `[TowerService]`",
        "",
        "### Recommended Full Demo Command",
        "",
        "```powershell",
        "powershell -ExecutionPolicy Bypass -File .\\scripts\\demo_autofix_loop.ps1",
        "```",
        "",
        "This builds, opens Studio, presses F5, records video, collects logs,",
        "and writes `logs/demo_autofix_report.md`.",
        "",
        "## Artifact Paths",
        f"- Pipeline smoke report: `{REPORT_PATH}`",
        f"- Demo test report: `{LOGS_DIR / 'demo_test_report.md'}`",
        f"- Demo autofix report: `{LOGS_DIR / 'demo_autofix_report.md'}`",
        f"- Marker report: `{LOGS_DIR / 'roblox_latest_markers.md'}`",
        f"- Recordings: `{RECORDINGS_DIR}`",
        f"- Build output: `{BUILD_DIR / 'game.rbxlx'}`",
    ])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT_PATH


def main() -> int:
    git_info = _git_info()

    checks: list[Check] = []
    checks.extend(check_required_files())
    checks.append(check_rojo())
    checks.append(check_build())
    checks.append(check_venv())
    checks.append(check_demo_report())
    checks.append(check_marker_report())
    checks.append(check_recordings())
    checks.append(check_server_markers_in_logs())

    report_path = generate_report(checks, git_info)

    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    all_pass = passed == total

    print(f"Pipeline Smoke Test: {'PASS' if all_pass else 'FAIL'} ({passed}/{total})")
    print(f"Branch: {git_info['branch']} @ {git_info['commit']}")
    print(f"Report: {report_path}")

    for check in checks:
        icon = "PASS" if check.passed else "FAIL"
        print(f"  [{icon}] {check.name}: {check.detail}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

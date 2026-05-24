from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pyautogui

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"
BUILD_DIR = PROJECT_ROOT / "build"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from operator_state import (
    add_report,
    add_screenshot,
    load_state,
    save_state,
    update_status,
)
from process_manager import (
    cleanup_duplicate_own_processes,
    cleanup_own_processes,
    detect_foreign_processes,
    is_process_alive,
    list_relevant_processes,
    start_process_once,
)
from roblox_logs import collect_latest_markers
from screenshot import take_screenshot
from common import REQUIRED_FILES, built_place_path, ensure_logs_dir, find_studio_exe, find_windows, get_rojo_command, plugin_path, run_command
from window_focus import focus_studio_window, get_active_window_title, is_active_studio_window


def _log_file(name: str, kind: str) -> Path:
    return LOGS_DIR / f"{name}.{kind}.log"


def ensure_bridge_once(state: dict[str, Any], report: dict[str, Any]) -> None:
    ok, output = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "try { Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:8765/health' | ConvertTo-Json -Compress } catch { exit 1 }",
        ]
    )
    if ok:
        report["bridge_status"] = "ok"
        return

    command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(PROJECT_ROOT / "scripts" / "start_bridge.ps1")]
    pid = start_process_once(
        state,
        "bridge",
        command,
        PROJECT_ROOT,
        stdout_path=_log_file("bridge_runtime", "stdout"),
        stderr_path=_log_file("bridge_runtime", "stderr"),
    )
    time.sleep(3)
    ok, _ = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "try { Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:8765/health' | ConvertTo-Json -Compress } catch { exit 1 }",
        ]
    )
    report["bridge_status"] = "ok" if ok else "not_responding"
    report["bridge_pid"] = pid


def ensure_rojo_once(state: dict[str, Any], report: dict[str, Any]) -> None:
    ok, _ = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "try { (Invoke-WebRequest -Uri 'http://localhost:34872/' -UseBasicParsing -TimeoutSec 5).StatusCode } catch { exit 1 }",
        ]
    )
    if ok:
        report["rojo_status"] = "ok"
        return

    command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(PROJECT_ROOT / "scripts" / "start_rojo.ps1")]
    pid = start_process_once(
        state,
        "rojo",
        command,
        PROJECT_ROOT,
        stdout_path=_log_file("rojo_runtime", "stdout"),
        stderr_path=_log_file("rojo_runtime", "stderr"),
    )
    time.sleep(4)
    ok, _ = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "try { (Invoke-WebRequest -Uri 'http://localhost:34872/' -UseBasicParsing -TimeoutSec 5).StatusCode } catch { exit 1 }",
        ]
    )
    report["rojo_status"] = "ok" if ok else "not_responding"
    report["rojo_pid"] = pid


def build_place(state: dict[str, Any], report: dict[str, Any]) -> bool:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    rojo_command = get_rojo_command()
    if not rojo_command:
        report["build_status"] = "failed"
        update_status(state, "BUILD_FAILED", "Rojo executable not found.")
        return False

    place_path = built_place_path()
    ok, output = run_command(rojo_command + ["build", "default.project.json", "-o", str(place_path)])
    report["build_output"] = output
    report["build_place_path"] = str(place_path)
    report["build_status"] = "ok" if ok and place_path.exists() else "failed"
    state["last_build_path"] = str(place_path) if place_path.exists() else None
    return report["build_status"] == "ok"


def open_built_place_once(state: dict[str, Any], report: dict[str, Any]) -> bool:
    studio_path = find_studio_exe()
    place_path = built_place_path()
    report["roblox_studio_path"] = str(studio_path) if studio_path else "not_found"
    report["build_place_path"] = str(place_path)

    if not studio_path or not place_path.exists():
        report["open_status"] = "failed"
        return False

    if is_process_alive(state.get("studio_pid")):
        report["open_status"] = "already_open"
        return True

    for item in find_windows():
        title = item["title"].lower()
        if "game.rbxlx" in title or ".rbxlx" in title:
            report["open_status"] = "already_open_foreign"
            return True

    command = [str(studio_path), str(place_path)]
    pid = start_process_once(
        state,
        "studio",
        command,
        PROJECT_ROOT,
        stdout_path=_log_file("studio_runtime", "stdout"),
        stderr_path=_log_file("studio_runtime", "stderr"),
    )
    report["studio_pid"] = pid
    report["open_status"] = "started"
    time.sleep(18)
    return True


def capture_and_record(state: dict[str, Any], report: dict[str, Any], label: str) -> None:
    screenshot_path = take_screenshot(LOGS_DIR)
    add_screenshot(state, str(screenshot_path), label)
    report.setdefault("screenshots", []).append({"label": label, "path": str(screenshot_path)})


def detect_ui_blocker(windows: list[dict[str, Any]]) -> str | None:
    for window in windows:
        title = window["title"].lower()
        if any(keyword in title for keyword in ("login", "2fa", "captcha", "verify", "sign in")):
            return window["title"]
    return None


def safe_focus(report: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    report["found_windows"] = find_windows()
    blocker = detect_ui_blocker(report["found_windows"])
    if blocker:
        report["manual_action_needed"] = f"Auth-related window detected: {blocker}"
        state["last_active_window"] = blocker
        return {
            "success": False,
            "before_title": get_active_window_title(),
            "after_title": get_active_window_title(),
            "chosen_title": None,
            "reason": "UI blocker detected.",
        }

    focus_result = focus_studio_window()
    state["last_active_window"] = focus_result.get("after_title")
    return focus_result


def run_assisted_focus(report: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    capture_and_record(state, report, "before_assisted_focus")
    print("Click Roblox Studio window now. Operator will check focus in 5 seconds.")
    time.sleep(5)
    active_title = get_active_window_title()
    success = is_active_studio_window()
    state["last_active_window"] = active_title
    return {
        "success": success,
        "before_title": active_title,
        "after_title": active_title,
        "chosen_title": active_title if success else None,
        "reason": None if success else "Foreground window could not be confirmed after assisted focus wait.",
    }


def perform_play_sequence(state: dict[str, Any], report: dict[str, Any], click_mode: str, focus_mode: str) -> None:
    report["focus_mode"] = focus_mode

    if focus_mode == "assisted":
        focus_result = run_assisted_focus(report, state)
        report["active_window_before_focus"] = focus_result["before_title"]
        report["active_window_after_focus"] = focus_result["after_title"]
        report["focus_chosen_title"] = focus_result["chosen_title"]
    else:
        capture_and_record(state, report, "before_focus")
        focus_result = safe_focus(report, state)
        report["active_window_before_focus"] = focus_result["before_title"]
        report["active_window_after_focus"] = focus_result["after_title"]
        report["focus_chosen_title"] = focus_result["chosen_title"]
        capture_and_record(state, report, "after_focus")

    if click_mode == "off":
        report["play_status"] = "skipped"
        update_status(state, "PLAY_SKIPPED")
        return

    if not focus_result["success"] and focus_mode == "auto":
        ok, output = run_command(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(PROJECT_ROOT / "scripts" / "focus_studio.ps1"),
            ]
        )
        report["focus_fallback_status"] = "ok" if ok else "failed"
        report["focus_fallback_output"] = output
        report["active_window_after_fallback"] = get_active_window_title()

    capture_and_record(state, report, "before_play")
    print("[warning] cautious-mode will press F5 only if Roblox Studio focus is confirmed.")
    time.sleep(3)

    report["active_window_before_f5"] = get_active_window_title()
    if not is_active_studio_window():
        if focus_mode == "assisted":
            report["play_status"] = "PLAY_BLOCKED_ASSISTED_FOCUS_NOT_CONFIRMED"
            update_status(state, "PLAY_BLOCKED_ASSISTED_FOCUS_NOT_CONFIRMED")
            report["manual_action_needed"] = "Play blocked because assisted focus was not confirmed."
        else:
            report["play_status"] = "PLAY_BLOCKED_FOCUS_NOT_CONFIRMED"
            update_status(state, "PLAY_BLOCKED_FOCUS_NOT_CONFIRMED")
            report["manual_action_needed"] = "Play blocked because Studio focus was not confirmed."
        capture_and_record(state, report, "play_blocked")
        return

    pyautogui.press("f5")
    report["play_status"] = "pressed_f5"
    report["f5_pressed"] = True
    capture_and_record(state, report, "after_play")
    time.sleep(20)


def build_flow_report(state: dict[str, Any], report: dict[str, Any]) -> Path:
    report_path = LOGS_DIR / "studio_flow_report.md"
    lines = [
        "# Studio Flow Report",
        "",
        f"- Launch time: {report['launch_time']}",
        f"- Flow: `{report['flow']}`",
        f"- Click mode: `{report['click_mode']}`",
        f"- Focus mode: `{report.get('focus_mode', 'auto')}`",
        f"- Bridge status: `{report.get('bridge_status', 'unknown')}`",
        f"- Rojo status: `{report.get('rojo_status', 'unknown')}`",
        f"- Roblox Studio path: `{report.get('roblox_studio_path', 'not_found')}`",
        f"- Build place path: `{report.get('build_place_path', 'not_built')}`",
        f"- Build status: `{report.get('build_status', 'not_run')}`",
        f"- Open status: `{report.get('open_status', 'not_run')}`",
        f"- Play status: `{report.get('play_status', 'not_run')}`",
        f"- Active window before focus: `{report.get('active_window_before_focus', '')}`",
        f"- Active window after focus: `{report.get('active_window_after_focus', '')}`",
        f"- Active window before F5: `{report.get('active_window_before_f5', '')}`",
        f"- F5 pressed: `{report.get('f5_pressed', False)}`",
        "",
        "## Required Files",
    ]

    for path in REQUIRED_FILES:
        lines.append(f"- `{path.relative_to(PROJECT_ROOT)} : {'OK' if path.exists() else 'MISSING'}`")

    lines.extend(["", "## Process State"])
    lines.append(f"- `bridge_pid = {state.get('bridge_pid')}`")
    lines.append(f"- `rojo_pid = {state.get('rojo_pid')}`")
    lines.append(f"- `studio_pid = {state.get('studio_pid')}`")
    lines.append(f"- `last_flow_status = {state.get('last_flow_status')}`")
    lines.append(f"- `last_active_window = {state.get('last_active_window')}`")

    lines.extend(["", "## Windows"])
    windows = report.get("found_windows", [])
    if windows:
        for window in windows:
            lines.append(f"- `{window['title']}` at ({window['left']}, {window['top']}) size {window['width']}x{window['height']}")
    else:
        lines.append("- No matching Roblox-related windows found.")

    lines.extend(["", "## Processes"])
    for proc in report.get("relevant_processes", []):
        lines.append(f"- `pid={proc['pid']}` `{proc['name']}` `{proc['cmdline']}`")
    if report.get("foreign_processes"):
        lines.append("")
        lines.append("## Foreign Processes")
        for proc in report["foreign_processes"]:
            lines.append(f"- `pid={proc['pid']}` `{proc['name']}` `{proc['cmdline']}`")

    lines.extend(["", "## Screenshots"])
    for screenshot in report.get("screenshots", []):
        lines.append(f"- `{screenshot['label']}` -> `{screenshot['path']}`")
    if not report.get("screenshots"):
        lines.append("- No screenshots captured.")

    lines.extend(["", "## Roblox Logs"])
    if report.get("marker_report_path"):
        lines.append(f"- Marker report: `{report['marker_report_path']}`")
        lines.append(f"- Matched markers: `{', '.join(report.get('matched_markers', []))}`")
        lines.append(f"- Play confirmation status: `{report.get('play_confirmation_status', 'not_checked')}`")

    lines.extend(["", "## Manual Action"])
    lines.append(f"- {report.get('manual_action_needed', 'No manual action recorded.')}")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    add_report(state, str(report_path), "studio_flow_report")
    return report_path


def run_flow(flow: str, click_mode: str, focus_mode: str = "auto") -> dict[str, Any]:
    ensure_logs_dir()
    state = load_state()
    report: dict[str, Any] = {
        "launch_time": datetime.now().isoformat(),
        "flow": flow,
        "click_mode": click_mode,
        "focus_mode": focus_mode,
        "screenshots": [],
        "manual_action_needed": (
            "If Studio shows login, 2FA, captcha, publishing prompts, Allow HTTP Requests, or Rojo live-connect prompts, handle that manually."
        ),
        "rojo_plugin_exists": plugin_path().exists(),
    }

    cleanup_result: list[int] = []
    if flow in ("cleanup", "full-safe", "build-open-play", "build-open", "status"):
        cleanup_result = cleanup_duplicate_own_processes(state)
        report["duplicate_cleanup"] = cleanup_result

    if flow == "cleanup":
        stopped = cleanup_own_processes(state)
        report["stopped_pids"] = stopped
        update_status(state, "CLEANUP_COMPLETED")
    elif flow == "status":
        ensure_bridge_once(state, report)
        ensure_rojo_once(state, report)
        update_status(state, "STATUS_CAPTURED")
    else:
        ensure_bridge_once(state, report)
        ensure_rojo_once(state, report)
        if flow in ("build", "build-open", "build-open-play", "full-safe"):
            build_place(state, report)
        if flow in ("build-open", "build-open-play", "full-safe") and report.get("build_status") == "ok":
            open_built_place_once(state, report)
            if focus_mode == "auto":
                focus_result = safe_focus(report, state)
                report["focus_before_title"] = focus_result["before_title"]
                report["focus_after_title"] = focus_result["after_title"]
            capture_and_record(state, report, "studio_active")
        if flow in ("build-open-play", "full-safe") and report.get("build_status") == "ok":
            perform_play_sequence(state, report, click_mode, focus_mode)

    marker_report, matched_markers = collect_latest_markers(LOGS_DIR, LOGS_DIR / "roblox_latest_markers.md")
    add_report(state, str(marker_report), "roblox_latest_markers")
    report["marker_report_path"] = str(marker_report)
    report["matched_markers"] = matched_markers
    important_markers = [
        "[Server boot]",
        "[RuntimeService]",
        "[EconomyService]",
        "[EnemyService]",
        "[TowerService]",
        "[WaveService]",
        "[Main]",
        "[Client boot]",
        "[Bridge]",
    ]
    report["play_confirmation_status"] = "PLAY_LIKELY_STARTED" if any(marker in matched_markers for marker in important_markers) else "PLAY_NOT_CONFIRMED"
    report["found_windows"] = find_windows()
    report["relevant_processes"] = list_relevant_processes()
    report["foreign_processes"] = detect_foreign_processes(state)
    state["last_active_window"] = get_active_window_title()
    state["last_build_path"] = str(built_place_path()) if built_place_path().exists() else state.get("last_build_path")
    if flow == "full-safe" and report.get("play_status") in ("PLAY_BLOCKED_FOCUS_NOT_CONFIRMED", "PLAY_BLOCKED_ASSISTED_FOCUS_NOT_CONFIRMED"):
        update_status(state, "PLAY_BLOCKED_FOCUS_NOT_CONFIRMED")
    elif flow == "full-safe" and report.get("f5_pressed"):
        update_status(state, report["play_confirmation_status"])
    elif not state.get("last_flow_status"):
        update_status(state, flow.upper())

    report_path = build_flow_report(state, report)
    save_state(state)

    report["report_path"] = str(report_path)
    report["state_path"] = str(LOGS_DIR / "studio_operator_state.json")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Studio Operator v4 flow runner")
    parser.add_argument("--flow", choices=("status", "cleanup", "build", "observe", "build-open", "build-open-play", "full-safe"), required=True)
    parser.add_argument("--click-mode", choices=("off", "cautious"), default="off")
    parser.add_argument("--focus-mode", choices=("auto", "assisted"), default="auto")
    args = parser.parse_args()

    normalized_flow = "status" if args.flow == "observe" else args.flow
    if args.flow == "observe":
        result = run_flow("status", args.click_mode, args.focus_mode)
    else:
        result = run_flow(normalized_flow, args.click_mode, args.focus_mode)

    print(f"Flow report written to: {result['report_path']}")
    print(f"Marker report written to: {result['marker_report_path']}")
    print(f"State file written to: {result['state_path']}")
    print(f"Tip: for video capture use {PROJECT_ROOT / 'tools' / 'studio_operator' / 'demo_test_player.py'}")
    for screenshot in result.get("screenshots", []):
        print(f"Screenshot: {screenshot['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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

from common import REQUIRED_FILES, built_place_path, ensure_logs_dir, find_studio_exe, find_windows, get_rojo_command, run_command
from operator_state import add_report, add_screenshot, load_state, save_state, update_status
from process_manager import is_process_alive, list_relevant_processes, start_process_once
from roblox_logs import collect_latest_markers
from screen_recorder import record_screen
from screenshot import take_screenshot
from window_focus import get_active_window_title, is_active_studio_window


def _log_file(name: str, kind: str) -> Path:
	return LOGS_DIR / f"{name}.{kind}.log"


def capture_and_record(state: dict[str, Any], report: dict[str, Any], label: str) -> str:
	screenshot_path = take_screenshot(LOGS_DIR)
	add_screenshot(state, str(screenshot_path), label)
	report.setdefault("screenshots", []).append({"label": label, "path": str(screenshot_path)})
	return str(screenshot_path)


def build_place(report: dict[str, Any], state: dict[str, Any]) -> bool:
	BUILD_DIR.mkdir(parents=True, exist_ok=True)
	rojo_command = get_rojo_command()
	if not rojo_command:
		report["build_status"] = "failed"
		report["build_error"] = "Rojo executable not found."
		update_status(state, "DEMO_BUILD_FAILED", report["build_error"])
		return False

	place_path = built_place_path()
	ok, output = run_command(rojo_command + ["build", "default.project.json", "-o", str(place_path)])
	report["build_output"] = output
	report["build_path"] = str(place_path)
	report["build_status"] = "ok" if ok and place_path.exists() else "failed"
	state["last_build_path"] = str(place_path) if place_path.exists() else None
	return report["build_status"] == "ok"


def open_built_place(report: dict[str, Any], state: dict[str, Any]) -> bool:
	studio_path = find_studio_exe()
	place_path = built_place_path()
	report["roblox_studio_path"] = str(studio_path) if studio_path else "not_found"
	report["build_path"] = str(place_path)

	if not studio_path or not place_path.exists():
		report["open_status"] = "failed"
		return False

	if is_process_alive(state.get("studio_pid")):
		report["open_status"] = "already_open"
		return True

	for window in find_windows():
		title = window["title"].lower()
		if "game.rbxlx" in title or ".rbxlx" in title:
			report["open_status"] = "already_open_foreign"
			return True

	launch_command = [str(studio_path), str(place_path)]
	pid = start_process_once(
		state,
		"studio",
		launch_command,
		PROJECT_ROOT,
		stdout_path=_log_file("demo_studio_runtime", "stdout"),
		stderr_path=_log_file("demo_studio_runtime", "stderr"),
	)
	report["studio_pid"] = pid
	report["open_status"] = "started"
	time.sleep(18)
	return True


def write_demo_report(report: dict[str, Any], state: dict[str, Any]) -> Path:
	report_path = LOGS_DIR / "demo_test_report.md"
	lines = [
		"# Demo Test Report",
		"",
		f"- started_at: `{report['started_at']}`",
		f"- mode: `{report['mode']}`",
		f"- duration: `{report['duration']}`",
		f"- build path: `{report.get('build_path', 'not_built')}`",
		f"- build status: `{report.get('build_status', 'not_run')}`",
		f"- open status: `{report.get('open_status', 'not_run')}`",
		f"- active window before focus: `{report.get('active_window_before_focus', '')}`",
		f"- active window after focus: `{report.get('active_window_after_focus', '')}`",
		f"- was F5 pressed: `{report.get('f5_pressed', False)}`",
		f"- recording path: `{report.get('recording_path', '')}`",
		f"- result status: `{report.get('result_status', 'unknown')}`",
		f"- play status: `{report.get('play_status', 'unknown')}`",
		f"- video usefulness score: `{report.get('video_score', 0)}/5`",
		"",
		"## Required Files",
	]

	for path in REQUIRED_FILES:
		lines.append(f"- `{path.relative_to(PROJECT_ROOT)} : {'OK' if path.exists() else 'MISSING'}`")

	lines.extend(["", "## Screenshots"])
	for screenshot in report.get("screenshots", []):
		lines.append(f"- `{screenshot['label']}` -> `{screenshot['path']}`")
	if not report.get("screenshots"):
		lines.append("- No screenshots captured.")

	lines.extend(["", "## Recording"])
	if report.get("recording_error"):
		lines.append(f"- error: `{report['recording_error']}`")
	if report.get("recording_path"):
		recording_path = Path(report['recording_path'])
		file_size = recording_path.stat().st_size / (1024 * 1024) if recording_path.exists() else 0
		lines.append(f"- file: `{report['recording_path']}`")
		lines.append(f"- file size: `{file_size:.2f} MB`")
	if report.get("fallback_frames"):
		for frame in report["fallback_frames"]:
			lines.append(f"- fallback frame: `{frame}`")

	lines.extend(["", "## Roblox Logs"])
	lines.append(f"- marker report: `{report.get('marker_report_path', '')}`")
	matched_markers = report.get("matched_markers", [])
	lines.append(f"- matched markers: `{len(matched_markers)}` found")
	if matched_markers:
		for marker in matched_markers[:15]:
			lines.append(f"  - `{marker}`")
		if len(matched_markers) > 15:
			lines.append(f"  - ... and {len(matched_markers) - 15} more")

	lines.extend(["", "## Windows"])
	for window in report.get("windows", []):
		lines.append(f"- `{window['title']}` at ({window['left']}, {window['top']}) size {window['width']}x{window['height']}")
	if not report.get("windows"):
		lines.append("- No Roblox-related windows found.")

	lines.extend(["", "## Processes"])
	for proc in report.get("relevant_processes", []):
		lines.append(f"- `pid={proc['pid']}` `{proc['name']}` `{proc['cmdline']}`")
	if not report.get("relevant_processes"):
		lines.append("- No relevant processes found.")

	lines.extend(["", "## Notes"])
	lines.append(f"- {report.get('note', 'No extra notes.')}")

	lines.extend(["", "## Video Usefulness Score"])
	score = report.get("video_score", 0)
	score_descriptions = {
		0: "No video recorded",
		1: "Video recorded but Studio/game not visible",
		2: "Studio visible but Play not started",
		3: "Play started but gameplay unclear",
		4: "Map/enemies/towers visible",
		5: "Full gameplay loop visible",
	}
	lines.append(f"- Score: `{score}/5` - {score_descriptions.get(score, 'Unknown')}")

	report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
	add_report(state, str(report_path), "demo_test_report")
	return report_path


def collect_markers(report: dict[str, Any], state: dict[str, Any]) -> None:
	marker_report, matched_markers = collect_latest_markers(LOGS_DIR, LOGS_DIR / "roblox_latest_markers.md")
	add_report(state, str(marker_report), "roblox_latest_markers")
	report["marker_report_path"] = str(marker_report)
	report["matched_markers"] = matched_markers


def observe_mode(report: dict[str, Any], state: dict[str, Any]) -> None:
	report["windows"] = find_windows()
	capture_and_record(state, report, "observe")
	report["result_status"] = "OBSERVE_CAPTURED"
	report["note"] = "Observe mode does not press keys."
	update_status(state, "DEMO_OBSERVE_CAPTURED")


def record_only_mode(report: dict[str, Any], state: dict[str, Any], duration: int) -> None:
	recording = record_screen(duration_seconds=duration)
	report["recording_path"] = recording.get("recording_path")
	report["recording_error"] = recording.get("error")
	report["fallback_frames"] = recording.get("fallback_frames", [])
	report["result_status"] = "DEMO_RECORDED" if recording.get("success") else "DEMO_RECORDING_FAILED"
	report["note"] = "Record-only mode does not build or press Play."
	update_status(state, report["result_status"])


def manual_play_record_mode(report: dict[str, Any], state: dict[str, Any], duration: int) -> None:
	if not build_place(report, state):
		report["result_status"] = "DEMO_BUILD_FAILED"
		report["note"] = report.get("build_error", "Build failed.")
		return

	open_built_place(report, state)
	report["windows"] = find_windows()
	capture_and_record(state, report, "before_manual_play")

	print("\n" + "="*60)
	print("Recording is starting now.")
	print("Click Roblox Studio and press Play/F5 manually.")
	print("Do not switch windows during recording.")
	print("="*60 + "\n")

	recording = record_screen(duration_seconds=duration)
	report["recording_path"] = recording.get("recording_path")
	report["recording_error"] = recording.get("error")
	report["fallback_frames"] = recording.get("fallback_frames", [])

	capture_and_record(state, report, "after_recording")

	if recording.get("success"):
		report["result_status"] = "DEMO_RECORDED"
		update_status(state, "DEMO_RECORDED")
	else:
		report["result_status"] = "DEMO_RECORDING_FAILED"
		update_status(state, "DEMO_RECORDING_FAILED", recording.get("error"))


def run_demo_mode(report: dict[str, Any], state: dict[str, Any], duration: int, focus_mode: str) -> None:
	if not build_place(report, state):
		report["result_status"] = "DEMO_RECORDING_FAILED"
		report["note"] = report.get("build_error", "Build failed.")
		return

	open_built_place(report, state)
	report["windows"] = find_windows()
	capture_and_record(state, report, "before_play")
	report["active_window_before_focus"] = get_active_window_title()

	if focus_mode == "assisted":
		print("Click Roblox Studio window now. Demo runner will check focus in 5 seconds.")
		time.sleep(5)

	report["active_window_after_focus"] = get_active_window_title()
	if not is_active_studio_window():
		capture_and_record(state, report, "focus_blocked")
		report["f5_pressed"] = False
		report["result_status"] = "DEMO_BLOCKED_FOCUS_NOT_CONFIRMED"
		report["note"] = "Focus was not confirmed, so F5 was not pressed."
		update_status(state, "DEMO_BLOCKED_FOCUS_NOT_CONFIRMED")
		return

	pyautogui.press("f5")
	report["f5_pressed"] = True
	capture_and_record(state, report, "after_f5")
	recording = record_screen(duration_seconds=duration)
	report["recording_path"] = recording.get("recording_path")
	report["recording_error"] = recording.get("error")
	report["fallback_frames"] = recording.get("fallback_frames", [])

	if recording.get("success"):
		report["result_status"] = "DEMO_RECORDED"
		update_status(state, "DEMO_RECORDED")
	else:
		report["result_status"] = "DEMO_RECORDING_FAILED"
		update_status(state, "DEMO_RECORDING_FAILED", recording.get("error"))




def main() -> int:
	parser = argparse.ArgumentParser(description="Demo Test Player / Video Recorder for Roblox Studio Operator")
	parser.add_argument("--mode", choices=("observe", "record-only", "run-demo", "manual-play-record"), required=True)
	parser.add_argument("--duration", type=int, default=60)
	parser.add_argument("--focus-mode", choices=("assisted",), default="assisted")
	args = parser.parse_args()

	ensure_logs_dir()
	state = load_state()
	report: dict[str, Any] = {
		"started_at": datetime.now().isoformat(),
		"mode": args.mode,
		"duration": max(1, min(args.duration, 90)),
		"screenshots": [],
		"f5_pressed": False,
		"windows": [],
		"relevant_processes": [],
	}

	if args.mode == "observe":
		observe_mode(report, state)
	elif args.mode == "record-only":
		record_only_mode(report, state, report["duration"])
	elif args.mode == "manual-play-record":
		manual_play_record_mode(report, state, report["duration"])
	else:
		run_demo_mode(report, state, report["duration"], args.focus_mode)

	collect_markers(report, state)

	important_markers = [
		"[Server boot]",
		"[RuntimeService]",
		"[MapService]",
		"[PathService]",
		"[WaveService]",
		"[EnemyService]",
		"[TowerService]",
		"[EconomyService]",
	]

	client_markers = [
		"[Client boot]",
		"[Client] Demo camera activated",
	]

	all_gameplay_markers = important_markers + client_markers
	matched = report.get("matched_markers", [])

	if report.get("result_status") == "DEMO_RECORDED":
		if any(marker in matched for marker in important_markers):
			report["play_status"] = "DEMO_RECORDED_PLAY_CONFIRMED"
			report["video_score"] = 4 if any(marker in matched for marker in client_markers) else 3
		else:
			report["play_status"] = "DEMO_RECORDED_PLAY_NOT_CONFIRMED"
			report["video_score"] = 2
	elif report.get("result_status") == "DEMO_RECORDING_FAILED":
		report["play_status"] = "DEMO_RECORDING_FAILED"
		report["video_score"] = 0
	else:
		report["play_status"] = report.get("result_status", "UNKNOWN")
		report["video_score"] = 0

	report["windows"] = find_windows()
	report["relevant_processes"] = list_relevant_processes()
	state["last_active_window"] = get_active_window_title()
	report_path = write_demo_report(report, state)
	save_state(state)

	print(f"Demo report written to: {report_path}")
	if report.get("recording_path"):
		print(f"Recording: {report['recording_path']}")
	for screenshot in report.get("screenshots", []):
		print(f"Screenshot: {screenshot['path']}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

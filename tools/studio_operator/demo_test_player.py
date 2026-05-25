from __future__ import annotations

import argparse
import json
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
from studio_play_controller import force_play as force_studio_play
from window_focus import (
	choose_best_studio_window,
	find_ignored_studio_windows,
	focus_window,
	get_active_window_title,
	is_active_studio_window,
	is_safe_build_game_window_title,
)


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
	state["last_build_mtime"] = place_path.stat().st_mtime if place_path.exists() else None
	return report["build_status"] == "ok"


def open_built_place(report: dict[str, Any], state: dict[str, Any]) -> bool:
	studio_path = find_studio_exe()
	place_path = built_place_path()
	report["roblox_studio_path"] = str(studio_path) if studio_path else "not_found"
	report["build_path"] = str(place_path)

	if not studio_path or not place_path.exists():
		report["open_status"] = "failed"
		return False

	if is_process_alive(state.get("studio_pid")) and state.get("studio_loaded_build_mtime") == state.get("last_build_mtime"):
		report["open_status"] = "already_open"
		return True

	existing_place_windows = []
	for window in find_windows():
		title = window["title"].lower()
		if "game.rbxlx" in title or ".rbxlx" in title:
			existing_place_windows.append(window["title"])

	if existing_place_windows:
		report["existing_place_windows"] = existing_place_windows
		report["open_note"] = "Fresh build opened because existing Studio windows may contain stale in-memory place data."

	launch_command = [str(studio_path), str(place_path)]
	pid = start_process_once(
		state,
		"studio",
		launch_command,
		PROJECT_ROOT,
		stdout_path=_log_file("demo_studio_runtime", "stdout"),
		stderr_path=_log_file("demo_studio_runtime", "stderr"),
		force_new=True,
	)
	report["studio_pid"] = pid
	state["studio_pid"] = pid
	state["studio_loaded_build_mtime"] = state.get("last_build_mtime")
	report["open_status"] = "started"
	time.sleep(18)
	return True


def ensure_studio_window_visible(report: dict[str, Any], state: dict[str, Any]) -> bool:
	best = choose_best_studio_window()
	ignored_windows = find_ignored_studio_windows()
	report["ignored_studio_windows"] = [
		{
			"title": window["title"],
			"x": window["left"],
			"y": window["top"],
			"width": window["width"],
			"height": window["height"],
		}
		for window in ignored_windows
	]

	studio_window_before = None
	if best:
		report["selected_studio_window_title"] = best["title"]
		report["selected_studio_window_rect"] = {
			"x": best["left"],
			"y": best["top"],
			"width": best["width"],
			"height": best["height"],
		}
		studio_window_before = {
			"title": best["title"],
			"x": best["left"],
			"y": best["top"],
			"width": best["width"],
			"height": best["height"],
			"isMinimized": best["isMinimized"],
		}
		report["studio_window_before"] = studio_window_before

		if "installer" in best["title"].lower():
			report["studio_window_visible"] = False
			report["studio_window_preflight_status"] = "STUDIO_INSTALLER_WINDOW_BLOCKED"
			return False

	is_offscreen = False
	if best:
		if best["left"] <= -10000 or best["top"] <= -10000:
			is_offscreen = True
		elif best["width"] < 400 or best["height"] < 300:
			is_offscreen = True
		elif best["isMinimized"]:
			is_offscreen = True

	if is_offscreen and best:
		print("\nStudio window appears minimized or offscreen. Attempting to restore...")
		try:
			focus_window(best["window"])
			time.sleep(2)
		except Exception as exc:
			print(f"Could not restore window: {exc}")

	best_after = choose_best_studio_window()
	studio_window_after = None
	if best_after:
		studio_window_after = {
			"title": best_after["title"],
			"x": best_after["left"],
			"y": best_after["top"],
			"width": best_after["width"],
			"height": best_after["height"],
			"isMinimized": best_after["isMinimized"],
		}
		report["studio_window_after"] = studio_window_after

	is_visible = False
	preflight_status = "STUDIO_WINDOW_NOT_FOUND"

	if best_after:
		if best_after["left"] <= -10000 or best_after["top"] <= -10000:
			preflight_status = "STUDIO_WINDOW_OFFSCREEN"
		elif "installer" in best_after["title"].lower():
			preflight_status = "STUDIO_INSTALLER_WINDOW_BLOCKED"
		elif best_after["width"] < 400 or best_after["height"] < 300:
			preflight_status = "STUDIO_WINDOW_OFFSCREEN"
		elif best_after["isMinimized"]:
			preflight_status = "STUDIO_WINDOW_OFFSCREEN"
		else:
			is_visible = True
			if is_offscreen:
				preflight_status = "STUDIO_WINDOW_RESTORED"
			else:
				preflight_status = "STUDIO_WINDOW_VISIBLE"

	report["studio_window_visible"] = is_visible
	report["studio_window_preflight_status"] = preflight_status

	return is_visible


def is_safe_game_studio_title(title: str) -> bool:
	if is_safe_build_game_window_title(title):
		return True

	lowered = title.lower()
	if "game.rbxlx" not in lowered:
		return False
	if "roblox studio" not in lowered:
		return False

	blocked_tokens = (
		"autorecovery",
		"autosaves",
		"installer",
		"download and install",
		"setup",
		"updater",
		"browser",
		"powershell",
		"claude",
		"codex",
		"яндекс",
	)
	return not any(token in lowered for token in blocked_tokens)


def safe_click_focus_studio_window(report: dict[str, Any]) -> bool:
	report["click_focus_attempted"] = False
	report["click_focus_point"] = ""
	report["click_focus_result"] = False
	report["active_window_after_click_focus"] = get_active_window_title()

	best = choose_best_studio_window()
	if not best:
		report["click_focus_error"] = "No eligible game.rbxlx Roblox Studio window found."
		return False

	title = best["title"]
	report["selected_studio_window_title"] = title
	report["selected_studio_window_rect"] = {
		"x": best["left"],
		"y": best["top"],
		"width": best["width"],
		"height": best["height"],
	}

	if not is_safe_game_studio_title(title):
		report["click_focus_error"] = "Selected window title is not a safe game.rbxlx Roblox Studio window."
		return False

	focus_window(best["window"])
	time.sleep(1)

	x = best["left"] + best["width"] // 2
	y = best["top"] + min(200, best["height"] // 2)
	report["click_focus_attempted"] = True
	report["click_focus_point"] = f"{x},{y}"

	try:
		pyautogui.click(x, y)
	except Exception as exc:  # noqa: BLE001
		report["click_focus_error"] = str(exc)
		report["active_window_after_click_focus"] = get_active_window_title()
		return False

	time.sleep(1)
	report["active_window_after_click_focus"] = get_active_window_title()
	active_title = report["active_window_after_click_focus"].lower()
	report["click_focus_result"] = is_active_studio_window() or "robloxstudio" in active_title or "roblox studio" in active_title
	return report["click_focus_result"]


def wait_for_studio_focus(timeout_seconds: int = 30) -> bool:
	deadline = time.time() + timeout_seconds
	while time.time() < deadline:
		if is_active_studio_window():
			return True
		time.sleep(0.5)
	return False


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
		f"- auto-play enabled: `{report.get('auto_play_enabled', False)}`",
		f"- auto-play mode: `{report.get('auto_play_mode', 'safe')}`",
		f"- auto-play status: `{report.get('auto_play_status', 'AUTO_PLAY_DISABLED')}`",
		f"- selected studio window title: `{report.get('selected_studio_window_title', '')}`",
		f"- selected studio window rect: `{report.get('selected_studio_window_rect', '')}`",
		f"- click focus attempted: `{report.get('click_focus_attempted', False)}`",
		f"- click focus point: `{report.get('click_focus_point', '')}`",
		f"- click focus result: `{report.get('click_focus_result', False)}`",
		f"- active window after click focus: `{report.get('active_window_after_click_focus', '')}`",
		f"- active window before auto-play: `{report.get('active_window_before_auto_play', '')}`",
		f"- active window after auto-play: `{report.get('active_window_after_auto_play', '')}`",
		f"- was F5 pressed: `{report.get('f5_pressed', False)}`",
		f"- recording path: `{report.get('recording_path', '')}`",
		f"- result status: `{report.get('result_status', 'unknown')}`",
		f"- play status: `{report.get('play_status', 'unknown')}`",
		f"- video usefulness score: `{report.get('video_score', 0)}/5`",
		f"- diagnosis: `{report.get('diagnosis', 'UNKNOWN_FAILURE')}`",
		f"- success criteria passed: `{report.get('success_criteria_passed', False)}`",
		f"- checked log files count: `{report.get('checked_log_files_count', 0)}`",
		f"- project markers count: `{report.get('project_markers_count', 0)}`",
		f"- possible next fix: `{report.get('possible_next_fix', '')}`",
		"",
		"## Studio Play Controller",
		f"- selected title: `{report.get('studio_play_controller', {}).get('selected_title', '')}`",
		f"- selected hwnd: `{report.get('studio_play_controller', {}).get('selected_hwnd', 0)}`",
		f"- selected pid: `{report.get('studio_play_controller', {}).get('selected_pid', 0)}`",
		f"- selected process name: `{report.get('studio_play_controller', {}).get('selected_process_name', '')}`",
		f"- selected root hwnd: `{report.get('studio_play_controller', {}).get('selected_root_hwnd', 0)}`",
		f"- selected root title: `{report.get('studio_play_controller', {}).get('selected_root_title', '')}`",
		f"- selected rect: `{report.get('studio_play_controller', {}).get('selected_rect', {})}`",
		f"- foreground before hwnd: `{report.get('studio_play_controller', {}).get('foreground_before', {}).get('hwnd', 0)}`",
		f"- foreground before title: `{report.get('studio_play_controller', {}).get('foreground_before', {}).get('title', '')}`",
		f"- foreground before pid: `{report.get('studio_play_controller', {}).get('foreground_before', {}).get('pid', 0)}`",
		f"- foreground before process name: `{report.get('studio_play_controller', {}).get('foreground_before', {}).get('process_name', '')}`",
		f"- foreground before root hwnd: `{report.get('studio_play_controller', {}).get('foreground_before', {}).get('root_hwnd', 0)}`",
		f"- foreground before root title: `{report.get('studio_play_controller', {}).get('foreground_before', {}).get('root_title', '')}`",
		f"- foreground after hwnd: `{report.get('studio_play_controller', {}).get('foreground_after', {}).get('hwnd', 0)}`",
		f"- foreground after title: `{report.get('studio_play_controller', {}).get('foreground_after', {}).get('title', '')}`",
		f"- foreground after pid: `{report.get('studio_play_controller', {}).get('foreground_after', {}).get('pid', 0)}`",
		f"- foreground after process name: `{report.get('studio_play_controller', {}).get('foreground_after', {}).get('process_name', '')}`",
		f"- foreground after root hwnd: `{report.get('studio_play_controller', {}).get('foreground_after', {}).get('root_hwnd', 0)}`",
		f"- foreground after root title: `{report.get('studio_play_controller', {}).get('foreground_after', {}).get('root_title', '')}`",
		f"- foreground after F5 hwnd: `{report.get('studio_play_controller', {}).get('foreground_after_f5', {}).get('hwnd', 0)}`",
		f"- foreground after F5 title: `{report.get('studio_play_controller', {}).get('foreground_after_f5', {}).get('title', '')}`",
		f"- foreground after F5 pid: `{report.get('studio_play_controller', {}).get('foreground_after_f5', {}).get('pid', 0)}`",
		f"- foreground after F5 process name: `{report.get('studio_play_controller', {}).get('foreground_after_f5', {}).get('process_name', '')}`",
		f"- foreground after F5 root hwnd: `{report.get('studio_play_controller', {}).get('foreground_after_f5', {}).get('root_hwnd', 0)}`",
		f"- foreground after F5 root title: `{report.get('studio_play_controller', {}).get('foreground_after_f5', {}).get('root_title', '')}`",
		f"- foreground confirmed: `{report.get('studio_play_controller', {}).get('foreground_confirmed', False)}`",
		f"- foreground confirmation reason: `{report.get('studio_play_controller', {}).get('foreground_confirmation_reason', 'none')}`",
		f"- foreground confirmation checks: `{report.get('studio_play_controller', {}).get('foreground_confirmation_checks', {})}`",
		f"- f5 method: `{report.get('studio_play_controller', {}).get('f5_method', '')}`",
		f"- f5 methods attempted: `{', '.join(report.get('studio_play_controller', {}).get('f5_methods_attempted', []))}`",
		f"- f5 sent: `{report.get('studio_play_controller', {}).get('f5_pressed', False)}`",
		f"- f5 sent to selected hwnd: `{report.get('studio_play_controller', {}).get('f5_sent_to_selected_hwnd', False)}`",
		f"- play confirmation evidence: `{report.get('play_confirmation_evidence', 'runtime markers required')}`",
		f"- error: `{report.get('studio_play_controller', {}).get('error', '')}`",
		"",
		"## Expected Visual Runtime Beacons",
		"- Blue `ServerBootBeacon` near `Workspace/DemoDiagnostics`",
		"- Green `PlayerSpawnBeacon` near `Workspace/DemoDiagnostics`",
		"- Yellow `MapBuildBeacon` near `Workspace/DemoDiagnostics`",
		"- Red `WaveLoopBeacon` near `Workspace/DemoDiagnostics`",
		"- UI text: `DEMO SPECTATOR CAMERA ACTIVE`",
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
	lines.append(f"- checked log files count: `{report.get('checked_log_files_count', 0)}`")
	lines.append(f"- project markers count: `{report.get('project_markers_count', 0)}`")
	for checked_file in report.get("checked_log_files", []):
		lines.append(f"- checked: `{checked_file}`")
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

	lines.extend(["", "## Studio Window Preflight"])
	studio_before = report.get("studio_window_before")
	studio_after = report.get("studio_window_after")
	studio_visible = report.get("studio_window_visible", False)
	studio_status = report.get("studio_window_preflight_status", "UNKNOWN")

	if studio_before:
		lines.append(f"- before: `{studio_before['title']}` at ({studio_before['x']}, {studio_before['y']}) size {studio_before['width']}x{studio_before['height']}")
		if studio_before['x'] <= -10000 or studio_before['y'] <= -10000:
			lines.append("  - ⚠️ Studio appears minimized or offscreen")
	else:
		lines.append("- before: no window found")

	if studio_after:
		lines.append(f"- after: `{studio_after['title']}` at ({studio_after['x']}, {studio_after['y']}) size {studio_after['width']}x{studio_after['height']}")
		if studio_after['x'] <= -10000 or studio_after['y'] <= -10000:
			lines.append("  - ⚠️ Studio appears minimized or offscreen")
	else:
		lines.append("- after: no window found")

	lines.append(f"- visible: `{studio_visible}`")
	lines.append(f"- status: `{studio_status}`")

	lines.extend(["", "## Ignored Studio Windows"])
	for window in report.get("ignored_studio_windows", []):
		lines.append(f"- `{window['title']}` at ({window['x']}, {window['y']}) size {window['width']}x{window['height']}")
	if not report.get("ignored_studio_windows"):
		lines.append("- No ignored Studio-like windows.")

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
	marker_report, matched_markers = collect_latest_markers(LOGS_DIR, LOGS_DIR / "roblox_latest_markers.md", max_files=20)
	add_report(state, str(marker_report), "roblox_latest_markers")
	report["marker_report_path"] = str(marker_report)
	report["matched_markers"] = matched_markers
	metadata_path = LOGS_DIR / "roblox_latest_markers.json"
	report["checked_log_files_count"] = 0
	report["project_markers_count"] = 0
	report["checked_log_files"] = []
	if metadata_path.exists():
		try:
			metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
			report["checked_log_files_count"] = len(metadata.get("checked_files", []))
			report["project_markers_count"] = int(metadata.get("project_markers_count", 0))
			report["checked_log_files"] = [item.get("path", "") for item in metadata.get("checked_files", [])]
		except (OSError, ValueError, TypeError):
			report["checked_log_files_count"] = 0
			report["project_markers_count"] = 0


def diagnose_demo_report(report: dict[str, Any]) -> str:
	if report.get("build_status") == "failed":
		return "BUILD_FAILED"
	if report.get("studio_window_visible") is False:
		return "STUDIO_WINDOW_NOT_VISIBLE"

	selected_title = str(report.get("selected_studio_window_title", "")).lower()
	if selected_title and ("game.rbxlx" not in selected_title or "roblox studio" not in selected_title):
		return "WRONG_STUDIO_WINDOW"

	if not report.get("f5_pressed", False):
		controller = report.get("studio_play_controller", {})
		if controller and not controller.get("f5_pressed", False):
			return "STUDIO_FOREGROUND_BLOCKED"
		return "F5_NOT_PRESSED"

	if "FOREGROUND_NOT_CONFIRMED" in str(report.get("auto_play_status", "")):
		return "PLAY_NOT_CONFIRMED"

	matched = report.get("matched_markers", [])
	project_markers_count = int(report.get("project_markers_count", 0))
	gameplay_confirmed = any(marker in matched for marker in ("[WaveService]", "[TowerService]", "[EnemyService]"))
	diagnostics_confirmed = any(marker.startswith("[DemoDiagnostics]") for marker in matched)
	client_camera_confirmed = "[Client] Demo spectator camera activated" in matched
	if report.get("f5_pressed") and project_markers_count == 0:
		return "RUNTIME_MARKERS_NOT_CAPTURED"

	if 0 < project_markers_count < 3:
		return "PARTIAL_RUNTIME_CONFIRMED"

	if project_markers_count >= 3 and (not gameplay_confirmed or not diagnostics_confirmed or not client_camera_confirmed):
		return "PARTIAL_RUNTIME_CONFIRMED"

	server_confirmed = "[Server boot]" in matched or "[DemoDiagnostics] ServerBootBeacon marked" in matched
	if project_markers_count >= 3 and gameplay_confirmed and diagnostics_confirmed and client_camera_confirmed and server_confirmed:
		return "OK"

	if "[Server boot]" not in matched and "[DemoDiagnostics] ServerBootBeacon marked" not in matched:
		return "SERVER_BOOT_NOT_FOUND"
	if "[Client boot]" not in matched:
		return "CLIENT_BOOT_NOT_FOUND"
	if "[Client] Demo spectator camera activated" not in matched:
		return "DEMO_CAMERA_NOT_FOUND"
	if "[PlayerSpawnService]" not in matched and "[PlayerSpawnService] Demo spectator mode enabled" not in matched:
		return "PLAYERSPAWN_NOT_FOUND"
	if "[Main] Demo map build requested" not in matched and "[MapService]" not in matched:
		return "MAP_NOT_BUILT"
	if "[WaveService]" not in matched:
		return "WAVE_NOT_STARTED"

	return "OK"


def evaluate_success_criteria(report: dict[str, Any]) -> bool:
	matched = report.get("matched_markers", [])
	required_markers = [
		"[DemoDiagnostics] Init",
		"[DemoDiagnostics] ServerBootBeacon marked",
		"[DemoDiagnostics] PlayerSpawnBeacon marked",
		"[DemoDiagnostics] MapBuildBeacon marked",
		"[DemoDiagnostics] WaveLoopBeacon marked",
		"[Client] Demo spectator camera activated",
	]
	marker_hits = sum(1 for marker in required_markers if marker in matched)
	gameplay_confirmed = any(marker in matched for marker in ("[WaveService]", "[TowerService]", "[EnemyService]"))
	return (
		report.get("build_status") == "ok"
		and bool(report.get("recording_path"))
		and report.get("f5_pressed") is True
		and "F5_PRESSED" in str(report.get("auto_play_status", ""))
		and marker_hits >= 3
		and gameplay_confirmed
		and int(report.get("video_score", 0)) >= 3
	)


def possible_next_fix_for_diagnosis(diagnosis: str) -> str:
	fixes = {
		"BUILD_FAILED": "Inspect Rojo build output; do not run demo until build passes.",
		"STUDIO_WINDOW_NOT_VISIBLE": "Close extra Studio windows and keep build/game.rbxlx visible.",
		"FOCUS_FAILED": "Retry safe click-focus and inspect selected_studio_window_title.",
		"F5_NOT_PRESSED": "Use assisted click-focus mode or manually focus Studio during fallback wait.",
		"STUDIO_FOREGROUND_BLOCKED": "Close browser/extra Studio windows or run PowerShell as normal user, not admin.",
		"PLAY_NOT_CONFIRMED": "F5 was sent to the selected Studio window, but foreground/runtime evidence did not confirm Play mode.",
		"WRONG_STUDIO_WINDOW": "Close AutoRecovery/Installer windows so build/game.rbxlx is selected.",
		"ONLY_WARN_ERROR_MARKERS": "Inspect expanded roblox_latest_markers.md checked files; Play may not have started runtime or logs may be elsewhere.",
		"PLAY_LOGS_NOT_CAPTURED_OR_RUNTIME_FAILED": "Open Studio Output and check whether server/client scripts ran after F5.",
		"RUNTIME_MARKERS_NOT_CAPTURED": "F5/video succeeded, but server markers are not currently observed in the automated Studio run. Check Studio Output for [Server boot] and DemoDiagnostics markers.",
		"PARTIAL_RUNTIME_CONFIRMED": "Some runtime markers were captured; inspect missing DemoDiagnostics beacon markers.",
		"SERVER_BOOT_NOT_FOUND": "Verify Main.server.lua is mapped into ServerScriptService and prints [Server boot].",
		"CLIENT_BOOT_NOT_FOUND": "Verify Main.client.lua is mapped into StarterPlayerScripts and prints [Client boot].",
		"DEMO_CAMERA_NOT_FOUND": "Verify demo spectator camera script runs and can access Workspace.CurrentCamera.",
		"PLAYERSPAWN_NOT_FOUND": "Verify PlayerSpawnService:Init is called in Main.server.lua.",
		"MAP_NOT_BUILT": "Verify MapService:BuildBacklundFogDistrict runs inside Main.server.lua.",
		"WAVE_NOT_STARTED": "Verify WaveService:StartWaveLoop runs after path/tower setup.",
		"VIDEO_NOT_RECORDED": "Inspect screen_recorder output and disk permissions.",
		"VIDEO_TOO_SMALL": "Rerun with 45 seconds in the autofix loop.",
	}
	return fixes.get(diagnosis, "No safe automatic fix identified; inspect demo_autofix_report.md.")


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


def manual_play_record_mode(report: dict[str, Any], state: dict[str, Any], duration: int, auto_play: bool = False, auto_play_mode: str = "safe") -> None:
	if not build_place(report, state):
		report["result_status"] = "DEMO_BUILD_FAILED"
		report["note"] = report.get("build_error", "Build failed.")
		return

	open_built_place(report, state)
	report["windows"] = find_windows()

	if not ensure_studio_window_visible(report, state):
		capture_and_record(state, report, "studio_not_visible")
		report["result_status"] = "DEMO_STUDIO_WINDOW_NOT_VISIBLE"
		report["note"] = "Roblox Studio window is minimized/offscreen. Bring it to screen and rerun."
		update_status(state, "DEMO_STUDIO_WINDOW_NOT_VISIBLE")
		return

	capture_and_record(state, report, "before_manual_play")

	report["auto_play_enabled"] = auto_play
	report["auto_play_mode"] = auto_play_mode
	report["f5_pressed"] = False
	report["auto_play_status"] = "AUTO_PLAY_DISABLED"

	if auto_play:
		if auto_play_mode == "assisted":
			print("\n" + "="*60)
			print("ASSISTED AUTO-PLAY")
			print("The runner will try the Windows-level Studio play controller first.")
			print("If it fails, it will fall back to assisted focus.")
			print("Do not use mouse/keyboard during focus attempt.")
			print("="*60 + "\n")

			report["active_window_before_auto_play"] = get_active_window_title()
			controller_result = force_studio_play()
			report["studio_play_controller"] = controller_result

			if controller_result.get("f5_pressed"):
				print("[Demo] Windows Studio play controller pressed F5")
				report["f5_pressed"] = True
				if controller_result.get("foreground_confirmed"):
					report["auto_play_status"] = "AUTO_PLAY_FORCE_CONTROLLER_F5_PRESSED"
				else:
					report["auto_play_status"] = "AUTO_PLAY_FORCE_CONTROLLER_F5_SENT_FOREGROUND_NOT_CONFIRMED"
				report["active_window_after_auto_play"] = get_active_window_title()
				time.sleep(4)
			else:
				print("[Demo] Windows Studio play controller failed; falling back to assisted click-focus")
				report["auto_play_status"] = "AUTO_PLAY_FORCE_CONTROLLER_FAILED_FALLBACK_USED"
				click_focus_ok = safe_click_focus_studio_window(report)

				if click_focus_ok:
					print("[Demo] Assisted click-focus F5 pressed")
					pyautogui.press("f5")
					report["f5_pressed"] = True
					report["auto_play_status"] = "AUTO_PLAY_ASSISTED_CLICK_FOCUS_F5_PRESSED"
					report["active_window_after_auto_play"] = get_active_window_title()
					time.sleep(4)
				else:
					print("[Demo] Click-focus failed. Click Roblox Studio within 30 seconds.")
					if wait_for_studio_focus(30):
						print("[Demo] Assisted wait-focus F5 pressed")
						pyautogui.press("f5")
						report["f5_pressed"] = True
						report["auto_play_status"] = "AUTO_PLAY_ASSISTED_WAIT_FOCUS_F5_PRESSED"
						report["active_window_after_auto_play"] = get_active_window_title()
						time.sleep(4)
					else:
						print("[Demo] Assisted auto-play skipped: Studio focus timed out")
						report["f5_pressed"] = False
						report["auto_play_status"] = "AUTO_PLAY_ASSISTED_FOCUS_TIMEOUT"
						report["active_window_after_auto_play"] = get_active_window_title()
						time.sleep(2)
		else:
			print("\n" + "="*60)
			print("Auto-play is enabled.")
			print("The runner will focus Roblox Studio and press F5 only if Studio focus is confirmed.")
			print("="*60 + "\n")

			best = choose_best_studio_window()
			report["active_window_before_auto_play"] = get_active_window_title()

			if best:
				print("[Demo] Attempting to focus Roblox Studio...")
				focus_window(best["window"])
				time.sleep(2)

			report["active_window_after_auto_play"] = get_active_window_title()

			if is_active_studio_window():
				print("[Demo] F5 pressed")
				pyautogui.press("f5")
				report["f5_pressed"] = True
				report["auto_play_status"] = "AUTO_PLAY_F5_PRESSED"
				time.sleep(4)
			else:
				print("[Demo] Auto-play skipped: Studio focus not confirmed")
				report["f5_pressed"] = False
				report["auto_play_status"] = "AUTO_PLAY_FOCUS_NOT_CONFIRMED"
				time.sleep(2)
	else:
		print("\n" + "="*60)
		print("Recording will start in 5 seconds.")
		print("Make sure Roblox Studio is visible.")
		print("When recording starts, click Studio and press Play/F5.")
		print("Do not switch windows.")
		print("="*60 + "\n")

		time.sleep(5)

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
	parser.add_argument("--auto-play", action="store_true", help="Automatically press F5 to start Play mode (manual-play-record only)")
	parser.add_argument("--auto-play-mode", choices=("safe", "assisted"), default="safe", help="Auto-play mode: safe (auto-focus) or assisted (user clicks)")
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
		"auto_play_enabled": False,
		"auto_play_mode": args.auto_play_mode,
		"auto_play_status": "AUTO_PLAY_DISABLED",
	}

	try:
		if args.mode == "observe":
			observe_mode(report, state)
		elif args.mode == "record-only":
			record_only_mode(report, state, report["duration"])
		elif args.mode == "manual-play-record":
			manual_play_record_mode(report, state, report["duration"], auto_play=args.auto_play, auto_play_mode=args.auto_play_mode)
		else:
			run_demo_mode(report, state, report["duration"], args.focus_mode)
	except Exception as exc:
		report["result_status"] = "DEMO_ERROR"
		report["note"] = f"Error during demo execution: {str(exc)}"
		update_status(state, "DEMO_ERROR", str(exc))
		print(f"Error: {exc}", file=sys.stderr)

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

	spectator_markers = [
		"[Client] Demo spectator camera activated",
		"[Main] Demo spectator spawn ready",
		"[Main] Demo map build requested",
	]

	gameplay_loop_markers = [
		"[WaveService]",
		"[TowerService]",
		"[EnemyService]",
	]

	diagnostic_beacon_markers = [
		"[DemoDiagnostics] Init",
		"[DemoDiagnostics] ServerBootBeacon marked",
		"[DemoDiagnostics] PlayerSpawnBeacon marked",
		"[DemoDiagnostics] MapBuildBeacon marked",
		"[DemoDiagnostics] WaveLoopBeacon marked",
		"[Client] Demo spectator camera activated",
	]

	matched = report.get("matched_markers", [])
	project_markers_count = int(report.get("project_markers_count", 0))

	if report.get("result_status") == "DEMO_RECORDED":
		spectator_hits = sum(1 for marker in spectator_markers if marker in matched)
		gameplay_hits = sum(1 for marker in gameplay_loop_markers if marker in matched)
		diagnostic_hits = sum(1 for marker in diagnostic_beacon_markers if marker in matched)

		if (diagnostic_hits >= 3 or project_markers_count >= 3) and gameplay_hits > 0:
			report["play_status"] = "DEMO_RECORDED_RUNTIME_DIAGNOSTICS_CONFIRMED"
			report["video_score"] = 4
		elif diagnostic_hits >= 3 or project_markers_count >= 3:
			report["play_status"] = "DEMO_RECORDED_RUNTIME_PARTIAL_CONFIRMED"
			report["video_score"] = 3
		elif spectator_hits >= 3 and gameplay_hits > 0:
			report["play_status"] = "DEMO_RECORDED_SPECTATOR_GAMEPLAY_CONFIRMED"
			report["video_score"] = 4
		elif spectator_hits >= 3:
			report["play_status"] = "DEMO_RECORDED_SPECTATOR_CONFIRMED"
			report["video_score"] = 3
		elif any(marker in matched for marker in important_markers):
			report["play_status"] = "DEMO_RECORDED_PLAY_CONFIRMED"
			report["video_score"] = 3
		else:
			report["play_status"] = "DEMO_RECORDED_PLAY_NOT_CONFIRMED"
			report["video_score"] = 2
	elif report.get("result_status") == "DEMO_RECORDING_FAILED":
		report["play_status"] = "DEMO_RECORDING_FAILED"
		report["video_score"] = 0
	else:
		report["play_status"] = report.get("result_status", "UNKNOWN")
		report["video_score"] = 0

	report["diagnosis"] = diagnose_demo_report(report)
	report["success_criteria_passed"] = evaluate_success_criteria(report)
	report["possible_next_fix"] = possible_next_fix_for_diagnosis(report["diagnosis"])
	if report.get("project_markers_count", 0) > 0:
		report["play_confirmation_evidence"] = "project runtime markers found in Roblox logs"
	else:
		report["play_confirmation_evidence"] = "no project runtime markers found after F5/send-key attempt"
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

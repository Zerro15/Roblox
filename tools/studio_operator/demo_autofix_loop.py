from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"
REPORT_PATH = LOGS_DIR / "demo_autofix_report.md"
DEMO_REPORT_PATH = LOGS_DIR / "demo_test_report.md"
MARKER_REPORT_PATH = LOGS_DIR / "roblox_latest_markers.md"
MARKER_METADATA_PATH = LOGS_DIR / "roblox_latest_markers.json"
RECORDINGS_DIR = LOGS_DIR / "recordings"

SUCCESS_MARKERS = [
    "[DemoDiagnostics] Init",
    "[DemoDiagnostics] ServerBootBeacon marked",
    "[DemoDiagnostics] PlayerSpawnBeacon marked",
    "[DemoDiagnostics] MapBuildBeacon marked",
    "[DemoDiagnostics] WaveLoopBeacon marked",
    "[Client] Demo spectator camera activated",
]

GAMEPLAY_MARKERS = [
    "[Playable] Game started",
    "[Playable] Camera ready",
    "[Playable] UI ready",
    "[Playable] Map ready",
    "[Playable] Tower pad ready",
    "[Playable] Wave started",
    "[Playable] Enemy spawned",
    "[Playable] Enemy pathing started",
    "[Playable] Enemy reached base",
    "[Playable] Base damaged",
    "[Playable] Tower placed",
    "[Playable] Tower selected",
    "[Playable] Tower sold",
    "[Playable] Tower attack fired",
    "[Playable] Enemy damaged",
    "[Playable] Enemy killed",
    "[Playable] Reward granted",
    "[Playable] Wave completed",
    "[Playable] Game over",
    "[Playable] Victory",
    "[DemoGameplay] Map ready",
    "[DemoGameplay] Enemy spawned",
    "[DemoGameplay] Enemy pathing started",
    "[DemoGameplay] Tower placed",
    "[DemoGameplay] Tower attack fired",
    "[DemoGameplay] Enemy damaged",
    "[DemoGameplay] Wave completed",
    "[Hub] Hub ready",
    "[Hub] Portal ready",
    "[Hub] Start defense clicked",
    "[Hub] Defense started",
    "[WaveService]",
    "[TowerService]",
    "[EnemyService]",
]

HUB_FLOW_REQUIRED_MARKERS = [
    "[Hub] Hub ready",
    "[Hub] Portal ready",
    "[Hub] Defense started",
    "[Playable] Game started",
    "[Playable] Camera ready",
    "[Playable] UI ready",
    "[Playable] Wave started",
    "[Playable] Enemy spawned",
    "[Playable] Tower attack fired",
    "[Playable] Enemy damaged",
]

DIAGNOSES = [
    "BUILD_FAILED",
    "STUDIO_WINDOW_NOT_VISIBLE",
    "FOCUS_FAILED",
    "F5_NOT_PRESSED",
    "STUDIO_FOREGROUND_BLOCKED",
    "PLAY_NOT_CONFIRMED",
    "SERVER_BOOT_NOT_FOUND",
    "CLIENT_BOOT_NOT_FOUND",
    "DEMO_CAMERA_NOT_FOUND",
    "PLAYERSPAWN_NOT_FOUND",
    "MAP_NOT_BUILT",
    "WAVE_NOT_STARTED",
    "VIDEO_NOT_RECORDED",
    "VIDEO_TOO_SMALL",
    "ONLY_WARN_ERROR_MARKERS",
    "PLAY_LOGS_NOT_CAPTURED_OR_RUNTIME_FAILED",
    "RUNTIME_MARKERS_NOT_CAPTURED",
    "PARTIAL_RUNTIME_CONFIRMED",
    "UNKNOWN_FAILURE",
    "OK",
]


def run_command(command: list[str], timeout_seconds: int = 180) -> tuple[bool, str]:
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_seconds,
        shell=False,
    )
    return completed.returncode == 0, completed.stdout


def parse_markdown_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    if not path.exists():
        return fields

    field_pattern = re.compile(r"^- ([^:]+): `?(.*?)`?$")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
            value = match.group(2).strip().strip("`")
            fields[key] = value
    return fields


def latest_recording() -> Path | None:
    if not RECORDINGS_DIR.exists():
        return None
    candidates = sorted(RECORDINGS_DIR.glob("*.mp4"), key=lambda path: path.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def load_marker_metadata() -> dict[str, Any]:
    if not MARKER_METADATA_PATH.exists():
        return {}
    try:
        return json.loads(MARKER_METADATA_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def bool_field(value: str) -> bool:
    return value.lower() == "true"


def int_prefix(value: str) -> int:
    match = re.match(r"(\d+)", value.strip())
    return int(match.group(1)) if match else 0


def diagnose() -> dict[str, Any]:
    fields = parse_markdown_fields(DEMO_REPORT_PATH)
    marker_metadata = load_marker_metadata()
    recording = latest_recording()
    matched_markers = marker_metadata.get("matched_markers", [])
    project_markers = marker_metadata.get("project_markers", [])
    checked_files = marker_metadata.get("checked_files", [])

    build_status = fields.get("build_status", "not_run")
    selected_title = fields.get("selected_studio_window_title", "")
    selected_hwnd = fields.get("selected_hwnd", "")
    selected_pid = fields.get("selected_pid", "")
    selected_root_hwnd = fields.get("selected_root_hwnd", "")
    selected_root_title = fields.get("selected_root_title", "")
    foreground_before_title = fields.get("foreground_before_title", "")
    foreground_before_pid = fields.get("foreground_before_pid", "")
    foreground_before_root_hwnd = fields.get("foreground_before_root_hwnd", "")
    foreground_before_root_title = fields.get("foreground_before_root_title", "")
    foreground_after_title = fields.get("foreground_after_title", "")
    foreground_after_pid = fields.get("foreground_after_pid", "")
    foreground_after_root_hwnd = fields.get("foreground_after_root_hwnd", "")
    foreground_after_root_title = fields.get("foreground_after_root_title", "")
    foreground_after_f5_title = fields.get("foreground_after_f5_title", "")
    foreground_after_f5_pid = fields.get("foreground_after_f5_pid", "")
    foreground_after_f5_root_hwnd = fields.get("foreground_after_f5_root_hwnd", "")
    foreground_after_f5_root_title = fields.get("foreground_after_f5_root_title", "")
    foreground_confirmed = fields.get("foreground_confirmed", "")
    foreground_confirmation_reason = fields.get("foreground_confirmation_reason", "")
    f5_method = fields.get("f5_method", "")
    f5_methods_attempted = fields.get("f5_methods_attempted", "")
    f5_sent_to_selected_hwnd = fields.get("f5_sent_to_selected_hwnd", "")
    play_confirmation_evidence = fields.get("play_confirmation_evidence", "")
    f5_pressed = bool_field(fields.get("was_f5_pressed", "false"))
    auto_play_status = fields.get("auto_play_status", "")
    score = int_prefix(fields.get("video_usefulness_score", "0"))
    project_marker_count = int(fields.get("project_markers_count", marker_metadata.get("project_markers_count", 0) or 0))

    diagnosis = classify_failure(
        build_status=build_status,
        selected_title=selected_title,
        f5_pressed=f5_pressed,
        auto_play_status=auto_play_status,
        recording=recording,
        recording_size=recording.stat().st_size if recording and recording.exists() else 0,
        matched_markers=matched_markers,
        project_markers=project_markers,
        project_marker_count=project_marker_count,
    )

    success = success_criteria(
        build_status=build_status,
        recording=recording,
        f5_pressed=f5_pressed,
        auto_play_status=auto_play_status,
        matched_markers=matched_markers,
        score=score,
    )

    return {
        "timestamp": datetime.now().isoformat(),
        "diagnosis": diagnosis,
        "success": success,
        "build_status": build_status,
        "selected_studio_window_title": selected_title,
        "selected_hwnd": selected_hwnd,
        "selected_pid": selected_pid,
        "selected_root_hwnd": selected_root_hwnd,
        "selected_root_title": selected_root_title,
        "foreground_before_title": foreground_before_title,
        "foreground_before_pid": foreground_before_pid,
        "foreground_before_root_hwnd": foreground_before_root_hwnd,
        "foreground_before_root_title": foreground_before_root_title,
        "foreground_after_title": foreground_after_title,
        "foreground_after_pid": foreground_after_pid,
        "foreground_after_root_hwnd": foreground_after_root_hwnd,
        "foreground_after_root_title": foreground_after_root_title,
        "foreground_after_f5_title": foreground_after_f5_title,
        "foreground_after_f5_pid": foreground_after_f5_pid,
        "foreground_after_f5_root_hwnd": foreground_after_f5_root_hwnd,
        "foreground_after_f5_root_title": foreground_after_f5_root_title,
        "foreground_confirmed": foreground_confirmed,
        "foreground_confirmation_reason": foreground_confirmation_reason,
        "f5_method": f5_method,
        "f5_methods_attempted": f5_methods_attempted,
        "f5_sent_to_selected_hwnd": f5_sent_to_selected_hwnd,
        "play_confirmation_evidence": play_confirmation_evidence,
        "f5_pressed": f5_pressed,
        "auto_play_status": auto_play_status,
        "score": score,
        "recording": str(recording) if recording else "",
        "recording_size": recording.stat().st_size if recording and recording.exists() else 0,
        "matched_markers": matched_markers,
        "project_markers": project_markers,
        "project_markers_count": project_marker_count,
        "checked_log_files": checked_files,
        "demo_report": str(DEMO_REPORT_PATH) if DEMO_REPORT_PATH.exists() else "",
        "marker_report": str(MARKER_REPORT_PATH) if MARKER_REPORT_PATH.exists() else "",
    }


def classify_failure(
    build_status: str,
    selected_title: str,
    f5_pressed: bool,
    auto_play_status: str,
    recording: Path | None,
    recording_size: int,
    matched_markers: list[str],
    project_markers: list[str],
    project_marker_count: int,
) -> str:
    selected_lower = selected_title.lower()
    if build_status == "failed":
        return "BUILD_FAILED"
    if selected_title and ("game.rbxlx" not in selected_lower or "roblox studio" not in selected_lower):
        return "FOCUS_FAILED"
    if not f5_pressed:
        if "FOCUS_TIMEOUT" in auto_play_status or "FORCE_CONTROLLER_FAILED" in auto_play_status:
            return "STUDIO_FOREGROUND_BLOCKED"
        return "F5_NOT_PRESSED"
    if "FOREGROUND_NOT_CONFIRMED" in auto_play_status:
        return "PLAY_NOT_CONFIRMED"
    if "F5_PRESSED" not in auto_play_status:
        return "PLAY_NOT_CONFIRMED"
    if not recording:
        return "VIDEO_NOT_RECORDED"
    if recording_size < 300_000:
        return "VIDEO_TOO_SMALL"
    if project_marker_count == 0:
        return "RUNTIME_MARKERS_NOT_CAPTURED"
    gameplay_confirmed = any(marker in project_markers for marker in GAMEPLAY_MARKERS)
    diagnostics_confirmed = any(marker.startswith("[DemoDiagnostics]") for marker in project_markers)
    client_camera_confirmed = (
        "[Client] Demo spectator camera activated" in project_markers
        or "[Playable] Camera ready" in project_markers
    )
    hub_playable_confirmed = all(marker in project_markers for marker in HUB_FLOW_REQUIRED_MARKERS)
    if project_marker_count < 3:
        return "PARTIAL_RUNTIME_CONFIRMED"
    if not gameplay_confirmed:
        return "PARTIAL_RUNTIME_CONFIRMED"
    if hub_playable_confirmed and client_camera_confirmed:
        return "OK"
    if not diagnostics_confirmed or not client_camera_confirmed:
        return "PARTIAL_RUNTIME_CONFIRMED"
    if "[Server boot]" in project_markers or "[DemoDiagnostics] ServerBootBeacon marked" in project_markers:
        return "OK"
    if "[Server boot]" not in project_markers and "[DemoDiagnostics] ServerBootBeacon marked" not in project_markers:
        return "SERVER_BOOT_NOT_FOUND"
    if "[Client boot]" not in project_markers:
        return "CLIENT_BOOT_NOT_FOUND"
    if "[Client] Demo spectator camera activated" not in project_markers:
        return "DEMO_CAMERA_NOT_FOUND"
    if not any(marker.startswith("[PlayerSpawnService]") or marker == "[PlayerSpawnService]" for marker in project_markers):
        return "PLAYERSPAWN_NOT_FOUND"
    if "[Main] Demo map build requested" not in project_markers and "[MapService]" not in project_markers:
        return "MAP_NOT_BUILT"
    if "[WaveService]" not in project_markers:
        return "WAVE_NOT_STARTED"
    return "UNKNOWN_FAILURE"


def success_criteria(
    build_status: str,
    recording: Path | None,
    f5_pressed: bool,
    auto_play_status: str,
    matched_markers: list[str],
    score: int,
) -> bool:
    marker_hits = sum(1 for marker in SUCCESS_MARKERS if marker in matched_markers)
    gameplay_confirmed = any(marker in matched_markers for marker in GAMEPLAY_MARKERS)
    hub_playable_confirmed = all(marker in matched_markers for marker in HUB_FLOW_REQUIRED_MARKERS)
    return (
        build_status == "ok"
        and recording is not None
        and f5_pressed
        and "F5_PRESSED" in auto_play_status
        and (marker_hits >= 3 or hub_playable_confirmed)
        and gameplay_confirmed
        and score >= 3
    )


def safe_fix_strategy(diagnosis_name: str, attempt: int) -> dict[str, Any]:
    strategies = {
        "FOCUS_FAILED": "No source edit applied. Existing assisted click-focus is already enabled; rerun after closing extra Studio windows.",
        "F5_NOT_PRESSED": "F5_NOT_PRESSED detected; force controller enabled for next attempt.",
        "STUDIO_FOREGROUND_BLOCKED": "Close browser/extra Studio windows or run PowerShell as normal user, not admin.",
        "ONLY_WARN_ERROR_MARKERS": "No gameplay edit applied. Expanded Roblox log aggregation is active; next step is to inspect checked log files and Studio Output.",
        "PLAY_LOGS_NOT_CAPTURED_OR_RUNTIME_FAILED": "No gameplay edit applied. Runtime may not have started or logs may be in another file.",
        "RUNTIME_MARKERS_NOT_CAPTURED": "No gameplay edit applied. F5/video succeeded, but server markers are not currently observed in the automated Studio run.",
        "PARTIAL_RUNTIME_CONFIRMED": "No gameplay edit applied. Some runtime markers were found, but hub/playable confirmation is incomplete.",
        "SERVER_BOOT_NOT_FOUND": "No automatic gameplay edit applied. Verify Main.server.lua mapping and [Server boot] print manually.",
        "CLIENT_BOOT_NOT_FOUND": "No automatic gameplay edit applied. Verify Main.client.lua mapping and [Client boot] print manually.",
        "DEMO_CAMERA_NOT_FOUND": "No automatic gameplay edit applied. Verify Scriptable camera execution in Studio Output.",
        "PLAYERSPAWN_NOT_FOUND": "No automatic gameplay edit applied. Verify PlayerSpawnService:Init in Main.server.lua.",
        "MAP_NOT_BUILT": "No automatic gameplay edit applied. Verify MapService build step in Main.server.lua.",
        "WAVE_NOT_STARTED": "No automatic gameplay edit applied. Verify WaveService:StartWaveLoop in Main.server.lua.",
        "VIDEO_TOO_SMALL": "Next run should use longer duration; this loop keeps the default script unchanged.",
    }
    return {
        "attempt": attempt,
        "diagnosis": diagnosis_name,
        "applied": False,
        "description": strategies.get(diagnosis_name, "No safe automatic fix identified."),
    }


def run_once() -> dict[str, Any]:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    build_ok, build_output = run_command(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ".\\scripts\\build_place.ps1"],
        timeout_seconds=120,
    )
    demo_ok, demo_output = run_command(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ".\\scripts\\run_demo_assisted_auto_play_30s.ps1"],
        timeout_seconds=240,
    )
    result = diagnose()
    result["build_command_ok"] = build_ok
    result["demo_command_ok"] = demo_ok
    result["build_output_tail"] = build_output[-2000:]
    result["demo_output_tail"] = demo_output[-3000:]
    write_autofix_report([result], [])
    return result


def run_loop(max_attempts: int) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    fixes: list[dict[str, Any]] = []
    bounded_attempts = max(1, min(max_attempts, 3))

    for attempt_number in range(1, bounded_attempts + 1):
        result = run_once()
        result["attempt"] = attempt_number
        attempts.append(result)

        if result["success"]:
            write_autofix_report(attempts, fixes)
            return result

        fix = safe_fix_strategy(result["diagnosis"], attempt_number)
        fixes.append(fix)
        write_autofix_report(attempts, fixes)

        if not fix["applied"]:
            return result

    write_autofix_report(attempts, fixes)
    return attempts[-1]


def write_autofix_report(attempts: list[dict[str, Any]], fixes: list[dict[str, Any]]) -> Path:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    latest = attempts[-1] if attempts else diagnose()
    lines = [
        "# Demo Autofix Report",
        "",
        f"- generated_at: `{datetime.now().isoformat()}`",
        f"- latest diagnosis: `{latest.get('diagnosis', 'UNKNOWN_FAILURE')}`",
        f"- success: `{latest.get('success', False)}`",
        f"- attempts: `{len(attempts)}`",
        f"- demo report: `{latest.get('demo_report', '')}`",
        f"- marker report: `{latest.get('marker_report', '')}`",
        f"- recording: `{latest.get('recording', '')}`",
        f"- recording size: `{latest.get('recording_size', 0)}` bytes",
        f"- score: `{latest.get('score', 0)}/5`",
        f"- f5 pressed: `{latest.get('f5_pressed', False)}`",
        f"- auto-play status: `{latest.get('auto_play_status', '')}`",
        f"- selected hwnd: `{latest.get('selected_hwnd', '')}`",
        f"- selected pid: `{latest.get('selected_pid', '')}`",
        f"- selected root hwnd: `{latest.get('selected_root_hwnd', '')}`",
        f"- selected root title: `{latest.get('selected_root_title', '')}`",
        f"- foreground before: `{latest.get('foreground_before_title', '')}`",
        f"- foreground before pid/root: `{latest.get('foreground_before_pid', '')}` / `{latest.get('foreground_before_root_hwnd', '')}` `{latest.get('foreground_before_root_title', '')}`",
        f"- foreground after: `{latest.get('foreground_after_title', '')}`",
        f"- foreground after pid/root: `{latest.get('foreground_after_pid', '')}` / `{latest.get('foreground_after_root_hwnd', '')}` `{latest.get('foreground_after_root_title', '')}`",
        f"- foreground after F5: `{latest.get('foreground_after_f5_title', '')}`",
        f"- foreground after F5 pid/root: `{latest.get('foreground_after_f5_pid', '')}` / `{latest.get('foreground_after_f5_root_hwnd', '')}` `{latest.get('foreground_after_f5_root_title', '')}`",
        f"- foreground confirmed: `{latest.get('foreground_confirmed', '')}`",
        f"- foreground confirmation reason: `{latest.get('foreground_confirmation_reason', '')}`",
        f"- f5 method: `{latest.get('f5_method', '')}`",
        f"- f5 methods attempted: `{latest.get('f5_methods_attempted', '')}`",
        f"- f5 sent to selected hwnd: `{latest.get('f5_sent_to_selected_hwnd', '')}`",
        f"- play confirmation evidence: `{latest.get('play_confirmation_evidence', '')}`",
        f"- project markers count: `{latest.get('project_markers_count', 0)}`",
        f"- foreground recovery note: `{safe_fix_strategy(latest.get('diagnosis', 'UNKNOWN_FAILURE'), len(attempts) or 1)['description']}`",
        "",
        "## Expected Visual Runtime Beacons",
        "- Blue `ServerBootBeacon` near `Workspace/DemoDiagnostics`",
        "- Green `PlayerSpawnBeacon` near `Workspace/DemoDiagnostics`",
        "- Yellow `MapBuildBeacon` near `Workspace/DemoDiagnostics`",
        "- Red `WaveLoopBeacon` near `Workspace/DemoDiagnostics`",
        "- UI text: `DEMO SPECTATOR CAMERA ACTIVE`",
        "",
        "## Attempts",
    ]

    for attempt in attempts:
        lines.extend(
            [
                f"### Attempt {attempt.get('attempt', len(lines))}",
                f"- diagnosis: `{attempt.get('diagnosis')}`",
                f"- success: `{attempt.get('success')}`",
                f"- build status: `{attempt.get('build_status')}`",
                f"- selected window: `{attempt.get('selected_studio_window_title')}`",
                f"- selected hwnd: `{attempt.get('selected_hwnd')}`",
                f"- selected pid/root: `{attempt.get('selected_pid')}` / `{attempt.get('selected_root_hwnd')}` `{attempt.get('selected_root_title')}`",
                f"- foreground before: `{attempt.get('foreground_before_title')}`",
                f"- foreground before pid/root: `{attempt.get('foreground_before_pid')}` / `{attempt.get('foreground_before_root_hwnd')}` `{attempt.get('foreground_before_root_title')}`",
                f"- foreground after: `{attempt.get('foreground_after_title')}`",
                f"- foreground after pid/root: `{attempt.get('foreground_after_pid')}` / `{attempt.get('foreground_after_root_hwnd')}` `{attempt.get('foreground_after_root_title')}`",
                f"- foreground after F5: `{attempt.get('foreground_after_f5_title')}`",
                f"- foreground after F5 pid/root: `{attempt.get('foreground_after_f5_pid')}` / `{attempt.get('foreground_after_f5_root_hwnd')}` `{attempt.get('foreground_after_f5_root_title')}`",
                f"- foreground confirmed: `{attempt.get('foreground_confirmed')}`",
                f"- foreground confirmation reason: `{attempt.get('foreground_confirmation_reason')}`",
                f"- f5 method: `{attempt.get('f5_method')}`",
                f"- f5 methods attempted: `{attempt.get('f5_methods_attempted')}`",
                f"- f5 sent to selected hwnd: `{attempt.get('f5_sent_to_selected_hwnd')}`",
                f"- f5 pressed: `{attempt.get('f5_pressed')}`",
                f"- play confirmation evidence: `{attempt.get('play_confirmation_evidence')}`",
                f"- score: `{attempt.get('score')}/5`",
                f"- matched markers: `{', '.join(attempt.get('matched_markers', []))}`",
            ]
        )

    lines.extend(["", "## Safe Fix Decisions"])
    if fixes:
        for fix in fixes:
            lines.append(f"- attempt `{fix['attempt']}` `{fix['diagnosis']}` applied=`{fix['applied']}`: {fix['description']}")
    else:
        lines.append("- No fix decisions yet.")

    lines.extend(["", "## Checked Log Files"])
    checked_files = latest.get("checked_log_files", [])
    if checked_files:
        for item in checked_files:
            if isinstance(item, dict):
                lines.append(f"- `{item.get('path', '')}` modified `{item.get('modified_at', '')}`")
            else:
                lines.append(f"- `{item}`")
    else:
        lines.append("- No checked log files recorded.")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT_PATH


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded autonomous demo diagnose/autofix loop.")
    parser.add_argument("--mode", choices=("diagnose", "run-once", "loop"), default="loop")
    parser.add_argument("--max-attempts", type=int, default=3)
    args = parser.parse_args()

    if args.mode == "diagnose":
        result = diagnose()
        write_autofix_report([result], [])
    elif args.mode == "run-once":
        result = run_once()
    else:
        result = run_loop(args.max_attempts)

    print(f"Diagnosis: {result['diagnosis']}")
    print(f"Success: {result['success']}")
    print(f"Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

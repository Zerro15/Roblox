"""Generate a reviewer-friendly demo evidence report.

This tool aggregates existing pipeline/demo reports without launching Roblox
Studio and without copying generated artifacts into source control.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"
RECORDINGS_DIR = LOGS_DIR / "recordings"
REPORT_PATH = LOGS_DIR / "demo_evidence_report.md"
JSON_REPORT_PATH = LOGS_DIR / "demo_evidence_report.json"

PIPELINE_REPORT = LOGS_DIR / "pipeline_smoke_report.md"
DEMO_REPORT = LOGS_DIR / "demo_test_report.md"
AUTOFIX_REPORT = LOGS_DIR / "demo_autofix_report.md"
MARKER_REPORT = LOGS_DIR / "roblox_latest_markers.md"
MARKER_JSON = LOGS_DIR / "roblox_latest_markers.json"
PLACE_REPORT = LOGS_DIR / "place_structure_report.md"

KEY_MARKERS = [
    "[Server boot]",
    "[DemoDiagnostics] Init",
    "[DemoDiagnostics] ServerBootBeacon marked",
    "[RuntimeService]",
    "[MapService]",
    "[PathService]",
    "[DemoGameplay] Map ready",
    "[DemoGameplay] Enemy spawned",
    "[DemoGameplay] Enemy pathing started",
    "[DemoGameplay] Tower placed",
    "[DemoGameplay] Tower attack fired",
    "[DemoGameplay] Enemy damaged",
    "[DemoGameplay] Wave completed",
    "[Hub] Authored hub found",
    "[Hub] Walkable hub ready",
    "[Hub] Defense portal ready",
    "[Hub] Start defense prompt ready",
    "[Hub] Hub ready",
    "[Hub] Portal ready",
    "[Hub] Start defense clicked",
    "[Hub] Defense started",
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
    "[WaveService]",
    "[TowerService]",
    "[EnemyService]",
    "[Client boot]",
    "[Client] Demo spectator camera activated",
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


def run_command(command: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=30,
        )
        return completed.returncode == 0, completed.stdout.strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)


def git_info() -> dict[str, Any]:
    ok_branch, branch = run_command(["git", "branch", "--show-current"])
    ok_sha, sha = run_command(["git", "rev-parse", "--short", "HEAD"])
    ok_title, title = run_command(["git", "log", "-1", "--format=%s"])
    ok_status, status = run_command(["git", "status", "--short"])
    return {
        "branch": branch if ok_branch else "unknown",
        "commit": sha if ok_sha else "unknown",
        "commit_title": title if ok_title else "unknown",
        "working_tree_status": status.splitlines() if ok_status and status else [],
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def parse_markdown_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    field_pattern = re.compile(r"^- ([^:]+): `?(.*?)`?$")
    for line in read_text(path).splitlines():
        match = field_pattern.match(line.strip())
        if not match:
            continue
        key = match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
        fields[key] = match.group(2).strip().strip("`")
    return fields


def load_marker_metadata() -> dict[str, Any]:
    if not MARKER_JSON.exists():
        return {}
    try:
        return json.loads(MARKER_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def latest_recording() -> dict[str, Any]:
    if not RECORDINGS_DIR.exists():
        return {"path": "", "size_bytes": 0, "size_mb": 0.0, "modified_at": ""}
    recordings = sorted(RECORDINGS_DIR.glob("*.mp4"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not recordings:
        return {"path": "", "size_bytes": 0, "size_mb": 0.0, "modified_at": ""}
    latest = recordings[0]
    stat = latest.stat()
    return {
        "path": str(latest),
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }


def extract_smoke_status(fields: dict[str, str]) -> dict[str, str]:
    return {
        "result": fields.get("result", "not found"),
        "checks_passed": fields.get("checks_passed", "not found"),
    }


def extract_marker_summary(metadata: dict[str, Any]) -> dict[str, Any]:
    project_markers = metadata.get("project_markers", []) or []
    missing_expected = metadata.get("missing_expected_markers", []) or []
    important_found = [marker for marker in KEY_MARKERS if marker in project_markers]
    missing_hub_flow = [marker for marker in HUB_FLOW_REQUIRED_MARKERS if marker not in project_markers]
    return {
        "project_markers_count": metadata.get("project_markers_count", 0),
        "runtime_diagnosis": metadata.get("runtime_diagnosis", "not available"),
        "important_markers_found": important_found,
        "missing_expected_markers": missing_expected,
        "missing_hub_flow_markers": missing_hub_flow,
        "hub_playable_confirmed": not missing_hub_flow,
        "checked_log_files_count": len(metadata.get("checked_files", []) or []),
    }


def classify_result(smoke: dict[str, str], demo_fields: dict[str, str], marker_summary: dict[str, Any], recording: dict[str, Any]) -> str:
    smoke_ok = smoke.get("result") == "PASS"
    demo_ok = demo_fields.get("diagnosis") == "OK"
    success_ok = demo_fields.get("success_criteria_passed") == "True"
    hub_playable_ok = bool(marker_summary.get("hub_playable_confirmed"))
    no_missing_expected = not marker_summary.get("missing_expected_markers")
    marker_count = int(marker_summary.get("project_markers_count", 0) or 0)
    has_video = bool(recording.get("path")) and int(recording.get("size_bytes", 0)) >= 300_000

    if smoke_ok and demo_ok and marker_count >= 3 and has_video:
        return "OK"
    if smoke_ok and success_ok and hub_playable_ok and no_missing_expected and marker_count >= 3 and has_video:
        return "OK"
    if smoke_ok and (marker_count > 0 or has_video):
        return "PARTIAL"
    return "FAIL"


def collect_evidence() -> dict[str, Any]:
    smoke_fields = parse_markdown_fields(PIPELINE_REPORT)
    demo_fields = parse_markdown_fields(DEMO_REPORT)
    autofix_fields = parse_markdown_fields(AUTOFIX_REPORT)
    marker_metadata = load_marker_metadata()
    marker_summary = extract_marker_summary(marker_metadata)
    recording = latest_recording()
    smoke = extract_smoke_status(smoke_fields)
    result = classify_result(smoke, demo_fields, marker_summary, recording)

    return {
        "generated_at": datetime.now().isoformat(),
        "git": git_info(),
        "result": result,
        "smoke": smoke,
        "demo": {
            "diagnosis": demo_fields.get("diagnosis", autofix_fields.get("latest_diagnosis", "not found")),
            "success_criteria_passed": demo_fields.get("success_criteria_passed", autofix_fields.get("success", "not found")),
            "play_status": demo_fields.get("play_status", "not found"),
            "video_usefulness_score": demo_fields.get("video_usefulness_score", autofix_fields.get("score", "not found")),
            "studio_window_title": demo_fields.get("selected_studio_window_title", autofix_fields.get("selected_window", "not found")),
            "selected_hwnd": demo_fields.get("selected_hwnd", autofix_fields.get("selected_hwnd", "not found")),
            "selected_pid": demo_fields.get("selected_pid", autofix_fields.get("selected_pid", "not found")),
            "selected_root_hwnd": demo_fields.get("selected_root_hwnd", autofix_fields.get("selected_root_hwnd", "not found")),
            "f5_method": demo_fields.get("f5_method", autofix_fields.get("f5_method", "not found")),
            "f5_methods_attempted": demo_fields.get("f5_methods_attempted", autofix_fields.get("f5_methods_attempted", "not found")),
            "play_confirmation_evidence": demo_fields.get(
                "play_confirmation_evidence",
                autofix_fields.get("play_confirmation_evidence", "not found"),
            ),
        },
        "markers": marker_summary,
        "recording": recording,
        "reports": {
            "pipeline_smoke_report": str(PIPELINE_REPORT) if PIPELINE_REPORT.exists() else "not found",
            "demo_test_report": str(DEMO_REPORT) if DEMO_REPORT.exists() else "not found",
            "demo_autofix_report": str(AUTOFIX_REPORT) if AUTOFIX_REPORT.exists() else "not found",
            "roblox_latest_markers": str(MARKER_REPORT) if MARKER_REPORT.exists() else "not found",
            "place_structure_report": str(PLACE_REPORT) if PLACE_REPORT.exists() else "not found",
        },
        "generated_artifacts_not_committed": [
            "logs/*.md",
            "logs/*.json",
            "logs/recordings/*.mp4",
            "logs/screenshots/*",
            "build/*.rbxlx",
            "agentrouter-*.csv",
            "claude-agentrouter-*.csv",
        ],
    }


def write_markdown(evidence: dict[str, Any]) -> Path:
    git = evidence["git"]
    demo = evidence["demo"]
    markers = evidence["markers"]
    recording = evidence["recording"]
    reports = evidence["reports"]

    lines = [
        "# Demo Evidence Report",
        "",
        f"- generated_at: `{evidence['generated_at']}`",
        f"- result: `{evidence['result']}`",
        f"- branch: `{git['branch']}`",
        f"- commit: `{git['commit']}`",
        f"- commit_title: `{git['commit_title']}`",
        "",
        "## Summary",
        f"- smoke test: `{evidence['smoke']['result']}`",
        f"- smoke checks: `{evidence['smoke']['checks_passed']}`",
        f"- demo diagnosis: `{demo['diagnosis']}`",
        f"- demo success criteria: `{demo['success_criteria_passed']}`",
        f"- play status: `{demo['play_status']}`",
        f"- video usefulness score: `{demo['video_usefulness_score']}`",
        "",
        "## Studio Play Evidence",
        f"- Studio window title: `{demo['studio_window_title']}`",
        f"- selected hwnd: `{demo['selected_hwnd']}`",
        f"- selected pid: `{demo['selected_pid']}`",
        f"- selected root hwnd: `{demo['selected_root_hwnd']}`",
        f"- F5 method: `{demo['f5_method']}`",
        f"- F5 methods attempted: `{demo['f5_methods_attempted']}`",
        f"- Play confirmation evidence: `{demo['play_confirmation_evidence']}`",
        "",
        "## Runtime Markers",
        f"- project markers count: `{markers['project_markers_count']}`",
        f"- checked log files count: `{markers['checked_log_files_count']}`",
        f"- runtime diagnosis: `{markers['runtime_diagnosis']}`",
        f"- hub/playable confirmation: `{'Hub and playable runtime markers confirmed' if markers['hub_playable_confirmed'] else 'missing hub/playable runtime markers'}`",
        "",
        "### Important Markers Found",
    ]

    if markers["important_markers_found"]:
        for marker in markers["important_markers_found"]:
            lines.append(f"- `{marker}`")
    else:
        lines.append("- not found")

    lines.extend(["", "### Missing Expected Markers"])
    if markers["missing_expected_markers"]:
        for marker in markers["missing_expected_markers"]:
            lines.append(f"- `{marker}`")
    else:
        lines.append("- none")

    lines.extend(["", "### Missing Hub/Playable Flow Markers"])
    if markers["missing_hub_flow_markers"]:
        for marker in markers["missing_hub_flow_markers"]:
            lines.append(f"- `{marker}`")
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Video Artifact",
            f"- path: `{recording['path'] or 'not found'}`",
            f"- size bytes: `{recording['size_bytes']}`",
            f"- size MB: `{recording['size_mb']}`",
            f"- modified_at: `{recording['modified_at'] or 'not found'}`",
            "",
            "## Report Paths",
        ]
    )
    for name, path in reports.items():
        lines.append(f"- {name}: `{path}`")

    lines.extend(["", "## Working Tree Summary"])
    if git["working_tree_status"]:
        for item in git["working_tree_status"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- clean")

    lines.extend(["", "## Generated Artifacts Not Committed"])
    for item in evidence["generated_artifacts_not_committed"]:
        lines.append(f"- `{item}`")

    lines.extend(
        [
            "",
            "## Interpretation",
            "- `OK` means smoke passed, a non-trivial video artifact exists, and either demo diagnosis is OK or hub/playable runtime markers are fully confirmed.",
            "- `PARTIAL` means some evidence exists but at least one expected confirmation is missing.",
            "- `FAIL` means the current reports do not prove the demo pipeline worked.",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT_PATH


def main() -> int:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    evidence = collect_evidence()
    report_path = write_markdown(evidence)
    JSON_REPORT_PATH.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    print(f"Demo Evidence Report: {report_path}")
    print(f"Demo Evidence JSON: {JSON_REPORT_PATH}")
    print(f"Result: {evidence['result']}")
    print(f"Smoke: {evidence['smoke']['result']} ({evidence['smoke']['checks_passed']})")
    print(f"Demo diagnosis: {evidence['demo']['diagnosis']}")
    print(f"Markers: {evidence['markers']['project_markers_count']}")
    if evidence["recording"]["path"]:
        print(f"Video: {evidence['recording']['path']} ({evidence['recording']['size_bytes']} bytes)")
    else:
        print("Video: not found")
    return 0 if evidence["result"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())

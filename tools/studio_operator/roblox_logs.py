from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_MARKERS = [
    "[Server boot]",
    "[Client boot]",
    "[DemoDiagnostics] Init",
    "[DemoDiagnostics] ServerBootBeacon marked",
    "[DemoDiagnostics] PlayerSpawnBeacon marked",
    "[DemoDiagnostics] MapBuildBeacon marked",
    "[DemoDiagnostics] WaveLoopBeacon marked",
    "[Main] Demo runtime server boot confirmed",
    "[Main] Demo spectator bootstrap starting",
    "[Main] Demo spectator spawn ready",
    "[Main] Demo map build requested",
    "[Main] Demo wave loop requested",
    "[Main] Starting",
    "[Main] Completed",
    "[Main] Failed",
    "[PlayerSpawnService]",
    "[Client] Demo spectator",
    "[Client] Demo spectator camera activated",
    "[Client] Demo camera target found",
    "[Client] Demo camera path center found",
    "[RuntimeService]",
    "[MapService]",
    "[PathService]",
    "[WaveService]",
    "[TowerService]",
    "[EnemyService]",
    "[EconomyService]",
    "[Bridge]",
]

DIAGNOSTIC_MARKERS = [
    "error",
    "warn",
]

MARKERS = PROJECT_MARKERS + DIAGNOSTIC_MARKERS


def find_roblox_log_dirs() -> list[Path]:
    candidates = [
        Path.home() / "AppData" / "Local" / "Roblox" / "logs",
    ]
    return [path for path in candidates if path.exists()]


def _read_tail(path: Path, max_lines: int = 20000) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return lines[-max_lines:]


def collect_marker_details(logs_dir: Path, max_files: int = 5, minutes: int = 15) -> dict[str, Any]:
    now = time.time()
    cutoff = now - (minutes * 60)
    log_dirs = find_roblox_log_dirs()
    all_logs: list[Path] = []

    for log_dir in log_dirs:
        all_logs.extend(log_dir.glob("*.log"))

    fresh_logs = [path for path in all_logs if path.stat().st_mtime >= cutoff]
    candidates = sorted(fresh_logs or all_logs, key=lambda path: path.stat().st_mtime, reverse=True)[:max_files]

    checked_files: list[dict[str, Any]] = []
    matched_markers: list[str] = []
    project_markers: list[str] = []
    grouped_matches: list[dict[str, Any]] = []

    for candidate in candidates:
        stat = candidate.stat()
        checked_files.append(
            {
                "path": str(candidate),
                "name": candidate.name,
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size": stat.st_size,
            }
        )

        file_matches: list[str] = []
        for line in _read_tail(candidate):
            lowered = line.lower()
            if any(marker.lower() in lowered for marker in MARKERS):
                stripped = line.strip()
                file_matches.append(stripped)
                for marker in MARKERS:
                    if marker.lower() in lowered and marker not in matched_markers:
                        matched_markers.append(marker)
                    if marker.lower() in lowered and marker in PROJECT_MARKERS and marker not in project_markers:
                        project_markers.append(marker)

        grouped_matches.append(
            {
                "path": str(candidate),
                "name": candidate.name,
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "matches": file_matches[-80:],
            }
        )

    return {
        "log_dirs": [str(path) for path in log_dirs],
        "checked_files": checked_files,
        "matched_markers": matched_markers,
        "project_markers": project_markers,
        "project_markers_count": len(project_markers),
        "grouped_matches": grouped_matches,
        "minutes": minutes,
        "max_files": max_files,
    }


def collect_latest_markers(logs_dir: Path, output_path: Path, max_files: int = 20, minutes: int = 15) -> tuple[Path, list[str]]:
    details = collect_marker_details(logs_dir, max_files=max_files, minutes=minutes)
    lines = ["# Roblox Latest Markers", ""]

    if not details["log_dirs"]:
        lines.append("- Roblox logs directory not found.")
    else:
        lines.append("## Checked Log Files")
        if details["checked_files"]:
            for item in details["checked_files"]:
                lines.append(f"- `{item['path']}`")
                lines.append(f"  - modified: `{item['modified_at']}`")
                lines.append(f"  - size: `{item['size']}` bytes")
        else:
            lines.append("- No Roblox Studio log files found.")

        lines.extend(["", "## Matched Markers"])
        if details["matched_markers"]:
            for marker in details["matched_markers"]:
                lines.append(f"- `{marker}`")
        else:
            lines.append("- No matching markers found in the selected Roblox Studio logs.")

        lines.extend(["", "## Project Runtime Marker Summary"])
        lines.append(f"- project markers found: `{details['project_markers_count']}`")
        if details["project_markers"]:
            for marker in details["project_markers"]:
                lines.append(f"- `{marker}`")
        else:
            lines.append("- No project runtime markers found. Possible causes: Play did not start, logs are in another file, server script failed before print, or wrong place opened.")

        lines.extend(["", "## Matches By File"])
        for group in details["grouped_matches"]:
            lines.append(f"### {group['name']}")
            lines.append(f"- path: `{group['path']}`")
            lines.append(f"- modified: `{group['modified_at']}`")
            if group["matches"]:
                for line in group["matches"]:
                    lines.append(f"- `{line}`")
            else:
                lines.append("- No matching marker lines in this file.")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    metadata_path = logs_dir / "roblox_latest_markers.json"
    metadata_path.write_text(json.dumps(details, indent=2), encoding="utf-8")
    return output_path, details["matched_markers"]


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    logs_dir = project_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    report_path, _ = collect_latest_markers(logs_dir, logs_dir / "roblox_latest_markers.md", max_files=20)
    print(report_path)

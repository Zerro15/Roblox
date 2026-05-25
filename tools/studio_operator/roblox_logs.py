from __future__ import annotations

from pathlib import Path


MARKERS = [
    "[Server boot]",
    "[RuntimeService]",
    "[EconomyService]",
    "[EnemyService]",
    "[TowerService]",
    "[WaveService]",
    "[Main]",
    "[Client boot]",
    "[Bridge]",
    "[Main] Demo spectator bootstrap starting",
    "[Main] Demo spectator spawn ready",
    "[Main] Demo map build requested",
    "[Main] Demo wave loop requested",
    "[PlayerSpawnService] Demo spectator mode enabled",
    "[PlayerSpawnService] CharacterAutoLoads disabled",
    "[PlayerSpawnService] Player configured as demo spectator",
    "[PlayerSpawnService] Character hidden for demo spectator mode",
    "[Client] Demo spectator camera starting",
    "[Client] Demo spectator camera activated",
    "error",
    "warn",
]


def collect_latest_markers(logs_dir: Path, output_path: Path, max_files: int = 5) -> tuple[Path, list[str]]:
    roblox_logs_dir = Path.home() / "AppData" / "Local" / "Roblox" / "logs"
    excerpts: list[str] = []
    matched_markers: list[str] = []

    if not roblox_logs_dir.exists():
        output_path.write_text("# Roblox Latest Markers\n\n- Roblox logs directory not found.\n", encoding="utf-8")
        return output_path, matched_markers

    candidates = sorted(roblox_logs_dir.glob("*.log"), key=lambda path: path.stat().st_mtime, reverse=True)[:max_files]

    for candidate in candidates:
        try:
            content = candidate.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        file_matches: list[str] = []
        for line in content[-600:]:
            lowered = line.lower()
            if any(marker.lower() in lowered for marker in MARKERS):
                file_matches.append(line.strip())
                for marker in MARKERS:
                    if marker.lower() in lowered and marker not in matched_markers:
                        matched_markers.append(marker)

        if file_matches:
            excerpts.append(f"## {candidate.name}")
            excerpts.extend(f"- `{line}`" for line in file_matches[-50:])

    lines = ["# Roblox Latest Markers", ""]
    if excerpts:
        lines.extend(excerpts)
    else:
        lines.append("- No matching markers found in the newest Roblox Studio logs.")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path, matched_markers


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    logs_dir = project_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    report_path, _ = collect_latest_markers(logs_dir, logs_dir / "roblox_latest_markers.md")
    print(report_path)

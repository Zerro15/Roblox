from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import pygetwindow as gw


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"

REQUIRED_FILES = [
    PROJECT_ROOT / "default.project.json",
    PROJECT_ROOT / "scripts" / "start_bridge.ps1",
    PROJECT_ROOT / "scripts" / "start_rojo.ps1",
    PROJECT_ROOT / "src" / "server" / "Main.server.lua",
    PROJECT_ROOT / "src" / "server" / "BridgeClient.server.lua",
]


def ensure_logs_dir() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    (LOGS_DIR / "screenshots").mkdir(parents=True, exist_ok=True)


def run_command(command: list[str], cwd: Path | None = None) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd or PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return False, str(exc)

    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part).strip()
    return completed.returncode == 0, output


def get_rojo_command() -> list[str] | None:
    ok, _ = run_command(["rojo", "--version"])
    if ok:
        return ["rojo"]

    local_rojo = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Rojo" / "rojo.exe"
    if local_rojo.exists():
        return [str(local_rojo)]

    return None


def find_studio_exe() -> Path | None:
    versions_dir = Path(os.environ["LOCALAPPDATA"]) / "Roblox" / "Versions"
    if not versions_dir.exists():
        return None

    candidates = sorted(
        versions_dir.rglob("RobloxStudioBeta.exe"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def plugin_path() -> Path:
    return Path(os.environ["LOCALAPPDATA"]) / "Roblox" / "Plugins" / "Rojo.rbxm"


def built_place_path() -> Path:
    return PROJECT_ROOT / "build" / "game.rbxlx"


def find_windows() -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for window in gw.getAllWindows():
        title = (window.title or "").strip()
        if not title:
            continue
        lowered = title.lower()
        if any(token in lowered for token in ("roblox", "rojo", ".rbxlx")):
            matches.append(
                {
                    "title": title,
                    "left": window.left,
                    "top": window.top,
                    "width": window.width,
                    "height": window.height,
                    "isMinimized": window.isMinimized,
                    "isMaximized": window.isMaximized,
                }
            )
    return matches

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = PROJECT_ROOT / "logs"
STATE_PATH = LOGS_DIR / "studio_operator_state.json"

DEFAULT_STATE: dict[str, Any] = {
    "started_at": None,
    "last_run_at": None,
    "project_root": str(PROJECT_ROOT),
    "bridge_pid": None,
    "rojo_pid": None,
    "studio_pid": None,
    "launched_processes": [],
    "screenshots": [],
    "reports": [],
    "last_build_path": None,
    "last_flow_status": None,
    "last_active_window": None,
    "last_error": None,
}


def _ensure_logs_dir() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> dict[str, Any]:
    _ensure_logs_dir()
    if not STATE_PATH.exists():
        state = dict(DEFAULT_STATE)
        now = datetime.now().isoformat()
        state["started_at"] = now
        state["last_run_at"] = now
        save_state(state)
        return state

    try:
        loaded = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        loaded = {}

    state = dict(DEFAULT_STATE)
    state.update(loaded)
    if not state["started_at"]:
        state["started_at"] = datetime.now().isoformat()
    state["last_run_at"] = datetime.now().isoformat()
    return state


def save_state(state: dict[str, Any]) -> Path:
    _ensure_logs_dir()
    state["project_root"] = str(PROJECT_ROOT)
    state["last_run_at"] = datetime.now().isoformat()
    if not state.get("started_at"):
        state["started_at"] = state["last_run_at"]
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return STATE_PATH


def register_process(state: dict[str, Any], name: str, pid: int, command: str) -> None:
    existing = [item for item in state.get("launched_processes", []) if item.get("pid") != pid]
    existing.append(
        {
            "name": name,
            "pid": pid,
            "command": command,
            "registered_at": datetime.now().isoformat(),
        }
    )
    state["launched_processes"] = existing
    field_name = f"{name}_pid"
    if field_name in state:
        state[field_name] = pid


def unregister_process(state: dict[str, Any], pid: int) -> None:
    state["launched_processes"] = [item for item in state.get("launched_processes", []) if item.get("pid") != pid]
    for key in ("bridge_pid", "rojo_pid", "studio_pid"):
        if state.get(key) == pid:
            state[key] = None


def add_screenshot(state: dict[str, Any], path: str, label: str) -> None:
    state.setdefault("screenshots", []).append(
        {
            "path": path,
            "label": label,
            "captured_at": datetime.now().isoformat(),
        }
    )


def add_report(state: dict[str, Any], path: str, label: str) -> None:
    state.setdefault("reports", []).append(
        {
            "path": path,
            "label": label,
            "written_at": datetime.now().isoformat(),
        }
    )


def update_status(state: dict[str, Any], status: str, error: str | None = None) -> None:
    state["last_flow_status"] = status
    state["last_error"] = error

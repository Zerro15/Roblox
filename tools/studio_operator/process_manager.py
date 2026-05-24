from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import psutil

from operator_state import register_process, unregister_process


CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def list_relevant_processes() -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for proc in psutil.process_iter(["pid", "name", "cmdline", "exe"]):
        try:
            name = (proc.info.get("name") or "").lower()
            cmdline = " ".join(proc.info.get("cmdline") or [])
            exe = (proc.info.get("exe") or "")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        lowered = f"{name} {cmdline} {exe}".lower()
        if any(token in lowered for token in ("rojo", "bridge_server.py", "robloxstudiobeta.exe", "game.rbxlx")):
            matches.append(
                {
                    "pid": proc.pid,
                    "name": proc.info.get("name"),
                    "cmdline": cmdline,
                    "exe": exe,
                }
            )
    return matches


def is_process_alive(pid: int | None) -> bool:
    if not pid:
        return False
    return psutil.pid_exists(pid)


def start_process_once(
    state: dict[str, Any],
    name: str,
    command: list[str],
    cwd: Path,
    stdout_path: Path | None = None,
    stderr_path: Path | None = None,
) -> int | None:
    field_name = f"{name}_pid"
    existing_pid = state.get(field_name)
    if is_process_alive(existing_pid):
        return existing_pid

    if name == "studio":
        for proc in psutil.process_iter(["name", "cmdline", "exe"]):
            try:
                proc_name = (proc.info.get("name") or "").lower()
                cmdline = " ".join(proc.info.get("cmdline") or []).lower()
                exe = (proc.info.get("exe") or "").lower()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            if "robloxstudiobeta.exe" in exe or proc_name == "robloxstudiobeta.exe":
                if "game.rbxlx" in cmdline or not cmdline:
                    return proc.pid

    stdout_handle = open(stdout_path, "a", encoding="utf-8") if stdout_path else subprocess.DEVNULL
    stderr_handle = open(stderr_path, "a", encoding="utf-8") if stderr_path else subprocess.DEVNULL

    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        stdout=stdout_handle,
        stderr=stderr_handle,
        creationflags=CREATE_NO_WINDOW,
    )
    register_process(state, name, process.pid, " ".join(command))
    return process.pid


def stop_process_by_pid(state: dict[str, Any], pid: int) -> bool:
    if not is_process_alive(pid):
        unregister_process(state, pid)
        return False

    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=8)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
        try:
            proc.kill()
        except Exception:  # noqa: BLE001
            return False
    unregister_process(state, pid)
    return True


def cleanup_own_processes(state: dict[str, Any]) -> list[int]:
    stopped: list[int] = []
    for entry in list(state.get("launched_processes", [])):
        pid = entry.get("pid")
        if not pid:
            continue
        if stop_process_by_pid(state, pid):
            stopped.append(pid)
    return stopped


def cleanup_duplicate_own_processes(state: dict[str, Any]) -> list[int]:
    stopped: list[int] = []
    by_name: dict[str, list[dict[str, Any]]] = {}
    for entry in state.get("launched_processes", []):
        by_name.setdefault(entry.get("name", "unknown"), []).append(entry)

    for name, entries in by_name.items():
        alive_entries = [entry for entry in entries if is_process_alive(entry.get("pid"))]
        if len(alive_entries) <= 1:
            continue

        alive_entries.sort(key=lambda item: item.get("registered_at", ""))
        for duplicate in alive_entries[:-1]:
            pid = duplicate.get("pid")
            if pid and stop_process_by_pid(state, pid):
                stopped.append(pid)

        latest_pid = alive_entries[-1].get("pid")
        field_name = f"{name}_pid"
        if field_name in state:
            state[field_name] = latest_pid

    return stopped


def detect_foreign_processes(state: dict[str, Any]) -> list[dict[str, Any]]:
    own_pids = {entry.get("pid") for entry in state.get("launched_processes", [])}
    return [item for item in list_relevant_processes() if item.get("pid") not in own_pids]

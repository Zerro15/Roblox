from __future__ import annotations

import argparse
import ctypes
import json
import time
from ctypes import wintypes
from typing import Any

import pyautogui


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

SW_RESTORE = 9
SW_SHOW = 5
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_F5 = 0x74

DISALLOWED_TOKENS = (
    "autorecovery",
    "autosaves",
    "installer",
    "download and install",
    "setup",
    "updater",
    "browser",
    "яндекс",
    "powershell",
    "codex",
    "claude",
    "chatgpt",
)


def _window_text(hwnd: int) -> str:
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return ""
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value.strip()


def _window_rect(hwnd: int) -> dict[str, int]:
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return {
        "left": int(rect.left),
        "top": int(rect.top),
        "right": int(rect.right),
        "bottom": int(rect.bottom),
        "width": int(rect.right - rect.left),
        "height": int(rect.bottom - rect.top),
    }


def _window_pid(hwnd: int) -> int:
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return int(pid.value)


def _is_disallowed_title(title: str) -> bool:
    lowered = title.lower()
    is_target = "game.rbxlx" in lowered and "roblox studio" in lowered
    if is_target and "build" in lowered:
        return False
    return any(token in lowered for token in DISALLOWED_TOKENS)


def _is_target_title(title: str) -> bool:
    lowered = title.lower()
    if _is_disallowed_title(title):
        return False
    return "game.rbxlx" in lowered and "roblox studio" in lowered


def list_windows() -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []

    def callback(hwnd: int, _: int) -> bool:
        if not user32.IsWindowVisible(hwnd):
            return True
        title = _window_text(hwnd)
        if not title:
            return True
        rect = _window_rect(hwnd)
        if rect["width"] <= 0 or rect["height"] <= 0:
            return True
        windows.append(
            {
                "hwnd": int(hwnd),
                "title": title,
                "rect": rect,
                "pid": _window_pid(hwnd),
            }
        )
        return True

    user32.EnumWindows(EnumWindowsProc(callback), 0)
    return windows


def _score_window(window: dict[str, Any]) -> tuple[int, int]:
    title = window["title"].lower()
    score = 0
    if "game.rbxlx" in title:
        score += 300
    if "build" in title:
        score += 200
    if "roblox studio" in title:
        score += 100
    if ".rbxlx" in title:
        score += 50
    if _is_disallowed_title(window["title"]):
        score -= 5000
    rect = window["rect"]
    area = max(rect["width"], 0) * max(rect["height"], 0)
    return score, area


def find_target_studio_window() -> dict[str, Any] | None:
    candidates = [window for window in list_windows() if _is_target_title(window["title"])]
    if not candidates:
        return None
    return sorted(candidates, key=_score_window, reverse=True)[0]


def get_foreground_window_info() -> dict[str, Any]:
    hwnd = int(user32.GetForegroundWindow())
    if not hwnd:
        return {"hwnd": 0, "title": "", "pid": 0, "rect": {}}
    return {
        "hwnd": hwnd,
        "title": _window_text(hwnd),
        "pid": _window_pid(hwnd),
        "rect": _window_rect(hwnd),
    }


def _is_foreground_target(hwnd: int) -> bool:
    foreground = get_foreground_window_info()
    if foreground["hwnd"] == int(hwnd):
        return True
    return _is_target_title(foreground.get("title", ""))


def force_foreground(hwnd: int) -> dict[str, Any]:
    before = get_foreground_window_info()
    errors: list[str] = []

    try:
        user32.ShowWindow(hwnd, SW_RESTORE)
        user32.ShowWindow(hwnd, SW_SHOW)
        user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))

    if not _is_foreground_target(hwnd):
        try:
            foreground_hwnd = int(user32.GetForegroundWindow())
            current_thread_id = int(kernel32.GetCurrentThreadId())
            target_thread_id = int(user32.GetWindowThreadProcessId(hwnd, None))
            foreground_thread_id = int(user32.GetWindowThreadProcessId(foreground_hwnd, None)) if foreground_hwnd else 0

            if foreground_thread_id:
                user32.AttachThreadInput(current_thread_id, foreground_thread_id, True)
            user32.AttachThreadInput(current_thread_id, target_thread_id, True)
            user32.BringWindowToTop(hwnd)
            user32.SetForegroundWindow(hwnd)
            user32.SetFocus(hwnd)
            time.sleep(0.5)
            user32.AttachThreadInput(current_thread_id, target_thread_id, False)
            if foreground_thread_id:
                user32.AttachThreadInput(current_thread_id, foreground_thread_id, False)
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    after = get_foreground_window_info()
    return {
        "foreground_before": before,
        "foreground_after": after,
        "foreground_confirmed": _is_foreground_target(hwnd),
        "errors": errors,
    }


def press_f5_foreground() -> bool:
    pyautogui.press("f5")
    return True


def send_f5_to_hwnd(hwnd: int) -> dict[str, Any]:
    result = {
        "method": "hwnd_postmessage",
        "success": False,
        "error": "",
    }
    try:
        down = user32.PostMessageW(hwnd, WM_KEYDOWN, VK_F5, 0)
        time.sleep(0.05)
        up = user32.PostMessageW(hwnd, WM_KEYUP, VK_F5, 0)
        result["success"] = bool(down and up)
        if not result["success"]:
            result["error"] = "PostMessageW returned false."
    except Exception as exc:  # noqa: BLE001
        result["error"] = str(exc)
    return result


def force_play() -> dict[str, Any]:
    result: dict[str, Any] = {
        "selected_title": "",
        "selected_hwnd": 0,
        "selected_rect": {},
        "selected_pid": 0,
        "foreground_before": get_foreground_window_info(),
        "foreground_after": {},
        "foreground_confirmed": False,
        "f5_method": "skipped",
        "f5_pressed": False,
        "error": "",
    }

    target = find_target_studio_window()
    if not target:
        result["error"] = "No eligible build/game.rbxlx Roblox Studio window found."
        return result

    hwnd = int(target["hwnd"])
    result["selected_title"] = target["title"]
    result["selected_hwnd"] = hwnd
    result["selected_rect"] = target["rect"]
    result["selected_pid"] = target["pid"]

    focus_result = force_foreground(hwnd)
    result.update(focus_result)

    if result["foreground_confirmed"]:
        try:
            press_f5_foreground()
            result["f5_method"] = "foreground_pyautogui"
            result["f5_pressed"] = True
            return result
        except Exception as exc:  # noqa: BLE001
            result["error"] = str(exc)

    fallback = send_f5_to_hwnd(hwnd)
    result["f5_method"] = fallback["method"]
    result["f5_pressed"] = bool(fallback["success"])
    if fallback["error"]:
        result["error"] = fallback["error"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Windows-level Roblox Studio Play controller.")
    parser.add_argument("--mode", choices=("status", "focus", "press-f5", "force-play"), required=True)
    args = parser.parse_args()

    target = find_target_studio_window()
    if args.mode == "status":
        payload = {
            "target": target,
            "foreground": get_foreground_window_info(),
        }
    elif args.mode == "focus":
        payload = {"target": target}
        if target:
            payload.update(force_foreground(int(target["hwnd"])))
        else:
            payload["error"] = "No eligible target window found."
    elif args.mode == "press-f5":
        foreground = get_foreground_window_info()
        payload = {"foreground": foreground, "f5_pressed": False, "error": ""}
        if _is_target_title(foreground.get("title", "")):
            payload["f5_pressed"] = press_f5_foreground()
            payload["f5_method"] = "foreground_pyautogui"
        else:
            payload["error"] = "Foreground is not the target Roblox Studio window."
            payload["f5_method"] = "skipped"
    else:
        payload = force_play()

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

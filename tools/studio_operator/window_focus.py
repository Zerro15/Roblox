from __future__ import annotations

import time
from typing import Any

import pygetwindow as gw


PRIMARY_KEYWORDS = (
    "roblox studio",
    ".rbxlx",
    "game.rbxlx",
    "new-chat",
)

DISALLOWED_KEYWORDS = (
    "installer",
)


def list_windows() -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []
    for window in gw.getAllWindows():
        title = (window.title or "").strip()
        if not title:
            continue

        windows.append(
            {
                "title": title,
                "left": window.left,
                "top": window.top,
                "width": window.width,
                "height": window.height,
                "isMinimized": window.isMinimized,
                "isMaximized": window.isMaximized,
                "window": window,
            }
        )

    return windows


def find_studio_windows() -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for item in list_windows():
        lowered = item["title"].lower()
        if any(keyword in lowered for keyword in PRIMARY_KEYWORDS):
            matches.append(item)
    return matches


def _score_window(item: dict[str, Any]) -> tuple[int, int]:
    title = item["title"].lower()
    score = 0

    if "game.rbxlx" in title:
        score += 100
    if ".rbxlx" in title:
        score += 80
    if "new-chat" in title:
        score += 60
    if "roblox studio" in title:
        score += 40
    if any(keyword in title for keyword in DISALLOWED_KEYWORDS):
        score -= 1000
    if item["left"] <= -30000 or item["top"] <= -30000:
        score -= 200
    if item["isMinimized"]:
        score -= 50

    area = max(item["width"], 0) * max(item["height"], 0)
    return score, area


def choose_best_studio_window() -> dict[str, Any] | None:
    candidates = find_studio_windows()
    if not candidates:
        return None

    ranked = sorted(candidates, key=_score_window, reverse=True)
    return ranked[0]


def get_active_window_title() -> str:
    try:
        active = gw.getActiveWindow()
    except Exception:  # noqa: BLE001
        return ""

    if active is None:
        return ""

    return (active.title or "").strip()


def is_active_studio_window() -> bool:
    title = get_active_window_title().lower()
    if not title:
        return False
    if any(keyword in title for keyword in DISALLOWED_KEYWORDS):
        return False
    return any(keyword in title for keyword in ("roblox studio", "game.rbxlx", ".rbxlx", "new-chat"))


def focus_window(window: Any) -> bool:
    try:
        if getattr(window, "isMinimized", False):
            window.restore()
            time.sleep(1)
    except Exception:  # noqa: BLE001
        pass

    try:
        window.activate()
    except Exception:  # noqa: BLE001
        pass

    time.sleep(1.5)
    if is_active_studio_window():
        return True

    try:
        window.maximize()
        time.sleep(1.5)
    except Exception:  # noqa: BLE001
        pass

    return is_active_studio_window()


def focus_studio_window() -> dict[str, Any]:
    best = choose_best_studio_window()
    before_title = get_active_window_title()

    if best is None:
        return {
            "success": False,
            "before_title": before_title,
            "after_title": get_active_window_title(),
            "chosen_title": None,
            "reason": "No Studio-like window found.",
        }

    success = focus_window(best["window"])
    after_title = get_active_window_title()

    return {
        "success": success,
        "before_title": before_title,
        "after_title": after_title,
        "chosen_title": best["title"],
        "reason": None if success else "Foreground window could not be confirmed as Roblox Studio.",
    }

from __future__ import annotations

from typing import Iterable

import pygetwindow as gw


WINDOW_KEYWORDS = (
    "Roblox",
    "Roblox Studio",
    "Rojo",
)


def find_windows(keywords: Iterable[str] = WINDOW_KEYWORDS) -> list[dict]:
    matches: list[dict] = []
    normalized = tuple(keyword.lower() for keyword in keywords)

    for window in gw.getAllWindows():
        title = (window.title or "").strip()
        if not title:
            continue

        lowered = title.lower()
        if any(keyword in lowered for keyword in normalized):
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


def print_windows() -> None:
    windows = find_windows()
    if not windows:
        print("No matching windows found.")
        return

    for window in windows:
        print(
            f"{window['title']} | pos=({window['left']},{window['top']}) "
            f"size=({window['width']}x{window['height']}) "
            f"minimized={window['isMinimized']} maximized={window['isMaximized']}"
        )


if __name__ == "__main__":
    print_windows()

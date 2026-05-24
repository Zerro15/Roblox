from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pyautogui


def take_screenshot(logs_dir: Path) -> Path:
    screenshot_dir = logs_dir / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = screenshot_dir / f"screenshot_{timestamp}.png"

    image = pyautogui.screenshot()
    image.save(output_path)

    print(output_path)
    return output_path


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    take_screenshot(project_root / "logs")

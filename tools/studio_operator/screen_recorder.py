from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any

import imageio.v2 as imageio
import mss
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = PROJECT_ROOT / "logs"
RECORDINGS_DIR = LOGS_DIR / "recordings"


def record_screen(output_path: Path | None = None, duration_seconds: int = 60, fps: int = 10) -> dict[str, Any]:
	RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
	duration_seconds = max(1, min(duration_seconds, 60))
	fps = max(1, min(fps, 30))

	if output_path is None:
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
		output_path = RECORDINGS_DIR / f"demo_recording_{timestamp}.mp4"

	frame_interval = 1.0 / fps
	frame_count = max(1, duration_seconds * fps)
	fallback_frames: list[str] = []

	try:
		with mss.mss() as sct:
			monitor = sct.monitors[1]
			with imageio.get_writer(output_path, fps=fps, codec="libx264", quality=6) as writer:
				for frame_index in range(frame_count):
					start_time = time.perf_counter()
					raw_frame = sct.grab(monitor)
					frame = np.array(raw_frame)
					writer.append_data(frame[:, :, :3])
					elapsed = time.perf_counter() - start_time
					sleep_time = max(0.0, frame_interval - elapsed)
					if sleep_time > 0:
						time.sleep(sleep_time)
	except Exception as exc:  # noqa: BLE001
		return {
			"success": False,
			"recording_path": str(output_path),
			"error": str(exc),
			"fallback_frames": fallback_frames,
		}

	return {
		"success": output_path.exists(),
		"recording_path": str(output_path),
		"error": None,
		"fallback_frames": fallback_frames,
	}


if __name__ == "__main__":
	result = record_screen()
	print(result["recording_path"])

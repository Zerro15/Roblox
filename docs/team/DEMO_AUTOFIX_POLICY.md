# Demo Autofix Policy

## Goal

The demo autofix loop is a bounded diagnostic helper for Roblox Studio demo recording. It can build the project, run the assisted demo recorder, inspect reports/logs/video metadata, classify what failed, and stop with a clear report.

It is intentionally conservative. It does not try to brute-force Studio, delete files, merge pull requests, or change core gameplay systems.

## Max Attempts

The loop is capped at 3 attempts per run.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1 -MaxAttempts 3
```

For a lightweight check:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1 -DiagnoseOnly
```

## Success Criteria

A demo run is considered successful when:

- Rojo build passes.
- An MP4 recording exists.
- F5 was pressed.
- `auto_play_status` contains `F5_PRESSED`.
- At least 3 project runtime markers are found.
- Video usefulness score is at least `3/5`.

Score `4/5` or higher is considered a strong demo.

## Supported Diagnosis Values

- `BUILD_FAILED`
- `STUDIO_WINDOW_NOT_VISIBLE`
- `FOCUS_FAILED`
- `F5_NOT_PRESSED`
- `PLAY_NOT_CONFIRMED`
- `SERVER_BOOT_NOT_FOUND`
- `CLIENT_BOOT_NOT_FOUND`
- `DEMO_CAMERA_NOT_FOUND`
- `PLAYERSPAWN_NOT_FOUND`
- `MAP_NOT_BUILT`
- `WAVE_NOT_STARTED`
- `VIDEO_NOT_RECORDED`
- `VIDEO_TOO_SMALL`
- `ONLY_WARN_ERROR_MARKERS`
- `PLAY_LOGS_NOT_CAPTURED_OR_RUNTIME_FAILED`
- `UNKNOWN_FAILURE`

## Allowed Fixes

- Improve diagnosis and reports.
- Improve Roblox log aggregation.
- Retry the safe assisted demo flow.
- Use longer recording duration inside the autofix loop if the video is too small.
- Add or strengthen demo/runtime/test markers when a missing marker is clearly the problem.

## Forbidden Actions

- No force push.
- No automatic PR merge.
- No deletion of files, branches, logs, screenshots, recordings, or Studio projects.
- No killing Roblox Studio processes.
- No committing `build/`, `logs/`, screenshots, recordings, MP4 files, `.env`, `.venv`, or `.claude`.
- No changes to core gameplay economy, balance, or tower/enemy mechanics.
- No infinite loops.

## Reports

Primary reports:

- `logs/demo_autofix_report.md`
- `logs/demo_test_report.md`
- `logs/roblox_latest_markers.md`

If the diagnosis is `ONLY_WARN_ERROR_MARKERS` or `PLAY_LOGS_NOT_CAPTURED_OR_RUNTIME_FAILED`, inspect `logs/roblox_latest_markers.md` first. It lists the checked Roblox log files and explains whether project runtime markers were found.

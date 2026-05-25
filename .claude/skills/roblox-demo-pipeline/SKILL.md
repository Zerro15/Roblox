# Roblox Demo Pipeline Skill

**Purpose:** Automate Roblox Studio demo/video/testing pipeline with honest pass/fail reporting.

**Scope:** Studio automation, video recording, runtime marker collection, report generation.

---

## Quick Start

### Smoke Test (Fast Validation)
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\pipeline_smoke_test.ps1
```
Validates: build, Rojo, venv, reports, recordings, server markers.
Expected: 21/22 checks passing (server_markers may fail until full demo runs).

### Full Demo Loop (Complete Verification)
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1
```
Executes: build → open Studio → press F5 → record video → collect logs → generate report.
Expected: demo_autofix_report.md with diagnosis and video artifact.

---

## Key Files to Inspect

### Reports & Artifacts
- `logs/pipeline_smoke_report.md` — smoke test results (21 checks)
- `logs/demo_test_report.md` — demo execution report (F5, video, markers)
- `logs/demo_autofix_report.md` — autofix loop diagnosis (PASS/FAIL/PARTIAL)
- `logs/roblox_latest_markers.md` — runtime markers found in Roblox logs
- `logs/recordings/demo_recording_*.mp4` — video artifact

### Source Code
- `tools/studio_operator/pipeline_smoke_test.py` — 22-check smoke test
- `tools/studio_operator/demo_test_player.py` — demo automation (850 lines)
- `tools/studio_operator/demo_autofix_loop.py` — bounded autofix with diagnosis
- `tools/studio_operator/roblox_logs.py` — log collection (scans 20 recent files)

### Configuration
- `default.project.json` — Rojo build config
- `scripts/build_place.ps1` — Rojo build wrapper
- `scripts/demo_autofix_loop.ps1` — PowerShell orchestrator

---

## Runtime Markers

### Server-Side (Lua warn/print in Main.server.lua)
```
[Server boot]
[DemoDiagnostics] Init
[DemoDiagnostics] ServerBootBeacon marked
[DemoDiagnostics] PlayerSpawnBeacon marked
[DemoDiagnostics] MapBuildBeacon marked
[DemoDiagnostics] WaveLoopBeacon marked
[RuntimeService]
[MapService]
[WaveService]
```

### Client-Side (Lua warn/print in Main.client.lua)
```
[Client boot]
[Client] Demo spectator
[Client] Demo spectator camera activated
[Client] Demo camera target found
```

### Diagnostic Markers
```
warn
error
[Bridge]
```

---

## Log Collection Strategy

**File:** `tools/studio_operator/roblox_logs.py`

**Behavior:**
1. Scans `C:\Users\Bogdan\AppData\Local\Roblox\logs\` for `*.log` files
2. Checks up to 20 most recent files (by modification time)
3. Searches last 20,000 lines of each file for markers
4. Writes results to `logs/roblox_latest_markers.md`
5. Saves metadata to `logs/roblox_latest_markers.json`

**Why 20 files?**
- Studio creates new log files for each session
- Server-side output may be in older log files than client-side
- Scanning 20 files covers ~1 hour of Studio activity

**If server markers still missing:**
- Inspect `logs/roblox_latest_markers.md` "Checked Log Files" section
- Verify which files were scanned and their timestamps
- Check if server-side Lua actually executed (read Main.server.lua)
- Run full demo_autofix_loop again with fresh Studio session

---

## Diagnosis Rules

**PASS Criteria:**
- Build succeeds
- Studio window visible and foreground
- F5 pressed (AUTO_PLAY_FORCE_CONTROLLER_F5_PRESSED)
- Video recorded (≥0.5 MB)
- All 6 diagnostic beacons found:
  - `[DemoDiagnostics] Init`
  - `[DemoDiagnostics] ServerBootBeacon marked`
  - `[DemoDiagnostics] PlayerSpawnBeacon marked`
  - `[DemoDiagnostics] MapBuildBeacon marked`
  - `[DemoDiagnostics] WaveLoopBeacon marked`
  - `[Client] Demo spectator camera activated`
- Gameplay confirmed (WaveService/TowerService/EnemyService markers)
- Video score ≥3/5

**PARTIAL_RUNTIME_CONFIRMED:**
- F5 pressed and video recorded
- Some runtime markers found (3-5 markers)
- Missing server-side markers or diagnostics
- **Action:** Inspect which beacons are missing; improve server-side Lua or log collection

**FAIL Diagnosis:**
- BUILD_FAILED — Rojo build error
- STUDIO_WINDOW_NOT_VISIBLE — Studio minimized/offscreen
- F5_NOT_PRESSED — Auto-play failed
- RUNTIME_MARKERS_NOT_CAPTURED — No markers in logs despite F5 pressed
- SERVER_BOOT_NOT_FOUND — [Server boot] missing
- CLIENT_BOOT_NOT_FOUND — [Client boot] missing

---

## Honest Reporting Rules

**NEVER:**
- ❌ Fake video size or duration
- ❌ Invent markers that weren't in logs
- ❌ Report PASS when markers are missing
- ❌ Skip log collection or marker verification

**ALWAYS:**
- ✅ Report actual video file size from disk
- ✅ Report actual markers found in Roblox logs
- ✅ Report PARTIAL if some markers missing
- ✅ Show which log files were scanned
- ✅ Explain why markers may be missing (e.g., "Server output may be in older log file")

---

## Artifact Paths

All artifacts are generated in `logs/` directory:

```
logs/
├── pipeline_smoke_report.md          # Smoke test results
├── demo_test_report.md               # Demo execution report
├── demo_autofix_report.md            # Autofix diagnosis
├── roblox_latest_markers.md          # Markers found in logs
├── roblox_latest_markers.json        # Markers metadata
├── recordings/
│   └── demo_recording_*.mp4          # Video artifact
└── screenshots/
    ├── screenshot_*.png              # Before/after screenshots
    └── ...
```

---

## Debugging Server Markers

**If server markers are missing:**

1. **Check if server code runs:**
   - Open `src/server/Main.server.lua`
   - Verify `warn("[Server boot]")` is at top
   - Verify services are initialized

2. **Verify Studio Play mode:**
   - Check `logs/demo_test_report.md` for `f5_pressed: True`
   - Check `auto_play_status: AUTO_PLAY_FORCE_CONTROLLER_F5_PRESSED`
   - Verify video was recorded (size > 0.5 MB)

3. **Inspect Roblox logs:**
   - Check `logs/roblox_latest_markers.md` "Checked Log Files" section
   - Verify files are from recent Studio sessions
   - Look for any server-side output (even if not our markers)

4. **Improve log collection:**
   - Increase `max_files` parameter in `roblox_logs.py` (currently 20)
   - Check if RCC subprocess logs are in separate location
   - Add diagnostic section to marker report showing which files scanned

5. **Rerun demo:**
   - Close all Studio instances
   - Run `powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1`
   - Wait for new report

---

## Final Response Checklist

When reporting demo/smoke test results, include:

- [ ] Command run (smoke_test.ps1 or demo_autofix_loop.ps1)
- [ ] Build status (ok/failed)
- [ ] Studio window (visible/not visible)
- [ ] F5 pressed (yes/no, with method)
- [ ] Video recorded (yes/no, size in MB)
- [ ] Markers found (count and list)
- [ ] Diagnosis (OK/PARTIAL_RUNTIME_CONFIRMED/FAIL_*)
- [ ] Artifact paths (report, video, screenshots)
- [ ] Next action (commit/improve/rerun)

---

## Example: Running Full Demo

```powershell
# 1. Run full demo loop
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1

# 2. Wait ~2 minutes for completion

# 3. Check report
cat logs/demo_autofix_report.md

# 4. If PARTIAL_RUNTIME_CONFIRMED, inspect markers
cat logs/roblox_latest_markers.md

# 5. If server markers missing, improve and rerun
# (e.g., increase max_files, check server Lua, etc.)

# 6. When ready to commit, use safe-git-review skill
```

---

## See Also

- `CLAUDE.md` — Claude workflow rules
- `README.md` — Project setup and overview
- `AGENTS.md` — Team agent roles
- `.claude/skills/token-saver-code-agent/SKILL.md` — Token optimization
- `.claude/skills/safe-git-review/SKILL.md` — Pre-commit review

# Continue Demo Command

**Purpose:** Resume demo/video verification pipeline from current state.

**Use when:**
- Continuing work from previous session
- Running smoke test to validate setup
- Running full demo loop to verify runtime markers
- Checking test reports and artifacts

---

## Quick Start

```powershell
# 1. Check current state
git status --short
git branch --show-current

# 2. Run smoke test (fast, ~30 seconds)
powershell -ExecutionPolicy Bypass -File .\scripts\pipeline_smoke_test.ps1

# 3. Check results
cat logs/pipeline_smoke_report.md

# 4. If smoke test passes (21/22), run full demo
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1

# 5. Check demo results
cat logs/demo_autofix_report.md
cat logs/roblox_latest_markers.md

# 6. Review artifacts
ls -lh logs/recordings/
```

---

## Skills Used

- `roblox-demo-pipeline/SKILL.md` — Demo automation and marker collection
- `token-saver-code-agent/SKILL.md` — Efficient file reading and reporting

---

## Expected Outcomes

### Smoke Test (21/22 checks)
```
✅ file:default.project.json
✅ file:src/server/Main.server.lua
✅ rojo_available
✅ rojo_build
✅ venv_exists
✅ demo_report_exists
✅ marker_report
✅ recordings
❌ server_markers (expected until full demo runs)
... (13 more passing checks)
```

### Full Demo Loop
```
Build: OK
Studio: Visible and foreground
F5: Pressed (AUTO_PLAY_FORCE_CONTROLLER_F5_PRESSED)
Video: Recorded (0.5+ MB)
Markers: Found (count and list)
Diagnosis: OK | PARTIAL_RUNTIME_CONFIRMED | FAIL_*
```

---

## Artifact Paths

After running demo, check:
- `logs/demo_autofix_report.md` — Final diagnosis and summary
- `logs/demo_test_report.md` — Detailed execution report
- `logs/roblox_latest_markers.md` — Runtime markers found
- `logs/recordings/demo_recording_*.mp4` — Video artifact
- `logs/screenshots/screenshot_*.png` — Before/after screenshots

---

## If Server Markers Missing

1. **Inspect marker report:**
   ```powershell
   cat logs/roblox_latest_markers.md | Select-String "Checked Log Files" -A 20
   ```

2. **Verify server code:**
   ```powershell
   cat src/server/Main.server.lua | Select-String "warn\|print" | head -10
   ```

3. **Check if F5 actually pressed:**
   ```powershell
   cat logs/demo_test_report.md | Select-String "f5_pressed|auto_play_status"
   ```

4. **Rerun demo with fresh Studio session:**
   ```powershell
   # Close all Studio instances first
   taskkill /F /IM RobloxStudioBeta.exe
   
   # Wait 5 seconds
   Start-Sleep -Seconds 5
   
   # Run demo again
   powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1
   ```

---

## Next Steps

### If Smoke Test Fails
- Check `logs/pipeline_smoke_report.md` for which check failed
- Fix the issue (e.g., install Rojo, create venv)
- Rerun smoke test

### If Demo Succeeds (OK)
- Review `logs/demo_autofix_report.md`
- Verify all markers present
- Ready to commit changes

### If Demo Partial (PARTIAL_RUNTIME_CONFIRMED)
- Inspect `logs/roblox_latest_markers.md`
- Identify missing markers
- Improve server-side code or log collection
- Rerun demo

### If Demo Fails
- Check `logs/demo_autofix_report.md` for diagnosis
- Follow recommended fix in report
- Rerun demo

---

## Do NOT Commit Yet

This command is for verification only. Do not commit until:
1. Demo succeeds (diagnosis = OK)
2. All markers present
3. Video recorded and verified
4. You explicitly confirm with `precommit-review` command

---

## See Also

- `.claude/commands/precommit-review.md` — Pre-commit review
- `.claude/skills/roblox-demo-pipeline/SKILL.md` — Demo automation
- `.claude/skills/token-saver-code-agent/SKILL.md` — Token optimization

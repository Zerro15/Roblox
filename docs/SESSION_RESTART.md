# Session Restart Guide

**Date:** 2026-05-25
**Status:** Safe checkpoint before system restart

---

## Last Known Status

### Current Branch
```
feature/demo-camera-video-smoke-test
```

### Git Status
```
## feature/demo-camera-video-smoke-test...origin/feature/demo-camera-video-smoke-test
(clean - no uncommitted changes)
```

### Local Branches
```
* feature/demo-camera-video-smoke-test ea52355 [origin/feature/demo-camera-video-smoke-test] Improve demo Studio window preflight
  feature/demo-test-player-recorder    1ae0a4a [origin/feature/demo-test-player-recorder] Add demo test player video recorder
  main                                 ed8807b [origin/main] Add demo camera and video smoke test (#12)
```

### Last Commits (feature/demo-camera-video-smoke-test)
```
ea52355 Improve demo Studio window preflight
acade34 Fix manual demo recording mode
83726a5 Fix manual demo recording mode
dd450ee Add demo camera and video smoke test
ccf7870 Add tower placement spending (#11)
```

### Last Commits (main)
```
ed8807b Add demo camera and video smoke test (#12)
ccf7870 Add tower placement spending (#11)
c1b4002 Fix team_plan_next.ps1: replace ternary operator with if-else for PowerShell 5.1 compatibility (#10)
cf8674e Add AI team operating system: model routing, documentation, and orchestration (#9)
1eb9d52 Add safe PR merge manager (#8)
```

### Open PRs
```
(none)
```

### Recently Merged PRs
```
#12 Add demo camera and video smoke test (MERGED 2026-05-24T18:56:40Z)
#11 Add tower placement spending (MERGED 2026-05-24T18:48:08Z)
#10 Fix team_plan_next PowerShell compatibility (MERGED 2026-05-24T18:37:57Z)
#9  Add AI team operating system (MERGED 2026-05-24T17:34:02Z)
#8  Add safe PR merge manager (MERGED 2026-05-24T14:21:18Z)
```

### Remote
```
origin https://github.com/Zerro15/Roblox.git (fetch)
origin https://github.com/Zerro15/Roblox.git (push)
```

---

## ⚠️ CRITICAL: Unpushed Commit

**Commit:** `ea52355 Improve demo Studio window preflight`

**Status:** ✅ Pushed to `origin/feature/demo-camera-video-smoke-test`

**Content:**
- Added `ensure_studio_window_visible()` function
- Checks if Studio window is visible/offscreen
- Attempts to restore minimized/offscreen windows
- Updated `manual_play_record_mode()` to use preflight check
- Updated `write_demo_report()` to show Studio window status
- Updated `run_demo_record_30s.ps1` and `run_demo_test.ps1` with better instructions

**Branch contains this commit:** `feature/demo-camera-video-smoke-test`

**Main branch contains this commit:** ❌ NO

**Action needed:** This commit needs to be in main via a new PR after restart.

---

## What Was Being Worked On

### Demo Camera + Video Smoke Test (PR #12)
- ✅ Demo camera added to `src/client/Main.client.lua`
- ✅ Automatic camera positioning on Play
- ✅ Manual-play-record mode implemented
- ✅ Video recording without automated F5 press
- ✅ Smoke test analysis of Roblox logs
- ✅ Video usefulness score (0-5)
- ✅ PR #12 merged to main

### Studio Window Preflight (NOT YET IN MAIN)
- ✅ Function `ensure_studio_window_visible()` created
- ✅ Detects offscreen/minimized windows
- ✅ Attempts safe window restoration
- ✅ Reports window status in demo_test_report.md
- ✅ Prevents recording if window not visible
- ✅ Commit ea52355 pushed to feature/demo-camera-video-smoke-test
- ❌ NOT YET merged to main (needs new PR)

### Known Issues Fixed
- ✅ NameError: focus_mode not defined (fixed in acade34)
- ✅ Manual recording mode now works
- ✅ Studio window visibility now checked before recording

### Last Test Result
- Video recorded but Play not confirmed
- Studio window was offscreen at (-32000, -32000)
- Need Studio Window Preflight to fix this

---

## Important Next Action After Restart

### Step 1: Verify Status
```powershell
cd C:\Users\Bogdan\Documents\Codex\2026-05-21\new-chat
git fetch origin
git status -sb
git branch -vv
```

### Step 2: Create PR for Studio Window Preflight
```powershell
# Checkout main and update
git checkout main
git pull origin main

# Create new branch from main
git checkout -b fix/demo-window-preflight

# Cherry-pick the Studio Window Preflight commit
git cherry-pick ea52355

# Verify it looks good
git log --oneline -3
git diff main..HEAD
```

### Step 3: Test the Changes
```powershell
# Build to verify no syntax errors
powershell -ExecutionPolicy Bypass -File .\scripts\build_place.ps1

# Quick test (30 seconds)
powershell -ExecutionPolicy Bypass -File .\scripts\run_demo_record_30s.ps1
```

### Step 4: Create PR
```powershell
# Push the branch
git push -u origin fix/demo-window-preflight

# Create PR
gh pr create --base main --head fix/demo-window-preflight `
  --title "Improve demo Studio window preflight" `
  --body "Adds Studio window visibility check before recording.

Changes:
- ensure_studio_window_visible() function to detect offscreen/minimized windows
- Attempts safe window restoration via focus_window()
- Reports window status in demo_test_report.md
- Prevents recording if window not visible
- Updated manual_play_record_mode() to use preflight check
- Better user instructions in run_demo_test.ps1 and run_demo_record_30s.ps1

Fixes issue where video was recorded but Studio window was offscreen at (-32000, -32000)."
```

---

## Quick Resume Commands

```powershell
# Navigate to project
cd C:\Users\Bogdan\Documents\Codex\2026-05-21\new-chat

# Fetch latest from remote
git fetch origin

# Check status
git status -sb
git branch -vv

# Check team status
powershell -ExecutionPolicy Bypass -File .\scripts\team_status.ps1

# Check next tasks
powershell -ExecutionPolicy Bypass -File .\scripts\team_plan_next.ps1

# Check open PRs
gh pr list --state open

# Check recent commits
git log --oneline -10
```

---

## File Structure Summary

### Key Game Files
- `src/client/Main.client.lua` — Demo camera setup
- `src/server/Main.server.lua` — Game bootstrap
- `src/server/services/` — Game services (Economy, Enemy, Tower, Wave, etc.)
- `src/shared/configs/` — Game configs (Tower, Enemy, Wave, Map)

### Demo/Test Files
- `tools/studio_operator/demo_test_player.py` — Main demo test runner
- `tools/studio_operator/window_focus.py` — Window management utilities
- `scripts/run_demo_test.ps1` — 90-second demo test
- `scripts/run_demo_record_30s.ps1` — 30-second quick test

### Documentation
- `docs/team/CURRENT_STATE.md` — Current game state
- `docs/team/NEXT_ACTIONS.md` — Next 5 tasks
- `docs/team/VIDEO_REVIEW_GUIDE.md` — Video quality evaluation
- `README.md` — Project overview

### Build & Automation
- `default.project.json` — Rojo config
- `scripts/build_place.ps1` — Build game.rbxlx
- `scripts/team_status.ps1` — Team status check
- `scripts/team_plan_next.ps1` — Show next tasks

---

## Do NOT Do After Restart

- ❌ Do NOT merge PR #12 again (already merged)
- ❌ Do NOT delete any branches
- ❌ Do NOT force push
- ❌ Do NOT commit build/game.rbxlx
- ❌ Do NOT commit logs/, recordings/, screenshots/, mp4
- ❌ Do NOT commit .env, venv, .claude/
- ❌ Do NOT start new features without planning

---

## Do After Restart

- ✅ Run `git fetch origin` to sync
- ✅ Create PR for fix/demo-window-preflight (cherry-pick ea52355)
- ✅ Test with `run_demo_record_30s.ps1`
- ✅ Check team status with `team_status.ps1`
- ✅ Review next tasks in `NEXT_ACTIONS.md`

---

## Contact Points

- **GitHub:** https://github.com/Zerro15/Roblox
- **Project Root:** C:\Users\Bogdan\Documents\Codex\2026-05-21\new-chat
- **Last Session:** 2026-05-25

---

## Session Complete

All important commits are safe:
- ✅ ea52355 pushed to origin/feature/demo-camera-video-smoke-test
- ✅ All branches synced with remote
- ✅ No uncommitted changes
- ✅ PR #12 merged successfully
- ✅ Ready for system restart

**Next action after restart:** Create PR for fix/demo-window-preflight via cherry-pick of ea52355.

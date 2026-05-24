# Video Review Guide

## Overview

This guide explains how to evaluate the usefulness of demo test videos recorded during gameplay testing.

---

## Usefulness Score Scale (0-5)

### Score 0: No Video
**Status:** `DEMO_RECORDING_FAILED`

- Video file was not created
- Recording failed or did not start
- Check logs for recording errors

**Action:** Re-run demo test, check disk space and permissions

---

### Score 1: Not Visible
**Status:** `DEMO_RECORDED_PLAY_NOT_CONFIRMED`

- Video file exists but is too small or corrupted
- Studio window not visible in video
- Game window not visible
- Only white/blue screen or black screen

**Action:** Check video file size, verify Studio window is visible before recording

---

### Score 2: Play Not Started
**Status:** `DEMO_RECORDED_PLAY_NOT_CONFIRMED`

- Studio window visible
- Game loaded and visible
- Play mode NOT activated (F5 not pressed)
- No gameplay visible

**Markers:** No `[Server boot]` or gameplay markers in logs

**Action:** Press F5/Play manually during recording

---

### Score 3: Play Started, Unclear Gameplay
**Status:** `DEMO_RECORDED_PLAY_CONFIRMED`

- Play mode active
- Some game objects visible
- Gameplay loop not clear
- Missing key elements (enemies, towers, or map)

**Markers:** Some gameplay markers found, but not all

**Action:** Record longer, ensure camera can see gameplay

---

### Score 4: Map/Enemies/Towers Visible
**Status:** `DEMO_RECORDED_PLAY_CONFIRMED`

- Map visible (Backlund Fog District)
- Enemies visible and moving
- Towers visible
- Gameplay partially clear

**Markers:** Most gameplay markers found:
- `[Server boot]`
- `[RuntimeService]`
- `[MapService]`
- `[PathService]`
- `[EnemyService]`
- `[TowerService]`

**Action:** Acceptable for basic testing

---

### Score 5: Full Loop Visible
**Status:** `DEMO_RECORDED_PLAY_CONFIRMED`

- Map visible (Backlund Fog District)
- Enemies spawning and moving along path
- Towers visible and attacking
- Rewards being awarded (money changes)
- Wave progression visible
- Complete gameplay loop visible

**Markers:** All gameplay markers found:
- `[Server boot]`
- `[RuntimeService]`
- `[MapService]`
- `[PathService]`
- `[WaveService]`
- `[EnemyService]`
- `[TowerService]`
- `[EconomyService]`
- `[Client boot]`
- `[Client] Demo camera activated`

**Action:** Excellent for comprehensive testing

---

## How to Review a Demo Test

### Step 1: Check Report
Open `logs/demo_test_report.md` and look for:
- `result status`
- `play status`
- `video usefulness score`
- `matched markers`

### Step 2: Watch Video
Open the video file from `logs/recordings/` and observe:
- Is Studio visible?
- Is the game loaded?
- Is Play mode active?
- Can you see the map?
- Can you see enemies?
- Can you see towers?
- Is there gameplay happening?

### Step 3: Check Markers
Look at `logs/roblox_latest_markers.md` and verify:
- Server boot messages
- Service initialization messages
- Gameplay events (enemy spawning, tower attacking, etc.)

### Step 4: Assign Score
Based on observations, assign a score 0-5 using the scale above.

---

## Common Issues and Solutions

### Video is blank/white/blue
- **Cause:** Studio window not visible or camera not set up
- **Solution:** Ensure Studio is visible before recording, check demo camera setup

### Video shows Studio but no Play
- **Cause:** F5 not pressed during recording
- **Solution:** Press F5 manually during recording

### Video shows gameplay but markers missing
- **Cause:** Roblox logs not captured or cleared
- **Solution:** Check Roblox logs directory, re-run test

### Video too short
- **Cause:** Recording duration too short
- **Solution:** Use longer duration (60-90 seconds)

### Video file very small (< 1 MB)
- **Cause:** Recording failed or mostly blank
- **Solution:** Check recording errors in report, re-run test

---

## Automatic Scoring Logic

The demo test player automatically assigns scores based on:

1. **Video exists?**
   - No → Score 0
   - Yes → Continue

2. **Gameplay markers found?**
   - No → Score 1-2
   - Yes → Score 3-5

3. **How many markers?**
   - < 4 markers → Score 3
   - 4-7 markers → Score 4
   - 8+ markers → Score 5

4. **Client demo camera markers?**
   - Found → Add +1 to score (max 5)
   - Not found → No change

---

## Recording Tips

### For Best Results:
1. Ensure Roblox Studio is visible on screen
2. Click Studio window before recording starts
3. Press F5/Play within first 5 seconds of recording
4. Let recording run for full duration (60-90 seconds)
5. Don't switch windows during recording
6. Check that demo camera is activated (look for `[Client] Demo camera activated` in logs)

### If Windows Focus Fails:
- Recording will still happen automatically
- You can manually click Studio and press F5 while recording
- Video will capture whatever happens on screen
- Markers will confirm if Play was actually started

---

## Video Quality Metrics

| Metric | Good | Bad |
|--------|------|-----|
| **Duration** | 60+ seconds | < 30 seconds |
| **File Size** | 2-10 MB | < 1 MB or > 50 MB |
| **Visibility** | Studio clearly visible | Mostly blank/white |
| **Gameplay** | Clear gameplay loop | No gameplay visible |
| **Markers** | 8+ markers found | 0-3 markers found |
| **Score** | 4-5 | 0-2 |

---

## Next Steps

If video score is:
- **0-1:** Re-run test, check setup
- **2-3:** Test is partially useful, consider re-running
- **4-5:** Test is good, can proceed with analysis


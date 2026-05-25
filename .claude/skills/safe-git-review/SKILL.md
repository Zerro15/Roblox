# Safe Git Review Skill

**Purpose:** Pre-commit review to classify files, avoid staging generated artifacts, and propose safe commits.

**Scope:** Git status, file classification, staging decisions, commit messages.

---

## Quick Start

### Pre-Commit Checklist
```powershell
# 1. Show what changed
git status --short
git diff --stat

# 2. Review each changed file
git diff tools/studio_operator/roblox_logs.py

# 3. Classify untracked files
# (See "File Classification" section below)

# 4. Stage only safe files
git add tools/studio_operator/roblox_logs.py
git add tools/studio_operator/demo_test_player.py
# (Do NOT add CSV, logs, videos, recordings)

# 5. Verify staging
git status

# 6. Commit with clear message
git commit -m "Improve log collection: scan 20 files instead of 5"

# 7. Verify commit
git log --oneline -1
```

---

## File Classification

### Safe to Commit (Modified Source Code)
- ✅ `src/` — Game code
- ✅ `tools/studio_operator/*.py` — Automation scripts
- ✅ `scripts/*.ps1` — Build/test scripts
- ✅ `*.md` — Documentation
- ✅ `default.project.json` — Rojo config
- ✅ `.gitignore` — Ignore rules

### Never Commit (Generated Artifacts)
- ❌ `logs/` — Test reports, markers, recordings
- ❌ `build/game.rbxlx` — Compiled place file
- ❌ `screenshots/` — Demo screenshots
- ❌ `recordings/` — Video files
- ❌ `.venv*` — Python virtual environments
- ❌ `*.csv` — Diagnostic/test data
- ❌ `.claude/plans/` — Local planning files
- ❌ `*.mp4` — Video recordings

### Untracked Files to Ignore
```
agentrouter-five-models-test.csv
agentrouter-models.csv
claude-agentrouter-model-test-fixed.csv
claude-agentrouter-model-test.csv
logs/pipeline_smoke_report.md
logs/demo_test_report.md
logs/demo_autofix_report.md
logs/roblox_latest_markers.md
logs/roblox_latest_markers.json
logs/recordings/demo_recording_*.mp4
logs/screenshots/screenshot_*.png
scripts/pipeline_smoke_test.ps1  (if auto-generated)
tools/studio_operator/pipeline_smoke_test.py  (if auto-generated)
```

---

## Staging Strategy

### Explicit Add (Recommended)
```powershell
# Add specific files
git add tools/studio_operator/roblox_logs.py
git add tools/studio_operator/demo_test_player.py
git add README.md

# Verify
git status

# Commit
git commit -m "Improve log collection: scan 20 files instead of 5"
```

### Never Use
```powershell
git add .              # ❌ Adds everything including CSV, logs, videos
git add -A             # ❌ Adds all untracked files
git add logs/          # ❌ Adds test artifacts
git add build/         # ❌ Adds compiled place file
```

---

## Commit Message Format

### Good Commit Messages
```
Improve log collection: scan 20 files instead of 5

- Increased max_files parameter in roblox_logs.py from 5 to 20
- Updated demo_test_player.py to use new default
- Improves chances of capturing server-side markers
- Server markers may be in older log files outside top 5
```

### Bad Commit Messages
```
❌ "fix stuff"
❌ "update code"
❌ "WIP"
❌ "asdf"
```

### Template
```
<short summary, 50 chars max>

<detailed explanation, 72 chars per line>

- Bullet point 1
- Bullet point 2
- Bullet point 3
```

---

## Pre-Commit Review Checklist

### Before Staging
- [ ] Run `git status --short` to see all changes
- [ ] Run `git diff --stat` to see summary
- [ ] Review each changed file with `git diff <file>`
- [ ] Verify no build artifacts in changes
- [ ] Verify no secrets/tokens in changes
- [ ] Verify no generated logs in changes

### Before Committing
- [ ] Run `git status` to verify only intended files staged
- [ ] Verify commit message is clear and descriptive
- [ ] Verify commit message follows template
- [ ] Check that no untracked artifacts are staged

### After Committing
- [ ] Run `git log --oneline -1` to verify commit
- [ ] Run `git status` to verify working tree clean
- [ ] Verify branch is correct: `git branch --show-current`

---

## Common Scenarios

### Scenario 1: Code Changes Only
```powershell
# Changes: tools/studio_operator/roblox_logs.py
# Untracked: logs/pipeline_smoke_report.md, *.csv files

git status --short
# M  tools/studio_operator/roblox_logs.py
# ?? logs/pipeline_smoke_report.md
# ?? agentrouter-models.csv

git diff tools/studio_operator/roblox_logs.py
# Review changes...

git add tools/studio_operator/roblox_logs.py
git commit -m "Improve log collection: scan 20 files instead of 5"
```

### Scenario 2: Multiple Code Files
```powershell
# Changes: roblox_logs.py, demo_test_player.py, README.md
# Untracked: logs/*, *.csv

git diff --stat
# tools/studio_operator/roblox_logs.py       | 4 ++--
# tools/studio_operator/demo_test_player.py  | 2 +-
# README.md                                  | 24 ++++++++++++++++++++++++

git diff tools/studio_operator/roblox_logs.py
git diff tools/studio_operator/demo_test_player.py
git diff README.md
# Review all changes...

git add tools/studio_operator/roblox_logs.py
git add tools/studio_operator/demo_test_player.py
git add README.md
git commit -m "Improve log collection and documentation"
```

### Scenario 3: Accidental Staging
```powershell
# Oops: staged logs/pipeline_smoke_report.md

git status
# Changes to be committed:
#   modified: tools/studio_operator/roblox_logs.py
#   new file: logs/pipeline_smoke_report.md

# Unstage the log file
git reset HEAD logs/pipeline_smoke_report.md

# Verify
git status
# Changes to be committed:
#   modified: tools/studio_operator/roblox_logs.py
# Untracked files:
#   logs/pipeline_smoke_report.md

# Now safe to commit
git commit -m "Improve log collection"
```

---

## Safety Rules

### Always
- ✅ Review changes before committing
- ✅ Use explicit `git add <file>` paths
- ✅ Write clear commit messages
- ✅ Verify working tree clean after commit
- ✅ Check branch is correct

### Never
- ❌ Use `git add .` or `git add -A`
- ❌ Commit without reviewing changes
- ❌ Commit build artifacts or logs
- ❌ Commit secrets or tokens
- ❌ Force push without explicit approval

---

## Git Commands Reference

### Status & Diff
```powershell
git status                    # Full status
git status --short            # Compact status
git diff                      # Show all changes
git diff --stat               # Summary of changes
git diff <file>               # Changes in one file
git diff HEAD~1               # Changes since last commit
```

### Staging
```powershell
git add <file>                # Stage specific file
git add <dir>/                # Stage all files in directory
git reset HEAD <file>         # Unstage file
git reset HEAD                # Unstage all files
git checkout -- <file>        # Discard changes in file
```

### Committing
```powershell
git commit -m "message"       # Commit with message
git commit --amend            # Modify last commit
git log --oneline -5          # Show last 5 commits
git log -p <file>             # Show changes to file
```

### Branches
```powershell
git branch                    # List branches
git branch --show-current     # Current branch
git checkout -b <branch>      # Create new branch
git checkout <branch>         # Switch branch
```

---

## Integration with Roblox Demo Pipeline

### After Running Smoke Test
```powershell
# 1. Check status
git status --short
# M  README.md
# M  tools/studio_operator/roblox_logs.py
# ?? logs/pipeline_smoke_report.md

# 2. Review changes
git diff --stat
git diff tools/studio_operator/roblox_logs.py

# 3. Stage code changes only
git add tools/studio_operator/roblox_logs.py
git add README.md

# 4. Commit
git commit -m "Improve log collection: scan 20 files instead of 5"

# 5. Verify
git log --oneline -1
```

### After Running Demo Loop
```powershell
# 1. Check what changed
git status --short

# 2. If only logs/reports changed (no code changes):
# Do NOT commit logs/
# Wait for code changes before committing

# 3. If code changed:
git diff --stat
git diff tools/studio_operator/demo_autofix_loop.py
# Review and stage code changes only

git add tools/studio_operator/demo_autofix_loop.py
git commit -m "Fix demo autofix diagnosis logic"
```

---

## See Also

- `CLAUDE.md` — Claude workflow rules
- `roblox-demo-pipeline/SKILL.md` — Demo automation
- `token-saver-code-agent/SKILL.md` — Token optimization

# Precommit Review Command

**Purpose:** Review changes before committing to ensure only safe files are staged.

**Use when:**
- Ready to commit code changes
- Need to verify no artifacts are staged
- Want to propose commit message
- Need pre-commit safety check

---

## Quick Start

```powershell
# 1. Show what changed
git status --short
git diff --stat

# 2. Review each changed file
git diff tools/studio_operator/roblox_logs.py
git diff tools/studio_operator/demo_test_player.py
git diff README.md

# 3. Classify untracked files
# (See "File Classification" below)

# 4. Stage only safe files
git add tools/studio_operator/roblox_logs.py
git add tools/studio_operator/demo_test_player.py
git add README.md

# 5. Verify staging
git status

# 6. Commit with proposed message
git commit -m "Improve log collection: scan 20 files instead of 5"

# 7. Verify commit
git log --oneline -1
```

---

## Skills Used

- `safe-git-review/SKILL.md` — File classification and staging strategy
- `token-saver-code-agent/SKILL.md` — Efficient diff review

---

## File Classification

### Safe to Commit (Source Code)
- ✅ `src/` — Game code
- ✅ `tools/studio_operator/*.py` — Automation scripts
- ✅ `scripts/*.ps1` — Build/test scripts
- ✅ `*.md` — Documentation
- ✅ `default.project.json` — Rojo config

### Never Commit (Generated Artifacts)
- ❌ `logs/` — Test reports, markers, recordings
- ❌ `build/game.rbxlx` — Compiled place file
- ❌ `*.csv` — Diagnostic data
- ❌ `*.mp4` — Video files
- ❌ `.venv*` — Python environments

---

## Review Checklist

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

## Commit Message Template

```
<short summary, 50 chars max>

<detailed explanation, 72 chars per line>

- Bullet point 1
- Bullet point 2
- Bullet point 3
```

### Example
```
Improve log collection: scan 20 files instead of 5

Increased max_files parameter in roblox_logs.py and demo_test_player.py
to scan up to 20 recent Roblox log files instead of just 5. This improves
the chances of capturing server-side runtime markers that may be in older
log files outside the top 5 most recent.

- Increased max_files from 5 to 20 in roblox_logs.py
- Updated demo_test_player.py to use new default
- Updated README.md with Pipeline Smoke Test section
- Server markers may be in older log files; wider scan helps capture them
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

## Common Scenarios

### Scenario 1: Code Changes Only
```powershell
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

# Now safe to commit
git commit -m "Improve log collection"
```

---

## Untracked Files to Ignore

These should NOT be committed:
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
scripts/pipeline_smoke_test.ps1
tools/studio_operator/pipeline_smoke_test.py
```

---

## Git Commands Reference

### Status & Diff
```powershell
git status                    # Full status
git status --short            # Compact status
git diff                      # Show all changes
git diff --stat               # Summary of changes
git diff <file>               # Changes in one file
```

### Staging
```powershell
git add <file>                # Stage specific file
git add <dir>/                # Stage all files in directory
git reset HEAD <file>         # Unstage file
git reset HEAD                # Unstage all files
```

### Committing
```powershell
git commit -m "message"       # Commit with message
git log --oneline -1          # Show last commit
```

---

## Next Steps

### If Review Passes
- Commit changes with proposed message
- Verify commit: `git log --oneline -1`
- Push to remote: `git push origin <branch>`

### If Issues Found
- Unstage problematic files: `git reset HEAD <file>`
- Fix issues
- Rerun precommit-review

---

## See Also

- `.claude/commands/continue-demo.md` — Continue demo verification
- `.claude/skills/safe-git-review/SKILL.md` — Detailed review guide
- `CLAUDE.md` — Claude workflow rules

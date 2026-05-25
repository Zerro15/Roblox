# Token Saver Code Agent Skill

**Purpose:** Reduce token usage in Claude sessions by using targeted reads, compact summaries, and smart tool selection.

**Scope:** File reading, log inspection, code review, diff analysis.

---

## Core Principles

1. **Read smart, not big** — Use line limits and offsets for large files
2. **Search before reading** — Use `grep_search` or `Select-String` to find relevant sections
3. **Summarize aggressively** — Compact final reports, avoid repeating context
4. **Use git diff** — Show changes with `git diff --stat` before full reads
5. **Avoid log dumps** — Never read entire log files; search for patterns first

---

## File Reading Strategy

### Large Files (>1000 lines)
**Never read the whole file.** Instead:

1. **Determine relevant section:**
   ```powershell
   # Find line numbers of interest
   Select-String -Path "file.py" -Pattern "def collect_markers" | Select-Object LineNumber
   ```

2. **Read only that section:**
   ```
   read_file(path, offset=430, limit=50)  # Read 50 lines starting at line 430
   ```

3. **Example: demo_test_player.py (850 lines)**
   ```
   # Instead of reading all 850 lines:
   read_file(path, offset=430, limit=20)  # Read collect_markers function
   read_file(path, offset=451, limit=30)  # Read diagnose_demo_report function
   ```

### Small Files (<500 lines)
**Safe to read in full** — CLAUDE.md, AGENTS.md, skill files, etc.

### Log Files
**Always search first, never dump:**
```powershell
# Bad: cat logs/demo_test_report.md (entire file)
# Good: Select-String -Path logs/demo_test_report.md -Pattern "diagnosis|success|markers"
```

---

## Search Before Read

### PowerShell Select-String
```powershell
# Find all function definitions
Select-String -Path "tools/studio_operator/roblox_logs.py" -Pattern "^def " | Select-Object LineNumber, Line

# Find specific marker
Select-String -Path "logs/demo_test_report.md" -Pattern "diagnosis|PARTIAL|OK" | Select-Object -First 5
```

### Git Diff
```powershell
# Show what changed
git diff --stat

# Show specific file changes
git diff tools/studio_operator/roblox_logs.py

# Show only line numbers of changes
git diff --unified=0 tools/studio_operator/roblox_logs.py
```

### Grep Search Tool
```
grep_search(pattern="def collect_latest_markers", path="tools/studio_operator/roblox_logs.py", output_mode="content", context=5)
```

---

## Compact Reporting

### Status Report Template
```
## Summary
- Branch: feature/demo-runtime-score-4
- Commit: c6b0c24
- Changes: 4 files modified, 28 insertions, 4 deletions
- Untracked: 4 CSV files, 1 smoke report, 1 pipeline script

## Modified Files
- README.md: +24 lines (added Pipeline Smoke Test section)
- demo_autofix_loop.py: +2 lines (fixed classify_failure return)
- demo_test_player.py: +2 lines (increased max_files to 20)
- roblox_logs.py: +4 lines (increased max_files default)

## Test Result
- Smoke test: 21/22 checks passing
- Failing check: server_markers (expected until full demo runs)
- Next action: Run demo_autofix_loop.ps1 for full verification
```

### Avoid
- ❌ Repeating entire file contents
- ❌ Listing all 22 smoke test checks individually
- ❌ Dumping full git diff output
- ❌ Showing entire log files
- ❌ Repeating context from previous messages

### Use
- ✅ `git diff --stat` for overview
- ✅ `git diff <file>` for specific changes
- ✅ Line counts and summaries
- ✅ Targeted quotes (3-5 lines max)
- ✅ Artifact paths instead of contents

---

## Model Selection

### Use Haiku (Default)
- Status checks (`git status`, `git branch`)
- File existence checks
- Smoke test runs
- Report summarization
- Documentation updates
- Simple script execution

**Cost:** ~1-2 tokens per operation

### Use Opus Only For
- Complex debugging (server markers missing)
- Architecture decisions
- Security reviews
- Risky git operations (merge, force push)
- Cross-service refactoring

**Cost:** ~10x Haiku, use sparingly

---

## Efficient Workflows

### Workflow 1: Check Status (Haiku)
```
1. git status --short
2. git branch --show-current
3. git diff --stat
4. Summarize in 3-5 lines
```
**Tokens:** ~50

### Workflow 2: Run Smoke Test (Haiku)
```
1. powershell -ExecutionPolicy Bypass -File .\scripts\pipeline_smoke_test.ps1
2. Wait for completion
3. Read logs/pipeline_smoke_report.md (search for "FAIL" first)
4. Report: "21/22 checks passing, server_markers failing (expected)"
```
**Tokens:** ~100-150

### Workflow 3: Review Code Change (Haiku)
```
1. git diff --stat
2. For each changed file:
   a. git diff <file> (show specific changes)
   b. Read only changed lines (use offset/limit)
   c. Verify syntax/style
3. Summarize changes in 5-10 lines
```
**Tokens:** ~200-300

### Workflow 4: Debug Server Markers (Opus)
```
1. Read logs/roblox_latest_markers.md (search for "[Server boot]" first)
2. Read logs/demo_test_report.md (search for "f5_pressed")
3. Read src/server/Main.server.lua (search for warn statements)
4. Analyze why markers missing
5. Propose fix
```
**Tokens:** ~500-1000 (use Opus for this)

---

## Quick Reference

| Task | Tool | Model | Tokens |
|------|------|-------|--------|
| Check status | `git status --short` | Haiku | 50 |
| Run smoke test | `pipeline_smoke_test.ps1` | Haiku | 150 |
| Review diff | `git diff --stat` | Haiku | 100 |
| Read small file | `read_file(path)` | Haiku | 50-100 |
| Search in file | `grep_search(pattern)` | Haiku | 50 |
| Debug markers | `read_file` + analysis | Opus | 500+ |
| Design feature | Architecture review | Opus | 1000+ |

---

## Anti-Patterns

### ❌ Don't Do This
```
# Reading entire 850-line file
read_file("tools/studio_operator/demo_test_player.py")  # 5000+ tokens

# Dumping full log
cat logs/demo_test_report.md  # 2000+ tokens

# Repeating context
"As I mentioned before, the server markers are missing because..."

# Using Opus for status check
/model opus
git status

# Listing all 22 smoke test checks
"Check 1: file:default.project.json PASS
 Check 2: file:src/server/Main.server.lua PASS
 ..."
```

### ✅ Do This Instead
```
# Read only relevant section
read_file("tools/studio_operator/demo_test_player.py", offset=430, limit=20)  # 200 tokens

# Search for pattern
grep_search(pattern="diagnosis|PARTIAL", path="logs/demo_test_report.md")  # 100 tokens

# Summarize concisely
"Server markers missing; 21/22 smoke checks passing."

# Use Haiku for status
git status --short

# Summarize test results
"Smoke test: 21/22 passing (server_markers expected to fail until full demo)"
```

---

## Session Planning

### Start of Session
1. Run `git status --short` (50 tokens)
2. Run `git diff --stat` (50 tokens)
3. Summarize: "4 files modified, 28 insertions. Ready to review."
4. **Total: ~100 tokens**

### During Session
- Use Haiku for all routine work
- Search before reading large files
- Summarize aggressively
- Avoid repeating context

### End of Session
- Show `git diff --stat` (not full diff)
- Show `git status --short` (not full status)
- List artifact paths (not contents)
- Propose next command (1-2 lines)

---

## See Also

- `CLAUDE.md` — Claude workflow rules
- `roblox-demo-pipeline/SKILL.md` — Demo automation
- `safe-git-review/SKILL.md` — Pre-commit review

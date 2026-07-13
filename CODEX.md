# CODEX.md — Start here

You are working on **Greymoor: Paths of Mystery**, a Roblox tower-defense RPG.

## Immediate objective

Turn the existing prototype into a polished vertical slice:

- walkable occult hub
- portal into defense mode
- tactical tower-defense camera
- agent towers
- wave loop
- boss wave
- readable UI
- clean Rojo build

## Non-negotiables

- Do not copy protected names or lore text from existing franchises.
- Keep the game original while preserving the foggy occult mystery vibe.
- Preserve working behavior unless you have a better tested replacement.
- Never commit build artifacts, logs, recordings, screenshots, secrets, or `.env` files.
- Be honest about tests: say `not run` if not run.

## Preferred loop

```powershell
# 1. Inspect
Get-ChildItem
Get-Content .\README.md
Get-Content .\AGENTS.md

# 2. Plan
.\scripts\team_status.ps1
.\scripts\team_plan_next.ps1

# 3. Implement one vertical slice
# edit files under src/

# 4. Verify
.\scripts\build_place.ps1
.\scripts\team_review_demo.ps1
```

## First task to execute

Open `prompts/codex_build_mvp.md` and follow it as the first full Codex task.

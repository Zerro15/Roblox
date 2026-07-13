# Codex prompt — Build the Greymoor MVP vertical slice

You are Codex working inside the repository `Zerro15/Roblox`.

## Mission

Transform the current Roblox tower-defense prototype into a clean, playable vertical slice for **Greymoor: Paths of Mystery**.

This is not a generic anime tower defense. Build a foggy occult tower-defense RPG with original names and systems.

## Read first

1. `README.md`
2. `CODEX.md`
3. `AGENTS.md`
4. `docs/GAME_DESIGN.md`
5. Existing `src/` code
6. Existing scripts under `scripts/` and `tools/`

## Constraints

- Do not use protected names, characters, locations, logos, or text from existing IP.
- Do not remove working MVP behavior without replacing it with verified behavior.
- Keep server-authoritative gameplay.
- Do not commit generated build files, logs, screenshots, videos, `.env`, or secrets.
- Prefer small, reviewable changes.
- Report exact tests run. If Studio cannot be automated, say so and provide manual steps.

## Target player experience

A player should be able to:

1. Press Play in Roblox Studio.
2. Spawn inside a walkable Greymoor command hub.
3. See readable instructions.
4. Walk to a portal.
5. Press `E` to start `Veil Defense`.
6. Enter a tactical TD camera.
7. Select pads.
8. Build agent towers.
9. Upgrade and sell towers if systems exist or can be safely added.
10. Fight waves and a final boss.
11. See victory or defeat feedback.

## Implementation priorities

### Priority 1 — audit and stabilize

- Identify current working systems.
- Find services/configs responsible for waves, towers, economy, UI, hub, camera, and runtime state.
- Do not blindly rewrite.
- Fix broken references and stale project names.

### Priority 2 — brand and config

- Rename visible in-game text to `Greymoor: Paths of Mystery` and `Veil Defense`.
- Replace generic tower/enemy names with original Greymoor names.
- Put tunable stats in shared config modules when appropriate.

### Priority 3 — gameplay slice

Implement or polish:

- 5–6 agent towers.
- 10–15 waves.
- one final boss.
- basic economy balance.
- clear UI labels.
- selection/build/upgrade/sell feedback.

### Priority 4 — verification

Run available checks:

```powershell
.\scripts\team_status.ps1
.\scripts\build_place.ps1
.\scripts\team_review_demo.ps1
```

Also run if installed:

```powershell
stylua --check src
selene src
rojo build .\default.project.json -o build\game.rbxlx
```

If missing tools block verification, provide exact install commands and continue with static review.

## Acceptance criteria

- Rojo project name is `GreymoorPathsOfMystery`.
- README/CODEX/AGENTS remain accurate.
- Studio playtest path is documented.
- No direct copyrighted franchise naming remains in user-facing game text.
- At least one full match path is playable or the exact blocker is documented.
- Final response includes:
  - what changed
  - files changed
  - tests run
  - known issues
  - next best task

## Output style

Be direct and practical. Do not over-explain. Do not claim success without evidence.

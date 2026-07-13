# Greymoor: Paths of Mystery

Mystic Roblox tower-defense RPG built with Rojo, Codex/AI-assisted workflows, and safe Roblox Studio iteration.

The project is inspired by foggy occult urban fantasy: hidden paths, potions, agents, artifacts, veil breaches, and loss-of-control threats. Do **not** copy protected names, locations, characters, logos, or text from existing franchises.

## Current direction

**Game title:** `Greymoor: Paths of Mystery`  
**Primary mode:** `Veil Defense` / `Защита Завесы`  
**Genre:** story-driven tower defense + RPG progression  
**Core fantasy:** defend Greymoor from mist breaches by placing agents, upgrading artifacts, and advancing along mysterious paths without losing control.

## Development modes

The repository supports two workflows:

1. **Rojo + files** — preferred production workflow.
2. **Studio bridge** — optional live-iteration workflow for already-open Roblox Studio sessions.

Use Rojo whenever possible. Use the bridge only for quick visual iteration, diagnostics, and safe generated scene edits.

## Repository map

- `default.project.json` — Rojo project mapping.
- `src/shared` → `ReplicatedStorage/Shared`.
- `src/server` → `ServerScriptService`.
- `src/client` → `StarterPlayer/StarterPlayerScripts`.
- `src/workspace` → `Workspace` authored map/hub content.
- `AGENTS.md` — Codex/AI working rules.
- `CODEX.md` — short Codex entrypoint.
- `docs/` — design, roadmap, state, testing notes.
- `prompts/` — reusable AI prompts.
- `scripts/` — local build, bridge, test, and workflow helpers.
- `tools/` — Studio operator and automation utilities.

## Quick start on Windows PowerShell

```powershell
# Clone after GitHub/Codex access is configured
git clone https://github.com/Zerro15/Roblox.git
cd Roblox

# Check project status
.\scripts\team_status.ps1

# Build Roblox place file, if Rojo is available
.\scripts\build_place.ps1

# Start Rojo sync
.\scripts\start_rojo.ps1
```

## Tooling target

Preferred local tooling:

- Roblox Studio
- Rojo
- Aftman, if available, for pinned Roblox tooling
- StyLua for Lua formatting
- Selene for Luau linting
- GitHub CLI for PR workflow, if available
- Codex CLI / Codex in ChatGPT desktop for implementation loops

If tools are missing, Codex should install or provide exact install commands, then verify versions before changing game code.

## Game design constraints

- Keep the project legally distinct: no direct copyrighted names from `Lord of the Mysteries`.
- Use original names: `Greymoor`, `Veil`, `Paths`, `Agents`, `Potions`, `Artifacts`, `Mist Breaches`.
- Prioritize playable slices over giant world scope.
- Preserve existing working MVP features unless explicitly replacing them.
- Every new mechanic needs a visible test path in Studio.

## MVP target

First polished vertical slice:

1. Walkable occult command hub.
2. Portal prompt starts `Veil Defense`.
3. One authored map: foggy Greymoor district.
4. 15 waves.
5. 5–6 agent towers.
6. 3 player paths with one active ability each.
7. One boss: `Lost Adept`.
8. Currency, tower placement, upgrade, sell.
9. Basic victory/defeat loop.
10. Test report proving it runs in Studio.

## AI development rule

Codex should work in small safe branches, explain the plan, implement one vertical slice at a time, run available checks, and avoid committing generated build artifacts, logs, videos, screenshots, secrets, or `.env` files.

See `CODEX.md`, `AGENTS.md`, and `prompts/codex_build_mvp.md` for the recommended next task.

# Greymoor: Paths of Mystery — Game Design Foundation

## One-line pitch

A foggy occult Roblox tower-defense RPG where players defend Greymoor from veil breaches using agents, artifacts, and risky path progression.

## Core promise

The player should feel like a tactical commander inside a secret supernatural city, not like they are playing a generic anime tower defense clone.

## Main loop

1. Spawn in the occult command hub.
2. Choose path loadout and agent deck.
3. Enter a Greymoor district through the portal.
4. Defend against waves from mist breaches.
5. Earn currency and ingredients.
6. Upgrade agents/artifacts.
7. Advance path progression carefully.
8. Unlock harder districts and bosses.

## First vertical slice

### Hub

- Walkable authored hub.
- Portal with `E` prompt.
- Small readable UI panel.
- Atmosphere: fog, lamps, ritual circle, clockwork/occult props.

### Defense map

- One authored district map.
- Fixed enemy path.
- Tower pads.
- Tactical camera after defense starts.
- 15 waves.
- Boss on final wave.

### Agent towers

Initial agents:

1. `Lantern Warden` — cheap starter, reveals weak mist units.
2. `Clockwork Gunner` — reliable single-target damage.
3. `Archive Savant` — support aura.
4. `Veil Medium` — slow and curse.
5. `Iron Hunter` — high boss damage.
6. `Alchemist Surgeon` — poison/damage-over-time utility.

### Player paths

Initial paths:

1. `Seer Path` — previews or weakens next wave.
2. `Mechanist Path` — boosts mechanical agents and deployables.
3. `Shadow Path` — fear, slow, and ambush effects.

Keep path names original and legally safe.

### Enemies

Initial enemies:

1. `Mist Drifter` — basic fast unit.
2. `Ragged Cultist` — basic humanoid.
3. `Veil Hound` — fast pressure unit.
4. `Armored Heretic` — high health/armor.
5. `Lost Adept` — boss with aura or spawn effect.

## UX principles

- Russian UI first, English-ready naming in configs.
- Always show player what changed: money, health, wave, selected pad, selected tower.
- Keep controls visible.
- Avoid tiny unreadable text.
- Roblox players should understand the first match without reading docs.

## Technical principles

- Server-authoritative economy, tower placement, damage, and wave state.
- Client-only camera, input, UI, selection, and previews.
- Shared configs for tunable values.
- No hardcoded scattered stats if the data belongs in config.
- Keep each service small enough for Codex to reason about safely.

## Monetization-safe future ideas

Do not build monetization before the game is fun.

Later possibilities:

- cosmetic hub skins
- cosmetic agent skins
- VIP quality-of-life only if fair
- battle pass only after retention exists
- no pay-to-win stats in early design

## Anti-scope-creep rule

Do not build open world, trading, clans, gacha, huge quest systems, or 20 paths before the first vertical slice is stable.

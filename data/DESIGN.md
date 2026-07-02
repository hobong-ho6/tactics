# Aston Villa → FC tactics: system design

Goal: continuously turn Aston Villa's real performances (ratings, results, roles, heatmaps)
into an in-game recreation of Villa's tactics — for **any season** (25/26, 26/27, …) and
**any FC version** (FC26, FC27, …). The design keeps real-world data, the game role library,
and the derived mapping as **separate layers** so each new season or game is an *additive* change,
never a rewrite.

## Layers

1. **Real-world data (source of truth)** — SQLite `data/avl_analysis.db`, season-scoped.
   - `seasons(code,label)`
   - `players(id,name,…)` — stable identity across seasons.
   - `player_seasons(player_id,season,club,primary_position,shirt_no,minutes)` — squad membership per season (handles transfers in/out).
   - `matches(id,season,team,date,opponent,competition,venue,result)`
   - `appearances(player_id,match_id,rank_for_player,rating,minutes,position,role,heat_zones,heat_summary,goals,assists,source,confidence)` — one row per player per match (SofaScore rating + that-match position/role/heatmap).
   - `streaks(id,season,label,note)` + `match_streak(match_id,streak_id)` (m2m; overlapping runs like 11-all-comp ⊃ 8-PL).
   - View `v_best`.

2. **Game role library (per FC version)** — `game_roles(game_version,role_id,name,position_type,focuses)`.
   - FC26 role set differs from FC27's; each version is its own set of rows. The heatmap kernels
     (`MAPS` in the tool) belong here conceptually — long term they move out of hardcoded JS into this table
     so FC27 is "add rows", not "edit the tool".

3. **Derived mapping (what the tool renders)** — `player_role_map(player_id,season,game_version,kind,pos_label,x,y,role_id,focus,map25,rationale)`.
   - `kind`: `measured` (real avg heatmap → map25), `role` (closest game role to the heatmap), `optimal` (best position/role by rating+results).
   - This table is the **contract** between analysis and the tool: one query per (season, game_version, kind) yields a full 11-player formation spec.

## Pipeline (re-run each season)

```
research (Workflows) → ingest into DB → analyze (rating×result by position) → write player_role_map → export formation JSON → tool renders
```

- **Analysis → optimal**: per player, aggregate rating by position, weight by team result / win-streak membership → pick optimal position+role; map to the season's game_role via heatmap similarity.
- **Export**: generate a formations JSON keyed by (season, game_version) from `player_role_map`.

## Tool strategy (fc26-heatmap.html)

- **Now (25/26, FC26)**: formations are hardcoded in JS (incl. `아스톤 빌라 25/26 (실측)/(역할)`, and soon `(최적)`). Works, ships today.
- **Next (26/27 and/or FC27)**: refactor the tool to **load formations from the exported JSON** instead of hardcoding, and make the role/kernel library (`MAPS`/`ROLE_SETS`) selectable by game version. Then a new season = new DB rows + re-export; a new game = new `game_roles` + kernel set. No structural tool rewrite.

## Naming convention

Formations in the tool: `아스톤 빌라 <season> (<kind>)` e.g. `아스톤 빌라 26/27 (최적)`.
Keeps seasons/versions side-by-side and comparable in the A/B panels.

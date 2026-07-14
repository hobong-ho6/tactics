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
   - `tactic_observations(season,scope,claim,evidence,source,confidence)` — team-level tactical facts
     (philosophy, build-up, defensive block, in-possession shape, per-match modulation axes, verdicts).
   - `team_match_stats(event_id,date,xg/shots/big-chances/passes/long-balls/crosses/corners for both sides,formation_v/o)`
     — per-match TEAM stats (SofaScore); verifies foundation claims (formation constancy, short build-up)
     and powers possession/xG phase analysis.
   - `player_duties(season,player_id,position,duties,execution,adherence,game_role_implication,source,confidence)`
     — per-player duty spec vs measured execution review; feeds squad selection and game-role refinement.
     Variable-position players get one row per position held.
   - `player_match_positions(season,player_id,event_id,date,…,avg_x,avg_y,minutes,rating,started,pos_class)`
     — full-season per-match average positions (SofaScore API); the measured basis for
     most-used / best-performed position. Aggregated by the `v_position_profile` view.
   - `transfer_targets(window,name,slot,likelihood,map25,tool_x,tool_y,opt_role/focus,fit_role/focus,fit_sim,…)`
     — rumoured signings analyzed with the same pipeline (recent-6-match measured grid,
     kernel-fit role); one row per (target, Villa slot). Feeds the tool's squad-builder 영입 options.
   - `transfer_outgoing(window,player_id,dest_club,likelihood,rationale,source,confidence)`
     — rumoured departures of existing Villa players (`player_id` FK into `players`); one row
     per (window, player). No heatmap/fit analysis — this tracks departure risk, not role fit.
   - View `v_best`.

2. **Game system library (per FC version)** — `game_roles(game_version,role_id,name,position_type,focuses)`
   + `game_tactic_params(game_version,param,option,description)` (team-level setting vocabulary:
   build-up style, defensive approach, line height, tactic code).
   - FC26 role set differs from FC27's; each version is its own set of rows. The heatmap kernels
     (`MAPS` in the tool) belong here conceptually — long term they move out of hardcoded JS into this table
     so FC27 is "add rows", not "edit the tool".

3. **Derived mapping (what the tool renders)** — `player_role_map(player_id,season,game_version,kind,pos_label,x,y,role_id,focus,map25,rationale)`
   + `team_tactic_setups(season,game_version,kind,formation,build_up_style,defensive_approach,line_height,tactic_code,rationale,confidence)`.
   - `kind`: `measured` (position-pure aggregate of real heatmap grids at the player's primary slot), `measured:<class>` (position-pure aggregate at a secondary position, e.g. measured:CAM), `...@dom`/`...@tight` (context-split aggregates: 2+goal wins vs contested matches), `role` (closest game role to the heatmap), `optimal` (best position/role by rating+results), `match:<tag>` (single-match recreation).
   - These two tables are the **contract** between analysis and the game: one (season, game_version, kind) join yields the complete in-game tactic — team settings + 11 player roles.

## Pipeline (re-run each season)

```
research (Workflows) → ingest into DB → analyze (rating×result by position) → write player_role_map → export formation JSON → tool renders
```

- **Analysis → optimal**: per player, aggregate rating by position, weight by team result / win-streak membership → pick optimal position+role; map to the season's game_role via heatmap similarity.
- **Export**: generate a formations JSON keyed by (season, game_version) from `player_role_map`.

## Tool strategy (fc26-heatmap.html)

- **Now (25/26, FC26)**: formations are hardcoded in JS (incl. `아스톤 빌라 25/26 (실측)/(역할)`, and soon `(최적)`). Works, ships today.
- **Next (26/27 and/or FC27)**: refactor the tool to **load formations from the exported JSON** instead of hardcoding, and make the role/kernel library (`MAPS`/`ROLE_SETS`) selectable by game version. Then a new season = new DB rows + re-export; a new game = new `game_roles` + kernel set. No structural tool rewrite.
- **Done (2026-07-14, transfer-target slice only)**: `transfer_targets`/`transfer_outgoing` no
  longer need hand-edits in three places. `scripts/sync_transfer_ui.py` regenerates the
  `TRANSFER_TARGETS`/`TRANSFER_OUTGOING` mirror arrays from the DB, and the tool's
  `injectTransferCandidates()` derives SQUAD_SLOTS/PLAYER_BEST/XI_POOL incoming-candidate
  entries from that mirror at page load. Owned-squad data (FC_STATS, season formations, etc.)
  is still hand-curated — this only closes the recurring incoming-candidate sync gap.

## Naming convention

Formations in the tool: `아스톤 빌라 <season> (<kind>)` e.g. `아스톤 빌라 26/27 (최적)`.
Keeps seasons/versions side-by-side and comparable in the A/B panels.

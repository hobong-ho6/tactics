"""DB → site/data/*.json 익스포트 — v1 sync_transfer_ui.py의 후계.

파일 구조 (팀·버전 추가 = 파일 추가, 코드 수정 없음):
  site/data/index.json          — 팀·regime·버전 메타 (허브/네비가 로드)
  site/data/kernels/{GV}.json   — 역할·포커스·위치변형·팀전술 파라미터 (버전당 1파일)
  site/data/teams/{CODE}.json   — regime 자산 전체: slots / slot_candidates / squad / prescriptions /
                                  match_reports / transfer{targets,outgoing,ledger} / setups / profile

원칙:
  · 값은 DB 컬럼의 1:1 사상 — 여기서 가공하지 않는다 (가공은 분석 단계의 일)
  · 매 실행 전 게이트 통과 필수 (호출측 scripts/export.py가 강제)
  · 키 정렬·결정적 직렬화 — DB 무변경이면 diff 0
"""
import json
import sqlite3
from pathlib import Path

from . import DB, ROOT

SITE_DATA = ROOT / "site" / "data"

__all__ = ["export_all"]


def _rows(con, sql, params=()):
    con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute(sql, params).fetchall()]


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def export_all(db_path=None, window="2026-summer"):
    con = sqlite3.connect(db_path or DB)
    written = []

    # ── index.json ───────────────────────────────────────────────────
    regimes = _rows(con, """SELECT r.id, r.team_code, t.name team_name, t.name_kr team_kr,
                                   r.manager, r.manager_kr, r.is_main, r.start
                            FROM regimes r JOIN teams t ON t.code=r.team_code
                            WHERE r.end IS NULL ORDER BY r.is_main DESC, r.id""")
    versions = _rows(con, "SELECT code, released, notes FROM game_versions ORDER BY code")
    written.append(_write(SITE_DATA / "index.json",
                          {"regimes": regimes, "game_versions": versions, "window": window}))

    # ── kernels/{GV}.json ────────────────────────────────────────────
    for (gv,) in con.execute("SELECT code FROM game_versions"):
        roles = _rows(con, """SELECT role_id, name, name_en, position_type, focuses
                              FROM game_roles WHERE game_version=? ORDER BY role_id""", (gv,))
        changes = _rows(con, """SELECT area, change, evidence, impact, source, confidence, recorded
                               FROM game_system_changes WHERE game_version=? ORDER BY id""", (gv,))
        if not roles and not changes:
            continue                      # 커널도 시스템 사실도 없는 버전은 파일을 만들지 않는다
        # ⭐ 역할 커널이 없어도 system_changes가 있으면 파일을 쓴다(2026-09-21) — FC27은 역할 목록 확정 전이라
        #    커널이 비어 있는데, 그 때문에 FC27 시스템 사실 16건이 웹에서 통째로 안 보이고 있었다.
        focus = _rows(con, """SELECT role_id, focus, kernel25, plus, equal, negative,
                                     ea_role_name, description, movement_kr
                              FROM game_role_focus WHERE game_version=?
                              ORDER BY role_id, focus""", (gv,))
        variants = _rows(con, """SELECT role_id, focus, pitch_x, kernel25
                                 FROM game_role_variants WHERE game_version=?
                                 ORDER BY role_id, focus, pitch_x""", (gv,))
        params = _rows(con, """SELECT param, option, description FROM game_tactic_params
                               WHERE game_version=? ORDER BY param, option""", (gv,))
        # 역할별 핵심 속성 가중(migration 038) — 진화 순위의 「역할 가중 점수」 원료. 판단값(MEDIUM)이며 커널(kernel25)과 별개 층.
        key_attrs = _rows(con, """SELECT role_id, attr, weight FROM game_role_key_attrs
                                  WHERE game_version=? ORDER BY role_id, weight DESC, attr""", (gv,))
        written.append(_write(SITE_DATA / "kernels" / f"{gv}.json",
                              {"game_version": gv, "roles": roles, "focus": focus,
                               "variants": variants, "tactic_params": params,
                               "system_changes": changes, "role_key_attrs": key_attrs}))

    # ── game_stats/{GV}.json — sofifa 스탯·플레이스타일 (name_kr 키, 표시 전용) ──
    for (gv,) in con.execute("SELECT DISTINCT game_version FROM player_game_stats"):
        # ⚠️ 같은 name_kr에 roster_date가 여럿이다(FC26 5개·FC27 3개). ORDER BY roster_date로
        #    **최신 행이 마지막에 와서 이기게** 고정한다 — 종전에는 어느 행이 이길지 비결정적이었다.
        #    `player_id`·`roster_date`·`source`는 화면이 id 우선 조인·시점·공식여부를 읽는 데 쓴다.
        gs = _rows(con, """SELECT name_kr, player_id, roster_date, sofifa_name, sofifa_id, club,
                                  positions, best_pos, age, height_cm, weight_kg, card_image_url,
                                  value_eur, preferred_foot, accelerate,
                                  ovr, pot, pac, sho, pas, dri, def, phy, playstyles, role_familiarity, attrs,
                                  source
                           FROM player_game_stats WHERE game_version=?
                             AND COALESCE(source,'') NOT LIKE '%collect_futgg_history%'
                           ORDER BY name_kr, roster_date""", (gv,))
        # ⛔ 출시판 시계열 행(collect_futgg_history.py)은 여기서 제외한다 — 이 파일은 name_kr 키라 sofifa 표시명과
        #    players.name_kr이 다른 선수(스즈키 지온↔스즈키)에서 출시판 행이 라이브판을 가로채 카드 비교의 기준 시점이 바뀐다.
        #    시계열은 아래 history.json(player_id 키)이 담는다.
        if not gs:
            continue
        written.append(_write(SITE_DATA / "game_stats" / f"{gv}.json", {g["name_kr"]: g for g in gs}))

    # ── game_stats/meta.json — 「지금 메타」 스냅샷(migration 042). 최신 pulled + 과거 날짜 목록.
    #    ⛔ 우리 감독 재현(team_tactic_setups)과 다른 층이다 — 화면이 섞어 쓰지 않도록 파일부터 분리한다.
    meta_rows = _rows(con, """SELECT game_version, pulled, kind, category, item, value, alternatives, scope, priority,
                                     rationale, source, confidence
                              FROM fc_meta_snapshots
                              WHERE pulled=(SELECT MAX(pulled) FROM fc_meta_snapshots)
                              ORDER BY kind, priority IS NULL, priority, category, item""")
    meta_dates = [r["pulled"] for r in _rows(con, "SELECT DISTINCT pulled FROM fc_meta_snapshots ORDER BY pulled DESC")]
    written.append(_write(SITE_DATA / "game_stats" / "meta.json", {"rows": meta_rows, "pulled_dates": meta_dates}))

    # ── game_stats/history.json — 버전별 변화 추적(player_id 키, 2026-09-12 신설) ──
    # ⭐ 한 버전에 시점이 둘이다: 「출시판」(fut.gg base 아이템 — collect_futgg_history.py, FC27 fut.gg 공식 드롭)과
    #    「라이브판」(sofifa 시즌 중 로스터). 기준 시점을 섞으면 Δ 부호가 뒤집힌다(obs#249) — kind로 갈라 내보낸다.
    hist = {}
    for r in _rows(con, """SELECT player_id, game_version, roster_date, ovr, pac, sho, pas, dri, def, phy,
                                  positions, best_pos, playstyles, club, source
                           FROM player_game_stats WHERE player_id IS NOT NULL
                           ORDER BY player_id, game_version, roster_date"""):
        src = r.pop("source") or ""
        r["kind"] = "출시판" if ("collect_futgg_history" in src or r["game_version"] == "FC27") else "라이브판"
        hist.setdefault(str(r.pop("player_id")), []).append(r)
    written.append(_write(SITE_DATA / "game_stats" / "history.json", hist))

    # ── game_stats/cards.json — 카드 버전(base + 프로모, player_id 키, 2026-09-14 신설) ──
    # ⭐ player_game_stats(능력치 정본)와 다른 축이다 — 같은 선수에게 시즌 중 계속 붙는 **아이템 목록**.
    #    OVR 내림차순으로 내보내 화면이 「가장 높은 카드」를 먼저 보여준다.
    cards = {}
    for r in _rows(con, """SELECT player_id, game_version, ea_item_id, is_base, rarity_name, released_at,
                                  ovr, pac, sho, pas, dri, def, phy, positions, best_pos, playstyles,
                                  skill_moves, weak_foot, accelerate, card_image_url, futgg_url,
                                  roles_plus, roles_plus_plus, ea_item_id AS item_id,
                                  acquisition, is_special, first_seen,
                                  attrs, height_cm, weight_kg, birthdate, preferred_foot, nation, league, club,
                                  simple_card_url, render_url
                           FROM player_card_items WHERE player_id IS NOT NULL
                           ORDER BY player_id, game_version DESC, ovr DESC, released_at DESC"""):
        cards.setdefault(str(r.pop("player_id")), []).append(r)
    written.append(_write(SITE_DATA / "game_stats" / "cards.json", cards))

    # ── game_stats/evolutions.json — 진화 경로와 결과 카드 (2026-09-17 신설, 사용자 지시
    #    「어떻게 진화하면 좋을지도 수집해서 페이지 내에서 최적의 제안을 보여줘」).
    #    ⭐ 카드와 층이 다르다: cards.json은 **이미 발매된 아이템**, 여기는 **적용하면 생기는 결과**다.
    #    ⛔ 「최적」 순위를 여기서 굳히지 않는다 — 화면이 그 선수의 처방 역할과 대조해 만든다.
    #    Role+/++가 raw id라 `fc_role_familiarity_map`을 함께 내보낸다(FC27 커널은 아직 없다 — obs#629).
    evos = {}
    # ⚠️ `player_evolutions.name_kr`은 fut.gg 수집 당시 표기라 `players.name_kr`과 갈린다
    #    (지모알로바가 `Jamaldeen Jimoh-Aloba`로 남아 있었다). 사람 이름의 정본은 `players`다.
    for r in _rows(con, """SELECT e.game_version, e.player_id, e.base_ea_id,
                                  COALESCE(p.name_kr, p.name, e.name_kr) name_kr, e.path_key,
                                  e.evolution_ids, e.evolution_names, e.evolution_urls, e.steps,
                                  e.coins_cost, e.points_cost, e.training_time, e.is_expired,
                                  e.ovr_before, e.ovr_after, e.upgrades, e.six_before, e.six_after,
                                  e.playstyles_after, e.roles_plus_after, e.roles_plus_plus_after, e.pulled,
                                  e.path_json, e.path_choices
                           FROM player_evolutions e
                           LEFT JOIN players p ON p.id=e.player_id
                           JOIN (SELECT player_id, MAX(pulled) mp FROM player_evolutions
                                  WHERE player_id IS NOT NULL GROUP BY player_id) m
                             ON m.player_id=e.player_id AND m.mp=e.pulled
                            WHERE e.player_id IS NOT NULL
                           ORDER BY e.player_id, (e.ovr_after - e.ovr_before) DESC, e.steps"""):
        evos.setdefault(str(r.pop("player_id")), []).append(r)
    # ⛔⛔ **부분 수집이 온전한 직전 회차를 덮지 않게 한다** (2026-09-23 사용자 지적
    #    「Midfield Glow Up은 보가르드가 할 수 있는데 적용 가능 0명이라고 나온다」).
    #    ⑴ 무엇이 터졌나: 종전 조건은 `pulled = (SELECT MAX(pulled) …)` **전역 최신 하나**였다.
    #       그날 수집이 ATM 11명에서 끊기자 **나머지 42명의 경로가 통째로 사라졌고**, 보가르드의
    #       `Intro to Pathway → Midfield Glow Up`이 화면에서 없는 것이 됐다(fut.gg는 지금도 준다).
    #    ⑵ ⇒ **선수별 최신 스냅샷**을 쓴다. 한 선수만 다시 받아도 다른 선수가 비지 않는다.
    #       만료는 `is_expired`가, 소진은 내 구단 원장이 따로 잡으므로 이월이 위험하지 않다.
    #    ⚠️ 다만 **이월분은 실측과 같은 얼굴로 두지 않는다**(카탈로그의 `carried_from`과 같은 규약) —
    #       그 회차에 조회되지 않았다는 사실을 화면이 배지로 적는다.
    _latest_pull = con.execute("SELECT MAX(pulled) FROM player_evolutions").fetchone()[0]
    for rows in evos.values():
        for r in rows:
            if r["pulled"] != _latest_pull:
                r["carried_from"] = r["pulled"]
    rolemap = _rows(con, """SELECT game_version, ea_id, kind, slug, name, position_name
                            FROM fc_role_familiarity_map ORDER BY game_version, kind, ea_id""")
    # 카탈로그(fc_evolutions, 최신 pulled) + 내 구단 원장(fut_*) — 진화 메뉴(evolutions.html)가 읽는다 (migration 036)
    catalog = _rows(con, """SELECT game_version, evo_id, name, slug, url, description, category, unlock_text,
                                   coins_cost, points_cost, token_cost, repeatability, is_reward, is_gk, is_timed,
                                   training_time, created_at, end_time, end_submission_time, requirements_text,
                                   total_upgrades_text, levels, allowed_prior_ids, number_of_players, is_expired, pulled,
                                   carried_from
                            FROM fc_evolutions WHERE pulled=(SELECT MAX(pulled) FROM fc_evolutions)
                            ORDER BY is_expired, end_time, evo_id""")
    # ⭐⭐ **적용 가능 선수**(migration 058) — 경로 축(`player_evolutions`)이 못 덮는 진화를 여는 축이다.
    #    fut.gg `paths/v2`는 base 카드 기준 조합 경로만 줘서 ⑴ 특별 카드 전용 진화 ⑵ 단독 진화를 놓친다
    #    (2026-09-22 실측 33쌍 · Relentless는 카탈로그에도 없어 손수집했다).
    #    ⛔ 경로가 없다는 사실을 화면에서 숨기지 않는다 — `has_path`로 함께 내려보낸다(결손과 0은 다르다, obs#132).
    elig_rows = _rows(con, """
        SELECT e.evo_id, e.player_id, e.ea_item_id, e.is_base,
               COALESCE(p.name_kr, p.name) name, e.pulled
          FROM fc_evolution_eligibility e JOIN players p ON p.id=e.player_id
          JOIN (SELECT evo_id, MAX(pulled) mp FROM fc_evolution_eligibility GROUP BY evo_id) m
            ON m.evo_id=e.evo_id AND m.mp=e.pulled
         ORDER BY e.evo_id, p.id""")
    # ⚠️ 여기도 **진화별 최신 회차**를 쓴다(위 경로 축과 같은 이유) — 부분 수집이 다른 진화의 목록을 비우면 안 된다.
    #    ⛔ 단 회차가 **조회한 진화 안에서** 선수가 빠진 것은 사실이므로 그건 그대로 반영된다.
    # ⛔ `has_path` 판정은 **위에서 실제로 내보낸 경로**와 같은 집합이어야 한다 —
    #    여기만 전역 MAX(pulled)로 세면 경로가 있는 쌍이 「경로 미제공」으로 중복 표시된다.
    _covered = set()
    for pid, rows in evos.items():
        for r in rows:
            for i in json.loads(r["evolution_ids"] or "[]"):
                _covered.add((int(pid), i))
    for r in elig_rows:
        r["has_path"] = (r["player_id"], r["evo_id"]) in _covered
    # ⭐ PlayStyle **숫자 id → 이름** (2026-09-22) — 진화 분기(upgradeOptions)가 PS를 **id로만** 주기 때문에
    #    이게 없으면 화면이 「옵션1: play_style 5」처럼 못 읽는 값을 띄운다.
    #    ⛔ 표를 손으로 적지 않는다 — `player_evolutions`의 **id 배열 ↔ 이름 배열**을 교차시켜 역산한다
    #       (262건 표본에서 29개 확정 · 런북에 적힌 알려진 값 6=Pinged Pass·19=First Touch 등과 일치).
    ps_pairs = {}
    for r in _rows(con, """SELECT playstyles_after, path_json FROM player_evolutions
                            WHERE playstyles_after IS NOT NULL"""):
        try:
            ids = json.loads(r["playstyles_after"] or "[]")
            pj = json.loads(r["path_json"] or "[]")
            names = (pj[-1].get("playstyles") if pj else None) or []
        except Exception:
            continue
        if not ids or len(ids) != len(names):
            continue
        for i in ids:
            c = ps_pairs.setdefault(i, {})
            for nm in names:
                c[nm] = c.get(nm, 0) + 1
    ps_names = {}
    for i, c in ps_pairs.items():
        top = max(c.values())
        best = [nm for nm, v in c.items() if v == top]
        if len(best) == 1:          # 동률이면 확정하지 않는다(추측 금지)
            ps_names[str(i)] = best[0]
    # ⛔⛔ **역산은 표본이 줄면 함께 줄어든다** — 코스메틱 경로 210행을 지우자 29개 → 17개가 되어
    #     화면에 「PlayStyle #8」이 떴다(2026-09-22 실증). ⇒ 누적 표(migration 057)를 **먼저 깔고**
    #     이번 역산은 **새로 확정된 것만 덧칠**한다. 한번 확정된 이름은 다시 사라지지 않는다.
    #     ⭐ 새로 확정된 id가 있으면 그 표에도 넣어 줘야 다음 회차가 이어받는다(collect_futgg_evolutions 몫).
    table = {str(r["ea_id"]): r["name"] for r in _rows(con,
        "SELECT ea_id, name FROM fc_playstyle_ids WHERE game_version='FC27'")}
    ps_names = {**table, **ps_names}

    # 진화 해금 과제(migration 056) — 최신 pulled만. 화면이 진화 카드에 「그래서 뭘 하면 되나」를 띄운다.
    # ⚠️ 해금 문구는 **과제 이름**일 때도 그룹 이름일 때도 있어 양쪽을 다 내보낸다(매칭은 화면이 한다).
    obj_tasks = _rows(con, """SELECT group_slug, group_name, group_category, task_name, task_text,
                                     task_text_kr, reward
                              FROM fc_objective_tasks
                             WHERE pulled=(SELECT MAX(pulled) FROM fc_objective_tasks)
                             ORDER BY group_name, id""")
    # ⭐⭐ **선수별 「지금 카드 상태」 정본** (2026-09-22 — 사용자 지적
    #    「각 메뉴가 공통 DB를 보지 않고 개별적으로 업데이트되는가 — 동일한 상태를 갖도록 개선」).
    #    ⛔ 종전에는 화면마다 「현재」를 **각자 골랐다** — 어디선 `player_card_items`(기준 카드),
    #       어디선 `fut_club_players.current_*`(EA 실측), 어디선 fut.gg 경로의 `ovr_before`(기준 카드).
    #       같은 선수가 메뉴마다 다른 OVR로 보였다(Alysson 70 ↔ 78).
    #    ⇒ **여기서 한 번 정하고 `club.state`로 내보낸다.** 화면은 고르지 말고 이걸 읽는다.
    #    규칙: EA 싱크 실측(`fut_club_players`)이 있으면 그것이 현재다. 없으면 기준 카드로 물러선다.
    #    `basis`에 어느 쪽인지 적어 화면이 「실측인가 기준값인가」를 숨기지 않게 한다.
    #    ⭐ **표시 이름도 여기서 하나로 정한다**(2026-09-22 전수 조사). `fut_club_players.name`은
    #       fut.gg 표기라 **영문·한글이 섞여 있고**(Suzuki·Jackson·Madjo…) 음차도 갈린다
    #       (루제리 ↔ `players.name_kr` 마테오 루헤리). 같은 선수가 화면마다 다른 이름으로 보였다.
    #    ⇒ 사람 이름의 정본은 `players.name_kr`이다(불변규칙 6의 조인 규칙과 같은 축). fut.gg 원표기는
    #       `name_fut`로 함께 내보낸다 — 지우면 EA/fut.gg 화면과 대조할 때 근거를 잃는다.
    club_state = _rows(con, """
        SELECT c.player_id, c.id club_player_id,
               COALESCE(pl.name_kr, pl.name, c.name) name, c.name name_fut,
               c.current_ovr ovr, c.current_six six, c.current_attrs attrs,
               c.current_playstyles playstyles, c.current_roles_plus roles_plus,
               c.current_roles_plus_plus roles_plus_plus,
               c.chem_style_ea, c.chem_points,
               i.ovr base_ovr, i.attrs base_attrs, i.ea_item_id base_ea_id,
               i.skill_moves, i.weak_foot, i.preferred_foot, i.accelerate,
               i.height_cm, i.weight_kg, i.positions, i.card_image_url,
               CASE WHEN c.current_attrs IS NOT NULL THEN 'ea-sync' ELSE 'base-card' END basis,
               (SELECT COUNT(*) FROM fut_evolution_log l
                 WHERE l.club_player_id=c.id AND l.is_void=0 AND COALESCE(l.level,1)=1) evo_runs,
               -- ⭐ **화면의 「진화 N회」는 이것이다** — 「회 = 밟은 단계 수」가 사용자 결정이다
               --    (2026-09-21, 4단계 완주 = 4회). `evo_runs`(적용 횟수)는 **소진 계산 전용**이라
               --    단위가 다르다. 둘을 섞으면 같은 선수가 화면마다 다른 횟수로 보인다
               --    (지모알로바 6 ↔ 2 · 루제리 3 ↔ 1). ⛔ `fut_club_players.evo_count`는 스크립트가
               --    +1 하는 값이라 원장과 어긋날 수 있다 — 원장에서 직접 센 이 값을 쓴다.
               (SELECT COUNT(*) FROM fut_evolution_log l
                 WHERE l.club_player_id=c.id AND l.is_void=0) evo_levels,
               (SELECT GROUP_CONCAT(DISTINCT l.evo_name) FROM fut_evolution_log l
                 WHERE l.club_player_id=c.id AND l.is_void=0) evo_names
          FROM fut_club_players c
          LEFT JOIN player_card_items i ON i.ea_item_id=c.ea_item_id
          LEFT JOIN players pl ON pl.id=c.player_id
         WHERE c.status='owned' AND c.player_id IS NOT NULL""")
    # ⭐⭐ 경기 기록·자산 축(migration 061) — GG Club 보유행이 주는 **EA 실측**이다.
    #    ⛔ 누적값이라 **최신 pulled만** 내보낸다(추이는 DB에 남는다 — 화면이 쌓인 걸 다 읽을 이유가 없다).
    #    ⚠️ `games_played`는 현재 보유분 기준, `lifetime_*`은 카드 일생 누적이라 다를 수 있다.
    club_stats = {str(r["club_player_id"]): r for r in _rows(con, """
        SELECT s.club_player_id, s.games_played, s.goals, s.assists, s.yellow_cards, s.red_cards, s.ga,
               s.lifetime_games_played, s.lifetime_goals, s.lifetime_assists, s.pulled,
               c.is_untradeable, c.is_in_active_squad, c.is_captain, c.kit_number, c.number_of_owners
          FROM fut_club_player_stats s JOIN fut_club_players c ON c.id=s.club_player_id
         WHERE s.pulled=(SELECT MAX(pulled) FROM fut_club_player_stats)""")}

    # ⭐ 해금 상태(migration 060) — **소진과 다른 축**이다. 시즌패스 레벨·프리미엄 구매 여부가 없으면
    #    `[SP 11]`·`[SP+ 14]` 진화를 「지금 걸 수 있다」로 잘못 보여준다(2026-09-23 실증).
    # ⛔⛔ **결손 속성을 0으로 세지 않는다**(2026-09-23 실측 · obs#132 「결손과 0은 다르다」).
    #    GG Club의 `current_attrs`는 **28속성**만 준다 — 「프리킥 정확도」가 **보유 99명 전원에서 빠진다.**
    #    그런데 6대 스탯 구성식(`fc_face_stats`)은 PAS에서 그 속성을 0.05로 요구한다.
    #    ⇒ 화면이 0으로 계산해 **PAS가 89명 전원 2~4 낮게** 나왔다(「적용 후 6대 스탯」도 같이 틀렸다).
    #    ⇒ 기준 카드(`player_card_items.attrs`)에서 **빠진 속성만** 메운다. 6대 스탯 전항 일치율이
    #      **0% → 91%**로 회복된다(남는 9%는 진화가 그 속성을 올린 카드·반올림 경계).
    #    ⚠️ 덮어쓰지 않는다 — EA가 준 값이 있으면 그것이 이긴다. 메운 사실은 `attrs_filled`에 적는다.
    for r in club_state:
        cur = json.loads(r["attrs"] or "null") or None
        base = json.loads(r["base_attrs"] or "null") or None
        if cur and base:
            miss = {k: v for k, v in base.items() if k not in cur}
            if miss:
                r["attrs"] = json.dumps({**miss, **cur}, ensure_ascii=False)
                r["attrs_filled"] = sorted(miss)          # 어느 속성을 기준 카드에서 가져왔는지
    accounts = _rows(con, "SELECT id, name, platform, game_version, notes, created, "
                          "season_pass_level, has_premium_pass, unlocks_checked FROM fut_accounts ORDER BY id")
    # 목표형 해금(「Pep's Domination」 등)은 레벨로 계산되지 않는다 — 진화 단위 기록을 함께 내보낸다.
    unlocks = _rows(con, "SELECT account_id, evo_id, unlocked, noted, note FROM fut_evolution_unlocks")
    # 보유 선수 — 케미스트리 원료(국적·리그·클럽·포지션, migration 044)를 카드 표에서 붙여 함께 내보낸다.
    # 화면이 케미 XI를 계산하려면 이 4개가 있어야 한다. 조인은 아이템 id로만 한다(이름 조인 금지).
    # ⭐ `name`은 `club.state`와 **같은 규칙**으로 정한다(위 주석) — 두 표가 갈리면 같은 화면 안에서도 이름이 섞인다.
    club = _rows(con, """SELECT f.id, f.account_id, f.player_id, f.ea_item_id,
                                COALESCE(pl.name_kr, pl.name, f.name) AS name, f.name AS name_fut,
                                f.acquired, f.acquired_how, f.status,
                                f.current_ovr, f.current_six, f.current_playstyles, f.current_roles_plus,
                                f.current_roles_plus_plus, f.evo_count, f.notes, f.updated,
                                -- ⭐ 29속성 EA 실측(2026-09-22) — GG Club이 그대로 준다. 화면은 이것을 정본으로 쓰고
                                --    기준 카드+진화 보상 재구성은 검증용으로만 쓴다.
                                f.current_attrs,
                                c.ovr AS card_ovr, c.positions, c.nation, c.league, c.club, c.is_icon, c.is_hero,
                                c.chem_extra, c.card_image_url, c.attrs,
                                -- 스킬무브·약발·주발(2026-09-21 사용자 요청) — 카드 표에만 있다.
                                c.skill_moves, c.weak_foot, c.preferred_foot, c.accelerate,
                                c.height_cm, c.weight_kg, c.birthdate,
                                f.chem_style_ea, f.chem_points, f.synced_at
                         FROM fut_club_players f
                         LEFT JOIN player_card_items c ON c.ea_item_id=f.ea_item_id AND c.game_version='FC27'
                         LEFT JOIN players pl ON pl.id=f.player_id
                         ORDER BY f.account_id, f.status, f.name""")
    # ⭐ `is_void`(migration 053)를 함께 내보낸다 — 화면의 소진 계산이 **무효 행을 세면 안 된다**
    #   (마조 Striker Glow Up은 적용된 적이 없는데 소진으로 잠겨 있었다).
    log = _rows(con, """SELECT id, club_player_id, evo_id, evo_name, level, applied_at, completed_at, ovr_before, ovr_after,
                               six_before, six_after, attrs_delta, playstyles_after, roles_plus_after, roles_plus_plus_after,
                               is_void, notes
                        FROM fut_evolution_log ORDER BY applied_at, id""")
    # 시세 — 최신 pulled만(ea_item_id 키). NULL은 「미형성」이며 화면이 그렇게 쓴다(migration 037)
    prices = {str(r.pop("ea_item_id")): r for r in _rows(con, """SELECT ea_item_id, price, has_price, momentum, platform, pulled
                                                              FROM player_card_prices
                                                              WHERE pulled=(SELECT MAX(pulled) FROM player_card_prices)""")}
    # 케미스트리 스타일 24종(migration 045) — 화면이 역할 가중과 곱해 추천 순위를 만든다.
    chem_styles = _rows(con, """SELECT style_id, ea_id, name, is_gk, boosts FROM fc_chemistry_styles
                                WHERE game_version='FC27' ORDER BY is_gk, style_id""")
    # 실제 스쿼드(migration 050) — 「제안」과 대조하려면 지금 쓰는 XI가 있어야 한다.
    squad = _rows(con, "SELECT * FROM fut_squads")
    squad_slots = _rows(con, "SELECT account_id, grp, idx, ea_item_id, gg_player_id FROM fut_squad_slots ORDER BY grp DESC, idx")
    # ⭐ 내 구단 **인게임 전술**(migration 054) — 최신 pulled 1회차만. 날짜별로 쌓이므로 화면은 최신만 읽고 갱신일을 함께 띄운다.
    #   ⛔ 감독 재현(`team_tactic_setups`)과 **다른 층**이다 — 화면에서도 섞지 않는다.
    tactics = _rows(con, """SELECT * FROM fut_tactics
                            WHERE pulled=(SELECT MAX(pulled) FROM fut_tactics)""")
    tactic_roles = _rows(con, """SELECT position_id, position_name, role_ea_id, role_name, focus FROM fut_tactic_roles
                                 WHERE pulled=(SELECT MAX(pulled) FROM fut_tactic_roles) ORDER BY position_id""")
    written.append(_write(SITE_DATA / "game_stats" / "evolutions.json",
                          {"paths": evos, "role_map": rolemap, "catalog": catalog, "prices": prices,
                           "chem_styles": chem_styles, "squad": squad, "squad_slots": squad_slots,
                           "obj_tasks": obj_tasks, "ps_names": ps_names, "eligible": elig_rows,
                           # fut.gg 케미 신호(migration 055) — 최신 pulled만. 배지는 등급이 아니라 AcceleRATE다.
                           "chem_signals": _rows(con, """SELECT ea_item_id, style_name, accelerate, vote_pct
                                                           FROM futgg_chem_signals
                                                          WHERE pulled=(SELECT MAX(pulled) FROM futgg_chem_signals)"""),
                           "canon_roles": _rows(con, """SELECT pos, role_id, focus, game_version FROM slot_canon_roles
                                                       WHERE regime_id=1 AND formation='4-2-3-1 Wide'"""),
                           "face_stats": _rows(con, """SELECT abbr, is_gk, attr, weight FROM fc_face_stats
                                                      WHERE game_version='FC27' ORDER BY is_gk, abbr"""),
                           "chem_meta": _rows(con, """SELECT item, value, alternatives, rationale, source
                                                     FROM fc_meta_snapshots WHERE category='chem_style'
                                                     AND pulled=(SELECT MAX(pulled) FROM fc_meta_snapshots WHERE category='chem_style')"""),
                           "tactics": tactics, "tactic_roles": tactic_roles,
                           "club": {"accounts": accounts, "players": club, "log": log,
                                     # ⭐ 화면이 「현재」를 각자 고르지 않게 하는 정본(위 주석)
                                     "state": {str(r["player_id"]): r for r in club_state},
                                     "stats": club_stats, "unlocks": unlocks}}))

    # ── videos.json — 영상 1편 = 항목 1개 (2026-09-15 신설, 사용자 지시) ──
    # ⭐ 세 층을 그대로 내보낸다: 메타(파싱) · obs_points(검증된 판정) · summary/key_points(사람 요약).
    #    `by_report`는 경기 화면이, `all`은 채널 브라우징이 쓴다.
    obs_by_id = {r["id"]: r for r in _rows(con, """SELECT id, claim, scope, confidence FROM observations""")}
    # ⭐ 네 번째 층 — 구현 주장(migration 033, docs/30 8단계). 요약이 「구현의 무엇을 건드리는가」를
    #    정형 행으로 갖는다. 화면은 이걸로 배지를 그린다(자유 서술에서 추출하지 않는다).
    claims_by_vid = {}
    for c in _rows(con, """SELECT c.video_id, c.axis, c.role_id, c.focus, c.field, c.value,
                                  c.verdict, c.verdict_note, c.quote, c.team_code,
                                  COALESCE(p.name_kr, p.name) AS player
                           FROM video_impl_claims c
                           LEFT JOIN players p ON p.id = c.player_id
                           ORDER BY c.axis, c.id"""):
        claims_by_vid.setdefault(c.pop("video_id"), []).append(c)
    videos, by_report = [], {}
    for v in _rows(con, """SELECT id, video_id, lang, report_id, team_code, channel, title, published,
                                  published_approx, url, transcript_path, kind, summary, key_points,
                                  obs_refs, confidence
                           FROM match_videos
                           ORDER BY (published IS NULL), published DESC, channel"""):
        refs = [int(x) for x in (v.pop("obs_refs") or "").split(",") if x.strip().isdigit()]
        # ⛔ obs 전문을 그대로 싣는다 — 화면에서 요약하지 않는다(원장 텍스트가 정본이다)
        v["obs_points"] = [{"id": i, "claim": obs_by_id[i]["claim"], "scope": obs_by_id[i]["scope"]}
                           for i in refs if i in obs_by_id]
        v["key_points"] = [x for x in (v["key_points"] or "").split("\n") if x.strip()]
        # ⛔ 「주장 없음(none)」과 「미작성(빈 배열)」을 구분해 내보낸다 — DB에서와 같은 구분이다
        v["impl_claims"] = claims_by_vid.get(v["video_id"], [])
        videos.append(v)
        if v["report_id"]:
            by_report.setdefault(str(v["report_id"]), []).append(v["id"])
    written.append(_write(SITE_DATA / "videos.json", {"all": videos, "by_report": by_report}))

    # ── teams/{CODE}.json ────────────────────────────────────────────
    for rg in regimes:
        rid, code = rg["id"], rg["team_code"]
        slots = _rows(con, """SELECT formation, pos, slot_type, x, y, sort_order
                              FROM slots WHERE regime_id=? ORDER BY formation, sort_order""", (rid,))
        # 슬롯별 전술 정본(인선 무관) — migrations/008. 프리셋(fc26:opt:*)과 다르면 편차로 읽는다.
        canon = _rows(con, """SELECT c.formation, c.pos, c.game_version, c.role_id, c.focus,
                                     c.rationale, c.source, c.confidence, c.updated
                              FROM slot_canon_roles c JOIN slots s
                                ON s.regime_id=c.regime_id AND s.formation=c.formation AND s.pos=c.pos
                              WHERE c.regime_id=? ORDER BY c.formation, s.sort_order""", (rid,))
        # name_kr = 다른 맵(form·season_stats·fbref…)의 키. label은 표시용이라 접미·별칭이 붙어 다를 수 있다.
        squad = _rows(con, """SELECT s.player_id, COALESCE(s.label, p.name_kr, p.name) label,
                                     p.name name_en, COALESCE(p.name_kr, p.name) name_kr,
                                     s.slot_type, s.lh, s.map25, s.rate_v, s.rate_basis, s.rate_note,
                                     s.fit_role, s.fit_focus, s.fit_sim, s.sort_order, s.grid_club,
                                     s.grid_caveat, s.pos_only, sn.shirt_number
                              FROM squad_entries s JOIN players p ON p.id=s.player_id
                              LEFT JOIN player_shirt_numbers sn
                                ON sn.player_id = s.player_id AND sn.team_code = ?
                               AND sn.season = (SELECT MAX(season) FROM player_shirt_numbers
                                                 WHERE team_code = ?)
                              WHERE s.regime_id=? ORDER BY s.sort_order, label""", (code, code, rid))
        prescriptions = _rows(con, """
            SELECT pr.player_id, COALESCE(p.name_kr, p.name) label, pr.season, pr.game_version,
                   pr.kind, pr.pos_label, pr.x, pr.y, pr.role_id, pr.focus, pr.map25, pr.starter,
                   pr.fit_sim, pr.sample_n, pr.avg_rating, pr.rationale, pr.grid_club
            FROM prescriptions pr JOIN players p ON p.id=pr.player_id
            WHERE pr.regime_id=? ORDER BY pr.player_id, pr.kind""", (rid,))
        # 모든 화면이 공유하는 슬롯 후보 정본. squad/transfer를 페이지별로 다시 합치지 않는다.
        # v_slot_candidates가 (regime, formation, pos, player_id) 중복 제거와 승격 우선순위를 보장한다.
        # shirt_number는 player_shirt_numbers를 LEFT JOIN해 붙인다 — v_slot_candidates(뷰)를
        # 건드리지 않기 위해서다. 시즌은 그 팀의 최신 시즌을 쓴다(등번호는 시즌마다 재배정된다).
        slot_candidates = _rows(con, """
            SELECT v.regime_id, v.team_code, v.formation, v.pos, v.slot_type, v.player_id, v.label,
                   v.name_en, v.name_kr, v.source_kind, v.status, v.map25, v.rating, v.rate_basis,
                   v.rate_note, v.fit_role, v.fit_focus, v.fit_sim, v.source, v.confidence,
                   v.sort_order, v.grid_club, v.grid_caveat, sn.shirt_number
            FROM v_slot_candidates v
            LEFT JOIN player_shirt_numbers sn
              ON sn.player_id = v.player_id AND sn.team_code = v.team_code
             AND sn.season = (SELECT MAX(season) FROM player_shirt_numbers
                               WHERE team_code = v.team_code)
            WHERE v.regime_id=?
            ORDER BY v.formation, v.pos, v.source_kind, v.sort_order, v.label""", (rid,))
        # 대표 평균위치 — 히트맵 비교(A·실측)가 슬롯 좌표가 아니라 선수의 실제 평균 위치에
        # 칩을 찍기 위한 값. 대표 히트맵(map25)과 같은 유효 표본 기준(45분+ · 히트포인트 15+)을
        # 쓴다. 좌표 변환은 화면에서 한다(docs/30: 툴x=100−소파y, 툴y=소파x).
        avg_positions = _rows(con, """
            SELECT player_id, ROUND(AVG(avg_x),1) avg_x, ROUND(AVG(avg_y),1) avg_y,
                   COUNT(*) n, MIN(date) first_date, MAX(date) last_date
            FROM player_matches
            WHERE team_code=? AND avg_x IS NOT NULL AND avg_y IS NOT NULL
              AND minutes>=45 AND hit_points>=15
            GROUP BY player_id""", (code,))
        # ⭐ 부상·계약 상태(player_status, 2026-09-13 신설 — 사용자 지시 「부상 상태·복귀 일정을 선수 화면에」).
        #    스냅샷 테이블이라 **선수·종류별 최신 pulled 한 행만** 내보낸다. `stale_days`는 화면이 신선도를
        #    표시하기 위한 값 — 라이브 시스템에서 오래된 스냅샷을 현재 상태처럼 읽지 않게 한다.
        status = _rows(con, """
            SELECT s.player_id, s.kind, s.value, s.detail, s.as_of, s.pulled, s.source, s.confidence,
                   CAST(julianday('now') - julianday(s.pulled) AS INTEGER) stale_days,
                   -- ⭐ 교차검증: 이 스냅샷의 as_of 이후에 실제로 뛴 기록이 있으면 소스가 낡은 것이다.
                   --    2026-09-13 실증 — 만잠비는 FotMob이 07-07자 「무릎·Doubtful」인데 09-12에 27분 뛰었다.
                   --    라이브 시스템에서 이 모순을 화면이 직접 경고한다(값은 덮지 않는다 — 소스 원문 보존).
                   (SELECT MAX(pm.date) FROM player_matches pm
                     WHERE pm.player_id=s.player_id AND pm.minutes>0
                       AND pm.date > COALESCE(s.as_of, s.pulled)) played_after,
                   (SELECT pm.minutes FROM player_matches pm
                     WHERE pm.player_id=s.player_id AND pm.minutes>0
                       AND pm.date > COALESCE(s.as_of, s.pulled)
                     ORDER BY pm.date DESC LIMIT 1) played_after_minutes
              FROM player_status s
              JOIN (SELECT player_id, kind, MAX(pulled) mx FROM player_status GROUP BY player_id, kind) t
                ON t.player_id=s.player_id AND t.kind=s.kind AND t.mx=s.pulled
             WHERE s.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?)
             ORDER BY s.kind, s.player_id""", (rid,))
        setups = _rows(con, """SELECT season, game_version, kind, formation, build_up_style,
                                      defensive_approach, line_height, tactic_code, rationale, confidence
                               FROM team_tactic_setups WHERE regime_id=?
                               ORDER BY season, kind""", (rid,))
        # 재현 불가 항목(reproduction_limits, migration 027) — 공통(regime_id NULL) + 이 체제. 화면은
        # 설정 시트 옆에 「재현 불가 N건」으로 센다 — 설정값을 읽을 때 기대치를 맞추기 위해서다(점검 7번).
        # 인게임 커널 신뢰도(v_kernel_fidelity, migration 029) — 처방 화면이 역할/포커스 옆에 「게임검증 cos·n」을 붙인다.
        fidelity = _rows(con, """SELECT game_version, role_id, focus, n, n_matches, n_players, cos_avg, cos_min, cos_max, fidelity
                                 FROM v_kernel_fidelity""")
        limits = _rows(con, """SELECT id, game_version, regime_id, axis, real_feature, limitation,
                                      workaround, source, confidence, added
                               FROM reproduction_limits WHERE regime_id IS NULL OR regime_id=?
                               ORDER BY regime_id IS NOT NULL, axis, id""", (rid,))
        profile = _rows(con, """SELECT axis, content, evidence, confidence, updated
                                FROM manager_profiles WHERE regime_id=? ORDER BY axis""", (rid,))
        # 설정 층 변경 이력(migration 039) — 리포트 「전술 갱신 히스토리」. 서사 층 히스토리는 profile.content의 [날짜 …] 표식을 화면이 파싱한다.
        tactic_changes = _rows(con, """SELECT layer, key, before, after, changed_at, reason, source
                                       FROM tactic_change_log WHERE regime_id=? ORDER BY changed_at DESC, id DESC""", (rid,))
        targets = _rows(con, """SELECT player_id, name, name_kr, short_label, slot, club, position,
                                       likelihood, last_news_date, map25, sample_n, avg_rating,
                                       tool_x, tool_y,
                                       opt_role, opt_focus, fit_role, fit_focus, fit_sim,
                                       confidence, source, rationale
                                FROM transfer_targets WHERE team_code=? AND window=?
                                  AND likelihood!='OWNED'
                                ORDER BY id""", (code, window))
        # OWNED는 스쿼드(squad_entries)에 이미 있다 — 이적 목록에서 제외 (v1 동일 필터)
        outgoing = _rows(con, """SELECT p.name, p.name_kr, o.dest_club, o.likelihood,
                                        o.last_news_date, o.confidence, o.source, o.rationale
                                 FROM transfer_outgoing o JOIN players p ON p.id=o.player_id
                                 WHERE o.team_code=? AND o.window=? ORDER BY o.player_id""",
                         (code, window))
        ledger = _rows(con, """SELECT kind, label, amount_m, note, confidence, contract_years
                               FROM transfer_ledger WHERE team_code=? AND window=?
                               ORDER BY CASE kind WHEN 'in' THEN 0 WHEN 'deduct' THEN 1
                                        WHEN 'out' THEN 2 ELSE 3 END, amount_m DESC""",
                        (code, window))
        summary_rows = _rows(con, """SELECT summary, source, confidence, updated
                               FROM transfer_summary WHERE team_code=? AND window=?""",
                        (code, window))
        summary = summary_rows[0] if summary_rows else None
        # regime_id IS NULL = 아직 우리 선수가 아닌 영입 후보의 원소속 관측이다(불변규칙 7 —
        # 원소속 체제의 서사를 우리 체제 행으로 넣지 않는다). 그 행을 regime로만 걸러내면
        # 수집해 둔 서사가 어느 화면에도 뜨지 않아 페이지가 '영상 분석 미수행'이라고 잘못 적는다.
        # ⇒ 그 팀이 추적 중인 후보(transfer_targets)면 함께 싣는다. 출처 팀 경고는 화면이 이미 띄운다.
        # ⭐ player_id를 함께 싣는다 — 라벨 조인은 후보에서 조용히 0행이 된다(불변규칙 6).
        #   transfer_targets.name_kr('테일러 하우드-벨리스') ↔ players.name_kr('하우드-벨리스')처럼
        #   두 테이블의 표기 규약이 갈리면 화면이 '영상 분석 미수행'이라고 잘못 적는다.
        duties = _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, d.player_id, d.position, d.duties,
                                      d.execution, d.adherence, d.game_role_implication, d.source, d.confidence,
                                      d.observed_from, d.observed_to, d.sample_scope, d.sample_note,
                                      d.applied_status, d.applied_note
                               FROM player_duties d JOIN players p ON p.id=d.player_id
                               WHERE d.regime_id=?
                                  OR (d.regime_id IS NULL AND d.player_id IN
                                      (SELECT player_id FROM transfer_targets
                                       WHERE team_code=? AND window=? AND player_id IS NOT NULL))
                               ORDER BY p.id""", (rid, code, window))
        # ⭐ pos_group — 백분위 모집단을 **같은 포지션군**으로 자르기 위한 파생값(2026-09-18, 사용자 지적
        #   「6축 백분위가 포지션에 상관없이 모두 동일해?」 — 종전에는 GK를 스트라이커와 같은 풀에서 xG 백분위로 셌다).
        #   공식전 `pos_class` 최빈값을 슬롯군(GK/CB/FB/DM/CM/WM/CAM/ST)으로 접는다. 표본이 없으면 NULL이고 화면이 전체 풀로 폴백한다.
        pstats = _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, v.player_id, v.n, v.avg_rating, v.minutes,
                                      v.xg_pg, v.xa_pg, v.kp_pg, v.dw_pg, v.tk_pg, v.ic_pg,
                                      (SELECT CASE
                                          WHEN pm.pos_class='GK' THEN 'GK'
                                          WHEN pm.pos_class LIKE '%CB' THEN 'CB'
                                          WHEN pm.pos_class IN ('LB','RB','LWB','RWB') THEN 'FB'
                                          WHEN pm.pos_class LIKE '%DM' THEN 'DM'
                                          WHEN pm.pos_class LIKE '%CM' OR pm.pos_class='CM' THEN 'CM'
                                          WHEN pm.pos_class IN ('LM','RM','LW','RW','LAM','RAM') THEN 'WM'
                                          WHEN pm.pos_class='CAM' THEN 'CAM'
                                          WHEN pm.pos_class LIKE '%ST' OR pm.pos_class='ST' THEN 'ST' END
                                       FROM player_matches pm
                                       WHERE pm.player_id=v.player_id AND pm.pos_class IS NOT NULL
                                         AND pm.competition NOT LIKE '%Friendly%'
                                       GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 1) pos_group
                               FROM v_player_profile v JOIN players p ON p.id=v.player_id
                               WHERE v.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?)""", (rid, rid))
        evals = _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, p.name name_en, e.player_id,
                                     e.overall, e.traits, e.strengths, e.stat_eval, e.fotmob_eval,
                                     e.fit_emery, e.fit_alonso, e.fit_iraola,
                                     e.source, e.confidence, e.updated,
                                     -- 표본 정형 필드(T1) — 화면이 「이 평가가 몇 경기 전 기준인지」를 계산하는 데 쓴다
                                     e.sample_season, e.sample_n, e.sample_minutes, e.sample_avg_rating, e.sample_as_of
                              FROM player_evaluations e JOIN players p ON p.id=e.player_id
                              WHERE e.regime_id=?
                                 OR (e.regime_id IS NULL AND e.player_id IN
                                     (SELECT player_id FROM transfer_targets
                                      WHERE team_code=? AND window=? AND player_id IS NOT NULL))
                              ORDER BY e.player_id""", (rid, code, window))
        season_stats = {}
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, v.season, v.competition,
                                      v.n, v.starts, v.minutes, v.goals, v.assists, v.avg_rating
                               FROM v_player_season_stats v JOIN players p ON p.id=v.player_id
                               WHERE v.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?)
                               ORDER BY v.season DESC, v.n DESC""", (rid, rid)):
            season_stats.setdefault(r.pop("label"), []).append(r)
        # ⭐⭐ 선수 특성(`fotmob_traits`) — **상세 백분위가 없을 때의 대체 축**(2026-09-24 신설).
        #    ⛔ `fotmob_detail_stats`와 **모집단이 다르다**(이쪽은 「다른 미드필더와 비교」처럼 포지션군 전체).
        #       같은 표·같은 레이더에 섞지 않는다 — 화면이 따로 그리고 모집단을 명시한다.
        #    왜 필요한가: 출전이 얇은 선수는 FotMob이 **상세 백분위를 아예 만들지 않는다**
        #       (실측 2026-09-24: 뇨니 PL 26/27 3경기 38분 → detail 0행). 그런데 traits는 6축이 있다.
        #       ⇒ 그 선수가 낀 비교가 통째로 빈 화면이 되던 것을 막는다.
        traits = {}
        for r in _rows(con, """SELECT t.player_id, t.pos_group, t.metric, t.metric_kr, t.percentile, t.pulled
                               FROM fotmob_traits t
                              WHERE t.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                    UNION SELECT player_id FROM prescriptions WHERE regime_id=?)""", (rid, rid)):
            traits.setdefault(str(r.pop("player_id")), []).append(r)
        fbref = {}   # 리그 백분위 — Fotmob 상세 스탯(migrations/006). 지표별 동포지션 백분위.
        # ⭐ `player_id`를 함께 싣는다 — 딕셔너리 키는 players.name_kr이지만 화면의 영입 후보는
        # transfer_targets.name_kr을 쓰므로 라벨만으로는 조용히 어긋난다(토신 '아다라비오요' ↔ '토신 아다라비오요').
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, f.player_id, f.season, f.league,
                                      f.metric_key, f.metric, f.metric_kr, f.stat_value, f.per90,
                                      f.percentile, f.percentile_per90, f.pulled
                               FROM fotmob_detail_stats f JOIN players p ON p.id=f.player_id
                               WHERE f.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?
                                     UNION SELECT p2.id FROM transfer_targets t JOIN players p2
                                           ON p2.name=t.name WHERE t.team_code=?)
                               ORDER BY f.percentile DESC""", (rid, rid, code)):
            fbref.setdefault(r.pop("label"), []).append(r)
        fm_season = {}
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, f.player_id, f.league, f.season,
                                      f.metric, f.metric_kr, f.value, f.pulled
                               FROM fotmob_season_stats f JOIN players p ON p.id=f.player_id
                               WHERE f.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?
                                     UNION SELECT p2.id FROM transfer_targets t JOIN players p2
                                           ON p2.name=t.name WHERE t.team_code=?)
                               ORDER BY f.id""", (rid, rid, code)):
            fm_season.setdefault(r.pop("label"), []).append(r)
        form = {}
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, m.date, m.rating, m.competition
              FROM player_matches m JOIN players p ON p.id=m.player_id
              WHERE m.rating IS NOT NULL AND m.player_id IN
                (SELECT player_id FROM squad_entries WHERE regime_id=?
                 UNION SELECT player_id FROM prescriptions WHERE regime_id=?)
              ORDER BY m.date""", (rid, rid)):
            form.setdefault(r["label"], []).append([r["date"], r["rating"], r["competition"]])
        form = {k: v[-10:] for k, v in form.items()}   # 최근 10경기
        # 경기별 리포트 — 해석은 match_reports/match_player_reports, 원천 수치는
        # matches/player_matches/team_match_stats에서 같은 event_id로 묶는다.
        match_reports = _rows(con, """
            SELECT mr.id, mr.event_id, mr.match_id, mr.season, mr.report_date, mr.title,
                   mr.status, mr.tactical_description, mr.tactical_features,
                   mr.tactical_changes, mr.game_implications, mr.overall_assessment, mr.report_path,
                   mr.source, mr.confidence, mr.created_at, mr.updated_at,
                   m.date, m.opponent, m.competition, m.venue, m.result, m.stage,
                   m.possession, ts.xg_v, ts.xg_o, ts.xg_op_v, ts.xg_op_o,
                   ts.blocked_v, ts.blocked_o, ts.shots_v, ts.shots_o,
                   ts.sot_v, ts.sot_o, ts.bigch_v, ts.bigch_o, ts.passes_v,
                   ts.passes_o, ts.long_att_v, ts.long_acc_v, ts.long_att_o,
                   ts.long_acc_o, ts.cross_att_v, ts.cross_acc_v, ts.corners_v,
                   ts.corners_o, ts.duelpct_v, ts.fouls_v, ts.fouls_o,
                   ts.formation_v, ts.formation_o, ts.xg_source, ts.ppda_v, ts.ppda_o,
                   ts.def_x_v, ts.def_x_o,
                   -- 수비·경합 프로필(2026-09-22 신설) — 40/40 경기에서 결손 0인데 화면이 쓰지 않고 있었다.
                   ts.tackles_v, ts.tackles_o, ts.interceptions_v, ts.interceptions_o,
                   ts.clearances_v, ts.clearances_o,
                   ts.aerial_won_v, ts.aerial_att_v, ts.aerial_won_o, ts.aerial_att_o,
                   ts.dribble_succ_v, ts.dribble_att_v, ts.dribble_succ_o, ts.dribble_att_o,
                   (SELECT MAX(pm.possession) FROM player_matches pm
                     WHERE pm.event_id=mr.event_id AND pm.team_code=mr.team_code) pm_possession
            FROM match_reports mr
            LEFT JOIN matches m ON m.id=mr.match_id
            LEFT JOIN team_match_stats ts
              ON ts.event_id=mr.event_id AND ts.team_code=mr.team_code
            WHERE mr.team_code=?
            ORDER BY COALESCE(m.date,mr.report_date) DESC, mr.id DESC""", (code,))
        for report in match_reports:
            report["players"] = _rows(con, """
                SELECT mpr.player_id, COALESCE(p.name_kr,p.name) label, p.name name_en,
                       mpr.position, mpr.tactical_role, mpr.characteristics,
                       mpr.performance, mpr.game_implication, mpr.source, mpr.confidence,
                       pm.minutes, pm.rating, pm.started, pm.lineup_pos, pm.pos_class,
                       pm.avg_x, pm.avg_y, pm.hit_points, pm.map25, pm.xg, pm.xa,
                       -- 국면 분리 그리드(docs/30) — 수집해 두고 화면에 한 번도 안 나왔다.
                       pm.map25_poss, pm.map25_def, pm.phase_source,
                       pm.key_passes, pm.duels_won, pm.duels_lost, pm.tackles,
                       pm.interceptions, pm.goals, pm.assists, pm.touches,
                       pm.recoveries, pm.stats_json
                FROM match_player_reports mpr
                JOIN players p ON p.id=mpr.player_id
                LEFT JOIN player_matches pm
                  ON pm.player_id=mpr.player_id AND pm.event_id=?
                WHERE mpr.report_id=?
                ORDER BY COALESCE(pm.lineup_order,99), p.id""",
                (report["event_id"], report["id"]))
            setup = _rows(con, """
                SELECT report_id,game_version,formation,build_up_style,
                       defensive_approach,line_height,tactic_code,match_only,
                       rationale,source,confidence,rule_note
                FROM match_game_setups WHERE report_id=?""", (report["id"],))
            report["game_setup"] = setup[0] if setup else None
            if report["game_setup"]:
                # 규칙 제안(core.team_settings)을 기록값 옆에 병기 — G15가 편차 신고를 강제한다.
                from .team_settings import suggest
                # 점유는 G15와 같은 원천(player_matches.possession)을 우선한다 — matches.possession은 결손이 많다.
                report["game_setup"]["rule_suggest"] = suggest(
                    report.get("pm_possession") if report.get("pm_possession") is not None else report.get("possession"),
                    report.get("passes_v"),
                    report.get("long_att_v"), report.get("ppda_v"))
            report["game_players"] = _rows(con, """
                SELECT mpp.player_id,COALESCE(p.name_kr,p.name) label,p.name name_en,
                       mpp.game_version,mpp.pos_label,mpp.role_id,gr.name role_name,
                       mpp.focus,mpp.fit_sim,mpp.starter,mpp.sort_order,mpp.rationale,
                       mpp.replaced_player_id,mpp.minute_on,
                       mpp.source,mpp.confidence,
                       COALESCE(s.x,f.x) x, COALESCE(s.y,f.y) y
                FROM match_player_prescriptions mpp
                JOIN players p ON p.id=mpp.player_id
                JOIN game_roles gr
                  ON gr.game_version=mpp.game_version AND gr.role_id=mpp.role_id
                LEFT JOIN match_game_setups mgs ON mgs.report_id=mpp.report_id
                LEFT JOIN slots s ON s.regime_id=? AND s.formation=mgs.formation
                                 AND s.pos=mpp.pos_label
                -- 경기 포메이션이 slots에 없을 때의 기하 폴백. 커널이 이미
                -- formation을 조건에 넣지 않고 첫 행을 쓰므로(core.kernel.best_fit_slot)
                -- 같은 규칙을 따라야 fit_sim과 좌표의 출처가 일치한다.
                LEFT JOIN slots f ON f.rowid=(SELECT MIN(f2.rowid) FROM slots f2
                                              WHERE f2.regime_id=? AND f2.pos=mpp.pos_label)
                WHERE mpp.report_id=? ORDER BY mpp.sort_order,p.id""",
                (rid, rid, report["id"]))
            # 타임라인·하프별 정형 행(migration 040) — 경기 화면 차트(matchviz.js)의 원료. 없으면 빈 배열(화면이 「미수집」으로 쓴다).
            report["events"] = _rows(con, """SELECT minute, added, side, kind, player_id, player_name, assist_player_id, assist_name,
                                                    player_out_id, player_out_name, score_v, score_o, note
                                             FROM match_events WHERE match_id=? ORDER BY minute, id""", (report["match_id"],)) if report.get("match_id") else []
            report["periods"] = _rows(con, """SELECT period, possession_v, xg_v, xg_o, shots_v, shots_o, sot_v, sot_o, ppda_v, ppda_o
                                              FROM match_period_stats WHERE match_id=? ORDER BY period""", (report["match_id"],)) if report.get("match_id") else []
            report["shots"] = _rows(con, """SELECT minute, added, side, player_id, player_name, xg, xgot, outcome, situation, body_part, x, y, provider
                                            FROM match_shots WHERE match_id=? ORDER BY minute, id""", (report["match_id"],)) if report.get("match_id") else []
            report_file = ROOT / report["report_path"]
            report["report_markdown"] = (
                report_file.read_text(encoding="utf-8") if report_file.is_file() else None)
        departed = [r["label"] for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label
            FROM transfer_outgoing o JOIN players p ON p.id=o.player_id
            WHERE o.team_code=? AND o.likelihood='CONFIRMED'""", (code,))]
        written.append(_write(SITE_DATA / "teams" / f"{code}.json", {
            "regime": rg, "slots": slots, "slot_canon": canon,
            "slot_candidates": slot_candidates,
            "squad": squad, "prescriptions": prescriptions,
            "duties": duties, "player_stats": pstats, "departed": departed, "form": form,
            "avg_positions": avg_positions,
            "match_reports": match_reports,
            "evaluations": evals, "season_stats": season_stats, "fbref": fbref, "traits": traits,
            "fotmob_season": fm_season,
            "setups": setups, "limits": limits, "kernel_fidelity": fidelity, "profile": profile, "tactic_changes": tactic_changes,
            "player_status": status,
            "transfer": {"targets": targets, "outgoing": outgoing, "ledger": ledger, "summary": summary}}))

    con.close()
    return written

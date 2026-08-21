#!/usr/bin/env python3
"""FotMob 선수 지표 대량 수집 — 브라우저 MCP·에이전트 컨텍스트를 거치지 않는다.

왜 이 스크립트가 있는가 (2026-08-21 신설):
  ATM 31명을 수집하며 **브라우저 MCP → localhost 전송이 전부 차단**된다는 것이 확인됐다
  (`fetch`·form POST 모두 `ERR_BLOCKED_BY_CLIENT` — 하니스 네트워크 정책). 그래서 1,285행을
  에이전트 컨텍스트를 경유해 옮겨야 했고, 그것이 대량 수집의 구조적 비용 요인이었다(obs#273).
  ⭐ Playwright는 그 제약 밖에 있다 — 페이지 오리진에서 fetch하므로 API가 200으로 열리고
  (`scripts/fetch_fotmob.py`가 이미 쓰는 패턴), 결과를 그대로 DB에 쓴다. 컨텍스트 비용 0.

⛔ curl·WebFetch로는 안 된다 — FotMob API는 페이지 컨텍스트 밖에서 막힌다.

채우는 축 (player-collect 스킬 기준):
  축1 `players.fotmob_id` · 축5 `fotmob_detail_stats` · 축6 `fotmob_season_stats`
  축7 `fotmob_traits` · 축8 `player_tenures`

사용:
    # 팀 스쿼드 전원 (regime의 squad_entries)
    .venv/bin/python scripts/collect_fotmob_players.py --team ATM
    # 이적 후보까지 포함
    .venv/bin/python scripts/collect_fotmob_players.py --team LIV --include-targets
    # 특정 선수만 (players.id)
    .venv/bin/python scripts/collect_fotmob_players.py --players 177 178 94
    # 시즌 정책 · 미리보기
    .venv/bin/python scripts/collect_fotmob_players.py --team ATM --seasons latest2 --dry-run

⚠️ 시즌 정책(`--seasons`)이 중요하다 — 기본 `latest2`다.
   `latest` 하나만 받으면 **개막 직후에는 1~2경기 표본이 잡혀 백분위가 극단으로 튄다**
   (2026-08-21 ATM: 한츠코 26/27 1경기 평점 8.66, 패스 정확도 백분위 93). 직전 시즌을 함께 받아야
   의미 있는 표본이 생긴다. 화면(site/player.html)은 최신 시즌만 그리고 나머지는 노트에 열거한다.
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"

# 우리가 백분위 비교에 쓰는 「주 리그」. 컵·대표팀은 모집단이 달라 제외한다.
MAIN_LEAGUES = {
    "Premier League", "Championship", "LaLiga", "LaLiga2", "Serie A", "Bundesliga",
    "Ligue 1", "Eredivisie", "Liga Portugal", "First Division A", "MLS", "Liga MX",
    "Brasileirão", "Serie A Brazil",
}

# localizedTitleId → (영문 라벨, 한글 라벨). 없는 키는 NULL로 두고 경고한다(추측 금지).
LABELS = {
    "goals": ("Goals", "골"),
    "goals_subtitle": ("Penalty goals", "PK 득점"),
    "expected_goals": ("xG", "xG"),
    "expected_goals_on_target": ("xGOT", "xGOT"),
    "non_penalty_xg": ("xG excl. penalty", "xG(PK 제외)"),
    "shots": ("Shots", "슛"),
    "ShotsOnTarget": ("Shots on target", "유효 슛"),
    "headed_shots": ("Headed shots", "헤더 슛"),
    "assists": ("Assists", "어시스트"),
    "expected_assists": ("xA", "xA"),
    "successful_passes": ("Accurate passes", "정확한 패스"),
    "successful_passes_accuracy": ("Pass accuracy", "패스 정확도"),
    "long_balls_accurate": ("Accurate long balls", "정확한 롱볼"),
    "long_ball_succeeeded_accuracy": ("Long ball accuracy", "롱볼 정확도"),
    "line_breaking_passes": ("Line-breaking passes", "라인 브레이킹 패스"),
    "chances_created": ("Chances created", "기회 창출"),
    "big_chance_created_team_title": ("Big chances created", "빅찬스 창출"),
    "crosses_succeeeded": ("Successful crosses", "성공한 크로스"),
    "crosses_succeeeded_accuracy": ("Cross accuracy", "크로스 정확도"),
    "dribbles_succeeded": ("Dribbles", "드리블"),
    "won_contest_subtitle": ("Dribbles success rate", "드리블 성공률"),
    "duel_won": ("Duels won", "듀얼 승"),
    "duel_won_percent": ("Duels won %", "듀얼 승률"),
    "aerials_won": ("Aerials won", "공중 경합 승"),
    "aerials_won_percent": ("Aerials won %", "공중 경합 승률"),
    "touches": ("Touches", "터치"),
    "touches_opp_box": ("Touches in opposition box", "상대 박스 터치"),
    "dispossessed": ("Dispossessed", "볼 탈취당함"),
    "fouls_won": ("Fouls won", "파울 획득"),
    "penalty_won_title": ("Penalties awarded", "PK 획득"),
    "penalty_conceded_title": ("Penalties conceded", "PK 헌납"),
    "defensive_actions": ("Defensive actions", "수비 액션"),
    "matchstats.headers.tackles": ("Tackles", "태클"),
    "interceptions": ("Interceptions", "인터셉트"),
    "blocked_shots": ("Blocked scoring attempt", "슛 블록"),
    "fouls": ("Fouls committed", "파울"),
    "recoveries": ("Recoveries", "볼 리커버리"),
    "poss_won_att_3rd_team_title": ("Possession won final 3rd", "공격 3선 볼 획득"),
    "dribbled_past": ("Dribbled past", "드리블 돌파 허용"),
    "clearances": ("Clearances", "클리어런스"),
    "clean_sheet_team_title": ("Clean sheets", "클린시트"),
    "goals_conceded_while_on_pitch": ("Goals conceded while on pitch", "출전 중 실점"),
    "expected_goals_against_while_on_pitch": ("xG against while on pitch", "출전 중 피xG"),
    "yellow_cards": ("Yellow cards", "옐로카드"),
    "red_cards": ("Red cards", "레드카드"),
    # 피지컬 — 하이라인 적합성 판단의 직접 근거다(2026-08-21 토신·민테 대비).
    "physical_metrics_topspeed": ("Top Speed", "최고 속도"),
    "physical_metrics_distance_covered": ("Total Distance Covered", "총 이동거리"),
    "physical_metrics_running": ("Running", "러닝 거리"),
    "physical_metrics_sprinting": ("Sprinting", "스프린트 거리"),
    "physical_metrics_number_of_sprints": ("Number of Sprints", "스프린트 횟수"),
    # GK
    "saves": ("Saves", "세이브"),
    "save_percentage": ("Save percentage", "세이브율"),
    "goals_conceded": ("Goals conceded", "실점"),
    "goals_prevented": ("Goals prevented", "실점 방지"),
    "error_led_to_goal": ("Error led to goal", "실책 실점"),
    "keeper_sweeper": ("Sweeper clearances", "스위퍼 클리어"),
    "keeper_high_claim": ("High claims", "하이 클레임"),
    "penalty_saves": ("Penalties saved", "PK 선방"),
    "penalty_goals_conceded": ("Penalty goals conceded", "PK 실점"),
    "penalty_save_percent": ("Penalty save %", "PK 선방률"),
}

SEASON_LABELS = {
    "Goals": "골", "Assists": "어시스트", "Started": "선발", "Matches": "경기",
    "Minutes played": "출전 시간", "Rating": "평점", "Yellow cards": "경고",
    "Red cards": "퇴장", "Clean sheets": "클린시트", "Goals conceded": "실점",
    "Saved penalties": "PK 선방",
}

TRAIT_LABELS = {
    "Chances created": "기회 창출", "Aerial duels": "공중 볼 경합",
    "Defensive actions": "수비적 행동", "Goals": "득점", "Shot attempts": "슛 시도",
    "Touches": "터치", "Sweeper actions": "스위퍼 액션", "Goals conceded": "실점",
    "Save percentage": "세이브율", "High claims": "하이 클레임",
    "Clean sheets": "클린시트", "Long ball percentage": "롱볼 성공률",
}

# 페이지 컨텍스트에서 한 선수분을 통째로 받는다. ⛔ 셸(curl)에서는 막히므로 여기서 해야 한다.
JS = """
async ({fm, mains, wanted}) => {
  const out = {fm};
  const d = await fetch(`/api/data/playerData?id=${fm}`);
  if (!d.ok) return {fm, err: 'playerData ' + d.status};
  const j = await d.json();
  out.name = j.name;
  const ml = j.mainLeague || {};
  out.mainLeague = {league: ml.leagueName, season: ml.season,
                    stats: (ml.stats || []).map(s => [s.title, String(s.value)])};
  out.traitsTitle = (j.traits || {}).title || null;
  out.traits = ((j.traits || {}).items || []).map(t => [t.title, t.value]);
  const ch = (j.careerHistory || {}).careerItems || {};
  const senior = ch.senior && ch.senior.seasonEntries ? ch.senior.seasonEntries : (ch.senior || []);
  out.career = (senior || []).map(c => ({
    season: c.seasonName, team: c.team, apps: c.appearances,
    goals: c.goals, assists: c.assists,
    rating: c.rating && c.rating.rating ? c.rating.rating : null,
    leagues: (c.tournamentStats || []).map(t => t.leagueName)}));
  // statSeasons는 배열이다 — {seasons:[...]}가 아니다(2026-08-21에 이 오해로 한 번 빈 결과를 받았다).
  const cands = [];
  for (const s of (j.statSeasons || []))
    for (const t of (s.tournaments || []))
      if (mains.includes(t.name)) cands.push({season: s.seasonName, league: t.name, entry: t.entryId});
  out.candidates = cands;
  out.stats = [];
  for (const c of cands.slice(0, wanted)) {
    const r = await fetch(`/api/data/playerStats?playerId=${fm}&seasonId=${c.entry}`);
    if (!r.ok) { out.stats.push({...c, err: 'playerStats ' + r.status}); continue; }
    const pj = await r.json();
    const rows = [];
    const walk = o => {
      if (Array.isArray(o)) o.forEach(walk);
      else if (o && typeof o === 'object') {
        if (o.localizedTitleId && o.statValue !== undefined)
          rows.push([o.localizedTitleId, String(o.statValue),
                     o.per90 == null ? null : o.per90,
                     o.percentileRank == null ? null : Math.round(o.percentileRank),
                     o.percentileRankPer90 == null ? null : Math.round(o.percentileRankPer90)]);
        Object.values(o).forEach(walk);
      }};
    walk(pj.statsSection);
    out.stats.push({...c, rows});
  }
  return out;
}
"""


def season_code(name):
    """FotMob 시즌명 → seasons.code. '2025/2026'→'2025-26' · '2026'→'2026'."""
    if "/" in name:
        a, b = name.split("/")
        return f"{a}-{b[2:]}"
    return name


def targets(con, team, players, include_targets):
    if players:
        q = ("SELECT id, COALESCE(name_kr, name), fotmob_id FROM players "
             f"WHERE id IN ({','.join('?' * len(players))})")
        return con.execute(q, players).fetchall()
    if not team:
        sys.exit("--team 또는 --players 중 하나는 필요하다")
    rid = con.execute("SELECT id FROM regimes WHERE team_code=?", (team,)).fetchone()
    if not rid:
        sys.exit(f"regimes에 team_code={team} 없음")
    sql = """SELECT p.id, COALESCE(p.name_kr, p.name), p.fotmob_id FROM players p
             WHERE p.id IN (SELECT player_id FROM squad_entries WHERE regime_id=?)"""
    args = [rid[0]]
    if include_targets:
        sql += (" OR p.id IN (SELECT player_id FROM transfer_targets"
                " WHERE team_code=? AND player_id IS NOT NULL)")
        args.append(team)
    return con.execute(sql + " ORDER BY p.id", args).fetchall()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", help="팀 코드 (regime의 squad_entries)")
    ap.add_argument("--players", nargs="*", type=int, help="players.id 직접 지정")
    ap.add_argument("--include-targets", action="store_true",
                    help="transfer_targets의 후보도 포함 (player_id가 채워진 행만)")
    ap.add_argument("--seasons", choices=["latest", "latest2", "latest3"], default="latest2",
                    help="주 리그 시즌 개수. 기본 latest2 — 개막 직후 1~2경기 표본만 잡히는 것을 막는다")
    ap.add_argument("--pulled", default=None, help="수집일 (기본: 오늘). 결정적 재현용으로 명시 가능")
    ap.add_argument("--dry-run", action="store_true", help="DB에 쓰지 않고 요약만 출력")
    a = ap.parse_args()

    wanted = {"latest": 1, "latest2": 2, "latest3": 3}[a.seasons]
    if a.pulled:
        pulled = a.pulled
    else:
        import datetime
        pulled = datetime.date.today().isoformat()

    con = sqlite3.connect(DB)
    rows = targets(con, a.team, a.players, a.include_targets)
    if not rows:
        sys.exit("대상 0명")
    have = [(i, n, f) for i, n, f in rows if f]
    missing = [(i, n) for i, n, f in rows if not f]
    print(f"대상 {len(rows)}명 · fotmob_id 보유 {len(have)} · 결손 {len(missing)}")
    if missing:
        print("  ⛔ fotmob_id 없어 건너뜀:", ", ".join(f"{n}({i})" for i, n in missing))
        print("     → 팀 스쿼드에서 찾아 players.fotmob_id를 먼저 채울 것"
              " (/api/data/teams?id=<fotmob_team_id>&tab=squad)")

    from playwright.sync_api import sync_playwright
    results = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        # robots.txt = 동일 오리진 경량 페이지. 홈은 라이브스코어 스크립트가 렌더러를 얼린다(docs/30).
        pg.goto("https://www.fotmob.com/robots.txt", wait_until="domcontentloaded", timeout=60_000)
        for pid, name, fm in have:
            try:
                r = pg.evaluate(JS, {"fm": fm, "mains": sorted(MAIN_LEAGUES), "wanted": wanted})
            except Exception as e:                                  # noqa: BLE001
                print(f"  ⚠️ {name}({pid}) 실패: {e}")
                continue
            r["pid"], r["kr"] = pid, name
            results.append(r)
            if r.get("err"):
                print(f"  ⚠️ {name}: {r['err']}")
            else:
                got = sum(len(s.get("rows") or []) for s in r["stats"])
                seas = " / ".join(f"{s['league']} {s['season']}" for s in r["stats"]) or "주 리그 표본 없음"
                print(f"  {name}: {got}행 · {seas}")
        br.close()

    if a.dry_run:
        print("\n--dry-run — DB에 쓰지 않았다.")
        return

    cur = con.cursor()
    unknown, ins = set(), dict.fromkeys(
        ["detail", "season", "traits", "tenures", "fotmob_id"], 0)
    seasons_have = {r[0] for r in con.execute("SELECT code FROM seasons")}
    for r in results:
        if r.get("err"):
            continue
        pid, fm = r["pid"], r["fm"]
        src = f"fotmob.com/api/data (player {fm}, scripts/collect_fotmob_players.py, {pulled} 수집)"

        for s in r["stats"]:
            if s.get("err") or not s.get("rows"):
                continue
            for key, val, per90, pc, pc90 in s["rows"]:
                if key not in LABELS:
                    unknown.add(key)
                en, kr = LABELS.get(key, (None, None))
                cur.execute(
                    """INSERT INTO fotmob_detail_stats(player_id,pulled,season,league,metric_key,
                       metric,metric_kr,stat_value,per90,percentile,percentile_per90,source)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(player_id,season,league,metric_key) DO NOTHING""",
                    (pid, pulled, s["season"], s["league"], key, en, kr, val, per90, pc, pc90, src))
                ins["detail"] += cur.rowcount

        ml = r.get("mainLeague") or {}
        if ml.get("league"):
            for title, value in ml["stats"]:
                cur.execute(
                    """INSERT INTO fotmob_season_stats(player_id,pulled,league,season,metric,
                       metric_kr,value,source) VALUES(?,?,?,?,?,?,?,?)
                       ON CONFLICT(player_id,league,season,metric) DO NOTHING""",
                    (pid, pulled, ml["league"], ml["season"], title,
                     SEASON_LABELS.get(title), value, src))
                ins["season"] += cur.rowcount

        for title, value in (r.get("traits") or []):
            cur.execute(
                """INSERT INTO fotmob_traits(player_id,pulled,pos_group,metric,metric_kr,
                   percentile,source) VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(player_id,metric) DO NOTHING""",
                (pid, pulled, r.get("traitsTitle"), title, TRAIT_LABELS.get(title),
                 round(float(value) * 100), src))
            ins["traits"] += cur.rowcount

        # 커리어 — 같은 시즌에 복수 클럽이면 출전수 순으로 club_name에 병합한다
        # (player_tenures PK가 (player_id, season)이라 1행 제약).
        by_season = {}
        for c in (r.get("career") or []):
            by_season.setdefault(season_code(c["season"]), []).append(c)
        pos = con.execute("SELECT primary_position FROM players WHERE id=?", (pid,)).fetchone()
        for code, cs in by_season.items():
            if code not in seasons_have:      # FK. 없는 시즌 코드는 조용히 만들지 않는다.
                continue
            cs.sort(key=lambda c: -int(c["apps"] or 0))
            label = " / ".join(
                f"{c['team']} ({c['apps']}경기" + (f", 평점 {c['rating']}" if c["rating"] else "") + ")"
                for c in cs)
            cur.execute(
                """INSERT INTO player_tenures(player_id,season,club_code,club_name,position,
                   shirt_no,minutes) VALUES(?,?,NULL,?,?,NULL,NULL)
                   ON CONFLICT(player_id,season) DO NOTHING""",
                (pid, code, label, pos[0] if pos else None))
            ins["tenures"] += cur.rowcount

    con.commit()
    print("\n적재:", " · ".join(f"{k} +{v}" for k, v in ins.items() if k != "fotmob_id"))
    if unknown:
        print("⚠️ 라벨 미매핑 키(metric/metric_kr가 NULL로 들어갔다 — LABELS에 추가할 것):")
        print("   " + ", ".join(sorted(unknown)))
    miss_season = {season_code(c["season"]) for r in results if not r.get("err")
                   for c in (r.get("career") or [])} - seasons_have
    if miss_season:
        print("⚠️ seasons에 없어 player_tenures를 건너뛴 시즌 코드:", ", ".join(sorted(miss_season)))
        print("   → 필요하면 seasons에 추가한 뒤 재실행(멱등이라 중복 없음)")
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()

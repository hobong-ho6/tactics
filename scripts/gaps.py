#!/usr/bin/env python3
"""결손 점검 — 런북에 SQL 원문으로 박혀 있던 회차별 확인을 **한 줄 명령**으로 모았다.

왜 (2026-09-23 사용자 지시 「코드나 스크립트로 대체 — 유지보수 편의와 동일한 결과, 토큰 절감」):
  같은 쿼리를 세션이 매번 문서에서 옮겨 적고 있었다. 옮겨 적는 동안 컨텍스트가 늘고, 그 컨텍스트는
  이후 모든 툴 왕복에 다시 실린다. 더 나쁜 것은 **조금씩 다르게 옮겨 적는 것**이다 — 조건 하나가 빠지면
  「결손 없음」이라는 틀린 안심을 준다.
⛔ 판정을 여기서 바꾸지 않는다. 런북의 쿼리를 **그대로** 옮겼고, 바꿀 일이 생기면 여기만 고친다.

사용:
    python3 scripts/gaps.py links                 # 카드·보유·경로의 player_id 링크 결손 (club-sync)
    python3 scripts/gaps.py player 지모알로바      # 그 선수의 17축 결손 표 (player-collect §1)
    python3 scripts/gaps.py eval                  # 평가 신선도 — 갱신 대상 (match-watch T4)
    python3 scripts/gaps.py squad                 # 활성 스쿼드 전원이 진화 패스에 나오는가 (club-sync 검산)
    python3 scripts/gaps.py all                   # 전부
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"

# player-collect §1의 축 목록 — ⛔ 여기 순서·구성이 그 런북의 「작업 목록」이다.
AXES = ["player_game_stats", "player_matches", "fotmob_detail_stats", "fotmob_season_stats",
        "fotmob_traits", "player_duties", "player_tenures", "player_evaluations",
        "prescriptions", "squad_entries", "transfer_targets", "transfer_outgoing",
        "player_shot_profile", "fbref_percentiles", "match_player_reports",
        "player_market_values", "player_status", "understat_player_matches"]


def links(con):
    """⛔ 「우리 DB 선수와 이름이 맞는데 링크가 비어 있는 행」 — 셋 다 0이어야 정상.
    ⚠️ 관리 4팀 밖 카드는 player_id NULL이 **정상**이다(케미 계산 전용) — 그래서 이름 일치를 조건에 둔다."""
    rows = con.execute("""
        SELECT 'card_items' k, COUNT(*) n FROM player_card_items i JOIN players p
          ON (p.name=i.name_kr OR p.name_kr=i.name_kr) WHERE i.player_id IS NULL
        UNION ALL SELECT 'club_players', COUNT(*) FROM fut_club_players c JOIN players p
          ON (p.name=c.name OR p.name_kr=c.name) WHERE c.status='owned' AND c.player_id IS NULL
        UNION ALL SELECT 'evolutions', COUNT(*) FROM player_evolutions pe
          JOIN player_card_items i ON i.ea_item_id=pe.base_ea_id
          WHERE pe.player_id IS NULL AND i.player_id IS NOT NULL""").fetchall()
    bad = [(k, n) for k, n in rows if n]
    print("■ 링크 결손 (club-sync 「링크 3곳」)")
    for k, n in rows:
        print(f"   {'⛔' if n else '✅'} {k:14} {n}")
    if bad:
        print("   ⚠️ 이름만으로 잇지 말 것 — 소속팀·국적·포지션 3요소를 대조한다(docs/30).")
    return bool(bad)


def squad(con):
    """활성 스쿼드가 **두 수집 축의 조회 범위**에 드는가.
    ⚠️ 런북 경고: 「경로 없음」 자체는 정상일 수 있다(OVR이 높아 현행 진화 조건에 안 맞는 선수).
    ⇒ 「0건」이 아니라 **「조회조차 안 되는가」**를 본다. 두 축의 범위가 다르다:
         · 경로 축(`paths/v2`)   = FC27 **base 카드**가 있는 선수만
         · 적용 가능 축(eligibility) = **보유 카드**(base든 특별카드든) + players 링크
       어느 쪽도 안 부르면 그 선수는 진화 화면에서 **통째로 사라진다** — 그게 진짜 구멍이다."""
    rows = con.execute("""
        SELECT COALESCE(p.name_kr, p.name) nm, s.grp, c.player_id, c.current_ovr, c.status,
               (SELECT COUNT(*) FROM player_evolutions e WHERE e.player_id=c.player_id) np,
               (SELECT COUNT(*) FROM player_card_items i
                 WHERE i.player_id=c.player_id AND i.game_version='FC27' AND i.is_base=1) nbase,
               (SELECT COUNT(*) FROM player_card_items i
                 WHERE i.player_id=c.player_id AND i.game_version='FC27') ncard,
               (SELECT COUNT(*) FROM fc_evolution_eligibility g WHERE g.player_id=c.player_id) nelig
          FROM fut_squad_slots s
          JOIN fut_club_players c ON c.ea_item_id=s.ea_item_id
          LEFT JOIN players p ON p.id=c.player_id
         ORDER BY s.grp DESC, s.idx""").fetchall()
    broken, thin = [], []
    for nm, g, pid, ovr, st, np, nbase, ncard, nelig in rows:
        in_paths = bool(nbase)
        in_elig = bool(pid and ncard and st == "owned")
        if pid is None:
            broken.append((nm, g, "players 링크 없음 — 어느 축에도 안 잡힌다. 링크를 이어 줄 것(docs/30 동일성 규약)"))
        elif not in_paths and not in_elig:
            broken.append((nm, g, "FC27 카드가 없어 **두 축 모두** 이 선수를 부르지 않는다"))
        elif not np and not nelig:
            why = "base 카드가 없어 경로 축은 건너뛰지만, 적용 가능 축이 조회했고 해당 없음" if not in_paths \
                  else f"두 축 다 조회했고 해당 없음(OVR {ovr} — 조건 미달이면 정상)"
            thin.append((nm, g, why))
    print(f"■ 활성 스쿼드 ↔ 진화 수집 범위 ({len(rows)}명)")
    for nm, g, why in broken:
        print(f"   ⛔ {nm or '(이름 미상)':16} [{g}] — {why}")
    for nm, g, why in thin:
        print(f"   ℹ️ {nm:16} [{g}] — {why}")
    if not broken:
        print("   ✅ 조회 범위 밖인 선수 없음")
    return bool(broken)


def evals(con):
    """match-watch 4-1절 T4 — 판단을 내린 뒤 공식전을 3경기 이상 더 치른 선수."""
    rows = con.execute("""
        SELECT r.team_code, COALESCE(p.name_kr,p.name) nm, pe.updated, pe.sample_n,
               (SELECT COUNT(DISTINCT m.event_id) FROM player_matches m
                 WHERE m.player_id=p.id AND m.date > pe.updated AND m.minutes IS NOT NULL
                   AND m.competition NOT LIKE '%Friendly%') AS since
        FROM squad_entries se JOIN regimes r ON r.id=se.regime_id AND r.end IS NULL
        JOIN players p ON p.id=se.player_id
        JOIN player_evaluations pe ON pe.player_id=p.id AND pe.regime_id=r.id
        GROUP BY r.team_code, p.id HAVING since >= 3 ORDER BY since DESC""").fetchall()
    print(f"■ 평가 신선도 — 갱신 대상 {len(rows)}명 (T2/T3 트리거 확인 · ⛔ overall은 T1에서 건드리지 않는다)")
    for t, nm, up, n, since in rows[:25]:
        print(f"   {t} {nm:16} 갱신 {up} · 표본 {n} · 이후 {since}경기")
    if len(rows) > 25:
        print(f"   … 외 {len(rows) - 25}명")
    return bool(rows)


def player(con, who):
    """player-collect §1 결손 표 — ⭐ 이 표가 그 회차의 작업 목록이다."""
    r = con.execute("SELECT id, name, name_kr, sofascore_id, fotmob_id, sofifa_id FROM players "
                    "WHERE name LIKE ? OR name_kr LIKE ? OR CAST(id AS TEXT)=?",
                    (f"%{who}%", f"%{who}%", who)).fetchall()
    if not r:
        print(f"⛔ '{who}' 로 찾은 선수가 없다"); return True
    if len(r) > 1:
        print("⚠️ 여러 명이 걸렸다 — id로 지정할 것:")
        for x in r:
            print("   ", x)
        return True
    pid, name, kr, sofa, fm, sofifa = r[0]
    print(f"■ {kr or name} (id={pid})  id 3종: sofascore={sofa or '⛔'} fotmob={fm or '⛔'} sofifa={sofifa or '⛔'}")
    for t in AXES:
        try:
            n = con.execute(f"SELECT COUNT(*) FROM {t} WHERE player_id=?", (pid,)).fetchone()[0]
        except sqlite3.OperationalError:
            n = None
        print(f"   {'⛔' if n == 0 else '✅' if n else '  '} {t:26} {n if n is not None else '표 없음'}")
    # ⚠️ 카운트가 놓치는 두 가지(obs#234) — 런북이 경고하는 지점이라 함께 찍는다.
    orphan = con.execute("SELECT COUNT(*) FROM player_game_stats WHERE player_id IS NULL AND sofifa_id=?",
                         (sofifa,)).fetchone()[0] if sofifa else 0
    if orphan:
        print(f"   ⚠️ player_id가 비어 있는 game_stats 행 {orphan}건 — sofifa_id로 잡힌다. 링크를 이어 줄 것.")
    print("   ⚠️ 카운트가 1 이상이어도 **그 행의 빈 칸**은 따로 봐야 한다(‘축이 있다’ ≠ ‘채워졌다’).")
    return False


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    con = sqlite3.connect(DB)
    bad = False
    if cmd in ("links", "all"):
        bad |= links(con)
    if cmd in ("squad", "all"):
        bad |= squad(con)
    if cmd in ("eval", "evals", "all"):
        bad |= evals(con)
    if cmd == "player":
        bad |= player(con, sys.argv[2])
    elif cmd not in ("links", "squad", "eval", "evals", "all"):
        sys.exit(__doc__)
    con.close()
    sys.exit(0)          # ⛔ 결손은 **보고 대상**이지 실패가 아니다 — 게이트가 아니다.

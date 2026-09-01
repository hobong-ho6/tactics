#!/usr/bin/env python3
"""G13 「조용한 이중화」 회귀 테스트 — **결함을 합성 주입해** 게이트가 잡는지 확인한다. 읽기 전용.

왜 이렇게 만들었는가 (2026-09-01):
  G13은 2026-09-01 정리 4연쇄에서 나왔고, 그날의 검증은 `/tmp`에 남은 **정리 전 백업 DB 4개**와
  대조하는 방식이었다. 그건 재현이 안 된다 — /tmp는 비워지고, 백업은 커밋되지 않는다.
  그래서 **현재 DB 사본에 결함을 하나씩 주입**해 「깨끗하면 통과 / 주입하면 검출」을 매번 확인한다.

  ⛔ 원본 DB는 절대 건드리지 않는다. 사본을 임시 디렉터리에 만들어 쓰고 지운다.
  ⭐ 검사 SQL은 `scripts.gates.g13_checks()`를 **그대로 호출**한다 — 복사하면 게이트를 고쳤을 때
     테스트가 낡은 식을 검사하게 되어 회귀 테스트로서 무의미해진다.

사용:
    python3 scripts/test_g13_regression.py            # 전체
    python3 scripts/test_g13_regression.py -v         # 주입 SQL·검출 내역까지
종료 코드: 0 = 전항 통과, 1 = 실패.
"""
import argparse
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                    # noqa: E402
from scripts.gates import g13_checks, G13_LABELS       # noqa: E402


# (키, 이름, 주입 SQL 리스트, 그날 실제로 이 결함이 있었던 상태)
# 주입은 전부 "현실에서 실제로 났던 형태"를 재현한다 — 인위적인 값이 아니다.
CASES = [
    ("dup_person", "동일인 2-id (에수구 103/140 형)", [
        # 같은 사람을 두 번째 id로 복제한다. fotmob_id가 겹치므로 동일인이다.
        # ⚠️ players.name은 UNIQUE라 이름을 바꿔 넣는다 — 실제 에수구도
        #    'Dário Essugo'/'Dario Essugo'로 표기가 갈려 있어서 UNIQUE를 통과했다.
        """INSERT INTO players (id, name, fotmob_id, birth_year, primary_position)
           SELECT (SELECT MAX(id) FROM players) + 1, name || ' (dup)', fotmob_id,
                  birth_year, primary_position
             FROM players WHERE fotmob_id IS NOT NULL ORDER BY id LIMIT 1""",
    ]),
    ("dup_appearance", "이중 기록 (같은 출전 · SofaScore + FotMob 2행)", [
        # 같은 (player_id, match_id)에 FotMob 규약(event_id = −matchId)으로 한 행 더 넣는다.
        # UNIQUE(player_id, event_id)는 event_id가 달라 막지 못한다 — 그게 이 결함의 본질이다.
        """INSERT INTO player_matches (player_id, event_id, match_id, team_code, season,
                                       date, competition, minutes)
           SELECT player_id, -999001, match_id, team_code, season, date, competition, minutes
             FROM player_matches WHERE match_id IS NOT NULL ORDER BY id LIMIT 1""",
    ]),
    ("orphan_match_link", "match 링크 결손 (잭슨 08-05 형)", [
        # event_id로 matches를 특정할 수 있는데 match_id가 비어 있는 행.
        # 이 상태면 dup_appearance의 (player_id, match_id) 키가 무력해진다.
        """INSERT INTO player_matches (player_id, event_id, match_id, team_code, season,
                                       date, competition, minutes)
           SELECT (SELECT MIN(id) FROM players), m.event_id, NULL, m.team_code, m.season,
                  m.date, m.competition, 90
             FROM matches m WHERE m.event_id IS NOT NULL ORDER BY m.id LIMIT 1""",
    ]),
    ("mixed_team_code", "team_code ↔ 대회 성격 (완비사카 DR콩고=AVL 형)", [
        # 클럽 코드가 붙은 행의 대회를 대표팀 대회로 바꾼다 ⇒ 그 코드가 CLUB·NT 양쪽에 걸린다.
        """UPDATE player_matches SET competition = 'World Cup Qual. CAF'
            WHERE id = (SELECT MIN(pm.id) FROM player_matches pm
                         WHERE pm.team_code IS NOT NULL AND pm.competition IS NOT NULL
                           AND pm.competition NOT LIKE '%World Cup%'
                           AND pm.competition NOT LIKE '%International Friendly%')""",
    ]),
    ("club_league_conflict", "클럽 코드 ↔ 리그 충돌 (일링-주니어 AVL=Serie A 형)", [
        # 클럽 코드가 붙은 행의 대회를 **다른 나라 1부 리그**로 바꾼다 ⇒ 그 코드가 두 리그에 걸린다.
        # ⑷가 못 잡는 유형이다(CLUB/NT가 섞이지 않는다) — 2026-09-01에 AVL이 분데스·리그1·세리에A·
        # 챔피언십에 동시 출현하는 116행이 이 방식으로 발견됐다.
        """UPDATE player_matches SET competition = 'Eredivisie'
            WHERE id = (SELECT MIN(pm.id) FROM player_matches pm
                         WHERE pm.team_code IS NOT NULL
                           AND pm.competition IN ('Premier League','LaLiga'))""",
    ]),
]

# 「FIFA Club World Cup」은 클럽 대회인데 '%World Cup%'에 걸린다. 이 함정을 다시 놓치면
# 클럽월드컵 출전이 통째로 대표팀으로 분류돼 mixed_team_code가 오탐을 낸다.
# ⑷의 조건에서 제외돼 있는지를 **오탐 없음**으로 확인한다(2026-09-01에 실제로 6행이 걸렸었다).
FALSE_POSITIVE_CASES = [
    ("mixed_team_code", "FIFA Club World Cup은 클럽 대회다(오탐 금지)", [
        """UPDATE player_matches SET competition = 'FIFA Club World Cup'
            WHERE id = (SELECT MIN(pm.id) FROM player_matches pm
                         WHERE pm.team_code IS NOT NULL AND pm.competition IS NOT NULL
                           AND pm.competition NOT LIKE '%World Cup%'
                           AND pm.competition NOT LIKE '%International Friendly%')""",
    ]),
]


def counts(db_path):
    con = sqlite3.connect(db_path)
    try:
        return {k: len(v) for k, v in g13_checks(con).items()}
    finally:
        con.close()


def with_injection(src, sqls, tmpdir, tag):
    """원본 사본에 SQL을 주입한 임시 DB 경로를 만든다."""
    dst = Path(tmpdir) / f"inject-{tag}.db"
    shutil.copy(src, dst)
    con = sqlite3.connect(dst)
    try:
        con.execute("PRAGMA foreign_keys=ON")
        for s in sqls:
            con.execute(s)
        con.commit()
    finally:
        con.close()
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB), help="검사할 DB (기본: db/tactics.db)")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    src = Path(a.db)
    if not src.exists():
        sys.exit(f"⛔ DB 없음: {src}")

    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        # ── 0. 기준선 — 현재 DB는 4항 전부 0이어야 한다 ──
        base = counts(src)
        clean = not any(base.values())
        print(f"[기준선] {src.name}: "
              + " · ".join(f"{G13_LABELS[k]} {v}" for k, v in base.items())
              + ("  ✅ 깨끗함" if clean else "  ⛔ 이미 위반이 있다"))
        if not clean:
            fails.append("baseline")
            print("   ⚠️ 기준선이 더러우면 아래 주입 테스트의 의미가 약해진다"
                  " — 검출이 주입 때문인지 원래 위반 때문인지 구분되지 않는다.")

        # ── 1. 결함 주입 → 반드시 검출돼야 한다 ──
        for key, name, sqls in CASES:
            db = with_injection(src, sqls, tmp, key)
            got = counts(db)
            hit = got[key] > base[key]
            # 다른 항목까지 덩달아 늘면 검사들이 서로 얽혀 있다는 뜻이라 같이 본다.
            spill = {k: (base[k], got[k]) for k in got if k != key and got[k] != base[k]}
            mark = "✅ 검출" if hit else "⛔ 놓침"
            print(f"[주입] {G13_LABELS[key]:<20} {name}\n"
                  f"       {G13_LABELS[key]} {base[key]} → {got[key]}  {mark}"
                  + (f"  ⚠️ 부수 변화 {spill}" if spill else ""))
            if a.verbose:
                for s in sqls:
                    print("       SQL: " + " ".join(s.split())[:160] + "…")
            if not hit:
                fails.append(f"inject:{key}")

        # ── 2. 오탐 금지 — 함정 입력에 반응하면 안 된다 ──
        for key, name, sqls in FALSE_POSITIVE_CASES:
            db = with_injection(src, sqls, tmp, "fp-" + key)
            got = counts(db)
            ok = got[key] == base[key]
            print(f"[오탐] {G13_LABELS[key]:<20} {name}\n"
                  f"       {G13_LABELS[key]} {base[key]} → {got[key]}  "
                  + ("✅ 반응 없음" if ok else "⛔ 오탐"))
            if not ok:
                fails.append(f"false-positive:{key}")

    print()
    if fails:
        print(f"⛔ G13 회귀 실패: {fails}")
        return 1
    print(f"✅ G13 회귀 전항 통과 — 주입 {len(CASES)}종 전부 검출 · "
          f"오탐 검사 {len(FALSE_POSITIVE_CASES)}종 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())

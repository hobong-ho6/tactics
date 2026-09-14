#!/usr/bin/env python3
"""migration 031 — `player_duties.applied_status`/`applied_note` 신설 + 자동 백필 (2026-09-14).

왜 (사용자 지시 2026-09-14 「데이터만 수집하는 건 아무 의미 없다 — 시스템·전술 구현에 활용해야 한다」):
  영상·스카우트 분석은 `player_duties`까지는 반드시 오는데, **거기서 처방으로 가는 다리가 산문뿐이었다.**
  그래서 「검토했고 유지했다」와 「아무도 보지 않았다」가 DB에서 구분되지 않았다(obs#738·#740).
  ⇒ 반영 상태를 **정형 컬럼**으로 만들고 G16으로 결손을 막는다.

상태 어휘(4종, 자동 판정):
  MATCH    분석이 가리킨 역할이 그 선수의 처방(시즌·경기·squad_entries) 어딘가와 일치한다
  CONFLICT 역할 코드를 명시했는데 어떤 처방과도 일치하지 않는다 — **사람 판정 대기**
  NO_RX    분석은 있는데 그 선수의 처방 행이 아예 없다
  PROSE    산문만 있고 역할 코드가 없다 — 기계가 반영 여부를 볼 수 없다

⛔ 이 백필은 **자동 대조 결과**이지 사람의 승인이 아니다. `applied_note`에 그 사실을 적는다.
   사람이 판정하면 같은 컬럼을 APPLIED/HELD/REJECTED로 바꾸고 사유를 남긴다(그건 원장 정정이 아니라 상태 전이다).

재실행 안전: 컬럼이 이미 있으면 백필만 다시 계산해 **비어 있는 행에만** 채운다.
"""
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cols = {c[1] for c in con.execute("PRAGMA table_info(player_duties)")}
if "applied_status" not in cols:
    con.execute("ALTER TABLE player_duties ADD COLUMN applied_status TEXT")
    con.execute("ALTER TABLE player_duties ADD COLUMN applied_note TEXT")
    print("컬럼 추가: applied_status · applied_note")

roles = {r[0] for r in con.execute("SELECT DISTINCT role_id FROM game_role_focus")}
have = defaultdict(set)
for q, c in (("SELECT player_id, role_id FROM prescriptions WHERE role_id IS NOT NULL", "role_id"),
             ("SELECT player_id, role_id FROM match_player_prescriptions WHERE role_id IS NOT NULL", "role_id"),
             ("SELECT player_id, fit_role FROM squad_entries WHERE fit_role IS NOT NULL", "fit_role")):
    for r in con.execute(q):
        have[r["player_id"]].add(r[c])

NOTE = "[2026-09-14 백필] 자동 대조 결과다(사람 승인 아님) — 분석이 명시한 역할 코드 ↔ 그 선수의 prescriptions·match_player_prescriptions·squad_entries.fit_role 전량 대조."
n = defaultdict(int)
for d in con.execute("""SELECT id, player_id, game_role_implication imp FROM player_duties
                        WHERE applied_status IS NULL OR trim(applied_status)=''"""):
    found = {x for x in roles if x in (d["imp"] or "")}
    mine = have.get(d["player_id"], set())
    if not found:
        st, extra = "PROSE", " 역할 코드가 없어 기계 판정 불가 — 반영 여부는 사람이 적어야 한다."
    elif not mine:
        st, extra = "NO_RX", " 이 선수의 처방 행이 아직 없다."
    elif found & mine:
        st, extra = "MATCH", f" 일치 역할: {', '.join(sorted(found & mine))}."
    else:
        st, extra = "CONFLICT", f" 분석 {', '.join(sorted(found))} ↔ 보유 처방 {', '.join(sorted(mine))} — 사람 판정 대기."
    con.execute("UPDATE player_duties SET applied_status=?, applied_note=? WHERE id=?", (st, NOTE + extra, d["id"]))
    n[st] += 1
con.commit()
print("백필:", dict(n))
con.execute("INSERT OR IGNORE INTO _migration_log(run_at, v1_path, note) VALUES(?,?,?)",
            ("2026-09-14", "031-duty-applied",
             "player_duties.applied_status/applied_note 신설 — 영상·스카우트 분석이 처방에 반영됐는지를 정형화한다. "
             "사용자 지시 2026-09-14. G16이 결손을 막는다. 백필은 자동 대조(MATCH/CONFLICT/NO_RX/PROSE)이고 사람 승인이 아니다."))
con.commit()
print("다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")

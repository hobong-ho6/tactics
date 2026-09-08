#!/usr/bin/env python3
"""G14 「원장 정정 규약」 회귀 테스트 — 결함 3종을 **합성 주입**해 검사가 실제로 잡는지 본다.

scripts/test_g13_regression.py와 같은 원칙이다: 검사식을 복사하지 않고
scripts/gates.py의 g14_checks를 **import해서 공유**한다.
복사하면 게이트를 고쳤을 때 테스트가 낡은 식을 검사한다.

⭐ 2026-09-08 게이트 편입 완료(obs#518) — import 경로가 g14_prototype에서 scripts.gates로 바뀌었다.

⚠️ 원본 DB는 건드리지 않는다 — HEAD dump로 메모리 DB 2개(baseline·live)를 만들어
   live 쪽에만 결함을 주입한다. **읽기 전용 테스트다.**

사용: python3 scripts/test_g14_regression.py
종료 코드: 0 = 전항 통과, 1 = 실패.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.gates import g14_baseline as baseline, g14_checks   # noqa: E402

FAIL = []


def check(name, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {name}{'' if cond else '  ← ' + detail}")
    if not cond:
        FAIL.append(name)


def fresh():
    """baseline과 live를 같은 HEAD 상태로 만든다 — 이 시점의 위반은 0이어야 한다."""
    return baseline("HEAD"), baseline("HEAD")


def main():
    print("G14 회귀 테스트 — 합성 결함 주입\n")

    # ── 0. 무결 상태에서 0건 (오탐 없음) ──────────────────────────────────
    live, base = fresh()
    if live is None or base is None:
        print("⛔ HEAD dump 적재 실패 — db/dump가 커밋돼 있어야 한다."); return 1
    res = g14_checks(live, base)
    check("무결 상태: 위반 0", all(not v for v in res.values()),
          f"실제 { {k: len(v) for k, v in res.items() if v} }")
    live.close(); base.close()

    # ── 1. ⑴ prefix 비보존 재작성 ────────────────────────────────────────
    live, base = fresh()
    live.execute("UPDATE observations SET claim='완전히 다른 내용으로 바꿔 썼다' WHERE id=1")
    res = g14_checks(live, base)
    hit = [r for r in res["append_rewrite"] if r[1] == 1 and r[2] == "claim"]
    check("⑴ 재작성 적발", bool(hit), f"append_rewrite={res['append_rewrite'][:2]}")
    live.close(); base.close()

    # ── 2. ⑴ 덧붙임(prefix 보존)은 통과해야 한다 — 정당한 addendum ───────
    live, base = fresh()
    old = live.execute("SELECT claim FROM observations WHERE id=1").fetchone()[0]
    live.execute("UPDATE observations SET claim=? WHERE id=1",
                 (old + "\n\n[2026-09-08 추가] 덧붙임은 정상 작업이다.",))
    res = g14_checks(live, base)
    check("⑴ 덧붙임은 통과(오탐 아님)",
          not [r for r in res["append_rewrite"] if r[1] == 1],
          f"append_rewrite={res['append_rewrite'][:2]}")
    live.close(); base.close()

    # ── 3. ⑴ 행 삭제 적발 ───────────────────────────────────────────────
    live, base = fresh()
    live.execute("DELETE FROM observations WHERE id=1")
    res = g14_checks(live, base)
    check("⑴ 행 삭제 적발",
          any(r[1] == 1 and "삭제" in r[2] for r in res["append_rewrite"]))
    live.close(); base.close()

    # ── 4. ⑴ escape hatch (G14_ALLOW_REWRITE) ───────────────────────────
    import os
    live, base = fresh()
    live.execute("UPDATE observations SET claim='이관 때문에 재작성' WHERE id=1")
    os.environ["G14_ALLOW_REWRITE"] = "observations:1"
    res = g14_checks(live, base)
    del os.environ["G14_ALLOW_REWRITE"]
    check("⑴ 명시 허용 시 통과", not [r for r in res["append_rewrite"] if r[1] == 1])
    live.close(); base.close()

    # ── 4b. ⑴ player_duties도 보호 대상이다(observations 전용이 아니다) ──
    live, base = fresh()
    rid = live.execute("SELECT MIN(id) FROM player_duties WHERE duties IS NOT NULL").fetchone()[0]
    live.execute("UPDATE player_duties SET duties='덮어쓴 값' WHERE id=?", (rid,))
    res = g14_checks(live, base)
    check("⑴ player_duties 재작성 적발",
          any(r[0] == "player_duties" and r[1] == rid for r in res["append_rewrite"]),
          f"append_rewrite={res['append_rewrite'][:2]}")
    live.close(); base.close()

    # ── 4c. ⑴ NULL → 값은 결손 채움이라 통과해야 한다 ────────────────────
    #    obs#132(결손을 0으로 채우지 말 것)와 짝이다 — 뒤늦게 근거를 채우는 것은 정상 작업이다.
    live, base = fresh()
    row = live.execute("SELECT MIN(id) FROM observations WHERE evidence IS NULL").fetchone()[0]
    if row is not None:
        live.execute("UPDATE observations SET evidence='뒤늦게 채운 근거' WHERE id=?", (row,))
        res = g14_checks(live, base)
        check("⑴ NULL→값 결손 채움은 통과(오탐 아님)",
              not [r for r in res["append_rewrite"] if r[1] == row])
    else:
        print("  ⏭  ⑴ NULL→값: evidence가 NULL인 행이 없어 건너뜀")
    live.close(); base.close()

    # ── 5. ⑵ 한글 명사구 인접 반복 ──────────────────────────────────────
    live, base = fresh()
    live.execute("INSERT INTO observations (id, regime_id, season, scope, claim) "
                 "VALUES (999001, 1, '2026-27', 'reference', "
                 "'오나나 시즌아웃과 오나나 시즌아웃 + 고메스 정지가 겹쳤다')")
    res = g14_checks(live, base)
    check("⑵ 구 중복 적발", any(r[0] == 999001 for r in res["dup_phrase"]),
          f"dup_phrase={res['dup_phrase'][:2]}")
    live.close(); base.close()

    # ── 6. ⑵ 「」 안의 수사적 반복은 통과해야 한다 (오탐 방지의 핵) ──────
    live, base = fresh()
    live.execute("INSERT INTO observations (id, regime_id, season, scope, claim) "
                 "VALUES (999002, 1, '2026-27', 'reference', "
                 "'인용: 「볼을 가졌을 때가 혹독했다 혹독했다 혹독했다」로 반복했다')")
    res = g14_checks(live, base)
    check("⑵ 인용 안 반복은 통과(오탐 아님)",
          not any(r[0] == 999002 for r in res["dup_phrase"]),
          f"dup_phrase={[r for r in res['dup_phrase'] if r[0] == 999002]}")
    live.close(); base.close()

    # ── 7. ⑶ claim↔evidence 극성 모순 ───────────────────────────────────
    live, base = fresh()
    live.execute("INSERT INTO observations (id, regime_id, season, scope, claim, evidence) "
                 "VALUES (999003, 1, '2026-27', 'reference', "
                 "'더블피벗에서 카마라 로테이션 카드가 없다', "
                 "'에메리 확인 — 카마라 로테이션 카드가 이 1장뿐이다')")
    res = g14_checks(live, base)
    check("⑶ claim↔evidence 모순 적발",
          any(r[0] == 999003 for r in res["claim_evid_clash"]),
          f"clash={res['claim_evid_clash'][:2]}")
    live.close(); base.close()

    # ── 8. ⑶ 정상 행은 통과 ─────────────────────────────────────────────
    live, base = fresh()
    live.execute("INSERT INTO observations (id, regime_id, season, scope, claim, evidence) "
                 "VALUES (999004, 1, '2026-27', 'reference', "
                 "'카마라 로테이션 카드가 이 1장뿐이다', "
                 "'에메리 확인 — 카마라 로테이션 카드가 이 1장뿐이다')")
    res = g14_checks(live, base)
    check("⑶ 정합 행은 통과(오탐 아님)",
          not any(r[0] == 999004 for r in res["claim_evid_clash"]))
    live.close(); base.close()

    # ── 9. ⑵⑶은 델타 검사다 — 안 바뀐 기존 결함 행(obs#503)을 재적발하지 않는다 ──
    live, base = fresh()
    res = g14_checks(live, base)
    check("⑵⑶ 델타 검사: 기존 obs#503 재적발 안 함",
          not any(r[0] == 503 for r in res["dup_phrase"] + res["claim_evid_clash"]))
    live.close(); base.close()

    # ── 10. 빈 baseline 거짓 통과 방지 ──────────────────────────────────
    live, _ = fresh()
    empty = sqlite3.connect(":memory:")
    empty.executescript(
        "CREATE TABLE observations(id INTEGER PRIMARY KEY, claim TEXT, evidence TEXT,"
        " source TEXT, confidence TEXT);"
        "CREATE TABLE player_duties(id INTEGER PRIMARY KEY, duties TEXT, execution TEXT,"
        " adherence TEXT, game_role_implication TEXT, source TEXT, confidence TEXT,"
        " sample_note TEXT);")
    res = g14_checks(live, empty)
    check("빈 baseline은 「검사 불가」로 적발",
          any("baseline" in r[2] for r in res["append_rewrite"]),
          f"append_rewrite={res['append_rewrite'][:2]}")
    live.close(); empty.close()

    print(f"\n{'✅ 전항 통과' if not FAIL else '❌ 실패: ' + ', '.join(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""SBC 챌린지 포메이션을 **FUTBIN**에서 받아 `fc_sbc_formations`에 채운다 (2026-09-28 신설).

왜 (사용자 지시 「클럽싱크 돌릴 때 sbc 포메이션은 풋빈에서 가져와서 포메이션 정보가 입력된 상태로
    업데이트하고 해법을 바로 제공」):
  인게임 SBC는 챌린지마다 포메이션이 고정인데 EA·fut.gg는 그 값을 주지 않는다(migration 069).
  그래서 사람이 인게임 화면을 보고 손으로 적었고, 적기 전에는 해법이 안 나왔다(migration 087 `need_form`).
  FUTBIN 챌린지 페이지에는 `requirementData.formation.displayName`이 박혀 있다.
  ⭐ 검증(2026-09-28): 사용자가 인게임에서 적은 5건(26·27·32·44·48)과 **5/5 일치**.
  ⭐ FUTBIN URL의 챌린지 번호 = EA `challenge_ea_id`다. 이름 부분은 아무 값이어도 된다.
  ⭐ 원클릭 챌린지는 404다(포메이션이 없다) — 정상.

⛔ 스크립트가 직접 받을 수 없다 — Cloudflare 봇 검사로 urllib/curl은 **403**, in-app 브라우저 패널은
   검사를 못 넘는다(2026-09-28 실측). ⛔ 봇 검사를 우회하지 않는다.
   ⇒ 사용자의 **Chrome**(검사를 통과한 탭)에서 같은 출처 fetch로 받는다. GG Club과 같은 구조다.
   결과는 포메이션 이름 몇십 개라 작다 — 클립보드 없이 실행 결과를 그대로 파일에 옮긴다.

⛔ 사용자가 적은 값(source가 「사용자 입력」)과 FUTBIN이 갈리면 **덮지 않고 보고한다**(인게임 실측이 우선).
   FUTBIN에서 온 행끼리는 새 값으로 갱신한다(EA가 챌린지를 고치면 따라간다).

사용:
    python3 scripts/collect_futbin_sbc_formations.py --print-snippet     # Chrome에서 돌릴 JS
    python3 scripts/collect_futbin_sbc_formations.py --json-file /tmp/futbin-forms-YYYYMMDD.json
    python3 scripts/collect_futbin_sbc_formations.py --missing           # 포메이션이 빈 챌린지 수만
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                        # noqa: E402

GAME = "FC27"
TODAY = dt.date.today().isoformat()
SRC = "FUTBIN 챌린지 페이지 requirementData.formation.displayName (/27/squad-building-challenge/ea/<id>/)"
CONF = ("HIGH(FUTBIN 표기) — 등급 B(3자 사이트). 2026-09-28 사용자 인게임 기록 5건과 5/5 일치로 검증. "
        "⚠️ 사용자 인게임 기록과 갈리면 사용자 기록이 우선이다.")

# ⚠️ 두 번에 나눠 부른다 — 한 번에 기다리면 Chrome 도구의 평가 제한(45초)에 걸린다(2026-09-28 실측).
#    ① 시작(즉시 'started' 반환) → 약 1분 뒤 ② 결과 읽기(`done`이 1이면 끝).
SNIPPET = r"""window.__fbForms = {}; (async () => {
  // ⛔ www.futbin.com 탭(봇 검사 통과)에서 실행한다. 같은 출처 fetch라 쿠키가 따라간다.
  const ids = __IDS__;
  const out = {};
  for (const id of ids) {
    try {
      const r = await fetch(`/27/squad-building-challenge/ea/${id}/x`);
      if (r.status === 404) { out[id] = null; continue; }          // 원클릭 등 포메이션 없음
      if (!r.ok) { out[id] = 'HTTP' + r.status; continue; }
      const h = await r.text();
      const m = h.match(/"challengeName":"([^"]*)","formation":\{"formation":\{"value":"[^"]*"\},"displayName":"([^"]*)"/);
      out[id] = m ? m[2] : 'NOMATCH';
    } catch (e) { out[id] = 'ERR'; }
    await new Promise(x => setTimeout(x, 400));                     // 예의상 간격
  }
  out.done = 1;
  window.__fbForms = out;
})(); 'started'"""
READ = "JSON.stringify(window.__fbForms)   // done:1 이 보이면 끝 — 이 문자열을 그대로 파일에 쓴다"


def norm(s):
    """FUTBIN 「4-3-3(4)」 → 우리 표기 「4-3-3 (4)」."""
    return re.sub(r"\s*\((\d)\)", r" (\1)", s.strip())


def target_ids(con):
    """최신 수집의 스쿼드형 챌린지 전부(원클릭 제외). 이미 적힌 것도 넣는다 — 대조가 된다."""
    return [r[0] for r in con.execute(
        """SELECT DISTINCT challenge_ea_id FROM fc_sbc_challenges
           WHERE game_version=? AND pulled=(SELECT MAX(pulled) FROM fc_sbc_challenges WHERE game_version=?)
             AND challenge_type != 'ONE_CLICK_CHALLENGE' ORDER BY 1""", (GAME, GAME))]


def missing(con):
    return [i for i in target_ids(con) if not con.execute(
        "SELECT 1 FROM fc_sbc_formations WHERE game_version=? AND challenge_ea_id=?", (GAME, i)).fetchone()]


def apply(con, data):
    forms = {r[0] for r in con.execute("SELECT name FROM fc_formations WHERE game_version=?", (GAME,))}
    have = {r[0]: (r[1], r[2] or "") for r in con.execute(
        "SELECT challenge_ea_id, formation, source FROM fc_sbc_formations WHERE game_version=?", (GAME,))}
    new, same, upd, conflict, unknown, bad = [], [], [], [], [], []
    for k, v in data.items():
        if k == "done" or v is None:
            continue                                        # 404 = 포메이션 없는 챌린지
        cid = int(k)
        if v.startswith(("HTTP", "NOMATCH", "ERR")):
            bad.append((cid, v)); continue
        f = norm(v)
        if f not in forms:
            unknown.append((cid, v)); continue
        if cid in have:
            cur, src = have[cid]
            if cur == f:
                same.append(cid); continue
            if "FUTBIN" not in src:                         # 사용자 인게임 기록 — 덮지 않는다
                conflict.append((cid, cur, f)); continue
            con.execute("""UPDATE fc_sbc_formations SET formation=?, source=?, confidence=?, updated=?
                           WHERE game_version=? AND challenge_ea_id=?""", (f, SRC, CONF, TODAY, GAME, cid))
            upd.append((cid, cur, f)); continue
        con.execute("""INSERT INTO fc_sbc_formations(game_version, challenge_ea_id, formation, source, confidence, updated)
                       VALUES(?,?,?,?,?,?)""", (GAME, cid, f, SRC, CONF, TODAY))
        new.append((cid, f))
    con.commit()
    print(f"FUTBIN 포메이션: 신규 {len(new)} · 일치 {len(same)} · 갱신 {len(upd)} · "
          f"⚠️ 사용자 기록과 충돌 {len(conflict)} · 모르는 표기 {len(unknown)} · 실패 {len(bad)}")
    for cid, f in new:
        print(f"   ➕ {cid}: {f}")
    for cid, a, b in upd:
        print(f"   🔁 {cid}: {a} → {b}")
    for cid, a, b in conflict:
        print(f"   ⚠️ {cid}: 사용자 기록 {a} ↔ FUTBIN {b} — 덮지 않았다. 인게임에서 확인할 것")
    for cid, v in unknown:
        print(f"   ❔ {cid}: 「{v}」가 fc_formations에 없다 — collect_futgg_formations.py 확인")
    for cid, v in bad:
        print(f"   ⛔ {cid}: {v} — 봇 검사 만료면 Chrome에서 futbin 페이지를 한 번 열고 다시 돌린다")
    return bool(new or upd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print-snippet", action="store_true")
    ap.add_argument("--json-file")
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--no-solve", action="store_true", help="적재 뒤 해법 재계산을 건너뛴다")
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    if a.print_snippet:
        ids = target_ids(con)
        print("// ① 시작\n" + SNIPPET.replace("__IDS__", json.dumps(ids)))
        print("\n// ② 약 1분 뒤 결과 읽기\n" + READ)
        out = f"/tmp/futbin-forms-{TODAY.replace('-', '')}.json"
        print(f"\n── 이 뒤는 셸에서 ── (결과 JSON 문자열을 파일로)\n"
              f"# ⑴ Chrome의 www.futbin.com 탭에서 위를 실행 → 반환된 JSON을 {out}에 쓴다\n"
              f".venv/bin/python scripts/collect_futbin_sbc_formations.py --json-file {out}")
        return
    if a.json_file:
        raw = json.load(open(a.json_file))
        if isinstance(raw, str):
            raw = json.loads(raw)
        if not raw.get("done"):
            raise SystemExit("⛔ `done`이 없다 — 스니펫이 아직 끝나지 않았다. 잠시 뒤 ②를 다시 읽을 것")
        changed = apply(con, raw)
        left = missing(con)
        print(f"포메이션 미기록 스쿼드형 챌린지: {len(left)}개{' ' + str(left) if left else ''}")
        con.close()
        # ⭐ 「해법을 바로 제공」 — 적재했으면 그 자리에서 다시 푼다(부르는 걸 잊을 수 없게).
        if changed and not a.no_solve:
            py = ROOT / ".venv" / "bin" / "python"
            subprocess.run([str(py if py.exists() else sys.executable), str(ROOT / "scripts" / "sbc_solve.py"), "--save"])
        return
    left = missing(con)
    print(f"포메이션 미기록 스쿼드형 챌린지 {len(left)}개{': ' + str(left) if left else ''}")
    if left:
        print("⇒ Chrome(futbin 탭)에서 `collect_futbin_sbc_formations.py --print-snippet` 스니펫을 돌리고 "
              "`--json-file`로 넣는다 — 넣으면 해법을 바로 다시 푼다")


if __name__ == "__main__":
    main()

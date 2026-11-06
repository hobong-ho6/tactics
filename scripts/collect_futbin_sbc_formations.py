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

⭐⭐ **1차 출처는 FUTWIZ다**(2026-11-06 사용자 지시 「futwiz를 1차로 확인하도록해 futbin은 계속 막히자나」).
   FUTWIZ는 앱 안 브라우저에서 봇 검사 없이 열린다(2026-10-22·11-06 실측). 세트 페이지 `/sbcs/<아무 slug>/<set_ea_id>`
   번호 = EA `set_ea_id`이고, 챌린지마다 이름·FORMATION·조건이 있다. ⚠️ FUTWIZ 챌린지 링크 번호는 자체 id라 쓰지 않는다.
   ⇒ 세트 안 챌린지가 1개면 그대로, 여럿이면 **최소 케미 수치**(fut.gg 조건 「Chemistry: Min. N」 ↔ FUTWIZ 「Min Chem: N」)가
     세트 안에서 하나로만 맞을 때 잇는다. 갈리면 적재하지 않고 보고한다(이름 매칭 금지 · 불변규칙 6).
   FUTBIN은 2차다 — FUTWIZ에 없는 챌린지만 Chrome에서 돌린다.

사용:
    python3 scripts/collect_futbin_sbc_formations.py --futwiz-snippet    # ⭐ 1차 — 앱 안 브라우저 futwiz.com 탭에서 돌릴 JS
    python3 scripts/collect_futbin_sbc_formations.py --futwiz-file /tmp/futwiz-forms-YYYYMMDD.json
    python3 scripts/collect_futbin_sbc_formations.py --print-snippet     # 2차 — Chrome(FUTBIN)에서 돌릴 JS
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
from core.db import connect as connect_db  # noqa: E402  ⭐ DB 연결 정본(대기·작성 중 표시)

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

FW_SRC = "FUTWIZ 세트 페이지 FORMATION (https://www.futwiz.com/sbcs/x/{set} · URL 번호 = EA set_ea_id · {how})"
FW_CONF = ("MEDIUM(FUTWIZ 표기) — 등급 B(3자 사이트). 「442」식 표기를 변형 번호 없는 포메이션으로 읽었다. "
           "⚠️ 사용자 인게임 기록과 갈리면 사용자 기록이 우선이다.")
# ⭐ 앱 안 브라우저 futwiz.com 탭에서 실행한다(봇 검사 없음). 세트마다 HTML을 받아 챌린지 카드(article)를 읽는다.
#    DOMParser 문서에는 레이아웃이 없어 innerText가 줄을 안 나눈다 — 화면 밖 상자에 잠깐 붙여 읽는다.
FW_SNIPPET = r"""(async () => {
  const sets = __SETS__;
  const box = document.createElement('div');
  box.style.cssText = 'position:absolute;left:-99999px;top:0;width:800px';
  document.body.append(box);
  const out = {};
  for (const sid of sets) {
    try {
      const r = await fetch('/sbcs/x/' + sid);
      if (!r.ok) { out[sid] = 'HTTP' + r.status; continue; }
      const d = new DOMParser().parseFromString(await r.text(), 'text/html');
      out[sid] = [...d.querySelectorAll('article')].filter(a => a.textContent.includes('FORMATION')).map(a => {
        box.replaceChildren(document.importNode(a, true));
        const L = box.innerText.split('
').map(s => s.trim()).filter(Boolean);
        const j = L.indexOf('REQUIREMENTS');
        const k = L.findIndex((x, n) => n > j && /^(Lowest-cost solution|Open in squad builder)$/.test(x));
        return {name: L[0], form: L[L.indexOf('FORMATION') + 1], n: L[L.indexOf('TOTAL PLAYERS') + 1],
                req: j < 0 ? [] : L.slice(j + 1, k < 0 ? undefined : k)};
      });
    } catch (e) { out[sid] = 'ERR'; }
    await new Promise(x => setTimeout(x, 300));
  }
  box.remove();
  out.done = 1;
  return JSON.stringify(out);
})()"""


def norm(s):
    """FUTBIN 「4-3-3(4)」 → 우리 표기 「4-3-3 (4)」."""
    s = s.strip()
    m = re.fullmatch(r"(\d{3,5})(?:\s*\((\d)\)|-(\d))?", s)   # FUTWIZ 「442」·「433(4)」·「4231-2」
    if m:
        v = m.group(2) or m.group(3)
        return "-".join(m.group(1)) + (f" ({v})" if v else "")
    return re.sub(r"\s*\((\d)\)", r" (\1)", s)


def target_ids(con):
    """최신 수집의 스쿼드형 챌린지 전부(원클릭 제외). 이미 적힌 것도 넣는다 — 대조가 된다."""
    return [r[0] for r in con.execute(
        """SELECT DISTINCT challenge_ea_id FROM fc_sbc_challenges
           WHERE game_version=? AND pulled=(SELECT MAX(pulled) FROM fc_sbc_challenges WHERE game_version=?)
             AND challenge_type != 'ONE_CLICK_CHALLENGE' ORDER BY 1""", (GAME, GAME))]


def missing(con):
    return [i for i in target_ids(con) if not con.execute(
        "SELECT 1 FROM fc_sbc_formations WHERE game_version=? AND challenge_ea_id=?", (GAME, i)).fetchone()]


def apply(con, data, src_of=lambda cid: SRC, conf=CONF, site="FUTBIN"):
    forms = {r[0] for r in con.execute("SELECT name FROM fc_formations WHERE game_version=?", (GAME,))}
    have = {r[0]: (r[1], r[2] or "") for r in con.execute(
        "SELECT challenge_ea_id, formation, source FROM fc_sbc_formations WHERE game_version=?", (GAME,))}
    new, same, upd, conflict, unknown, bad, absent = [], [], [], [], [], [], []
    for k, v in data.items():
        if k == "done":
            continue
        if v is None:
            # ⛔⛔ 404를 「포메이션 없는 챌린지」로 조용히 넘기지 않는다(2026-09-30 사용자 지적
            #    「Destined for Glory Challenge 2의 포메이션이 실제 sbc 포메이션이 아니야」).
            #    대상(target_ids)은 이미 원클릭을 뺐으므로 404는 **FUTBIN이 아직 그 챌린지를 안 올렸다**는 뜻이다
            #    (실측: 49번 — FUTBIN 활성 목록엔 Challenge 1만 있었다). ⇒ 인게임 입력이 필요하다고 보고한다.
            if int(k) not in have:
                absent.append(int(k))
            continue
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
            if not src.startswith(("FUTBIN", "FUTWIZ")):    # 사용자 인게임 기록 — 덮지 않는다
                conflict.append((cid, cur, f)); continue
            con.execute("""UPDATE fc_sbc_formations SET formation=?, source=?, confidence=?, updated=?
                           WHERE game_version=? AND challenge_ea_id=?""", (f, src_of(cid), conf, TODAY, GAME, cid))
            upd.append((cid, cur, f)); continue
        con.execute("""INSERT INTO fc_sbc_formations(game_version, challenge_ea_id, formation, source, confidence, updated)
                       VALUES(?,?,?,?,?,?)""", (GAME, cid, f, src_of(cid), conf, TODAY))
        new.append((cid, f))
    con.commit()
    print(f"{site} 포메이션: 신규 {len(new)} · 일치 {len(same)} · 갱신 {len(upd)} · {site}에 없음 {len(absent)} · "
          f"⚠️ 사용자 기록과 충돌 {len(conflict)} · 모르는 표기 {len(unknown)} · 실패 {len(bad)}")
    for cid, f in new:
        print(f"   ➕ {cid}: {f}")
    for cid, a, b in upd:
        print(f"   🔁 {cid}: {a} → {b}")
    for cid, a, b in conflict:
        print(f"   ⚠️ {cid}: 사용자 기록 {a} ↔ {site} {b} — 덮지 않았다. 인게임에서 확인할 것")
    for cid, v in unknown:
        print(f"   ❔ {cid}: 「{v}」가 fc_formations에 없다 — collect_futgg_formations.py 확인")
    for cid, v in bad:
        print(f"   ⛔ {cid}: {v} — 봇 검사 만료면 Chrome에서 futbin 페이지를 한 번 열고 다시 돌린다")
    for cid in absent:
        print(f"   📐 {cid}: FUTBIN에 아직 없다(404) — **인게임 SBC 화면의 포메이션을 화면(SBC 탭)에서 골라 기록**한다."
              " 기록 전에는 해법을 풀지 않는다(need_form)")
    return bool(new or upd)


def _chem(lines):
    for x in lines:
        m = re.search(r"(?:Chemistry: Min\.|Min Chem:)\s*(\d+)", x)
        if m:
            return int(m.group(1))
    return None


def futwiz_map(con, raw):
    """FUTWIZ 세트별 카드 → {challenge_ea_id: 표기}. 못 잇는 것은 이유와 함께 돌려준다."""
    data, how, skip = {}, {}, []
    for sid, cards in raw.items():
        if sid == "done":
            continue
        chs = con.execute("""SELECT challenge_ea_id, name, requirements_text FROM fc_sbc_challenges
                             WHERE game_version=? AND set_ea_id=? AND challenge_type != 'ONE_CLICK_CHALLENGE'
                               AND pulled=(SELECT MAX(pulled) FROM fc_sbc_challenges WHERE game_version=?)""",
                          (GAME, int(sid), GAME)).fetchall()
        if not isinstance(cards, list) or not cards:
            skip.append((sid, f"FUTWIZ 응답 {cards!r}"[:60])); continue
        if len(chs) == 1 and len(cards) == 1:
            data[str(chs[0][0])] = cards[0]["form"]; how[chs[0][0]] = "세트 내 챌린지 1개"; continue
        fw = {}
        for c in cards:
            fw.setdefault(_chem(c.get("req") or []), []).append(c)
        for cid, nm, rq in chs:
            k = _chem(json.loads(rq or "[]"))
            hit = fw.get(k) if k is not None else None
            if hit and len(hit) == 1 and sum(1 for _, _, r2 in chs if _chem(json.loads(r2 or "[]")) == k) == 1:
                data[str(cid)] = hit[0]["form"]; how[cid] = f"세트 내 챌린지 {len(chs)}개 — 최소 케미 {k} 일치로 연결"
            else:
                skip.append((cid, f"{nm}: 최소 케미 {k}로 하나로 못 가른다"))
    data["done"] = 1
    return data, how, skip


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print-snippet", action="store_true")
    ap.add_argument("--json-file")
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--futwiz-snippet", action="store_true", help="⭐ 1차 — 앱 안 브라우저 futwiz.com 탭에서 돌릴 JS")
    ap.add_argument("--futwiz-file", help="FUTWIZ 스니펫 결과 JSON 파일")
    ap.add_argument("--no-solve", action="store_true", help="적재 뒤 해법 재계산을 건너뛴다")
    a = ap.parse_args()
    con = connect_db(DB)
    if a.futwiz_snippet:
        sets = [r[0] for r in con.execute(
            """SELECT DISTINCT set_ea_id FROM fc_sbc_challenges WHERE game_version=? AND challenge_type != 'ONE_CLICK_CHALLENGE'
               AND pulled=(SELECT MAX(pulled) FROM fc_sbc_challenges WHERE game_version=?) ORDER BY 1""", (GAME, GAME))]
        out = f"/tmp/futwiz-forms-{TODAY.replace('-', '')}.json"
        print("// 앱 안 브라우저에서 https://www.futwiz.com/ 을 연 탭에서 실행 — 반환 문자열을 그대로 파일에 쓴다\n"
              + FW_SNIPPET.replace("__SETS__", json.dumps(sets)))
        print(f"\n── 셸 ──\n.venv/bin/python scripts/collect_futbin_sbc_formations.py --futwiz-file {out}")
        return
    if a.futwiz_file:
        raw = json.load(open(a.futwiz_file))
        if isinstance(raw, str):
            raw = json.loads(raw)
        if not raw.get("done"):
            raise SystemExit("⛔ `done`이 없다 — 스니펫이 끝나지 않았다")
        data, how, skip = futwiz_map(con, raw)
        sid_of = {r[0]: r[1] for r in con.execute("SELECT challenge_ea_id, set_ea_id FROM fc_sbc_challenges WHERE game_version=?", (GAME,))}
        changed = apply(con, data, src_of=lambda cid: FW_SRC.format(set=sid_of.get(cid), how=how.get(cid, "")) + f" · {TODAY}",
                        conf=FW_CONF, site="FUTWIZ")
        for k, why in skip:
            print(f"   ⏭️ {k}: {why} — 적재 안 함")
        left = missing(con)
        print(f"포메이션 미기록 스쿼드형 챌린지: {len(left)}개{' ' + str(left) if left else ''}"
              + (" ⇒ 2차: Chrome(FUTBIN) `--print-snippet`" if left else ""))
        con.close()
        if changed and not a.no_solve:
            py = ROOT / ".venv" / "bin" / "python"
            subprocess.run([str(py if py.exists() else sys.executable), str(ROOT / "scripts" / "sbc_solve.py"), "--save"])
        return
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
        print("⇒ ⭐ 1차: 앱 안 브라우저 futwiz.com 탭에서 `--futwiz-snippet` 스니펫 → `--futwiz-file`로 넣는다"
              "(넣으면 해법을 바로 다시 푼다) · 그래도 남으면 2차: Chrome(futbin 탭)에서 `--print-snippet` → `--json-file`")


if __name__ == "__main__":
    main()

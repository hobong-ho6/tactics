#!/usr/bin/env python3
"""FC 목표(Objectives) 과제 수집 — fut.gg 목표 페이지 (2026-09-22 신설).

왜: `fc_evolutions.unlock_text`는 **과제 이름만** 들고 있다(예: 「Pep's Domination」).
    「그래서 뭘 하면 되나」는 매번 fut.gg를 봐야 했다 — 사용자 질문에서 드러난 구멍이다.
    ⇒ 목표 그룹 페이지의 과제(이름·조건·보상)를 적재해 진화 카드가 같이 띄운다.

⛔ API가 없다 — `/api/fut/objectives/…`는 전부 404다(2026-09-22 실측).
   목표 페이지는 **서버 렌더(RSC)**라 HTML 본문에 값이 그대로 박혀 있고, 태그를 지우면
   `|과제명|조건|보상|` 꼴로 깔끔하게 끊긴다. 그걸 읽는다.
⚠️ 목록 페이지 HTML에는 `<a href>`가 없지만 **RSC 페이로드에 경로 문자열이 남아 있어** 정규식으로 잡힌다.
⚠️ 기간제다 — 스냅샷으로 적재하고 지난 회차를 덮지 않는다(불변규칙 2).

⭐ 2026-10-09 전환(migration 102 · 사용자 지시 「fut.gg SP 목표 수집해서 얼티밋팀 페이지에」):
   태그를 지워 3칸씩 끊던 텍스트 파서를 버리고 **페이지에 박힌 구조화 상태**(TanStack Start SSR ·
   seroval 직렬화 `$R[n]=…`)를 읽는다. 텍스트 파서는 SP 과제를 11개만 잡았고 그룹 기간·그룹 완료 보상을 못 읽었다.
   ⛔ 페이지 스크립트를 **실행하지 않는다** — 값 리터럴만 파싱한다(아래 `_Tsr`).
   목록 페이지 `allObjectives` = 그룹(기간·그룹 보상) · 그룹 페이지 `objective.objectives` = 과제(조건·보상·인정 모드).
"""
import argparse, datetime as dt, json, re, sqlite3, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "tactics.db"
BASE = "https://www.fut.gg"
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en"}


def fetch(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


class _Tsr:
    """seroval 직렬화 JS 리터럴 파서 — `$R[n]=값` 정의와 `$R[n]` 참조, 객체·배열·문자열·숫자·!0/!1/null만 다룬다."""
    NUM = re.compile(r"-?\d+(\.\d+)?(e[+-]?\d+)?")
    KEY = re.compile(r"[A-Za-z_$][\w$]*")

    def __init__(self, t, i):
        self.t, self.i, self.refs = t, i, {}

    def _ws(self):
        while self.i < len(self.t) and self.t[self.i] in " \n\t\r":
            self.i += 1

    def val(self):
        self._ws()
        t, i = self.t, self.i
        if t.startswith("$R[", i):
            j = t.index("]", i)
            n = int(t[i + 3:j])
            self.i = j + 1
            if t[self.i:self.i + 1] == "=":
                self.i += 1
                v = self.val()
                self.refs[n] = v
                return v
            return self.refs.get(n)
        c = t[i]
        if c == "{":
            return self._obj()
        if c == "[":
            return self._arr()
        if c == '"':
            return self._str()
        for lit, v in (("!0", True), ("!1", False), ("null", None), ("void 0", None)):
            if t.startswith(lit, i):
                self.i += len(lit)
                return v
        m = self.NUM.match(t, i)
        if m:
            self.i = m.end()
            x = m.group()
            return float(x) if ("." in x or "e" in x) else int(x)
        raise ValueError(f"모르는 토큰 @{i}: {t[i:i + 40]!r}")

    def _str(self):
        t, i, out = self.t, self.i + 1, []
        while True:
            c = t[i]
            if c == "\\":
                n = t[i + 1]
                if n == "x":
                    out.append(chr(int(t[i + 2:i + 4], 16))); i += 4; continue
                if n == "u":
                    out.append(chr(int(t[i + 2:i + 6], 16))); i += 6; continue
                out.append({"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f"}.get(n, n)); i += 2; continue
            if c == '"':
                self.i = i + 1
                return "".join(out)
            out.append(c); i += 1

    def _key(self):
        self._ws()
        if self.t[self.i] == '"':
            return self._str()
        m = self.KEY.match(self.t, self.i)
        self.i = m.end()
        return m.group()

    def _obj(self):
        self.i += 1
        o = {}
        while True:
            self._ws()
            if self.t[self.i] == "}":
                self.i += 1
                return o
            k = self._key(); self._ws()
            self.i += 1                      # ':'
            o[k] = self.val(); self._ws()
            if self.t[self.i] == ",":
                self.i += 1

    def _arr(self):
        self.i += 1
        a = []
        while True:
            self._ws()
            if self.t[self.i] == "]":
                self.i += 1
                return a
            a.append(self.val()); self._ws()
            if self.t[self.i] == ",":
                self.i += 1


def loader(page, key):
    """페이지 상태에서 `key:$R[n]=…`(정의 지점)의 값을 읽는다. 없으면 None."""
    m = re.search(r"[{,]" + re.escape(key) + r":(?=\$R\[\d+\]=)", page)
    return _Tsr(page, m.end()).val() if m else None


def sp_of(awards):
    """보상 목록 → SP 합(없으면 None). fut.gg는 SP를 type='XP'로 준다."""
    xs = [a.get("xp") or 0 for a in awards or [] if a.get("type") == "XP"]
    return sum(xs) if xs else None


def names_of(awards):
    return [a.get("name") for a in awards or [] if a.get("name")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    idx = fetch(f"{BASE}/objectives/")
    if not idx:
        sys.exit("목록 페이지 조회 실패")
    allg = loader(idx, "allObjectives")
    if not allg:
        sys.exit("목록 페이지에서 allObjectives를 읽지 못했다 — fut.gg 구조 변경 여부를 볼 것")
    # 카테고리 slug는 목록 페이지 링크에서 잡는다(그룹 객체엔 categoryEaId만 있다)
    cat_of = {slug: cat for cat, slug in set(re.findall(r"/objectives/([a-z-]+)/(\d+-[a-z0-9-]+)/", idx))}
    # ⚠️ 시작 전 그룹(예: FC Pro 리더보드)은 목록에 링크가 없다 — 같은 categoryEaId를 가진 그룹의 slug로 메운다
    cat_by_id = {int(i): sl for i, sl in re.findall(r'\{eaId:(\d+),slug:"([a-z-]+)",name:"[^"]*"\}', idx)}
    cat_by_id.update({g.get("categoryEaId"): cat_of[g["slug"]] for g in allg if g["slug"] in cat_of})
    for g in allg:
        cat_of.setdefault(g["slug"], cat_by_id.get(g.get("categoryEaId")))
    print(f"목표 그룹 {len(allg)}개")

    rows, grows = [], []
    for g in allg:
        cat = cat_of.get(g["slug"])
        if not cat:
            print(f"  ⚠️ 카테고리 미상 — 건너뜀: {g['slug']}")
            continue
        gslug = f"{cat}/{g['slug']}"
        grows.append((a.game, g.get("eaId"), gslug, g.get("name"), cat, g.get("description"),
                      g.get("startTime"), g.get("endTime"), g.get("tasksCount"),
                      sp_of(g.get("awards")), json.dumps(names_of(g.get("awards")), ensure_ascii=False)))
        if not g.get("tasksCount"):
            continue
        page = fetch(f"{BASE}/objectives/{gslug}/")
        o = loader(page or "", "objective")
        if not o:
            print(f"  ⚠️ 조회·파싱 실패 {gslug}")
            continue
        for t in o.get("objectives") or []:
            modes = ((t.get("squadRequirements") or {}).get("match") or {}).get("modes")
            rows.append((a.game, gslug, g.get("name"), cat, t.get("name"), t.get("description"),
                         ", ".join(names_of(t.get("awards"))), t.get("eaId"), sp_of(t.get("awards")),
                         json.dumps(modes) if modes else None))
        time.sleep(0.3)
    print(f"과제 {len(rows)}개 수집")

    con = sqlite3.connect(DB)
    # 진화가 실제로 참조하는 과제만 보고한다 — 나머지는 조용히 적재한다(나중에 새 진화가 걸릴 수 있다).
    want = {r[0] for r in con.execute(
        "SELECT unlock_text FROM fc_evolutions WHERE unlock_text IS NOT NULL AND unlock_text<>''")}
    # ⚠️ 해금 문구가 **과제 이름**일 때도 있고 **그룹 이름**일 때도 있다
    #    (Pinged Pass → 과제 「Pep's Domination」 · Believe → 그룹 「Ted Lasso's Masterclass」).
    #    둘 다 맞춰 본다 — 한쪽만 보면 절반을 놓친다(2026-09-22 실측).
    hit = [r for r in rows if r[4] in want or r[2] in want]
    print(f"  그중 진화 해금과 이름이 맞는 것 {len(hit)}개:")
    for r in hit:
        via = "과제" if r[4] in want else f"그룹 「{r[2]}」"
        print(f"    ⭐ [{via}] {r[4]}  ←  {r[5]}  (보상 {r[6]})")
    miss = want - {r[4] for r in rows} - {r[2] for r in rows}
    if miss:
        print(f"  ⚠️ 과제를 못 찾은 해금 문구 {len(miss)}개(목표가 아니라 SBC·시즌패스일 수 있다): {', '.join(sorted(miss))}")

    if a.dry_run:
        print("(dry-run) 적재 안 함")
        return
    src = f"fut.gg 목표 페이지 SSR 상태 ({a.pulled} 수집, collect_futgg_objectives.py)"
    conf = ("HIGH — fut.gg가 EA 목표를 그대로 노출한다. ⚠️ 기간제라 pulled 시점의 사실이다. "
            "⚠️ 조건 문장은 원문 그대로이고 한국어 번역은 사람이 채운다(task_text_kr).")
    # ⭐ 원문이 같은 과제의 한국어 번역은 직전 회차에서 **이어받는다**(2026-09-25 신설).
    #    회차마다 행이 새로 생기므로 이월하지 않으면 손으로 채운 번역이 매번 사라지고
    #    화면(최신 pulled만 내보낸다)에서 번역이 통째로 빠진다 — 09-22·23·24 세 회차 모두 손으로 다시 채웠다.
    #    ⚠️ 이어받는 기준은 **원문(task_text)이 글자까지 같을 때**뿐이다. 원문이 바뀌면 번역도 다시 해야 한다.
    kr = {t: k for t, k in con.execute(
        """SELECT task_text, task_text_kr FROM fc_objective_tasks
           WHERE task_text_kr IS NOT NULL AND task_text_kr<>'' AND pulled<?
           ORDER BY pulled""", (a.pulled,))}
    n = 0
    for gv, slug, gname, cat, name, desc, rew, ea, sp, modes in rows:
        cur = con.execute(
            """INSERT INTO fc_objective_tasks(game_version,group_slug,group_name,group_category,
               task_name,task_text,task_text_kr,reward,source,confidence,pulled,task_ea_id,reward_sp,modes)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(game_version,group_slug,task_name,pulled) DO NOTHING""",
            (gv, slug, gname, cat, name, desc, kr.get(desc), rew, src, conf, a.pulled, ea, sp, modes))
        n += cur.rowcount
    ng = 0
    for r in grows:
        cur = con.execute(
            """INSERT INTO fc_objective_groups(game_version,group_ea_id,group_slug,group_name,group_category,description,
               start_time,end_time,tasks_count,group_sp,group_rewards,source,confidence,pulled)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(game_version,group_slug,pulled) DO NOTHING""", (*r, src, conf, a.pulled))
        ng += cur.rowcount
    con.commit()
    carried = sum(1 for r in rows if kr.get(r[5]))
    print(f"적재 과제 {n}행 (기존 {len(rows)-n}행) · 그룹 {ng}행 · 번역 이월 {carried}행")
    print(f"  SP 과제 {sum(1 for r in rows if r[8])}개 · SP 그룹 보상 {sum(1 for r in grows if r[9])}개")
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()

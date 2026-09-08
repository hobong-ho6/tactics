#!/usr/bin/env python3
"""회귀 게이트 — v2의 정본성 보증. DB 쓰기 스크립트는 시작 시 이걸 통과해야 한다.

게이트 (docs/20 게이트 표의 v2 이관):
  G1. 커널 정합 — 역할 37 / 조합 85 / 변형 217 (Kernel 로드 시 assert)
  G2. 인코딩 회귀 — player_matches 전 그리드 cells→map25 재인코딩 대조
  G3. 커널 앵커 — 저장 그리드로 기준 적합값 재현:
        캐시 measured:season RM(x=85, WM)  .835 wm_widemid/Support   (독립 앵커)
        Jackson ST(x=50, ST, 28경기)       .724 st_false9/Attack
        만잠비 CAM(x=50, CAM)              .861 cam_halfwinger/Balanced
        가르나초 LM(x=14, WM)              .771 wm_winger/Attack
        알리송 RM(x=85, WM)                .833 wm_widemid/Build-Up
        하지무사 RM(x=85, WM)              .821 wm_winger/Attack — 그리드 상수
          (DB에서 삭제된 행 — docs/20에 박힌 사본이 유일본, 커널 자체의 앵커)
  G4. 집계 공식 — 만잠비 대표팀 12경기 재집계가 저장 map25와 일치
  G5. JS 커널 동치 — 브라우저용 커널이 파이썬 앵커와 같은 값
  G6. DB 참조 정합 — PRAGMA foreign_key_check 결과 0건
  G8. 공통 후보 풀 — 슬롯 내 선수 중복 0, 도달 불가 squad 행 0, 활성 이적 실측 누락 0
  G9. 프리뷰 최신성 — 로컬 서버 no-store + JSON 요청 캐시 우회가 유지되는지 검사
  G10. 영상 레퍼런스 — duties 출처 결손 0 + 선수 화면의 기본 닫힘 details 유지
  G11. 현재 스쿼드 표시 — 확정 이탈·이적 후보·DEAD가 현재 선수 화면에 재노출되지 않음
  G12. 경기 리포트 — 완료본 필수 섹션·선수 전원·원문 파일·히트맵 메뉴가 모두 연결됨
       + draft 포함 모든 리포트가 선수 행을 최소 1개 갖는다(빈 피치 회귀 방지)
       + 경기 전용 FC 팀 설정·선발 11명 역할/포커스가 시즌 정본과 분리돼 있음
  G13. 조용한 이중화 — 동일인 2-id / 이중 기록 / match 링크 결손 / team_code↔대회 성격 불일치
       (2026-09-01 신설. **FK가 성립해서 G6가 원리적으로 못 잡는 부류**만 모았다 — obs#374.
        검사식 정본은 g13_checks()이고, 회귀 테스트 scripts/test_g13_regression.py가 이를 공유한다.)
  G14. 원장 정정 규약 — 불변규칙 2(추가만·재작성 금지)를 **행 단위로 강제**한다. 3항:
       ⑴ 원장재작성   보호 테이블의 기존 텍스트 필드가 **prefix를 보존하지 않고** 바뀌었다(또는 행 삭제).
       ⑵ 구중복       한 필드 안에서 한글 명사구가 인접 반복됐다(편집 사고의 지문).
       ⑶ claim↔evidence모순  같은 obs 행의 claim/evidence가 공유 명사구 뒤에서 극성이 반대다.
       (2026-09-08 신설. **G1~G13 전항 통과 상태에서 obs#503이 제자리 덮어써진 사고**가 계기다 — obs#517.
        기존 게이트는 전부 구조·수치 층이고 「행 내부 자연어」·「행의 편집 이력」은 사각지대였다.
        ⭐ 불변식은 「변경 금지」가 아니라 **「prefix 보존(덧붙임만)」**이다 — 정당한 덧붙임을 오탐하지 않는다.
        ⑵⑶은 **델타 검사**다: HEAD 이후 새로 생기거나 바뀐 obs 행만 본다. 보존해야 하는 과거 결함
        (obs#503)이 영구 실패를 만들지 않게 한다. 검사식 정본은 g14_checks(),
        회귀 테스트 scripts/test_g14_regression.py가 공유한다.
        ⚠️ 정당한 재작성이 필요하면 `G14_ALLOW_REWRITE=observations:503,...`로 행을 지정해 통과시킨다.)

사용: python3 scripts/gates.py                      (전체)
      python3 scripts/test_g13_regression.py        (G13 회귀 — 결함 합성 주입)
      python3 scripts/test_g14_regression.py        (G14 회귀 — 결함 합성 주입)
      python3 scripts/gates.py --g14-backtest 30    (G14 ⑴ 역검증: 최근 N커밋)
      from scripts.gates import run                 (프로그램 내 호출)
"""
import difflib
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB
from core.aggregate import player_aggregate
from core.encode import regression_check
from core.kernel import Kernel

HADJ_MOUSSA = "312691114X000140002400001"   # docs/20 게이트 표의 사본 (DB에 원본 없음)

ANCHORS = [
    # (라벨, 그리드 조회 SQL, params, x, slot_type, 기대 role, focus, sim)
    ("캐시 RM(measured:season)",
     "SELECT map25 FROM prescriptions p JOIN players pl ON pl.id=p.player_id "
     "WHERE pl.name='Matty Cash' AND p.kind='measured:season'", (), 85, "WM",
     "wm_widemid", "Support", 0.835),
    ("Jackson ST",
     "SELECT map25 FROM transfer_targets WHERE name='Nicolas Jackson' AND slot='ST'", (),
     50, "ST", "st_false9", "Attack", 0.724),
    ("만잠비 CAM",
     "SELECT map25 FROM transfer_targets WHERE name='Johan Manzambi' AND slot='CAM'", (),
     50, "CAM", "cam_halfwinger", "Balanced", 0.861),
    ("가르나초 LM",
     "SELECT map25 FROM transfer_targets WHERE name='Alejandro Garnacho' AND slot='LM'", (),
     14, "WM", "wm_winger", "Attack", 0.771),
    ("알리송 RM",
     "SELECT map25 FROM transfer_targets WHERE name='Alysson' AND slot='RM'", (),
     85, "WM", "wm_widemid", "Build-Up", 0.833),
    ("하지무사 RM(상수)", None, HADJ_MOUSSA, 85, "WM", "wm_winger", "Attack", 0.821),
]


G14_ROOT = Path(__file__).resolve().parent.parent

# 테이블 → prefix 보존을 요구하는 텍스트 필드.
#
# ⛔ 대상을 좁힌 근거(git 히스토리 실측, 2026-09-08) — 넓히면 정상 작업이 막힌다:
#   observations      재작성 8 / 커밋 160        → **강한 규약. 대상.**
#   player_duties     덧붙임 375 · 재작성 207(대부분 v1 i18n·스키마 이관) → **대상(전방 검사만).**
#   transfer_targets  69커밋 중 66이 편집(등급 갱신이 정상 작업)         → 대상 아님.
#   prescriptions / match_reports  fit 재산출·draft→complete가 정상       → 대상 아님.
G14_PROTECTED = {
    "observations": ["claim", "evidence", "source", "confidence"],
    "player_duties": ["duties", "execution", "adherence", "game_role_implication",
                      "source", "confidence", "sample_note"],
}

# ⑵⑶ 자연어 검사는 observations에만 적용한다(claim/evidence 쌍 구조가 있는 유일한 테이블).
G14_NEG = re.compile(r"(없다|없었다|없음|아니다|불가|0건|0장|0회|부재)")
G14_POS = re.compile(r"(있다|있었다|가용|가능|1장|1건|뿐이다|존재한다)")
G14_HAN = re.compile(r"[가-힣]")


def _g14_sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=G14_ROOT)
    return r.stdout


def g14_baseline(commit="HEAD"):
    """`commit` 시점 dump를 메모리 DB로 적재한다 — 이것이 「직전 정본」이다.

    ⭐ dump 텍스트를 직접 비교하지 않고 sqlite에 태워 필드로 비교한다.
       .dump가 특수문자 행을 unistr(...)로 직렬화하므로 텍스트 대조는 형식 차이로 오탐이 난다.
    """
    schema = _g14_sh(f"git show {commit}:db/dump/schema.sql")
    if not schema.strip():
        return None
    con = sqlite3.connect(":memory:")
    con.executescript(schema)
    for table in G14_PROTECTED:
        data = _g14_sh(f"git show {commit}:db/dump/{table}.sql")
        if data.strip():
            con.executescript(data)
    return con


def g14_strip_noise(t):
    """수사적 반복이 정당한 구역을 제거한다 — 이 필터가 ⑵의 오탐 0을 만든다.

    「」 안은 verbatim 인용이라 「Duro, duro, duro」·「혹독하고 혹독하고」 같은 반복이 정상이다.
    코드·URL·마크다운 표 문법도 반복 패턴을 정상적으로 갖는다.
    """
    t = re.sub(r"「[^」]*」", " ", t)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"https?://\S+|\S+\.(?:com|eus|es|ng|io|md|uk)\S*", " ", t)
    t = re.sub(r"[|\-]{3,}", " ", t)
    return t


def g14_dup_phrase(text):
    """한글 명사구 인접 반복(X + 짧은 연결 + X)."""
    out = []
    for m in re.finditer(r"([가-힣][가-힣 ]{5,25}?)([가-힣]{0,2} ?)\1", g14_strip_noise(text)):
        unit = m.group(1)
        if len(unit.strip()) >= 6:
            out.append(unit.strip())
    return out


def g14_clash(claim, evid, minblk=8, win=14):
    """claim·evidence의 공유 명사구 뒤 극성이 반대인 지점."""
    out = []
    sm = difflib.SequenceMatcher(None, claim, evid, autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        if n < minblk:
            continue
        blk = claim[i:i + n]
        if len(G14_HAN.findall(blk)) < 4:
            continue
        ta, tb = claim[i + n:i + n + win], evid[j + n:j + n + win]
        if (G14_NEG.search(ta) and G14_POS.search(tb)) or (G14_POS.search(ta) and G14_NEG.search(tb)):
            out.append((blk.strip()[-24:], ta.strip(), tb.strip()))
    return out


def g14_checks(con, base):
    """{키: 위반 리스트} — **읽기 전용**. base가 None이면 ⑴을 건너뛴다(첫 커밋 등)."""
    out = {"append_rewrite": [], "dup_phrase": [], "claim_evid_clash": []}

    # ⑴ prefix 비보존 재작성 + 행 삭제
    allow = {s.strip() for s in os.environ.get("G14_ALLOW_REWRITE", "").split(",") if s.strip()}
    if base is not None:
        for table, fields in G14_PROTECTED.items():
            cols = ", ".join(["id"] + fields)
            try:
                old = {r[0]: r[1:] for r in base.execute(f"SELECT {cols} FROM {table}")}
                new = {r[0]: r[1:] for r in con.execute(f"SELECT {cols} FROM {table}")}
            except sqlite3.Error:
                continue
            # ⚠️ 빈 baseline 가드 — 2026-09-08에 실제로 물린 함정이다.
            #    구 커밋은 dump가 data/dump/에 있어 `git show HEAD:db/dump/...`가 빈 문자열을
            #    돌려주고, 그러면 old={}가 되어 **모든 재작성이 조용히 통과**한다(거짓 ✅).
            #    baseline이 비었는데 현재는 행이 있으면 「검사 불가」를 위반으로 올린다.
            if not old and new:
                out["append_rewrite"].append(
                    (table, 0, "(baseline 적재 실패 — 검사 불가)", "", ""))
                continue
            for rid, ovals in old.items():
                key = f"{table}:{rid}"
                if key in allow:
                    continue
                if rid not in new:
                    out["append_rewrite"].append((table, rid, "(행 삭제)", "", ""))
                    continue
                for fld, o, n in zip(fields, ovals, new[rid]):
                    if o == n:
                        continue
                    if o is None:                     # NULL → 값: 결손 채움이므로 허용
                        continue
                    if n is not None and n.startswith(o):
                        continue                      # 덧붙임(prefix 보존) → 정상
                    out["append_rewrite"].append(
                        (table, rid, fld, (o or "")[:60], (n or "")[:60]))

    # ⑵⑶ observations 자연어 층 — ⭐ **델타 검사다**(전수 아님).
    #    전수로 두면 obs#503처럼 「불변규칙 2 때문에 일부러 고치지 않기로 한 행」이 영구 실패를 만든다.
    #    (obs#503의 중복·모순은 obs#517이 정정 기록으로 닫았고, 행 자체는 보존한다 — 재작성 금지.)
    #    ⇒ **HEAD 이후 새로 생기거나 텍스트가 바뀐 행만** 본다. 결함을 「도입 시점」에 잡는 것이 목적이다.
    try:
        rows = con.execute("SELECT id, claim, evidence, source, confidence "
                           "FROM observations").fetchall()
    except sqlite3.Error:
        rows = []
    if base is not None:
        try:
            prev = {r[0]: r[1:] for r in base.execute(
                "SELECT id, claim, evidence, source, confidence FROM observations")}
        except sqlite3.Error:
            prev = {}
        rows = [r for r in rows if prev.get(r[0]) != tuple(r[1:])]
    for rid, c, e, s, cf in rows:
        for fld, txt in (("claim", c), ("evidence", e), ("source", s), ("confidence", cf)):
            if not txt:
                continue
            for unit in g14_dup_phrase(txt):
                out["dup_phrase"].append((rid, fld, unit))
        if c and e:
            for blk, ta, tb in g14_clash(c, e):
                out["claim_evid_clash"].append((rid, blk, ta, tb))
    return out


G14_LABELS = {
    "append_rewrite": "원장재작성",
    "dup_phrase": "구중복",
    "claim_evid_clash": "claim↔evidence모순",
}


def g13_checks(con):
    """G13 「조용한 이중화」 4항을 실행해 {키: 위반행 리스트}를 돌려준다 — **읽기 전용**.

    run()과 scripts/test_g13_regression.py가 **같은 SQL을 공유**하도록 분리했다.
    회귀 테스트가 SQL을 복사해 가면 게이트를 고쳤을 때 테스트가 낡은 식을 검사하게 된다.

    넷 다 FK가 성립해서 G6(foreign_key_check)가 원리적으로 못 잡는 부류다.
    2026-09-01에 손으로 세다 각각 실물 결함을 발견해 게이트화했다(obs#368·#370·#372·#373·#374).
    """
    out = {}

    # ⑴ 동일인 2-id — 같은 선수가 players에 두 행으로 존재하는 것.
    #    실증: 에수구가 103/140 두 id로 있었고 **참조가 갈려** CHE 유출 행(140)이 실측 출전(103)과
    #    이어지지 않았다. 두 id가 모두 존재하므로 foreign_key_check는 통과한다(G6 사각지대).
    #    외부 소스 id가 겹치면 동일인이다 — fotmob_id/sofascore_id를 열쇠로 쓴다.
    out["dup_person"] = con.execute("""
        SELECT 'fotmob_id', fotmob_id, GROUP_CONCAT(id) FROM players
         WHERE fotmob_id IS NOT NULL GROUP BY fotmob_id HAVING COUNT(*) > 1
        UNION ALL
        SELECT 'sofascore_id', sofascore_id, GROUP_CONCAT(id) FROM players
         WHERE sofascore_id IS NOT NULL GROUP BY sofascore_id HAVING COUNT(*) > 1""").fetchall()

    # ⑵ 이중 기록 — 같은 출전이 SofaScore·FotMob 두 소스로 각각 적재된 것.
    #    UNIQUE(player_id, event_id)는 event_id가 다르므로 막지 못한다(FotMob은 −matchId 규약).
    #    실증: 2026-09-01에 전수를 세니 런북이 적어 온 「21쌍」이 아니라 **77쌍**이었고,
    #    행 수 기반 질의가 프리시즌 6경기에서 이중 계상되고 있었다.
    out["dup_appearance"] = con.execute("""
        SELECT player_id, match_id FROM player_matches
         WHERE match_id IS NOT NULL GROUP BY player_id, match_id HAVING COUNT(*) > 1""").fetchall()

    # ⑶ match 링크 결손 — ⑵의 사각지대를 메우는 짝이다.
    #    match_id가 한쪽만 NULL이면 ⑵의 (player_id, match_id) 키로 짝이 잡히지 않는다.
    #    실제로 잭슨 08-05 1쌍이 그렇게 숨어 있었고, 링크를 봉합하고 나서야 드러났다.
    out["orphan_match_link"] = con.execute("""
        SELECT pm.id FROM player_matches pm JOIN matches m ON m.event_id = pm.event_id
         WHERE pm.match_id IS NULL""").fetchall()

    # ⑷ team_code ↔ 대회 성격 정합 — team_code는 스키마상 「그 경기에서 소속」이다.
    #    실증: 수집기가 「수집 시점 현 소속」을 찍어 바르콜라의 Ligue 1 경기가 LIV,
    #    완비사카의 DR콩고 WC예선이 AVL이었다(클럽 333행 + 대표팀 406행).
    #    ⭐ 코드 목록을 하드코딩하지 않는다 — **한 코드가 클럽 대회와 대표팀 대회에 동시에
    #    쓰이면 위반**이라는 불변식으로 잡는다(클럽은 WC예선을 뛰지 않고 대표팀은 리그를 뛰지 않는다).
    #    새 코드가 늘어도 자기유지되고, 정리 전 DB에서 AVL·CHE·LIV 3건을 실제로 잡는다.
    #    ⚠️ 한계: 어떤 코드가 **오직 잘못된 쪽에만** 쓰이면 섞이지 않아 통과한다.
    #    ⚠️ 「FIFA Club World Cup」은 클럽 대회인데 '%World Cup%'에 걸리므로 반드시 제외한다.
    out["mixed_team_code"] = con.execute("""
        WITH cls AS (
          SELECT team_code,
                 CASE WHEN competition NOT LIKE '%Club World Cup%' AND (
                        competition LIKE '%World Cup Qual%'  OR competition LIKE '%FIFA World Cup%'
                     OR competition LIKE '%Africa Cup%'      OR competition LIKE '%Nations League%'
                     OR competition LIKE '%International Friendly%'
                     OR competition LIKE '%Euro%Qual%'       OR competition LIKE '%Copa America%'
                     OR competition LIKE '%Championship Qual%'
                     OR competition LIKE '%Asian Cup%'       OR competition LIKE '%Gold Cup%')
                      THEN 'NT' ELSE 'CLUB' END AS kind
            FROM player_matches
           WHERE team_code IS NOT NULL AND competition IS NOT NULL)
        SELECT team_code, GROUP_CONCAT(DISTINCT kind) FROM cls
         GROUP BY team_code HAVING COUNT(DISTINCT kind) > 1""").fetchall()

    # ⑸ 클럽 코드 ↔ 리그 정합 — ⑷보다 강하다. ⑷는 「한 코드가 CLUB·NT 양쪽에 쓰이면」만 잡는데,
    #    ⭐ 2026-09-01에 **AVL이 분데스리가·리그1·세리에A·챔피언십에 동시 출현**하는 107행이 발견됐다.
    #    ⑷는 이걸 못 잡는다(AVL이 클럽 대회에만 쓰여 CLUB/NT가 섞이지 않는다) — 명시했던 한계가 실제로 발현했다.
    #    원인: 09-01 1차 정리가 `transfer_targets` **CONFIRMED만** 스캔해서
    #    ⓐ유출 선수(로저스) ⓑ임대 나간 선수(네델코비치·일링-주니어) ⓒ아직 HIGH인 영입 후보(하우드-벨리스)
    #    ⓓ유스·이전 클럽(마조)을 통째로 놓쳤다.
    #    불변식: **한 클럽 코드는 서로 다른 나라의 1부 리그에 동시에 나올 수 없다.**
    #    코드 목록도 리그 소속도 하드코딩하지 않는다 — 리그 이름 집합만 쓰고 「2개 이상」을 위반으로 본다.
    out["club_league_conflict"] = con.execute("""
        SELECT team_code, GROUP_CONCAT(DISTINCT competition) FROM player_matches
         WHERE team_code IS NOT NULL
           AND competition IN ('Premier League','LaLiga','Bundesliga','Serie A','Ligue 1',
                               'Championship','Eredivisie','Primeira Liga','Süper Lig')
         GROUP BY team_code HAVING COUNT(DISTINCT competition) > 1""").fetchall()

    return out


G13_LABELS = {
    "dup_person": "동일인2id",
    "dup_appearance": "이중기록",
    "orphan_match_link": "match링크결손",
    "mixed_team_code": "team_code대회불일치",
    "club_league_conflict": "클럽코드리그충돌",
}



# ── G8 확장 · G15 — 2026-09-08 점검 후속(사용자 지시 5·2번). 검사식은 여기가 정본이다. ──
import re as _re
# prescriptions.kind 허용 어휘. pos_class(obs#527)와 같은 병(자유 어휘 60종)을 구조로 고정한다 —
# 기존 값을 바꾸지 않고 **형태**만 묶는다. 새 접두를 만들려면 여기와 docs/00을 함께 고친다.
KIND_RE = _re.compile(
    r"^(fc26:opt:[A-Z]{2,3}(-deprecated)?"
    r"|measured(:[A-Za-z0-9/_-]+)*(@(dom|tight))?"
    r"|optimal(:[A-Za-z0-9/_-]+)?(-deprecated)?"
    r"|role(:[A-Za-z0-9/_-]+)?"
    r"|projected(:[A-Za-z0-9/_-]+)?(-deprecated)?"
    r"|match:[A-Z]{3}-[0-9]+-[0-9]+)$")
G8X_LABELS = {"kind_vocab": "kind어휘이탈", "opt_pos_orphan": "opt슬롯없음",
              "opt_role_group": "opt역할군불일치", "opt_xi": "opt선발≠11/단일포메이션"}


def g8_prescription_checks(con):
    """게임 처방(prescriptions)이 그 체제의 slots 정본에 **입력 가능한 값**인지.
    docs/00 「slot_type과 fit_role의 역할군은 반드시 일치해야 한다 (게이트 미보유)」를 게이트화했다.
    2026-09-08 실물: CHE 선발 12명(3-4-2-1 + 5-4-1 RB) · CHE LDM/RDM 4행(슬롯 없음) · kind 60종."""
    out = {k: [] for k in G8X_LABELS}
    out["kind_vocab"] = [k for (k,) in con.execute("SELECT DISTINCT kind FROM prescriptions")
                         if not KIND_RE.match(k)]
    out["opt_pos_orphan"] = con.execute("""
        SELECT p.id, p.regime_id, p.pos_label FROM prescriptions p
        WHERE p.kind LIKE 'fc26:opt:%' AND p.kind NOT LIKE '%-deprecated'
          AND NOT EXISTS (SELECT 1 FROM slots s WHERE s.regime_id=p.regime_id AND s.pos=p.pos_label)
        """).fetchall()
    out["opt_role_group"] = con.execute("""
        SELECT p.id, p.regime_id, p.pos_label, p.role_id FROM prescriptions p
        JOIN game_roles gr ON gr.role_id=p.role_id AND gr.game_version=COALESCE(p.game_version,'FC26')
        WHERE p.kind LIKE 'fc26:opt:%' AND p.kind NOT LIKE '%-deprecated'
          AND NOT EXISTS (SELECT 1 FROM slots s WHERE s.regime_id=p.regime_id AND s.pos=p.pos_label
                            AND s.slot_type=gr.position_type)""").fetchall()
    # 선발은 체제·버전당 정확히 11명이고, 11명의 pos가 **한 포메이션**의 슬롯에 전부 들어가야 한다.
    for rid, gv in con.execute("""SELECT DISTINCT regime_id, COALESCE(game_version,'FC26')
                                  FROM prescriptions WHERE kind LIKE 'fc26:opt:%' AND starter=1"""):
        poss = [r[0] for r in con.execute("""SELECT pos_label FROM prescriptions
            WHERE regime_id=? AND COALESCE(game_version,'FC26')=? AND kind LIKE 'fc26:opt:%'
              AND kind NOT LIKE '%-deprecated' AND starter=1""", (rid, gv))]
        fits = [f for (f,) in con.execute("SELECT DISTINCT formation FROM slots WHERE regime_id=?", (rid,))
                if set(poss) <= {p for (p,) in con.execute(
                    "SELECT pos FROM slots WHERE regime_id=? AND formation=?", (rid, f))}]
        if len(poss) != 11 or len(set(poss)) != 11 or not fits:
            out["opt_xi"].append((rid, gv, len(poss), fits))
    return out


def g12_role_group_orphans(con):
    """경기 프리셋(match_player_prescriptions)의 역할이 그 슬롯의 역할군 밖이면 게임에 입력할 수 없다.
    2026-09-08 실물 6행 — 교체 투입 자리표시 cm_b2b가 RCB·LM·ST·LAM·RM에 박혀 있었다."""
    return con.execute("""
        SELECT mpp.report_id, mpp.pos_label, mpp.role_id
        FROM match_player_prescriptions mpp JOIN match_reports mr ON mr.id=mpp.report_id
        JOIN game_roles gr ON gr.role_id=mpp.role_id AND gr.game_version=mpp.game_version
        WHERE NOT EXISTS (SELECT 1 FROM slots s WHERE s.regime_id=mr.regime_id
                            AND s.pos=mpp.pos_label AND s.slot_type=gr.position_type)""").fetchall()


G15_LABELS = {"note_missing": "rule_note결손", "undeclared_diverge": "미신고편차",
              "false_nostats": "거짓NO-STATS"}


def g15_checks(con):
    """팀 설정 3축 규칙(core.team_settings) 준수 — 「규칙과 같거나, 다르면 사유가 있다」.
    규칙 자체는 사전 등록(docs/20)이며 여기서는 기록과 규칙의 **차이가 신고됐는지**만 본다."""
    from core.team_settings import suggest, compare
    out = {k: [] for k in G15_LABELS}
    for rid, status, bu, da, lh, note, poss, ppda, passes, long_att in con.execute("""
        SELECT mgs.report_id, mr.status, mgs.build_up_style, mgs.defensive_approach, mgs.line_height,
               mgs.rule_note,
               (SELECT MAX(possession) FROM player_matches pm
                 WHERE pm.event_id=mr.event_id AND pm.team_code=mr.team_code),
               ts.ppda_v, ts.passes_v, ts.long_att_v
        FROM match_game_setups mgs JOIN match_reports mr ON mr.id=mgs.report_id
        LEFT JOIN team_match_stats ts ON ts.event_id=mr.event_id AND ts.team_code=mr.team_code"""):
        if not note or not note.strip():
            if status == "complete":
                out["note_missing"].append(rid)
            continue
        sug = suggest(poss, passes, long_att, ppda)
        diff = compare(sug, bu, da, lh)
        if diff and not note.startswith("DIVERGE"):
            out["undeclared_diverge"].append((rid, diff))
        if note.startswith("NO-STATS") and sug["build_up_style"] and sug["defensive_approach"]:
            out["false_nostats"].append(rid)
    return out


def run(db_path=None, verbose=True):
    db_path = db_path or DB
    con = sqlite3.connect(db_path)
    fails = []

    # G1 — Kernel 로드가 정합 assert를 겸한다
    k = Kernel("FC26", db_path)
    if verbose:
        print("G1 커널 정합: 37/85/217 ✅")

    # G2
    bad, total = regression_check(con)
    if verbose:
        print(f"G2 인코딩 회귀: {total}행 중 불일치 {len(bad)} {'✅' if not bad else '⛔ ' + str(bad[:5])}")
    if bad:
        fails.append("G2")

    # G3
    for label, sql, params, x, st, wr, wf, ws in ANCHORS:
        if sql is None:
            m25 = params
        else:
            row = con.execute(sql, params).fetchone()
            if not row or not row[0]:
                if verbose:
                    print(f"G3 {label}: ⚠️ 행 없음 — 건너뜀 (보존정책 삭제 가능)")
                continue
            m25 = row[0]
        r, f, s = k.best_fit(m25, x, st)
        ok = r == wr and f == wf and abs(s - ws) < 0.001
        if verbose:
            print(f"G3 {label}: {r}/{f} {s:.3f} {'✅' if ok else f'⛔ 기대 {wr}/{wf} {ws}'}")
        if not ok:
            fails.append(f"G3:{label}")

    # G4 — 집계 공식 재현 (만잠비 대표팀 12경기 → prescriptions measured:national)
    manz = con.execute("SELECT id FROM players WHERE name='Johan Manzambi'").fetchone()
    if manz:
        stored = con.execute(
            "SELECT map25 FROM prescriptions WHERE player_id=? AND kind='measured:national'",
            (manz[0],)).fetchone()
        agg = player_aggregate(manz[0],
                               "competition IN ('FIFA World Cup','World Cup Qual. UEFA',"
                               "'International Friendly')", db_path=db_path)
        ok = stored and agg and agg["map25"] == stored[0] and agg["n"] == 12
        if verbose:
            print(f"G4 집계 재현(만잠비 national n={agg['n'] if agg else '?'}): "
                  f"{'✅' if ok else '⛔ 저장 ' + str(stored[0] if stored else None) + ' vs 재집계 ' + str(agg['map25'] if agg else None)}")
        if not ok:
            fails.append("G4")

    # G5 — JS 커널 동치 (site/assets/kernel.js가 파이썬과 같은 값을 내는가)
    #      node + 익스포트된 kernels/FC26.json으로 앵커 재계산. node/JSON 부재 시 건너뜀.
    import subprocess
    kern_json = Path(__file__).resolve().parent.parent / "site" / "data" / "kernels" / "FC26.json"
    if kern_json.exists():
        cases = []   # (map25, x, slot_type, 기대 sim)
        for label, sql, params, x, st, wr, wf, ws in ANCHORS:
            con2 = sqlite3.connect(db_path)
            m25 = params if sql is None else (con2.execute(sql, params).fetchone() or [None])[0]
            con2.close()
            if m25:
                cases.append((m25, x, st, ws))
        js = (
            "import { Kernel } from " + json_str(kernel_js_uri()) + ";\n"
            "import { readFileSync } from 'fs';\n"
            "const K = new Kernel(JSON.parse(readFileSync(" + json_str(str(kern_json)) + ", 'utf8')));\n"
            "const cases = " + json_str(cases) + ";\n"
            "for (const [m25, x, st, ws] of cases) {\n"
            "  const r = K.bestFit(m25, x, st);\n"
            "  if (Math.abs(r.sim - ws) >= 0.001) { console.log('MISMATCH', r.sim, ws); process.exit(1); }\n"
            "}\nconsole.log('OK', cases.length);\n")
        try:
            p = subprocess.run(["node", "--input-type=module", "-e", js],
                               capture_output=True, text=True, timeout=30)
            ok5 = p.returncode == 0
            if verbose:
                print(f"G5 JS 커널 동치({len(cases)}앵커): {'✅ ' + p.stdout.strip() if ok5 else '⛔ ' + p.stdout + p.stderr}")
            if not ok5:
                fails.append("G5")
        except FileNotFoundError:
            if verbose:
                print("G5 JS 커널 동치: ⚠️ node 없음 — 건너뜀")
    elif verbose:
        print("G5 JS 커널 동치: ⚠️ kernels/FC26.json 미익스포트 — 건너뜀")

    # G6 — SQLite는 연결별 foreign_keys 설정에 따라 고아 FK 삽입을 허용할 수 있다.
    #      읽기 전용 검사인 foreign_key_check는 설정과 무관하게 전체 고아 행을 찾는다.
    fk_bad = con.execute("PRAGMA foreign_key_check").fetchall()
    if verbose:
        print(f"G6 DB 참조 정합: 고아 FK {len(fk_bad)}건 "
              f"{'✅' if not fk_bad else '⛔ ' + str(fk_bad[:5])}")
    if fk_bad:
        fails.append("G6")

    # G7 — v1 appearances 기능 스탯이 v2 player_matches 위치 행과 병합됐는지 확인한다.
    #      migrate_v1.py의 옛 UPDATE가 이 필드들을 빼먹어 obs#132 보정 142행이 유실됐다.
    app_anchor = con.execute("""SELECT pm.duels_won,pm.tackles,pm.interceptions,
                                       json_extract(pm.stats_json,'$.passes_total')
                                FROM player_matches pm JOIN players p ON p.id=pm.player_id
                                WHERE p.name='Boubacar Kamara' AND pm.event_id=14025276""").fetchone()
    ok7 = app_anchor == (14, 6, 4, 93)
    if verbose:
        print(f"G7 appearances 병합 앵커: {app_anchor} "
              f"{'✅' if ok7 else '⛔ 기대 (14, 6, 4, 93)'}")
    if not ok7:
        fails.append("G7")

    # G8 — 모든 선수 목록 화면의 정본인 v_slot_candidates 정합.
    #      CONFIRMED target + 승격 squad가 같은 슬롯에 이중 노출되거나,
    #      현재 슬롯 유형이 없는 squad 행이 유령 후보로 남는 것을 막는다.
    dup_candidates = con.execute("""
        SELECT regime_id,formation,pos,COALESCE(player_id,-1),COUNT(*)
        FROM v_slot_candidates
        GROUP BY regime_id,formation,pos,COALESCE(player_id,-1)
        HAVING COUNT(*)>1""").fetchall()
    unreachable_squad = con.execute("""
        SELECT se.id
        FROM squad_entries se
        WHERE NOT EXISTS (
          SELECT 1 FROM slots sl
          WHERE sl.regime_id=se.regime_id AND sl.slot_type=se.slot_type
        )""").fetchall()
    uncovered_targets = con.execute("""
        SELECT tt.id
        FROM transfer_targets tt
        JOIN regimes r ON r.team_code=tt.team_code AND r.end IS NULL
        WHERE tt.map25 IS NOT NULL
          AND tt.likelihood!='OWNED' AND tt.likelihood NOT LIKE 'DEAD%'
          AND NOT EXISTS (
            SELECT 1 FROM v_slot_candidates vc
            WHERE vc.regime_id=r.id
              AND vc.pos=(CASE tt.slot WHEN 'LW' THEN 'LM' WHEN 'RW' THEN 'RM' ELSE tt.slot END)
              AND (vc.player_id=tt.player_id OR
                   (tt.player_id IS NULL AND vc.name_en=tt.name))
          )""").fetchall()
    ok8 = not dup_candidates and not unreachable_squad and not uncovered_targets
    if verbose:
        detail = (f"중복 {len(dup_candidates)} · 도달불가 {len(unreachable_squad)} · "
                  f"이적누락 {len(uncovered_targets)}")
        print(f"G8 공통 슬롯 후보 풀: {detail} {'✅' if ok8 else '⛔'}")
    if not ok8:
        fails.append("G8")

    # G8 확장 — 게임 처방이 slots 정본에 입력 가능한가(docs/00 「게이트 미보유」 항목의 게이트화, 2026-09-08).
    g8x = g8_prescription_checks(con)
    ok8x = not any(g8x.values())
    if verbose:
        summary = " · ".join(f"{G8X_LABELS[k]} {len(v)}" for k, v in g8x.items())
        detail = "" if ok8x else " ⛔ " + str({k: v[:3] for k, v in g8x.items() if v})
        print(f"G8+ 게임 처방 정합: {summary} {'✅' if ok8x else detail}")
    if not ok8x:
        fails.append("G8+")

    # G9 — 생성 JSON과 UI가 어긋나는 캐시 회귀를 정적 검사한다.
    root = Path(__file__).resolve().parent.parent
    serve_py = (root / "scripts" / "serve.py").read_text()
    data_js = (root / "site" / "assets" / "data.js").read_text()
    # ⚠️ launch.json의 heatmap 인라인 핸들러는 HTML/JS에 no-store를 보내지 않는다(그 파일 상단 주석).
    # 그래서 assets/*.js를 고쳐도 브라우저가 옛 사본을 계속 쓴다 — 2026-08-25에 실제로 발생했다:
    # decodeMap 방어를 넣었는데 캐시된 구 kernel.js가 예외를 던져 히트맵이 계속 비었다.
    # 공유 모듈(kernel.js·pitch.js)을 임포트할 때는 ?v= 캐시 무효화 쿼리를 달아 이를 막는다.
    versioned_js = ("kernel.js", "pitch.js")
    stale_js_imports = [
        f"{html.name}:{mod}"
        for html in sorted((root / "site").glob("*.html"))
        for mod in versioned_js
        if f"./assets/{mod}'" in html.read_text()
    ]
    ok9 = (
        'Cache-Control", "no-store' in serve_py
        and "cache: 'no-store'" in data_js
        and "searchParams.set('_', Date.now()" in data_js
        and "scripts/serve.py" in (root / "scripts" / "serve.sh").read_text()
        and not stale_js_imports
    )
    if verbose:
        print(f"G9 프리뷰 최신성: 서버·JSON 캐시 우회 · 무버전 JS 임포트 "
              f"{len(stale_js_imports)} {'✅' if ok9 else '⛔'}")
        if stale_js_imports:
            print(f"   ⛔ ?v= 없는 공유 모듈 임포트: {', '.join(stale_js_imports)}")
    if not ok9:
        fails.append("G9")

    # G10 — 영상·스카우트 결론은 원문/내부 근거를 접힌 상태로 추적할 수 있어야 한다.
    missing_duty_sources = con.execute("""
        SELECT id FROM player_duties
        WHERE source IS NULL OR trim(source)=''""").fetchall()
    missing_current_duties = con.execute("""
        SELECT r.team_code,p.id
        FROM squad_entries se
        JOIN regimes r ON r.id=se.regime_id AND r.end IS NULL
        JOIN players p ON p.id=se.player_id
        LEFT JOIN player_duties pd ON pd.regime_id=r.id AND pd.player_id=p.id
        WHERE NOT EXISTS (
          SELECT 1 FROM transfer_outgoing o
          WHERE o.team_code=r.team_code AND o.player_id=p.id AND o.likelihood='CONFIRMED'
        )
        GROUP BY r.team_code,p.id HAVING COUNT(pd.id)=0""").fetchall()
    missing_duty_provenance = con.execute("""
        SELECT id FROM player_duties
        WHERE sample_scope IS NULL OR trim(sample_scope)=''
           OR sample_note IS NULL OR trim(sample_note)=''""").fetchall()
    current_source_rows = con.execute("""
        SELECT r.team_code,p.id,group_concat(pd.source,' ')
        FROM squad_entries se
        JOIN regimes r ON r.id=se.regime_id AND r.end IS NULL
        JOIN players p ON p.id=se.player_id
        JOIN player_duties pd ON pd.regime_id=r.id AND pd.player_id=p.id
        WHERE NOT EXISTS (
          SELECT 1 FROM transfer_outgoing o
          WHERE o.team_code=r.team_code AND o.player_id=p.id AND o.likelihood='CONFIRMED'
        )
        GROUP BY r.team_code,p.id""").fetchall()
    ref_re = re.compile(
        r"https?://|www\.|(?:[a-z0-9-]+\.)+[a-z]{2,}/|obs#\d+|reports/[\w./-]+\.md|"
        r"SofaScore(?: API)? event\s+\d+", re.I)
    current_without_reference = [row[:2] for row in current_source_rows if not ref_re.search(row[2] or '')]
    player_html = (root / "site" / "player.html").read_text()
    ok10 = (
        not missing_duty_sources
        and not missing_current_duties
        and not missing_duty_provenance
        and not current_without_reference
        and '<details class="refs">' in player_html
        and 'references(d.source)' in player_html
        and 'analysisWindow(d)' in player_html
        and '<details class="refs" open' not in player_html
    )
    if verbose:
        print(f"G10 영상 레퍼런스: 출처 결손 {len(missing_duty_sources)} · 현재 분석 누락 "
              f"{len(missing_current_duties)} · 표본 메타 누락 {len(missing_duty_provenance)} · "
              f"현재 클릭근거 누락 {len(current_without_reference)} · 기본 닫힘 "
              f"{'✅' if ok10 else '⛔'}")
    if not ok10:
        fails.append("G10")

    # G11 — 이력은 DB에 보존하되 현재 선수 화면과 이적 화면의 노출 범위를 분리한다.
    # ⚠️ formation을 GROUP BY에 넣는다(2026-08-16). 한 regime에 포메이션이 하나뿐일 때는
    #    (regime,pos,player)로 충분했으나, AVL에 4-4-2가 추가되면서 같은 선수가 두 포메이션의
    #    같은 pos 후보로 정상적으로 잡힌다. 막아야 하는 것은 "같은 포메이션의 같은 칸에 두 번"이다.
    #    G8의 dup_candidates도 formation을 포함해 묶는다 — 두 게이트의 기준을 맞춘다.
    visible_dup = con.execute("""
        SELECT vc.regime_id,vc.formation,vc.pos,vc.player_id,COUNT(*)
        FROM v_slot_candidates vc
        WHERE vc.source_kind='squad'
          AND NOT EXISTS (
            SELECT 1 FROM transfer_outgoing o
            WHERE o.team_code=vc.team_code AND o.player_id=vc.player_id
              AND o.likelihood='CONFIRMED'
          )
        GROUP BY vc.regime_id,vc.formation,vc.pos,vc.player_id
        HAVING COUNT(*)>1""").fetchall()
    sancho_departed = con.execute("""
        SELECT 1 FROM transfer_outgoing
        WHERE team_code='AVL' AND player_id=15 AND likelihood='CONFIRMED'""").fetchone()
    departed_starters = con.execute("""
        SELECT pr.regime_id,pr.pos_label,pr.player_id
        FROM prescriptions pr JOIN regimes r ON r.id=pr.regime_id
        WHERE pr.kind LIKE 'fc26:opt:%' AND pr.starter=1
          AND EXISTS (
            SELECT 1 FROM transfer_outgoing o
            WHERE o.team_code=r.team_code AND o.player_id=pr.player_id
              AND o.likelihood='CONFIRMED'
          )""").fetchall()
    compare_html = (root / "site" / "compare.html").read_text()
    transfer_html = (root / "site" / "transfer.html").read_text()
    report_html = (root / "site" / "report.html").read_text()
    ok11 = (
        not visible_dup and bool(sancho_departed)
        and "includeTransfers: false" in compare_html
        and "includeDeparted = false" in data_js
        and "visible(T.targets)" in transfer_html
        and "visible(T.outgoing)" in transfer_html
        and (not departed_starters or (
            "departedStarterPositions" in report_html
            and "인선 공백 — 기존 선발 이탈" in report_html
        ))
    )
    if verbose:
        print(f"G11 현재 스쿼드 표시: 중복 {len(visible_dup)} · 산초 이탈 원장 "
              f"{'있음' if sancho_departed else '없음'} · 이탈 선발 공백 {len(departed_starters)} · "
              f"DEAD 숨김 {'✅' if ok11 else '⛔'}")
    if not ok11:
        fails.append("G11")

    # G12 — 수집된 경기 수치만 있고 해석·선수 역할·게임 반영 판단이 빠지는 회귀를 막는다.
    incomplete_reports = con.execute("""
        SELECT id FROM match_reports
        WHERE status='complete' AND (
          trim(title)='' OR trim(tactical_description)='' OR trim(tactical_features)=''
          OR trim(tactical_changes)='' OR trim(game_implications)=''
          OR trim(report_path)='' OR trim(source)='' OR trim(confidence)=''
        )""").fetchall()
    uncovered_report_players = con.execute("""
        SELECT mr.id,pm.player_id
        FROM match_reports mr
        JOIN player_matches pm ON pm.event_id=mr.event_id AND pm.team_code=mr.team_code
        LEFT JOIN match_player_reports mpr
          ON mpr.report_id=mr.id AND mpr.player_id=pm.player_id
        WHERE mr.status='complete' AND pm.minutes>0 AND mpr.player_id IS NULL""").fetchall()
    report_paths = con.execute("""
        SELECT id,report_path FROM match_reports WHERE status='complete'""").fetchall()
    missing_report_files = [rid for rid, path in report_paths if not (root / path).is_file()]
    missing_match_presets = con.execute("""
        SELECT mr.id
        FROM match_reports mr LEFT JOIN match_game_setups mgs ON mgs.report_id=mr.id
        WHERE mr.status='complete' AND (mgs.report_id IS NULL OR mgs.match_only!=1)
        UNION
        SELECT mr.id
        FROM match_reports mr LEFT JOIN match_player_prescriptions mpp
          ON mpp.report_id=mr.id AND mpp.starter=1
        WHERE mr.status='complete'
        GROUP BY mr.id HAVING COUNT(mpp.player_id)!=11""").fetchall()
    uncovered_match_prescriptions = con.execute("""
        SELECT mr.id,pm.player_id
        FROM match_reports mr
        JOIN player_matches pm ON pm.event_id=mr.event_id AND pm.team_code=mr.team_code
        LEFT JOIN match_player_prescriptions mpp
          ON mpp.report_id=mr.id AND mpp.player_id=pm.player_id
        WHERE mr.status='complete' AND pm.minutes>0 AND mpp.player_id IS NULL""").fetchall()
    # 경기 프리셋의 pos_label이 그 팀 slots 정본에 없으면 재현 피치의 x/y가 NULL이 되고
    # 선수 칩 11개가 전부 같은 자리에 겹쳐 그려진다(2026-08-25 실제 발생 — AVL 브라이턴전).
    # 두 경로로 깨졌다: ⑴ formation 문자열이 slots와 불일치 ⑵ pos_label 자체가 그 팀에 없음
    # (CHE 3-4-2-1에 LDM·RDM은 존재하지 않는다 — 그 팀엔 LCM·RCM이다, 불변규칙 7).
    # export는 ⑴을 기하 폴백으로 흡수하지만 ⑵는 흡수할 수 없다 — 여기서 잡는다.
    # 오픈플레이 xG는 전체 xG를 넘을 수 없다(전체 = 오픈플레이 + 세트피스 + PK, 모두 비음수).
    # 2026-08-25에 실제로 위반이 생겼다: xg_v는 경기 직후 수집분인데 xg_op_v를 나중에 채워
    # 스냅샷이 섞였고(CHE 풀럼전 1.96 > 1.70), 세트피스 xG가 -0.26이 됐다.
    # 밀도 검사와 달리 이 불변식은 임계값이 임의적이지 않아 게이트로 세울 수 있다.
    xg_openplay_violations = con.execute("""
        SELECT event_id, team_code FROM team_match_stats
        WHERE (xg_op_v IS NOT NULL AND xg_v IS NOT NULL AND xg_op_v > xg_v + 1e-9)
           OR (xg_op_o IS NOT NULL AND xg_o IS NOT NULL AND xg_op_o > xg_o + 1e-9)""").fetchall()
    # xG 값이 있으면 그 값이 어느 제공사·어느 스냅샷에서 왔는지 반드시 적혀 있어야 한다
    # (migration 025). 제공사별 절대값이 달라 provenance 없이 여러 경기를 집계하면 조용히 섞인다 —
    # 2026-09-06 축 검정에서 실제로 발현했다(obs#461·#463). 부등식 검사(위)는 이걸 잡지 못한다:
    # ATM 비야레알전은 xg_v가 SofaScore이고 xg_op_v가 FotMob인데 부등식은 깨지 않아 통과했다.
    xg_source_missing = con.execute("""
        SELECT event_id, team_code FROM team_match_stats
        WHERE xg_v IS NOT NULL AND (xg_source IS NULL OR trim(xg_source)='')""").fetchall()
    # 'MIXED:'는 이미 알려진 레거시 결함이라 실패시키지 않는다(값을 덮어쓰지 않기로 했다).
    # 대신 개수를 고정해 **새로 늘어나면 실패**시킨다 — 이게 드리프트를 막는 지점이다.
    xg_source_mixed = con.execute("""
        SELECT event_id, team_code FROM team_match_stats
        WHERE xg_source LIKE 'MIXED:%'""").fetchall()
    XG_MIXED_EXPECTED = 3   # ATM 말라가 · ATM 비야레알 · LIV 뉴캐슬 (2026-09-06 전수 분류)
    orphan_preset_roles = g12_role_group_orphans(con)
    orphan_preset_slots = con.execute("""
        SELECT mpp.report_id,mpp.pos_label
        FROM match_player_prescriptions mpp
        JOIN match_reports mr ON mr.id=mpp.report_id
        WHERE NOT EXISTS (SELECT 1 FROM slots s
                          WHERE s.regime_id=mr.regime_id AND s.pos=mpp.pos_label)""").fetchall()
    # draft라도 선수 행이 통째로 비면 경기 화면의 실측 평균위치·히트맵이 빈 피치가 된다.
    # core/export.py는 match_reports.players를 match_player_reports에서만 채우므로
    # (players 소스가 단일하다) 이 표가 비면 UI에서 조용히 사라진다 — obs#216의 회귀.
    # complete는 위에서 전원 커버를 따로 보므로, 여기서는 "비어 있지 않을 것"만 본다.
    playerless_reports = con.execute("""
        SELECT mr.id FROM match_reports mr
        WHERE EXISTS (SELECT 1 FROM player_matches pm
                      WHERE pm.event_id=mr.event_id AND pm.team_code=mr.team_code)
          AND NOT EXISTS (SELECT 1 FROM match_player_reports mpr
                          WHERE mpr.report_id=mr.id)""").fetchall()
    heatmap_html = (root / "site" / "heatmap.html").read_text()
    match_report_html = (root / "site" / "match-report.html").read_text()
    export_py = (root / "core" / "export.py").read_text()
    ok12 = (
        not incomplete_reports and not uncovered_report_players and not missing_report_files
        and not missing_match_presets and not uncovered_match_prescriptions
        and not playerless_reports and not orphan_preset_slots and not orphan_preset_roles
        and not xg_openplay_violations
        and not xg_source_missing
        and len(xg_source_mixed) <= XG_MIXED_EXPECTED
        and '대표 실측(시즌·유효 표본)' in heatmap_html
        # A(실측) 패널은 슬롯 좌표가 아니라 선수의 실제 평균 위치에 칩을 찍어야 한다.
        # 이 세 줄이 함께 있어야 export의 avg_positions가 화면까지 도달한다.
        and 'td.avg_positions' in heatmap_html
        and 'const toolPos' in heatmap_html
        and '"avg_positions": avg_positions' in export_py
        and 'id="matchReportSel"' in match_report_html
        and 'id="teamStats"' in match_report_html
        and 'id="matchPitch"' in match_report_html
        and 'playerStats(p)' in match_report_html
        and 'MATCH ONLY' in match_report_html
        and 'renderGamePreset(r)' in match_report_html
        and 'id="heatView"' in match_report_html
        # 경기 분석 메뉴는 초안도 노출하되 상태를 구분해야 한다(2026-08-16 결정).
        # 이 두 문자열이 사라지면 초안이 다시 안 보이거나, 보이되 완료본과 구별되지 않는다.
        and 'const isDraft' in match_report_html
        and '[초안]' in match_report_html
        and 'id="presetView"' in match_report_html
        and 'replaced_player_id' in match_report_html
        and "['match-report.html', '경기 분석']" in data_js
        and '"match_reports": match_reports' in export_py
    )
    if verbose:
        print(f"G12 경기 리포트: 불완전 {len(incomplete_reports)} · 선수행0 "
              f"{len(playerless_reports)} · 선수누락 "
              f"{len(uncovered_report_players)} · 원문누락 {len(missing_report_files)} · "
              f"경기프리셋누락 {len(missing_match_presets)} · 선수처방누락 {len(uncovered_match_prescriptions)} · "
              f"슬롯없는프리셋 {len(orphan_preset_slots)} · 역할군밖프리셋 {len(orphan_preset_roles)} · 오픈플레이xG모순 {len(xg_openplay_violations)} · "
              f"xG원천결손 {len(xg_source_missing)} · xG스냅샷혼합 {len(xg_source_mixed)}/{XG_MIXED_EXPECTED} "
              f"{'✅' if ok12 else '⛔'}")
    if not ok12:
        fails.append("G12")

    # G13 — 「조용한 이중화」. 검사식은 g13_checks()가 정본이다(회귀 테스트와 공유).
    g13 = g13_checks(con)
    ok13 = not any(g13.values())
    if verbose:
        summary = " · ".join(f"{G13_LABELS[k]} {len(v)}" for k, v in g13.items())
        detail = "" if ok13 else " ⛔ " + str({k: v[:3] for k, v in g13.items() if v})
        print(f"G13 조용한 이중화: {summary} {'✅' if ok13 else detail}")
    if not ok13:
        fails.append("G13")

    # G14 — 「원장 정정 규약」. 검사식은 g14_checks()가 정본이다(회귀 테스트와 공유).
    #   baseline은 HEAD의 db/dump다 — 이 게이트는 export→dump 前에 돌므로 「직전 커밋 정본」과 대조된다.
    g14_base = g14_baseline("HEAD")
    g14 = g14_checks(con, g14_base)
    if g14_base is not None:
        g14_base.close()
    ok14 = not any(g14.values())
    if verbose:
        summary = " · ".join(f"{G14_LABELS[k]} {len(g14[k])}" for k in G14_LABELS)
        detail = "" if ok14 else " ⛔ " + str({k: v[:3] for k, v in g14.items() if v})
        print(f"G14 원장 정정 규약: {summary} {'✅' if ok14 else detail}")
        if not ok14:
            print("    ⚠️ 정정은 새 obs 행으로 한다(불변규칙 2). 정당한 재작성이면 "
                  "G14_ALLOW_REWRITE=<table>:<id>,... 로 지정해 통과시킨다.")
    if not ok14:
        fails.append("G14")

    # G15 — 팀 설정 규칙 준수(core.team_settings · docs/20 「팀 설정 매핑 규칙」). 2026-09-08 신설.
    #   백필 결과 19행 중 규칙 일치 1 · 편차 14 · 스탯 결손 4 — 즉 지금까지의 설정값은 대부분 산문 판단이었다.
    #   이 게이트는 값을 강제하지 않고 **편차 신고**(rule_note 'DIVERGE: 사유')를 강제한다.
    g15 = g15_checks(con)
    ok15 = not any(g15.values())
    if verbose:
        summary = " · ".join(f"{G15_LABELS[k]} {len(v)}" for k, v in g15.items())
        detail = "" if ok15 else " ⛔ " + str({k: v[:3] for k, v in g15.items() if v})
        print(f"G15 팀 설정 규칙: {summary} {'✅' if ok15 else detail}")
    if not ok15:
        fails.append("G15")

    con.close()
    if verbose:
        print("✅ 게이트 전항 통과" if not fails else f"⛔ 실패: {fails}")
    return not fails


def json_str(v):
    import json as _json
    return _json.dumps(v, ensure_ascii=False)


def kernel_js_uri():
    return (Path(__file__).resolve().parent.parent / "site" / "assets" / "kernel.js").as_uri()


def g14_backtest(n):
    """최근 N커밋에 대해 G14 ⑴을 역검증한다(각 커밋을 그 부모와 대조) — 오탐률 확인용."""
    commits = _g14_sh(f"git log --format=%h -n {n}").split()
    print(f"G14 역검증: 최근 {len(commits)}커밋 (⑴ 원장재작성만)\n")
    flagged = 0
    for c in commits:
        cur, par = g14_baseline(c), g14_baseline(c + "^")
        if cur is None or par is None:
            continue
        hits = g14_checks(cur, par)["append_rewrite"]
        cur.close(); par.close()
        if hits:
            flagged += 1
            subj = _g14_sh(f"git log -1 --format=%s {c}").strip()[:56]
            print(f"  ❌ {c} 재작성 {len(hits):3d}  {subj}")
            for t, rid, fld, _o, _n in hits[:3]:
                print(f"        {t}#{rid}.{fld}")
    print(f"\n적발 커밋 {flagged} / {len(commits)}")


if __name__ == "__main__":
    if "--g14-backtest" in sys.argv:
        i = sys.argv.index("--g14-backtest")
        g14_backtest(int(sys.argv[i + 1]) if len(sys.argv) > i + 1 else 30)
        sys.exit(0)
    sys.exit(0 if run() else 1)

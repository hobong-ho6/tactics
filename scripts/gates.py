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

사용: python3 scripts/gates.py          (전체)
      from scripts.gates import run    (프로그램 내 호출)
"""
import sqlite3
import sys
import re
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

    # G9 — 생성 JSON과 UI가 어긋나는 캐시 회귀를 정적 검사한다.
    root = Path(__file__).resolve().parent.parent
    serve_py = (root / "scripts" / "serve.py").read_text()
    data_js = (root / "site" / "assets" / "data.js").read_text()
    ok9 = (
        'Cache-Control", "no-store' in serve_py
        and "cache: 'no-store'" in data_js
        and "searchParams.set('_', Date.now()" in data_js
        and "scripts/serve.py" in (root / "scripts" / "serve.sh").read_text()
    )
    if verbose:
        print(f"G9 프리뷰 최신성: 서버·JSON 캐시 우회 {'✅' if ok9 else '⛔'}")
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
        and not playerless_reports
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
              f"경기프리셋누락 {len(missing_match_presets)} · 선수처방누락 {len(uncovered_match_prescriptions)} "
              f"{'✅' if ok12 else '⛔'}")
    if not ok12:
        fails.append("G12")

    con.close()
    if verbose:
        print("✅ 게이트 전항 통과" if not fails else f"⛔ 실패: {fails}")
    return not fails


def json_str(v):
    import json as _json
    return _json.dumps(v, ensure_ascii=False)


def kernel_js_uri():
    return (Path(__file__).resolve().parent.parent / "site" / "assets" / "kernel.js").as_uri()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)

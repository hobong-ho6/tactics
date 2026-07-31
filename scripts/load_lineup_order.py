#!/usr/bin/env python3
"""2026-07-31 · SofaScore 라인업 배열순서 적재 (HANDOFF P0).

⑴ 왓킨스(555386)·캐시(833956)의 player_match_positions 행 신규 삽입
⑵ 기존 행에 lineup_order / formation / lineup_pos 채우기

포메이션 순서 규약(실측 검증): 배열은 GK → 각 라인을 **우→좌** 로 나열한다.
"""
import csv, sqlite3, sys

DB = 'data/avl_analysis.db'
SS = {833956: 2, 827679: 3, 96538: 5, 976263: 6, 923973: 8, 331737: 9, 250223: 10,
      1089388: 11, 826204: 12, 948261: 13, 783126: 14, 555386: 16, 930245: 18,
      1152923: 27, 996919: 28, 1398204: 30}

# (formation) -> index 0..10 의 슬롯 라벨. 각 라인 우→좌.
FORM = {
    '4-2-3-1': ['GK','RB','RCB','LCB','LB','RDM','LDM','RAM','CAM','LAM','ST'],
    '4-4-2':   ['GK','RB','RCB','LCB','LB','RM','RCM','LCM','LM','RST','LST'],
    '4-2-2-2': ['GK','RB','RCB','LCB','LB','RDM','LDM','RAM','LAM','RST','LST'],
    '4-3-3':   ['GK','RB','RCB','LCB','LB','RCM','CM','LCM','RW','ST','LW'],
    '3-4-2-1': ['GK','RCB','CCB','LCB','RM','RCM','LCM','LM','RAM','LAM','ST'],
    '3-4-3':   ['GK','RCB','CCB','LCB','RM','RCM','LCM','LM','RW','ST','LW'],
    '3-5-2':   ['GK','RCB','CCB','LCB','RM','RCM','CM','LCM','LM','RST','LST'],
    '5-4-1':   ['GK','RB','RCB','CCB','LCB','LB','RM','RCM','LCM','LM','ST'],
}

SRC = 'SofaScore API /event/{eid}/lineups players[] 배열순서 + /average-positions (2026-07-31)'
CONF_NEW = ('HIGH on minutes/rating/avg coords (API). lineup_order는 라인업 배열 인덱스 = 원천값이고 '
            '좌표 역산이 아니다. lineup_pos는 (formation, order) 파생 — 실측 y 레인과 대조 검증됨. '
            'pos_class는 minutes<45일 때 NULL(좌표 평균 신뢰불가).')

def pos_class_band(ax, ay, mins):
    """기존 행과 동일한 규약(0.4/0.6 레인 × 52 뎁스 밴딩)을 신규 행에도 적용."""
    if mins is None or mins < 45 or ax is None or ay is None:
        return None
    lane = 'right' if ay < 40 else ('left' if ay > 60 else 'centre')
    if ax < 52:
        return f'pivot-{lane}'
    return {'right': 'RM/AMR', 'left': 'LW/AML', 'centre': 'CAM'}[lane]

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # ── 이벤트 메타는 같은 경기의 기존 행에서 가져온다 (재수집 불필요)
    meta = {}
    for eid, season, date, opp, venue, comp, team in cur.execute(
            "SELECT event_id, season, date, opponent, venue, competition, team "
            "FROM player_match_positions GROUP BY event_id"):
        meta[eid] = (season, date, opp, venue, comp, team)

    order = {}   # (player_id, event_id) -> (order_idx, formation)
    for path in ('data/raw/2026-07-31_lineup_order.tsv',):
        with open(path) as f:
            for r in csv.DictReader(f, delimiter='\t'):
                order[(SS[int(r['ss_player_id'])], int(r['event_id']))] = (
                    int(r['order_idx']), r['formation'])

    # ── ⑴ 왓킨스·캐시 신규 삽입
    ins = upd_meta = skipped = 0
    with open('data/raw/2026-07-31_watkins_cash_positions.tsv') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            eid = int(r['event_id']); pid = SS[int(r['ss_player_id'])]
            if eid not in meta:
                print(f'  !! event {eid} 메타 없음 — 건너뜀', file=sys.stderr); skipped += 1; continue
            season, date, opp, venue, comp, team = meta[eid]
            g = lambda k: (float(r[k]) if r[k] else None)
            mins = int(r['minutes']) if r['minutes'] else None
            oi = int(r['order_idx'])
            started = 1 if oi >= 0 else 0
            form = r['formation']
            lo = oi if oi >= 0 else None
            lp = FORM.get(form, [None]*11)[oi] if oi >= 0 and oi < 11 else None
            ax, ay = g('avg_x'), g('avg_y')
            cur.execute("""INSERT OR IGNORE INTO player_match_positions
                (season, player_id, event_id, date, opponent, venue, competition, minutes, rating,
                 avg_x, avg_y, started, pos_class, source, confidence, team,
                 lineup_order, formation, lineup_pos)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (season, pid, eid, date, opp, venue, comp, mins, g('rating'),
                 ax, ay, started, pos_class_band(ax, ay, mins),
                 SRC.format(eid=eid), CONF_NEW, team, lo, form, lp))
            ins += cur.rowcount

    # ── ⑵ 기존 행에 lineup_order / formation / lineup_pos 채우기
    filled = nulled = 0
    for (pid, eid), (oi, form) in order.items():
        lp = FORM.get(form, [None]*11)[oi] if 0 <= oi < 11 else None
        if lp is None:
            nulled += 1
        cur.execute("""UPDATE player_match_positions
                       SET lineup_order=?, formation=?, lineup_pos=?
                       WHERE player_id=? AND event_id=? AND lineup_order IS NULL""",
                    (oi, form, lp, pid, eid))
        filled += cur.rowcount

    con.commit()
    print(f'삽입 {ins}행 · 순서 채움 {filled}행 · lineup_pos 미매핑 {nulled}건 · 메타없음 {skipped}건')
    con.close()

if __name__ == '__main__':
    main()

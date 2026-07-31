#!/usr/bin/env python3
"""2026-07-31 · 국면 분리(고점유/저점유) 그리드 집계 — obs#101.

`player_match_grids`(경기별 원시 카운트)를 `player_match_positions.lineup_pos`로
**포지션 필터**한 뒤 possession 중앙값으로 갈라 합산한다.
⚠️ 필터에 `pos_class`를 쓰면 포지션이 섞인다(obs#96 ② 자기정정 · obs#98) — 반드시 `lineup_pos`.
코사인은 스케일 불변이라 원시 카운트 합을 그대로 쓴다(정규화 불필요).
적합 산출은 브라우저에서 툴 `placedMap`·`cmpCos`로 한다(컨텍스트 노트 2).
"""
import sqlite3, json, statistics as st
con=sqlite3.connect('data/avl_analysis.db')
PAIRS=[(2,'RB',87),(16,'ST',50),(14,'LAM',14),(6,'LB',13),(10,'RAM',85),(8,'LDM',38),(8,'RDM',62),(12,'RDM',62)]
NAME={2:'캐시',16:'왓킨스',14:'부엔디아',6:'마첸',10:'맥긴',8:'오나나',12:'카마라'}
out={}
for pid,pos,x in PAIRS:
    rows=con.execute("""SELECT g.cells, g.possession FROM player_match_grids g
        JOIN player_match_positions m ON m.player_id=g.player_id AND m.event_id=g.event_id
        WHERE g.player_id=? AND m.lineup_pos=? AND g.possession IS NOT NULL""",(pid,pos)).fetchall()
    rows=[( [int(v) for v in c.split(',')], p) for c,p in rows]
    med=st.median([p for _,p in rows])
    def agg(sel):
        s=[0]*25
        for c,_ in sel:
            for i,v in enumerate(c): s[i]+=v
        return s
    hi=[r for r in rows if r[1]> med]; lo=[r for r in rows if r[1]<=med]
    key=f'{NAME[pid]}·{pos}'
    out[key]={'x':x,'n':len(rows),'median_poss':round(med,1),
              'all':agg(rows),'hi':agg(hi),'lo':agg(lo),
              'n_hi':len(hi),'n_lo':len(lo),
              'poss_hi':round(st.mean([p for _,p in hi]),1),'poss_lo':round(st.mean([p for _,p in lo]),1)}
print(json.dumps(out))

"""SofaScore 수집 헬퍼 — 브라우저 JS 스니펫 생성 + 응답 파서.

⚠️ API는 sofascore.com 오리진에서만 열린다 (curl은 UA/Referer 붙여도 403 — docs/30 ②).
   절차: 브라우저 탭을 https://www.sofascore.com/robots.txt (동일 오리진 경량 페이지)에
   띄우고 javascript_tool로 아래 스니펫을 실행한다. 홈에서 돌리면 라이브 스코어
   스크립트가 렌더러를 얼린다(레이트리밋 오진 주의).

⚠️ 스탯 0은 "키 생략"이다 (docs/30 ①) — 파서가 명시 0으로 확정해 기록한다.
"""
import json

__all__ = ["js_collect", "parse_collected", "STAT_FIELDS"]

# 브라우저에서 statistics 응답 → 파이프 직렬화할 필드 (순서 고정)
STAT_FIELDS = [
    ("minutes", "minutesPlayed"), ("rating", "rating"),
    ("xg", "expectedGoals"), ("xa", "expectedAssists"), ("key_passes", "keyPass"),
    ("pass_total", "totalPass"), ("pass_acc", "accuratePass"),
    ("duels_won", "duelWon"), ("duels_lost", "duelLost"),
    ("tackles", "totalTackle"), ("interceptions", "interceptionWon"),
    ("goals", "goals"), ("assists", "goalAssist"), ("touches", "touches"),
    ("recoveries", "ballRecovery"), ("shots_on", "onTargetScoringAttempt"),
    ("shots_total", "totalShots"), ("clearances", "totalClearance"),
    ("saves", "saves"),
]
FLOATS = {"rating", "xg", "xa"}


def js_collect(player_id, date_from, date_to, pages=2):
    """이 스니펫을 sofascore 오리진 탭에서 실행 → window.__RES에 수집,
    완료 후 window.__SER()로 파이프 직렬화 회수."""
    api_keys = ",".join(f"'{api}'" for _, api in STAT_FIELDS)
    return f"""
window.__RES=[]; window.__DONE=0; window.__DIAG={{pages:[],eventCount:0}};
window.__grid = hm => {{ const c=new Array(25).fill(0);
  for(const p of hm){{ let r=4-Math.floor(p.x/20), col=Math.floor((100-p.y)/20);
    r=Math.max(0,Math.min(4,r)); col=Math.max(0,Math.min(4,col)); c[r*5+col]++; }} return c; }};
(async () => {{
  const P={player_id}, KEYS=[{api_keys}];
  const evs=[];
  for (const pg of [...Array({pages}).keys()]) {{
    let j=null;
    try {{
      const r=await fetch(`/api/v1/player/${{P}}/events/last/${{pg}}`);
      window.__DIAG.pages.push({{page:pg,status:r.status}});
      if(r.ok) j=await r.json();
    }} catch(e) {{
      window.__DIAG.pages.push({{page:pg,status:null,error:String(e)}});
    }}
    if(!j) continue;
    for (const e of j.events) {{
      const d=new Date(e.startTimestamp*1000).toISOString().slice(0,10);
      if (d>='{date_from}' && d<='{date_to}')
        evs.push({{id:e.id, d, c:(e.tournament?.uniqueTournament?.name||e.tournament?.name),
          home:e.homeTeam?.name||'', away:e.awayTeam?.name||''}});
    }}
  }}
  window.__DIAG.eventCount=evs.length;
  for (let i=0;i<evs.length;i+=6) {{
    await Promise.all(evs.slice(i,i+6).map(async ev => {{
      try {{
        const [h,s,ap,lu]=await Promise.all([
          fetch(`/api/v1/event/${{ev.id}}/player/${{P}}/heatmap`).then(r=>r.ok?r.json():null),
          fetch(`/api/v1/event/${{ev.id}}/player/${{P}}/statistics`).then(r=>r.ok?r.json():null),
          fetch(`/api/v1/event/${{ev.id}}/average-positions`).then(r=>r.ok?r.json():null),
          fetch(`/api/v1/event/${{ev.id}}/lineups`).then(r=>r.ok?r.json():null)]);
        let ax=null, ay=null, side=null;
        if (ap) for (const sd of ['home','away']) {{
          const p=ap[sd]?.find(x=>x.player?.id===P); if(p){{ax=p.averageX;ay=p.averageY;side=sd;}} }}
        if(!side && lu) for (const sd of ['home','away']) {{
          if(lu[sd]?.players?.some(x=>x.player?.id===P)) side=sd; }}
        const lp=side&&lu?.[side]?.players?.find(x=>x.player?.id===P);
        const started=lp ? (lp.substitute?0:1) : '';
        const opponent=side==='home'?ev.away:(side==='away'?ev.home:'');
        const venue=side==='home'?'H':(side==='away'?'A':'');
        const st=s?.statistics||{{}};
        window.__RES.push([ev.id, ev.d, (ev.c||'').replace(/[|]/g,''),
          (opponent||'').replace(/[|]/g,''), venue, started, h?.heatmap?.length||0,
          s?.position||'', ax===null?'':Math.round(ax*100)/100, ay===null?'':Math.round(ay*100)/100,
          ...KEYS.map(k=>st[k]===undefined?'':st[k]),
          (h?.heatmap?window.__grid(h.heatmap):[]).join('.')].join('|'));
      }} catch(e) {{}}
    }}));
  }}
  window.__DONE=1;
}})();
window.__SER = () => window.__RES.join('\\n');
window.__DIAG_SER = () => JSON.stringify(window.__DIAG);
'started'
"""


def parse_collected(text):
    """window.__SER() 출력 → 행 dict 리스트 (player_matches 컬럼 사상)."""
    out = []
    for ln in text.strip().split("\n"):
        p = ln.split("|")
        old_len = 7 + len(STAT_FIELDS) + 1
        new_len = 10 + len(STAT_FIELDS) + 1
        if len(p) not in (old_len, new_len):
            raise ValueError(f"필드 수 불일치({len(p)}): {ln[:80]}")
        if len(p) == new_len:
            row = dict(event_id=int(p[0]), date=p[1], competition=p[2],
                       opponent=p[3] or None, venue=p[4] or None,
                       started=int(p[5]) if p[5] else None, hit_points=int(p[6]),
                       lineup_pos=p[7] or None,
                       avg_x=float(p[8]) if p[8] else None,
                       avg_y=float(p[9]) if p[9] else None)
            stat_start = 10
        else:  # 2026-08-13 이전 수집 문자열과의 호환
            row = dict(event_id=int(p[0]), date=p[1], competition=p[2],
                       opponent=None, venue=None, started=None, hit_points=int(p[3]),
                       lineup_pos=p[4] or None,
                       avg_x=float(p[5]) if p[5] else None,
                       avg_y=float(p[6]) if p[6] else None)
            stat_start = 7
        stats = {}
        for (name, _), raw in zip(STAT_FIELDS, p[stat_start:stat_start + len(STAT_FIELDS)]):
            if name in FLOATS:
                stats[name] = float(raw) if raw else None
            elif name in ("minutes",):
                stats[name] = int(raw) if raw else None
            else:
                stats[name] = int(raw) if raw else 0   # 키 생략 = 0 확정 (docs/30 ①)
        row.update(stats)
        row["cells"] = p[-1].replace(".", ",") if p[-1] else None
        row["stats_json"] = json.dumps(
            {k: v for k, v in stats.items() if v is not None}, ensure_ascii=False)
        out.append(row)
    return out

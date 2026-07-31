/* 전 조합 전수 계산 — HANDOFF P1 (obs#106, 2026-07-31)
 * 실행: localhost:8123 (툴)에서 이 파일 전체를 콘솔/javascript_tool에 붙여넣는다.
 *   ⚠️ 별도 구현 금지 규칙(컨텍스트 노트 2)에 따라 채점은 툴 자신의
 *   placedMap·cmpCos·roleOptions·pickFamiliar·funcAllows를 그대로 호출한다.
 *   __solveFor는 emerySolve의 C1~C6 로직을 sel 인자를 받도록 옮긴 것이다.
 * 규모: SQUAD_SLOTS 후보 전수 136,080 → 중복 선수 배제 후 42,972 라인업. 약 180ms.
 * 결과: window.__RANK (적합 평균 내림차순)
 */
window.__OPTC = {};                                  // 슬롯×선수 역할옵션 사전 계산 (36개 그리드)
for (const s of SQUAD_SLOTS) {
  window.__OPTC[s.pos] = {};
  for (const o of s.opts) {
    const g = sqGrid(s.pos, o.n);
    window.__OPTC[s.pos][o.n] = g ? roleOptions(s.pos, g).filter(x => funcAllows(o.n, x.role, x.f, s.t)) : [];
  }
}
window.__solveFor = function (sel) {
  const opt = window.__OPTC, warn = [], R = {};
  for (const p of ['GK','LCB','RCB','CAM','ST']) R[p] = pickFamiliar(sel[p], opt[p][sel[p]]);
  const oLM = opt['LM'][sel['LM']], oRM = opt['RM'][sel['RM']];
  const freeL = oLM.filter(o=>o.bank<0.01), bankL = oLM.filter(o=>o.bank>=EMERY_BANK_MIN);
  const freeR = oRM.filter(o=>o.bank<0.01), bankR = oRM.filter(o=>o.bank>=EMERY_BANK_MIN);
  const wide = [];
  if (freeL.length && bankR.length) wide.push({side:'L', LM:pickFamiliar(sel.LM,freeL), RM:pickFamiliar(sel.RM,bankR)});
  if (freeR.length && bankL.length) wide.push({side:'R', LM:pickFamiliar(sel.LM,bankL), RM:pickFamiliar(sel.RM,freeR)});
  if (!wide.length) warn.push('C1');
  wide.sort((a,b)=>(b.LM.s+b.RM.s)-(a.LM.s+a.RM.s));
  const W = wide[0]; if (W) { R.LM = W.LM; R.RM = W.RM; }
  const fbPick = (a,b) => { const A=opt[a][sel[a]], B=opt[b][sel[b]]; if(!A.length||!B.length) return null;
    let best=null;
    for (const x of A.slice(0,8)) for (const y of B.slice(0,8)) { if(!(x.fwd>y.fwd)) continue;
      const sc=x.s+y.s; if(!best||sc>best.sc) best={sc,x,y}; }
    return best; };
  const lAdv = fbPick('LB','RB'), rAdv = fbPick('RB','LB');
  const C6_BAND = 0.05, relSide = W ? W.side : null;
  let useL, c6applied = false;
  if (lAdv && rAdv && relSide && Math.abs(lAdv.sc-rAdv.sc) <= C6_BAND) {
    useL = (relSide === 'L');
    if ((useL?'L':'R') !== (lAdv.sc>=rAdv.sc?'L':'R')) c6applied = true;
  } else if (lAdv && (!rAdv || lAdv.sc>=rAdv.sc)) useL = true;
  else if (rAdv) useL = false;
  let fbSide = null;
  if (useL === true) { R.LB=lAdv.x; R.RB=lAdv.y; fbSide='L'; }
  else if (useL === false) { R.RB=rAdv.x; R.LB=rAdv.y; fbSide='R'; }
  else { warn.push('C2'); R.LB=opt['LB'][sel['LB']][0]; R.RB=opt['RB'][sel['RB']][0]; }
  const dlp = p => opt[p][sel[p]].filter(o=>o.role==='dm_dlp');
  const hold = p => opt[p][sel[p]].filter(o=>o.role==='dm_holding');
  const combos = [];
  if (dlp('LDM').length && hold('RDM').length) combos.push({t:'좌창조', LDM:dlp('LDM')[0], RDM:hold('RDM')[0]});
  if (hold('LDM').length && dlp('RDM').length) combos.push({t:'우창조', LDM:hold('LDM')[0], RDM:dlp('RDM')[0]});
  if (!combos.length) { warn.push('C3'); R.LDM=opt['LDM'][sel['LDM']][0]; R.RDM=opt['RDM'][sel['RDM']][0]; }
  else { combos.sort((a,b)=>(b.LDM.s+b.RDM.s)-(a.LDM.s+a.RDM.s)); R.LDM=combos[0].LDM; R.RDM=combos[0].RDM; }
  let bank4 = 0; for (const p of ['LM','CAM','RM','ST']) if (R[p]) bank4 += R[p].bank;
  const avg = SQUAD_SLOTS.reduce((a,s)=>a+(R[s.pos]?R[s.pos].s:0), 0) / 11;
  return { avg, R, warn, c6ok: !(W && fbSide && fbSide !== W.side), c6applied,
           wideSide: W?W.side:null, fbSide, bank4, piv: combos.length?combos[0].t:null };
};
(function enumerate() {
  const slots = SQUAD_SLOTS.map(s => ({pos:s.pos, names:s.opts.map(o=>o.n)}));
  const res = [], sel = {}, used = new Set();
  (function rec(i) {
    if (i === slots.length) {
      const r = window.__solveFor(sel);
      res.push({a:+r.avg.toFixed(4), s:Object.assign({},sel), w:r.warn.join(','),
                c6:r.c6ok?1:0, b4:+r.bank4.toFixed(2), wide:r.wideSide, fb:r.fbSide, piv:r.piv});
      return;
    }
    for (const n of slots[i].names) {
      if (used.has(n)) continue;                     // 중복 선수 배제
      used.add(n); sel[slots[i].pos] = n; rec(i+1); used.delete(n);
    }
  })(0);
  res.sort((x,y) => y.a - x.a);
  window.__RANK = res;
  console.log('라인업', res.length, '· 최고', res[0].a, '· 최저', res[res.length-1].a);
})();

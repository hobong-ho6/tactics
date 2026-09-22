/* 진화 경로의 **열림/닫힘 규칙** 정본 (2026-09-22 전수 조사에서 분리).

   ⛔⛔ 여기서만 정한다. 화면이 각자 판정하면 같은 경로가 어떤 메뉴에선 추천되고 어떤 메뉴에선
   사라진다 — 실제로 그랬다: `evolutions.html`은 소진·프리미엄을 걸렀는데 `player.html`의
   「진화 추천」은 `is_expired`만 봐서 **74건**을 그대로 1순위로 세우고 있었다
   (AVL만도 보가르드·부엔디아 프리미엄 경로, 지모알로바 소진 경로).
   evolutions.html 주석의 「세 탭이 같은 기준을 쓰게 한다」가 **네 번째 화면에는 닿지 않았다.**

   사용법:
     const R = evoRules(EVO, accountName);
     rows.filter(r => R.open(ids, pid) && (showPrem || !R.premium(ids)))

   ⚠️ `ids`는 그 경로의 **진화 id 배열**이다(`JSON.parse(row.evolution_ids)`).
   ⚠️ 카드 행 id(`club_player_id`)와 선수 id(`player_id`)는 다르다 — 섞으면 엉뚱한 선수에 붙는다. */

const J = (v, d) => { try { return JSON.parse(v ?? 'null') ?? d; } catch(e){ return d; } };

export function evoRules(EVO, accName){
  const C = EVO?.club || { accounts: [], players: [], log: [] };
  const acc = (C.accounts || []).find(a => a.name === accName) || (C.accounts || [])[0] || null;
  const own = Object.fromEntries((C.players || []).filter(p => !acc || p.account_id === acc.id).map(p => [p.id, p]));
  const repeat = {}; for (const c of EVO?.catalog || []) repeat[c.evo_id] = c.repeatability || 1;

  /* ⭐⭐ 세는 단위는 **적용 횟수(run)**이지 로그 행 수가 아니다(2026-09-20 정정).
     ⑴ 반복 배급은 4단계짜리라 한 번 적용해도 행이 4개 쌓인다 — 그대로 세면 1회가 4회가 된다. ⇒ **1단계 행만** 센다.
     ⑵ `is_void` 행은 세지 않는다(migration 053) — 적용된 적 없음이 실측으로 확인된 행이다. */
  const consumed = {};
  const applied = {};
  for (const l of C.log || []){
    const p = own[l.club_player_id]; if (!p || l.is_void) continue;
    if ((l.level ?? 1) === 1){
      (consumed[l.evo_id] ??= { count: 0, by: [] });
      consumed[l.evo_id].count++;
      consumed[l.evo_id].by.push({ name: p.name, pid: p.player_id, date: l.applied_at });
    }
    if (p.player_id == null) continue;
    const k = `${p.player_id}:${l.evo_id}`;
    const e = (applied[k] ??= { pid: p.player_id, evo_id: l.evo_id, name: l.evo_name, levels: [], done: false,
                                ovr_before: null, ovr_after: null, first: null, last: null });
    e.levels.push(l.level ?? 1);
    if (l.completed_at) e.done = true;
    if (e.ovr_before == null || (l.level ?? 1) === 1) e.ovr_before = l.ovr_before;
    e.ovr_after = l.ovr_after ?? e.ovr_after;
    e.first = e.first && e.first < l.applied_at ? e.first : l.applied_at;
    e.last = e.last && e.last > (l.completed_at || l.applied_at) ? e.last : (l.completed_at || l.applied_at);
  }
  for (const k in consumed) consumed[k].exhausted = consumed[k].count >= (repeat[k] ?? 1);
  for (const k in applied) applied[k].maxLevel = Math.max(...applied[k].levels);

  /* 프리미엄 시즌패스 — 판정 근거는 `unlock_text`의 「Premium Season Pass」다(이름의 `[SP+ N]`은 보조 신호). */
  const premIds = new Set((EVO?.catalog || [])
    .filter(c => /Premium Season Pass/i.test((c.unlock_text || '') + ' ' + (c.description || '')))
    .map(c => c.evo_id));

  return {
    acc, consumed, applied, premIds,
    /* 소진된 진화를 낀 경로는 **그 진화를 쓴 선수 본인 외** 모두에게서 닫힌다 */
    open: (ids, pid) => (ids || []).every(i => !consumed[i]?.exhausted || consumed[i].by.some(b => b.pid === pid)),
    premium: ids => (ids || []).some(i => premIds.has(i)),
    /* 이 경로에 들어 있는 진화 중 이 선수가 이미 밟은 것 */
    appliedIn: (ids, pid) => (ids || []).map(i => applied[`${pid}:${i}`]).filter(Boolean),
    idsOf: row => J(row?.evolution_ids, []) || [],
  };
}

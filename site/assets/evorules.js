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

/* ⭐⭐ 진화 로그 **한 행의 상태** 판정 정본 (2026-09-24 신설 — 사용자 지적 「마조 진화 완료했어 진화 진행중 아니야」).
   ⛔⛔ 화면이 각자 `!l.completed_at`만 보면 **무효 행이 「진행 중」으로 뜬다.** 실제로 그랬다:
   마조의 `Striker Glow Up [SP 7]`은 실측으로 「적용된 적 없음」이 확인돼 `is_void=1`인데
   `completed_at`이 NULL이라 카드가 계속 「진화 진행 중」이었다.
   ⭐ 같은 실수가 **두 번째**다 — 소진 계산에서 한 번(migration 053), 카드 뱃지에서 또 한 번.
      ⇒ 「조심하자」 대신 판정을 여기 한 곳에 두고 화면은 부르기만 한다(CLAUDE.md 불변규칙 13 ②). */
export const logState   = l => l.is_void ? 'void' : l.completed_at ? 'done' : 'progress';
export const inProgress = l => logState(l) === 'progress';

export function evoRules(EVO, accName){
  const C = EVO?.club || { accounts: [], players: [], log: [] };
  const acc = (C.accounts || []).find(a => a.name === accName) || (C.accounts || [])[0] || null;
  const own = Object.fromEntries((C.players || []).filter(p => !acc || p.account_id === acc.id).map(p => [p.id, p]));
  const repeat = {}; for (const c of EVO?.catalog || []) repeat[c.evo_id] = c.repeatability || 1;
  /* ⭐ 진화가 **몇 단계짜리인가** — 「완주」 판정에 쓴다(아래 `finished`). */
  const nLev = {};
  for (const c of EVO?.catalog || []) {
    try { nLev[c.evo_id] = (JSON.parse(c.levels || '[]') || []).length; } catch { nLev[c.evo_id] = 0; }
  }

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
  /* ⭐ **적용 횟수**는 로그 행 수가 아니라 «1단계 행 수»다 — 4단계짜리를 한 번 밟아도 행은 4개다
     (클럽 싱크 런북의 소진 계산과 같은 규약). 경로 투영이 「이미 밟은 만큼 건너뛰기」에 쓴다. */
  for (const k in applied) applied[k].runs = applied[k].levels.filter(v => (v ?? 1) === 1).length || 1;
  /* ⛔⛔ **`done`은 「완주」가 아니다**(2026-09-26 실측으로 드러났다). `done`은 「기록된 단계 중
     끝난 게 있다」는 뜻이라 **3단계짜리의 1단계만 끝내도 true**가 된다 — 그 상태로 「다음에 걸 수
     있는 진화」에서 통째로 빠져 **진행 중인 진화가 화면에서 사라졌다**(마조 × 최전방의 역설).
     ⇒ 완주는 **밟은 최고 단계가 카탈로그 단계 수에 닿았는가**로 가른다.
     ⚠️ 카탈로그에 단계 정보가 없으면(이월·미수집) 판정할 수 없으므로 종전대로 `done`을 쓴다. */
  for (const k in applied) {
    const a = applied[k], n = nLev[a.evo_id] || 0;
    a.finished = n ? (a.maxLevel >= n && a.done) : a.done;
    a.partial = a.done && !a.finished;          // 단계는 끝냈지만 진화는 남았다
  }

  /* ⛔⛔ **해금은 소진과 다른 축이고, 잠금이 세 종류다**(2026-09-23 사용자 지적
     「여전히 적용할 진화가 없는데 선수들이 노출되고 있음」).
       ⑴ `… level N in the Premium Season Pass.` — 프리미엄 구매 + 레벨 N
       ⑵ `… level N in the Standard Season Pass.` — 레벨 N (구매는 불필요)
       ⑶ 「Ted Lasso's Masterclass」·「Pep's Domination」 같은 **목표 완료**
     종전엔 ⑴만 걸러 ⑵⑶이 전 선수에게 「지금 걸 수 있는 진화」로 붙었다
     (Relentless [SP 11] · Creative or Composed? [SP 27] · Pinged Pass가 AVL 전원에게).
     ⚠️ 해금 여부는 **계정 상태**라 fut.gg가 주지 않는다 — `fut_accounts`·`fut_evolution_unlocks`(migration 060)가 정본.
     ⚠️ 레벨을 모르면(NULL) **「모름」으로 둔다** — 「해금됨」으로도 「잠김」으로도 단정하지 않는다(obs#132). */
  const spLevel = acc?.season_pass_level ?? null;
  const hasPrem = acc?.has_premium_pass === 1;
  const manual = {};
  for (const u of (EVO?.club?.unlocks || [])) if (!acc || u.account_id === acc.id) manual[u.evo_id] = !!u.unlocked;
  const lockInfo = {};
  for (const c of (EVO?.catalog || [])){
    const t = (c.unlock_text || '') + ' ' + (c.description || '');
    const m = /reaching level\s+(\d+)\s+in the\s+(Premium|Standard)\s+Season Pass/i.exec(t);
    let info = null;
    if (m){
      const need = +m[1], prem = /premium/i.test(m[2]);
      if (prem && !hasPrem) info = { locked: true, why: `프리미엄 시즌패스 미구매 (레벨 ${need} 필요)`, kind: 'prem' };
      else if (spLevel == null) info = { locked: true, unknown: true, why: `시즌패스 레벨 ${need} 필요 — 내 레벨을 모른다`, kind: 'sp' };
      else if (spLevel < need) info = { locked: true, why: `시즌패스 레벨 ${need} 필요 (지금 ${spLevel})`, kind: 'sp' };
    } else if (c.unlock_text && !/^Unlocked by/i.test(c.unlock_text)){
      /* 목표형 — 이름만 있고 조건식이 없다. 기록이 없으면 「모름」이다. */
      if (manual[c.evo_id] !== true)
        info = { locked: true, unknown: manual[c.evo_id] === undefined,
                 why: `목표 「${c.unlock_text}」 완료 필요`, kind: 'obj' };
    }
    if (manual[c.evo_id] === true) info = null;      // 사용자가 해금했다고 기록하면 그것이 이긴다
    if (info) lockInfo[c.evo_id] = info;
  }
  /* ⭐ 2026-09-23 사용자 지적 「진화 카탈로그의 필터 중에 (프리미엄) 시즌패스 필터가 없어졌어」 —
     잠금을 하나로 묶었더니 **프리미엄만 거르던 축**이 사라졌다. 둘은 성격이 다르다:
       · **프리미엄** = 돈을 내야 열리는 **구매 결정**(안 사면 영영 안 열린다)
       · **레벨·목표** = 플레이하면 열리는 **진행 상황**(시간이 지나면 열린다)
     ⇒ 집합을 갈라 내보내고 화면이 **따로 토글**한다. `premIds`는 「잠긴 것 전부」라 호출부 호환용으로 남긴다. */
  const premIds = new Set(Object.keys(lockInfo).map(Number));
  const premOnlyIds = new Set(Object.entries(lockInfo).filter(([, v]) => v.kind === 'prem').map(([k]) => +k));
  const progressIds = new Set(Object.entries(lockInfo).filter(([, v]) => v.kind !== 'prem').map(([k]) => +k));

  return {
    acc, consumed, applied, premIds, premOnlyIds, progressIds, lockInfo, spLevel, hasPrem,
    /* 소진된 진화를 낀 경로는 **그 진화를 쓴 선수 본인 외** 모두에게서 닫힌다 */
    open: (ids, pid) => (ids || []).every(i => !consumed[i]?.exhausted || consumed[i].by.some(b => b.pid === pid)),
    premium: ids => (ids || []).some(i => premIds.has(i)),
    /* 프리미엄 구매가 필요한 것 ↔ 플레이로 열리는 것 — 화면이 따로 거를 수 있게 나눠 준다. */
    premOnly: ids => (ids || []).some(i => premOnlyIds.has(i)),
    progressLocked: ids => (ids || []).some(i => progressIds.has(i)),
    /* 이 경로에 들어 있는 진화 중 이 선수가 이미 밟은 것 */
    appliedIn: (ids, pid) => (ids || []).map(i => applied[`${pid}:${i}`]).filter(Boolean),
    idsOf: row => J(row?.evolution_ids, []) || [],
  };
}

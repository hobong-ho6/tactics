// 경기 슬롯(RCB/RDM 등)과 EA 역할 숙련(CB/CDM)의 이름·포지션 연결 회귀.
import assert from 'node:assert/strict';
import { compareCards } from '../site/assets/clubviz.js';

const a = { name:'A', current_ovr:80, card_ovr:80, positions:'RB/CDM',
  current_attrs:JSON.stringify({ Pace:80 }), current_six:'{}',
  current_roles_plus:'[5,16]', current_roles_plus_plus:'[]' };
const b = { name:'B', current_ovr:80, card_ovr:80, positions:'RB/CDM',
  current_attrs:JSON.stringify({ Pace:70 }), current_six:'{}',
  current_roles_plus:'[]', current_roles_plus_plus:'[]' };
const ctx = {
  canon_roles:[
    { pos:'RB', role_id:'fb_wingback', focus:'Balanced' },
    { pos:'RDM', role_id:'dm_dlp', focus:'Roaming' },
  ],
  key_attrs:[
    { role_id:'fb_wingback', attr:'Pace', weight:1 },
    { role_id:'dm_dlp', attr:'Pace', weight:1 },
  ],
  role_map:[
    { game_version:'FC27', ea_id:5, kind:'plus', name:'Wingback', position_name:'RB' },
    { game_version:'FC27', ea_id:16, kind:'plus', name:'Deep-Lying Playmaker', position_name:'CDM' },
  ],
};
const html = compareCards(a, b, ctx);
for (const pos of ['RB', 'RDM']) {
  const start = html.indexOf(`<b>${pos}</b>`);
  assert(start >= 0, `${pos} 슬롯이 없음`);
  const end = html.indexOf('<div class="cmp-vrow">', start + 1);
  const row = html.slice(start, end < 0 ? undefined : end);
  assert(row.includes('<span class="chip wA">Role+</span>'), `${pos} Role+ 누락`);
}
const unknown = compareCards({ ...a, current_roles_plus:undefined,
  current_roles_plus_plus:undefined }, b, ctx);
assert(unknown.includes('미수집') && unknown.includes('확인 불가'), '결손을 숙련 없음으로 오표시');
console.log('카드 비교 RB/RDM 역할 숙련: ✅');

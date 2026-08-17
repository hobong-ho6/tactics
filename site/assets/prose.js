/* DB 서사 렌더러 — player_duties·player_evaluations의 긴 산문을 끊어 읽을 수 있게 만든다.
   DB가 이미 쓰고 있는 표기를 그대로 읽는다: **강조** · ⭐⚠️⛔ 판정 마커 · ⑴⑵⑶ 열거 ·
   앞머리 [obs#·날짜] 태그 · 앞머리 'HIGH —' 등급 · ' | ' 와 줄바꿈의 블록 구분.
   ⚠️ 값은 고치지 않는다 — 끊어 읽는 지점만 만든다. 원문에 없는 강조·순서를 만들지 않는다.
   글리프 색은 폰트가 정하므로(⭐⚠️⛔는 color가 듣지 않는다) 심각도는 블록 왼쪽 띠로 표시한다. */

import { annotate } from './glossary.js';

const esc = s => String(s ?? '').replace(/[&<>"]/g,
  c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const MARKER = /⭐+|⚠️|⚠|⛔/g;
const sev = m => m.startsWith('⭐') ? 'hi' : m === '⛔' ? 'bad' : 'warn';
/* 앞머리 등급 — adherence·overall·fit_* 가 'MEDIUM-HIGH — 서술' 꼴로 시작한다 */
const GRADE = /^(HIGH|MEDIUM-HIGH|MEDIUM-LOW|MEDIUM|LOW|[SABCD][+-]?)\s*—\s*/;
const TAG = /^\[([^\]]{1,70})\]\s*/;
const ENUM = /[⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽]/;

/* 마커 앞에서 끊는다. 첫 조각은 마커가 없다(mark=''). ⭐⭐는 한 마커로 묶는다. */
function split(text){
  const out = [];
  let last = 0, mark = '', m;
  MARKER.lastIndex = 0;
  while ((m = MARKER.exec(text))){
    out.push({ mark, body: text.slice(last, m.index) });
    mark = m[0];
    last = m.index + m[0].length;
  }
  out.push({ mark, body: text.slice(last) });
  return out.filter(b => b.body.trim());
}

const bold = s => s.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');

/* 블록 본문 — 앞머리 태그·등급을 칩으로 빼고, ⑴⑵⑶ 열거는 줄로 분리한다 */
function body(raw){
  let t = raw.trim(), head = '';
  const tag = t.match(TAG);
  if (tag){ head += `<span class="ptag">${bold(tag[1])}</span>`; t = t.slice(tag[0].length); }
  const grade = t.match(GRADE);
  if (grade){ head += `<span class="badge pgrade">${grade[1]}</span>`; t = t.slice(grade[0].length); }

  if (!ENUM.test(t)) return head + bold(t);
  const parts = t.split(/(?=[⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽])/);
  // ⑴이 **강조** 안에 들어간 원문이 있다(예: '**⑴ 출처가 브레스트 시절 ⑵ 3티어**').
  // 거기서 끊으면 강조가 쪼개져 * 가 화면에 남는다 — 그런 블록은 줄만 안 나눈다.
  if (parts.some(p => (p.match(/\*\*/g) || []).length % 2)) return head + bold(t);
  const lead = bold(parts.shift().trim());
  return head + lead + parts.map(p =>
    `<span class="pi"><b class="pn">${p[0]}</b>${bold(p.slice(1).trim())}</span>`).join('');
}

/* 긴 DB 산문 → 구조화 HTML. 짧은 인라인 문구는 그대로 annotate()를 쓴다. */
export function prose(text){
  const src = String(text ?? '').trim();
  if (!src) return '';
  const chunks = esc(src).split(/\s*\|\s*|\n+/).filter(x => x.trim());
  const html = chunks.flatMap(split).map(b =>
    `<p class="pb ${b.mark ? sev(b.mark) : 'plain'}">${
      b.mark ? `<span class="pm">${b.mark}</span>` : ''}${body(b.body)}</p>`).join('');
  return `<div class="prose">${annotate(html)}</div>`;
}

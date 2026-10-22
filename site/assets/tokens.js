/* 디자인 토큰 읽기 — 캔버스처럼 CSS var()를 직접 못 쓰는 곳의 **단일 경로** (2026-10-22 라이트 스킴).
   ⛔ JS에 색을 하드코딩하지 않는다 — 값은 theme.css :root(다크) / html[data-theme="light"] 한 곳에만 있다(불변규칙 13 ②).
   SVG 문자열은 fill="var(--token)"을 그대로 쓰면 되고(스킴이 바뀌면 브라우저가 알아서 다시 칠한다),
   <canvas>만 그릴 때 cssVar()로 읽는다. 캔버스는 스킴이 바뀌어도 다시 안 그려지므로
   onSchemeChange()가 페이지를 새로 고친다(모든 페이지 공통 · data.js mountHeader가 등록). */

export function cssVar(name, el = document.documentElement){
  const v = getComputedStyle(el).getPropertyValue(name).trim();
  if (!v) throw new Error(`디자인 토큰 없음: ${name} — theme.css :root에 추가할 것`);
  return v;
}

const MQ = typeof matchMedia === 'function' ? matchMedia('(prefers-color-scheme: light)') : null;
/* ⭐ 스킴은 <html data-theme>가 정본이다(theme-boot.js — 사용자 토글 · 2026-10-22). 기기 설정은 「자동」일 때만 따른다. */
export const isLightScheme = () => document.documentElement.dataset.theme === 'light';

/* 스킴 전환 시 콜백 — 기본은 새로 고침(캔버스 재렌더 비용이 페이지마다 달라 한 가지 규칙으로 통일).
   URL 상태(?event= · ?id=)는 남고, 셀렉트·탭 선택은 초기화된다(스킴 전환은 세션 중 드문 일이라 감수). */
export function onSchemeChange(cb = () => location.reload()){
  if (!MQ || MQ.__tacticsBound) return;
  MQ.__tacticsBound = true;
  /* 자동일 때만 기기 설정 변화를 따른다 — 라이트/다크를 직접 고른 사람에게는 기기가 바뀌어도 그대로 둔다 */
  MQ.addEventListener('change', () => { if ((document.documentElement.dataset.themePref || 'auto') === 'auto') cb(); });
}

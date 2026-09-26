-- 076 진화의 한국어 이름·설명·과제 (2026-09-26 사용자 질문 「진화의 한글명도 수집할 수 있어?」 → 가능)
--
-- 어디서: futmind.com이 **EA 공식 현지화 19개 언어**를 그대로 노출한다(`locales.names/descriptions`).
--   `https://futmind.com/api/evolutions` → [{ locales:{names:{en,ko,ja,…}, descriptions:{…}}, levels:[{objectives:[{locales:…}]}] }]
--   실증: Frontline Paradox = 「최전방의 역설」 · ST Roles++ = 「ST 역할++」.
--
-- ⛔⛔ **조인 키가 영문명뿐이다.** futmind의 id(2730)와 fut.gg의 evo_id(2508)는 **다른 체계**다.
--    불변규칙 6은 라벨 조인을 금하지만 여기는 **사람·팀·체제가 아니라 카탈로그 항목**이고
--    다른 키가 존재하지 않는다. ⇒ 영문명으로 잇되 ⑴ 중복 0을 확인하고(2026-09-26: 0건)
--    ⑵ fut.gg가 붙이는 접미 `[SP 7]`·`[SP+ 14]`를 떼고 맞추며 ⑶ 못 맞춘 것은 **NULL로 둔다**(추측 금지).
-- ⚠️ futmind 목록은 **24종**이라 시즌패스·목표 해금형 9종이 빠진다(fut.gg 목록 화면이 해금형을
--    감추던 것과 같은 현상). 그 9종의 한글명은 **없는 채로 둔다** — 지어내지 않는다.
-- ⚠️ 이 값은 **EA 현지화 추정**이다(등급 B) — futmind가 EA 원본이라 밝힌 적은 없다.
ALTER TABLE fc_evolutions ADD COLUMN name_kr TEXT;
ALTER TABLE fc_evolutions ADD COLUMN description_kr TEXT;

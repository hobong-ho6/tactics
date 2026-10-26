-- 126 진화의 fut.gg doNotGenerate (2026-10-26 사용자 지적 「Anticipate 이것도 다시 확인해봐 내 진화 목록에는 없어」).
--
-- 왜: Anticipate(2629)·Pinged Pass(2630)·Shadow Striker++(2621)·Batigol Precision(2624)은 해금 문구·코인·포인트·토큰이 전부 비어
--   「진화 랩에서 바로 시작 (무료)」로 떴는데, 사용자 인게임 진화 랩에 없다(Anticipate 확인).
--   fut.gg 객체의 `doNotGenerate`(경로 생성 제외)가 갈랐다 — 2026-10-26 현행 카탈로그 44종 대조(C · 통제 대조):
--     true  = 시즌패스·과제·토큰 해금형 전부 + Roles++·배지 + 위 4종
--     false = 진화 랩에 열린 것 전부(Witching Hour·Creep Inside·Center Spectre·Intro 3종·Future Stars Academy 4종 등 15종)
--   ⇒ 「해금 문구·비용 없음 + doNotGenerate」 = 진화 랩에 없고 얻는 경로를 fut.gg가 주지 않는다(과제·SBC·토큰 스토어 검색 0 · 2026-10-26).
-- 쓰기: scripts/collect_futgg_evolutions.py catalog_row(do_not_generate). 아래 UPDATE는 새 칸을 오늘 관측값으로 채운다(나머지 20종은 관측 못 함 = NULL).
ALTER TABLE fc_evolutions ADD COLUMN do_not_generate INTEGER;   -- fut.gg doNotGenerate · 1/0 · NULL = 미관측
UPDATE fc_evolutions SET do_not_generate=1 WHERE game_version='FC27' AND pulled='2026-10-26' AND evo_id IN (2493, 2494, 2496, 2498, 2499, 2509, 2512, 2513, 2514, 2515, 2518, 2547, 2558, 2605, 2606, 2607, 2608, 2609, 2610, 2611, 2615, 2616, 2620, 2621, 2622, 2623, 2624, 2629, 2630);
UPDATE fc_evolutions SET do_not_generate=0 WHERE game_version='FC27' AND pulled='2026-10-26' AND evo_id IN (2488, 2490, 2492, 2541, 2549, 2551, 2557, 2561, 2562, 2602, 2603, 2604, 2631, 2632, 2636);
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-26', '126-evo-do-not-generate',
  'fc_evolutions.do_not_generate — fut.gg doNotGenerate · 44종 관측(true 29 · false 15) · 해금 문구·비용 없음+true = 진화 랩에 없음·경로 미상(Anticipate·Pinged Pass 2630·Shadow Striker++·Batigol Precision) · 화면 「무료」 오표기 수정');

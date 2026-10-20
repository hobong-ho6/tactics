-- 113 영상 구현 주장 「헤드라인 + 요점」 (2026-10-20 사용자 지시 「40자가 넘는 구현 주장은 필요 내용만 요약해도 되지만
--     긴 내용을 어떻게 잘 전달할 수 있을지 검토하거나 검색해서 개선」).
--
-- 근거(NN/g): 화면 글은 대부분 훑어 읽고 시선은 문장 앞 몇 단어에 머문다 → ① 결론을 앞에 둔 짧은 헤드라인(front-load)
--   ② 긴 내용은 덩어리(chunk)로 나눈 요점 목록 ③ 전문은 필요할 때 펼친다(progressive disclosure).
-- ⛔ value_kr(한국어 전문)은 고치지 않는다 — 헤드라인·요점은 그 위에 얹는 읽기 층이다(불변규칙 2).
ALTER TABLE video_impl_claims ADD COLUMN headline_kr TEXT;   -- ≤40자 · 결론 먼저
ALTER TABLE video_impl_claims ADD COLUMN points_kr TEXT;     -- JSON 배열 · 2~5개 · 항목당 ≤30자 안팎
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-20', '113-claims-headline',
  'video_impl_claims.headline_kr·points_kr — 40자 초과 자유 문구 주장 24행 백필 · 화면은 헤드라인 굵게 + 요점 목록 + 전문 툴팁 · write_video_summary·G17이 40자 초과 시 필수로 막음');

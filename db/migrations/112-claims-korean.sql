-- 112 영상 구현 주장 한국어 칸 (2026-10-20 사용자 지적 「지시·운용에 보면 한국어 번역이 없어」 · 불변규칙 11).
--
-- 왜: instruction·limit·team_axis 축의 field·value가 요약 작성자의 영어 자유 문구(defensive_shape_first_half …)라
--   화면(labels.js claimLabel)이 영어 그대로 찍었다. 원문은 고치지 않고(추가만) 한국어 칸을 더한다 —
--   화면은 *_kr를 기본으로, 원문은 툴팁으로. write_video_summary.py가 이 세 축에서 *_kr 없는 적재를 거부하고 G17이 결손 0을 지킨다.
ALTER TABLE video_impl_claims ADD COLUMN field_kr TEXT;
ALTER TABLE video_impl_claims ADD COLUMN value_kr TEXT;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-20', '112-claims-korean', 'video_impl_claims.field_kr·value_kr — 지시·운용/재현 한계/팀 설정 축 한국어 표기(사용자 지적 2026-10-20) · 144행 백필');

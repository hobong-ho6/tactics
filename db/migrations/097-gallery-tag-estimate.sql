-- 097 갤러리 태그 보너스 추정 (2026-10-03 사용자 지시 「태그로 인해 점수를 더 얻는 부분을 분석하고 갤러리 시스템에 반영」)
-- 분석·근거는 core/gallery.py 머리말(fut.gg 조합 347개 재현 · 오차 중앙값 −1.3%).
-- base_score·grade = 기본 점수만(확정 하한) · est_score·est_grade = 태그 포함 추정 · tag_detail = {태그: [개수, %, 보너스]}.
ALTER TABLE fut_gallery_eval ADD COLUMN est_score INTEGER;
ALTER TABLE fut_gallery_eval ADD COLUMN est_grade TEXT;
ALTER TABLE fut_gallery_eval ADD COLUMN tag_detail TEXT;

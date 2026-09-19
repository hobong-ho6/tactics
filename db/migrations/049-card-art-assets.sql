-- 049 카드 합성용 자산 (2026-09-19, 사용자 제안 「카드별 배경 템플릿을 구해서 선수 이미지와 스탯을 직접 넣는 식으로」)
-- 진화 카드는 결과 이미지가 없어 기본 아트를 덮어 쓰다 보니 인쇄 수치와 충돌했다.
-- fut.gg는 **스탯·이름이 없는 「심플 카드」**와 **배경 없는 선수 렌더**를 따로 준다 — 그것으로 합성한다.
ALTER TABLE player_card_items ADD COLUMN simple_card_url TEXT;   -- 스탯·이름 없는 카드(OVR·포지션·엠블럼만 인쇄)
ALTER TABLE player_card_items ADD COLUMN render_url TEXT;        -- 선수 렌더(배경 투명)

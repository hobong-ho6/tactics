-- 008 · 슬롯별 전술 정본 세트 — 인선 무관 "감독 전술 그 자체"의 게임 값 (2026-08-12)
--
-- 사용자 요구: "스쿼드의 선수 구성과 상관없이 이게 딱 에메리의 전술을 게임에 구현한 값이다
--              하는 세트도 필요해".
--
-- 왜 필요한가: 지금까지 슬롯 역할은 인선(커널 적합) 프리셋이 대신해 왔다. 그래서
--   "감독 요구 ≠ 선수 적합"인 칸(예: 고메스 LDM dm_dlp/Roaming — 기능축은 dm_holding)에서
--   manager_profiles 산문과 프리셋이 충돌한다. 이 테이블이 생기면 두 층이 분리된다:
--     정본(이 테이블)   = 감독이 요구하는 슬롯 임무의 게임 번역 — 선수 무관
--     프리셋(prescriptions fc26:opt:*) = 현 인선으로 정본에 가장 가깝게 가는 근사
--   프리셋이 정본과 다르면 그 칸은 "편차 + 이유"로 읽는다.
--
-- 팀 세팅 층(포메이션·빌드업·수비·라인)은 이미 선수 무관 정본이 있다 —
--   team_tactic_setups kind='optimal'(+상황 변형 4종). 이 테이블은 그 짝인 슬롯 역할 층.
--
-- 근거는 manager_profiles(regime 1) 12축의 ⚙️게임 구현 노트 + docs/10. v1의
--   SLOT_EMERY_ROLE(archive/v1/fc26-heatmap.html 하드코딩)의 v2 승계이기도 하다.

CREATE TABLE slot_canon_roles(
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  formation TEXT NOT NULL,
  pos TEXT NOT NULL,                -- slots.pos와 동일 키
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  role_id TEXT NOT NULL,
  focus TEXT NOT NULL,
  rationale TEXT,                   -- 어느 축·obs에서 왔는지
  source TEXT, confidence TEXT,
  updated TEXT,
  PRIMARY KEY(regime_id, formation, pos, game_version),
  FOREIGN KEY(regime_id, formation, pos) REFERENCES slots(regime_id, formation, pos),
  FOREIGN KEY(game_version, role_id) REFERENCES game_roles(game_version, role_id)
);

INSERT INTO slot_canon_roles VALUES
(1,'4-2-3-1 Wide','GK','FC26','gk_goalkeeper','Defend',
 '5-2 빌드업 참여는 후방 패스 옵션이지 전진 스위핑이 아니다(obs#154 — 스위퍼 아님, 실측 .961). buildup·implementation ⑴.',
 'manager_profiles(1) implementation·buildup + obs#154','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','LCB','FC26','cb_bpd','Build-Up',
 'CB 비대칭의 전개측 — 좌 하프스페이스로 캐리·패스해 전진(player_duties id=4 "confirmed unambiguously"). 두 CB 동시 Aggressive는 rest-defense 붕괴(obs#13)이므로 비대칭 자체가 구조다(obs#33).',
 'obs#33·obs#13 + player_duties id=4 + docs/10','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','RCB','FC26','cb_bpd','Aggressive',
 'CB 비대칭의 압박측 — 볼을 갖고 우측 중앙으로 step out(player_duties id=3). 기능축 실측도 갈린다(인터셉트 2.0·패스 96% 압박형). 몸 던지는 태클 금지는 팀 태클 세팅(Conservative)이 담당.',
 'obs#33 + player_duties id=3 + docs/10','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','LB','FC26','fb_att_wb','Support',
 'C2 풀백 비대칭의 전진측 — 풀백은 한 번에 한 명만 전진(rest_defense). 같은 역할을 양쪽에 주면 C2 붕괴(obs#110, Δ.0101 지불 근거). 좌측 폭은 이 칸이 댄다(와이드는 안쪽 이동).',
 'manager_profiles(1) implementation ⑷·rest_defense + obs#110','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','RB','FC26','fb_wingback','Balanced',
 'C2 풀백 비대칭의 잔류·수비 기여측(role_demands ⑵ — 캐시 수비 기여 154회). role_demands ⚙️③: 더 보수적인 방향의 근거는 있으나 커널 판정 없이 바꾸지 말 것.',
 'manager_profiles(1) implementation ⑷·role_demands','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','LDM','FC26','dm_holding','Roaming',
 '더블 피벗은 자리 유지가 1차 임무(그 대가로 풀백 전진이 성립 — rest_defense). implementation ⑵의 "dm_holding(Roaming/Defend 분담)" 중 제한적 전진측. ⚠️ 좌/우 어느 쪽이 Roaming인지는 인선층 판단이다(카마라 서사 "기회 나면 길게 전진"은 우측 열중심 62.3과 긴장) — 현 XI 배치(오나나 LDM Roaming)를 따랐다.',
 'manager_profiles(1) implementation ⑵·rest_defense·role_demands ⑶','MEDIUM-HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','RDM','FC26','dm_holding','Defend',
 '더블 피벗의 앵커측 — 잔류 구조의 핵심(역습 실점 0의 기반). 하나라도 전진형 롤이면 잔류 구조가 무너진다(rest_defense ⚙️⑵).',
 'manager_profiles(1) implementation ⑵·rest_defense','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','LM','FC26','wm_wideplm','Attack',
 '와이드는 안쪽으로 들어오고 폭은 풀백이 댄다(role_demands ⑸) — 좌측은 LB가 전진측이므로 LM은 안쪽 창조형. ⚠️ implementation ⚙️ 산문에 좌측 와이드 명시가 없어 role_demands에서 도출 — 11칸 중 산문 근거가 가장 약한 칸. 현 XI(부엔디아 wm_wideplm/Attack)와 일치.',
 'manager_profiles(1) role_demands ⑸','MEDIUM','2026-08-12'),
(1,'4-2-3-1 Wide','CAM','FC26','cam_playmaker','Roaming',
 '자유 10번 — 수비 시 ST 옆 4-4-2 앞줄 합류(팀 압박 세팅이 담당), 공격 시 라인 사이 주머니(role_demands ⑴). implementation ⑸의 원칙값. 만잠비 cam_halfwinger는 인선 변형이지 정본이 아니다.',
 'manager_profiles(1) implementation ⑸·role_demands ⑴','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','RM','FC26','wm_widemid','Support',
 '미드블록 뱅크 복귀의 게임 대응 — EA 정의 "복귀해 수비 지원"(implementation ⑵). 안쪽 이동·컷인은 역할이 아니라 PlayStyles 층(role_demands ⚙️④).',
 'manager_profiles(1) implementation ⑵·role_demands ⑸','HIGH','2026-08-12'),
(1,'4-2-3-1 Wide','ST','FC26','st_advanced','Versatile',
 '좌우 채널로 흘러다니며 전환 시 즉시 출구(role_demands ⑹ — 왓킨스형 임무). Versatile 포커스가 채널 이동을 담당.',
 'manager_profiles(1) role_demands ⑹','MEDIUM-HIGH','2026-08-12');

INSERT INTO observations VALUES(193, 1, '2025-26', 'verdict',
 'obs#193 · 슬롯별 전술 정본 세트 신설(slot_canon_roles, 008) — 인선 무관 "에메리 전술 그 자체"의 FC26 번역 11칸. 정본 vs 인선 프리셋(fc26:opt:*)의 편차 예시: LDM 정본 dm_holding/Roaming vs 고메스 처방 dm_dlp/Roaming(울브스 그리드 적합 .789 우선, 기능축 포기 명기) / CAM 정본 cam_playmaker/Roaming vs 만잠비 cam_halfwinger(인선 변형).',
 'manager_profiles(1) 12축 ⚙️게임 구현 노트 + docs/10 + obs#13·#33·#110·#154. 팀 세팅 층 정본은 team_tactic_setups kind=optimal(+변형 4종)이 기존 보유.',
 '사용자 요구(2026-08-12) — 스쿼드 무관 정본 세트',
 'HIGH(8칸 산문 직접 명시) / MEDIUM-HIGH(LDM Roaming측·ST) / MEDIUM(LM — 산문 유일 공백, role_demands ⑸ 도출)');

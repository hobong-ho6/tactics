# 시스템 개요 — 실축→FC 구현 플랫폼 v2 (2026-08-11 재설계)

**목적**: 실제 축구(감독·팀 페어의 전술)를 FC 게임(FC26 → FC27…)상에서 구현한다.
대상: **에메리·아스톤 빌라(주)**, 알론소·첼시, 이라올라·리버풀. v1 설계는 `data/DESIGN.md`(구본).

## 데이터 흐름 — 손편집 지점 0

```
SofaScore(브라우저 오리진 수집) ─┐
sofifa / EA 피치노트 ────────────┤→  db/tactics.db  →  scripts/export.py  →  site/data/*.json  →  site/*.html
transfer-watch(스킬) ────────────┘        ↑                (게이트 통과 필수)
                                   scripts/gates.py = 정본성 보증 (G1~G12)
```

## 레이어 (db/migrations/001-schema.sql이 스키마 정본)

| 레이어 | 테이블 | 성격 |
|---|---|---|
| 축 | game_versions · regimes(감독·팀 페어) · teams · players(sofascore/sofifa id 컬럼) · seasons | 1급 엔티티 |
| 실세계(사실) | matches · **player_matches**(구 appearances+grids+positions 통합) · team_match_stats | team_code+date로 자명 |
| 경기 해석 | **match_reports** · **match_player_reports** · reports/match-watch 원문 | event_id+team_code로 사실층과 연결 |
| 지식 | observations(obs# 전역 연속) · manager_profiles(11축) · player_duties | 관찰·판단 기록 |
| 게임(버전별) | game_roles/…focus(커널 85)/…variants(변형 217) · player_game_stats(로스터 스냅샷) · **game_system_changes**(FIFA→FC 변천) | 버전 추가 = 행 추가 |
| 매핑(판단) | slots(regime 기하) · prescriptions(정형 필드: fit_sim/sample_n/avg_rating) · squad_entries(player_id FK) · team_tactic_setups | regime_id 명시 |
| 이적 | transfer_targets/outgoing/ledger | transfer-watch 스킬이 기록 |

## 게이트 (`python3 scripts/gates.py`) — 모든 DB 쓰기의 선행 조건

G1 커널 정합 37/85/217 · G2 인코딩 회귀(전 그리드 cells→map25) · G3 커널 앵커 6항
(캐시 measured:season RM **.835** 독립앵커 · 하지무사 **.821** 상수 그리드 · Jackson **.724**(28경기) ·
만잠비 CAM .861 · 가르나초 LM .771 · 알리송 RM .833) · G4 집계 공식 재현(만잠비 national 12경기) ·
G5 JS 커널 동치(site/assets/kernel.js ↔ core/kernel.py, node) · G6 DB FK 정합 ·
G7 appearances 병합 앵커 · G8 공통 슬롯 후보 풀(중복·도달불가·이적누락 0) ·
G9 프리뷰 최신성(no-store 서버 + JSON 캐시 우회) · G10 영상 레퍼런스(source 결손 0 + 기본 닫힘 UI) ·
G11 현재 스쿼드 표시(확정 이탈·이적 후보·DEAD 숨김) ·
G12 경기 리포트(필수 섹션·수집 선수 전원·원문·경기 분석 메뉴·MATCH ONLY 팀 설정/선발 11명 연결).

## 핵심 규약 (v1 교훈의 성문화 — 위반이 실제 사고를 냈던 것들)

1. **인코딩**: half-up + 9클램프 (`core/encode.py`). 파이썬 `round()`는 banker's라 금지 —
   v1에 두 세대가 섞였고 마이그레이션에서 112행을 정규화했다. `cells`가 무손실 원자료.
2. **커널**: 정본은 DB(`game_role_variants`). placedMap = 슬롯 x 최근접 변형 그대로(obs#94).
   **역할군 필터 필수**(obs#141) — 슬롯은 자기 slot_type의 역할만 후보.
3. **집계**: 경기별 max 정규화 → 균등가중(obs#139 검증 공식). 포지션-순수, 표본 2+, 히트포인트 15+.
4. **조인**: 사람은 `player_id`로만. 라벨 문자열 조인 금지(v1 사고 원인).
5. **팀 참조**: 어디서나 `team_code`. (v1 matches 풀네임 함정 제거됨)
6. **스탯 0**: SofaScore 키 생략의 확정값 — 결손과 다르다(obs#132).
7. **25/26 첼시·리버풀 팀 전술은 알론소·이라올라 것이 아니다** — 개인 성향 기준선으로만.

## 감독 분석 11축 (`manager_profiles.axis`)

philosophy · traits · role_demands · formation · situational (사용자 지정 5)
\+ pressing(PPDA — docs/12 정본표) · buildup · rest_defense(obs#101) · set_pieces · rotation · market (제안 6)

## 파이프라인

| 작업 | 명령 | 비고 |
|---|---|---|
| 실측 수집 | `core.sofascore.js_collect()` → 브라우저 → `parse_collected()` | sofascore.com 오리진 필수 |
| 익스포트 | `python3 scripts/export.py` | 게이트 통과 후 site/data 재생성 + 프리뷰 미러 |
| 게이트 | `python3 scripts/gates.py` | G1~G12 |
| v1 재흡수 | `python3 scripts/migrate_v1.py` | ⚠️ 컷오버 완료 — 재실행하면 v2 신규분이 날아간다. 사용 금지(아카이브 참조용) |
| 이적 감시 | transfer-watch 스킬 (매일 09/21시) | 3팀 루프 — v2에 기록 (2026-08-11 컷오버 완료) |

## 재설계 진행 상태 (2026-08-11)

- [x] 0 체크포인트(`pre-redesign` 태그) · 1 스키마+마이그레이션 · 2 core/ · 3 export/JSON · 4 site/ 6페이지
- [x] 5 CLAUDE.md 재작성 · docs/20 v2 배너 · HANDOFF (잔여: manager_profiles 시드, docs/22 신설)
- [x] 6 컷오버 — 구 툴 archive/v1/ 이동, db_dump v2 전환, transfer-watch 스킬 v2·**3팀 확장**
      (팀 루프 AVL 전체 / CHE·LIV 스캔+기록, teams.fotmob_id가 소스 정본 —
      ⚠️ CHE 8455·LIV 8650은 첫 실행에서 검증)
- [ ] 7 FC27 온보딩 (9월): game_system_changes 소급 기입 + docs/21·22 작성
- 데이터 백로그: AVL squad_entries의 가르나초·알리송·아브라함 그리드가 구표본(v1 승계) —
  prescriptions 확장 표본으로 갱신 필요. 만잠비 fit 재산출값의 transfer_targets 반영은 완료.

## 정합성 규칙 (2026-08-13 갱신 — 가르나초 중복·헤밍스 누락 사고에서)

**페이지 슬롯 후보 풀의 SSOT는 DB 뷰 `v_slot_candidates`다.** `squad_entries`를 우선하고
`transfer_targets`의 활성 실측 후보를 합치며, 같은 `player_id`가 스쿼드로 승격됐으면 이적 행은
화면 풀에서 숨긴다. 모든 선수 목록 화면은 export의 `slot_candidates`와 공용 JS 함수만 사용한다.
transfer_targets가 CONFIRMED가 되는 순간 squad_entries로 승격하는 규칙도 유지한다.
G8이 슬롯별 중복·도달 불가 스쿼드 행·활성 이적 후보 누락을 차단한다.

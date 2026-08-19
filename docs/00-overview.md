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

### 좌우 쌍 슬롯의 한쪽만 쓰기 — `squad_entries.pos_only` (2026-08-19 추가)

`squad_entries`는 `pos`가 아니라 **`slot_type`으로 슬롯과 조인**한다. 그런데 좌우 쌍 슬롯
(`FB`=LB/RB · `CB`=LCB/RCB · `DM`=LDM/RDM · `WM`=LM/RM)은 한 `slot_type`이 **두 pos를 덮으므로,
그 유형의 선수는 기본적으로 양쪽 후보에 모두 뜬다.** 왼발 전문 풀백이 RB 드롭다운에 나오는 것이 이 때문이다.

- 한쪽만 후보로 쓰려면 그 행의 **`pos_only`에 해당 pos를 적는다**(예: 루헤리 `pos_only='LB'`).
  `NULL`이면 종전대로 `slot_type`의 모든 pos에 노출된다 — **기본 동작은 바뀌지 않았다.**
- 필터는 뷰 `v_slot_candidates`의 squad 브랜치에 있다: `(se.pos_only IS NULL OR se.pos_only = sl.pos)`.
- ⚠️ **실측 좌우로 자동 판정하지 않는다** — `pos_only`는 **명시 지정 전용**이다. 근거:
  ⑴ **다포지션 겸업을 지워버린다.** 보가르드는 주포지션이 `DM`인데 FB 양쪽 후보로도 써야 하고,
  실측 툴x는 71.3(n=4)으로 LB(x=13)에서 58 어긋난다 — 자동 배제면 LB 후보에서 사라진다.
  ⑵ **표본이 작다.** 보가르드·네델코비치 n=4, 캐시 n=2 수준이고 상당수가 친선이다.
  ⑶ `avg_positions`는 **클럽 표본 전체 평균**이라 시즌 중 포지션 전환을 반영하지 못한다.
- ⛔ **`squad_entries.id`와 `players.id`를 혼동하지 말 것 — 2026-08-19에 실제로 오판했다.**
  AVL FB에서 두 id 공간이 우연히 교차한다(`se.id=2`→`player_id=6` 마첸 / `se.id=6`→`player_id=2` 캐시).
  `avg_positions`는 **`player_id` 키**이므로 `se.id`로 조회하면 **좌우가 뒤바뀐 결론**이 나온다.
  그때 「마첸·캐시 실측이 뒤집혔다」고 잘못 보고했고, **실제로는 전원 정상**이다
  (마첸 14.5·루헤리 13.7 = 좌 / 캐시 87.9·네델코비치 86.6 = 우). 반드시 `JOIN players p ON p.id=se.player_id`로 확인한다.

### 확정 영입 라벨 규약 (2026-08-19 변경)

`(합류확정)` 접미는 **쓰지 않는다.** 종전에는 `squad_entries.label`에 문자열로 박히고
`v_slot_candidates`의 transfer 브랜치가 `likelihood='CONFIRMED'`일 때 덧붙였는데, **양쪽 다 제거**했다.
확정 여부는 라벨이 아니라 **`lh`/`status` 값으로 전달**하고, 화면 배지는 그 값으로 그린다
(`compare.html`이 이미 그렇게 동작한다). `영입·` 접두(미확정 이적 후보)와 `(신규)`·`(보유)`는 그대로 유지한다.

# FC27 온보딩 체크리스트 (발매 **2026-09-25** — EA 공식 확정)

원칙: **버전 추가 = 행 추가** (game_versions에 FC27 행은 이미 있음).

## ⏰ EA 공식 공개 일정 (2026-08-18 EA 뉴스 원문 · obs#249)

| 시점 | 내용 | 우리 쪽 함의 |
|---|---|---|
| 08-17~18 | top-27 남녀 + **리그별 공개**(08-18 PL · 08-19 세리에A·라리가 · 08-20 리그1) | 구단 공식이 top-11을 낸다. **숫자를 본문에 적는 구단과 그래픽으로만 배포하는 구단이 갈린다**(리버풀=본문 ✅ / 빌라=그래픽 ⛔) |
| **08-21 18:00 BST** | **Full Base Item Database — ⛔ PlayStyles 없음** | **1단계 수집.** OVR·POT·6대 스탯·원능력치·포지션까지. ⚠️ 이적창 마감 전이라 **이번 창 이적이 반영되지 않는다** |
| **09-10** | **Full base Item Database — ⭐ PlayStyles 포함 + 이적 마감 후 갱신** | **2단계 수집이자 26/27 분석의 정본.** 스즈키·완비사카·루헤리·네델코비치가 그때야 새 소속으로 잡힌다 |

⛔ **`fcratings.com`을 쓰지 말 것** — 「FC 27」 라벨을 달지만 **실제 데이터는 FC26**이다(2026-08-19 확인:
빌라 스쿼드에 틸레만스·로저스·디뉴·산초가 그대로 있고 이번 창 영입 0명 · 마르티네스 6대 스탯이 우리 FC26 행과 완전 일치).
⚠️ sofifa·fut.gg는 **전체 DB 공개 전까지 FC26을 계속 표시**한다 — 라벨이 아니라 **스쿼드 구성으로 버전을 판별하라.**

## 실행 순서

1. **Day-1 스냅샷 — 2단계로 나눈다**(obs#249):
   - **1단계(08-21)**: sofifa 로스터 → `player_game_stats`(game_version='FC27', **roster_date 명기**).
     ⚠️ **`playstyles`·`traits`는 NULL로 남긴다** — 아직 공개되지 않은 것이지 없는 것이 아니다(결손 ≠ 0, obs#132).
     ⚠️ sofifa 상세는 **로그인 세션에서만 열린다**(obs#234) — 수집 전 로그인 확인.
   - **2단계(09-10)**: PlayStyles·traits 채우기 + **이적 반영 로스터를 새 roster_date 행으로 추가**(덮어쓰지 않는다, 불변규칙 2).
   - EA 피치노트 원문 → `game_system_changes`에 area별 기입(FIFA→FC26 소급 요약도 이때 함께).
   - ⭐ **3팀 전 스쿼드를 받는다.** ⚠️ **[2026-08-25 실측 갱신 — 「빌라 22 · 첼시 2 · 리버풀 0」은 낡은 수치다]**
     그 뒤 보강이 진행돼 지금은 **FC26 176명 · FC27 146명**이다. 델타의 실제 제약은 팀 편중이 아니라 **양쪽 교집합**이다:
     **FC26∩FC27 = 99명**(델타 산출 가능) · **FC27만 47명**(FC26 베이스라인 없음) · **FC26만 77명**(FC27 미수집).
     ⇒ 09-10 수집 시 **FC27만 있는 47명의 FC26 베이스라인을 함께 받는 것**이 델타 커버리지를 가장 크게 늘린다
     (sofifa는 전체 DB 공개 후에도 FC26 로스터를 계속 제공한다).
     재확인 질의: `WITH a AS (SELECT DISTINCT name_kr FROM player_game_stats WHERE game_version='FC26'), b AS (…'FC27') SELECT …`
   - ✅ **[2026-08-25 해소] 이름 충돌 — 알리송 건은 이미 처리돼 있다.** `players`가
     **`알리송`(59: Alysson, 빌라 RW/LM, OVR 70)** 과 **`알리송 베케르`(43: Alisson Becker, 리버풀 GK)** 로 이미 구분하고 있고
     `player_game_stats`에도 두 이름이 별도 행으로 공존한다. 재조사 불필요.
   - ⚠️⚠️ **[2026-08-25 신규 발견·해소] 그런데 문서가 지목하지 않은 실제 충돌이 하나 더 있었다 — `스캔런`.**
     **118 Calum Scanlon**(LIV LB, 2005, 경기 3·유출행 1·리포트 3)과 **145 Cody Scanlon**(MF)이 **같은 name_kr을 쓰고 있었다.**
     아직 `player_game_stats`에 없어 충돌이 발생하지 않았을 뿐, **09-10 수집에서 UNIQUE 제약에 걸려 한 명이 다른 한 명을 덮어쓸 수 있었다.**
     ⇒ **`캘럼 스캔런` / `코디 스캔런`으로 분리했다**(알리송 선례와 동일 방식). `players` name_kr 중복은 이제 **0건**이다.
     ⭐ **교훈**: 이 함정은 「알리송」 개별 사례가 아니라 **부류**다. 수집 전 반드시 전수 질의를 돌릴 것 —
     `SELECT name_kr, COUNT(*) c FROM players WHERE name_kr IS NOT NULL AND trim(name_kr)!='' GROUP BY name_kr HAVING c>1`
     ⚠️ `sofifa_name`이 같은 name_kr 안에서 갈리는 것(`A. Isak` ↔ `Alexander Isak`)은 **충돌이 아니라 원천의 약칭·정식명 차이**다 —
     이걸 충돌로 세면 80건 이상 오탐이 난다. **판정은 `players` 쪽 name_kr 중복으로 한다.**
2. **역할·커널 수집**: fut.gg `/api/fut/roles/` (키는 id, slug 아님 — obs#92 함정)
   → `game_roles`/`game_role_focus`/`game_role_variants` FC27 행. 좌표 변환은 docs/20 규약.
3. **게이트 확장**: `core/kernel.py`의 EXPECTED에 FC27 정합값 추가, gates.py 앵커는
   FC27 커널로 재산출한 값을 **새 행으로** 기록(FC26 앵커는 유지 — 버전별 병존).
4. **익스포트**: `scripts/export.py`가 kernels/FC27.json을 자동 생성(행만 있으면 됨).
   site/ 페이지는 버전 선택 UI 추가 전까지 FC26 고정 — 필요 시 data.js에 파라미터 추가.
5. **변화 관찰 로그**: FC26 대비 역할 수·커널 diff를 obs로 1건 기록.

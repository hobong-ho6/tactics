# 데이터 수집·기록 규칙

## 스키마 (data/avl_analysis.db)

전체 설계는 [data/DESIGN.md](../data/DESIGN.md). 테이블 요약:

- `seasons(code,label)` — 시즌 코드는 `2025-26` 형식.
- `players` / `player_seasons` — 선수 정체성은 시즌 불변, 소속·등번호·출전시간은 시즌별.
- `matches(date,opponent,competition,venue,result,season,…)` — venue는 H/A/N.
- `appearances` — 선수×경기. 평점·포지션·역할·히트맵·출처·신뢰도.
- `streaks` + `match_streak` — 연승 등 구간 정의 (다대다).
- `game_roles` — FC 버전별 역할 라이브러리.
- `player_role_map` — 실측→게임 매핑 결과 (분석과 툴 사이의 계약).
- `player_match_positions` — 경기별 평균위치 실측 (avg_x/avg_y, 분·평점, pos_class).
  가변 포지션 선수의 "가장 많이/가장 잘 맡은 역할" 판정의 원천. 집계는 `v_position_profile` 뷰.
- `player_duties` — 선수×포지션 임무 vs 수행 리뷰.

### pos_class 분류 밴딩 (player_match_positions)

- 레인: y<40 = R, 40–60 = C, y>60 = L / 깊이: avg_x≥52 = 전진(LW·CAM·RM), <52 = 피봇.
- 45분 미만 출전은 평균위치가 불안정하므로 pos_class = NULL.
- 경계(레인 60 부근)에 걸치는 선수는 밴드 2개로 갈라질 수 있음 — 해석 시 합산할 것
  (사례: 틸레만스 pivot-left 11 + pivot-centre 10 = 같은 역할 21선발).

## 표기 규약

- **competition**: 표준 명칭만 사용 — `Premier League`, `Europa League`, `FA Cup`, `EFL Cup`.
  스테이지·매치위크는 **`stage` 컬럼**에 기록 (`MW5`, `R16 1st leg`, `Final` 등). 기존 데이터 정규화 완료(2026-07-02).
- **result**: 홈-원정 순 원문 스코어 (`4-2`)만. 승패는 venue와 조합해 판정.
  `W 4-0` 같은 접두 표기 금지 (기존 10건 정규화 완료).
- **source**: URL 또는 API 엔드포인트를 그대로. 여러 소스는 ` ; `로 이어붙이고
  수집 날짜를 괄호로 남긴다.
- **confidence**: `HIGH / MEDIUM-HIGH / MEDIUM / QUALITATIVE` + 무엇이 어느 등급인지
  한 문장 근거. 항목별 등급이 다르면 나눠 적는다 (예: 평점 HIGH, 히트맵 MEDIUM).

## SofaScore 좌표 규약 ★중요

API 히트맵/평균위치 좌표는 0–100 스케일:

| 축 | 의미 |
|---|---|
| x | 공격 방향. 0=자기 골, 100=상대 골 |
| y | **낮음=오른쪽 측면, 높음=왼쪽 측면** |

- 홈/원정 관계없이 동일 (2026-07-02 검증: Cash(RB) y≈15–20, Digne(LB) y≈85–90,
  홈 3경기·원정/중립 2경기 교차 확인).
- 존 분할: x 3등분(def/mid/att) × y 3등분(right/centre/left, 33.34 경계).
- 툴(fc26-heatmap.html) 좌표는 x=좌우/y=공격방향으로 **축이 다르므로** 변환 주의.

## SofaScore 수집 절차

`api.sofascore.com`은 curl/서버 요청을 403으로 차단한다. **Chrome(claude-in-chrome)의
javascript_tool로 sofascore.com 페이지 컨텍스트에서 fetch** 하면 된다.

주요 엔드포인트:
```
/api/v1/search/all?q=<이름>                     → 선수/팀 ID
/api/v1/player/<pid>/events/last/<page>         → 선수의 과거 경기 목록 (event ID 확보)
/api/v1/event/<eid>/player/<pid>/heatmap        → 히트맵 좌표 배열 [{x,y},…]
/api/v1/event/<eid>/player/<pid>/statistics     → 그 경기 평점·분·터치·키패스
/api/v1/event/<eid>/lineups                     → 라인업·포메이션·전원 평점
/api/v1/event/<eid>/average-positions           → 팀 전원 경기 평균좌표 (averageX/averageY)
```

대량 수집 팁: javascript_tool 결과는 ~1KB에서 잘리므로, 루프는 window 변수에 담아
백그라운드로 돌리고 (`window.__done` 플래그 + setTimeout 폴링) 결과는 슬라이스로
나눠 회수한다. localhost POST 브리지는 Chrome의 로컬네트워크 차단으로 불가.

수집 시 기록할 것: 존 분포 %(상위부터), 중심좌표(centroid), x/y 범위, 히트포인트 수,
터치 수 → `heat_zones`(존 요약)와 `heat_summary`(움직임 서술 + 수치)로.
추가로 **5×5 툴좌표 그리드**를 `appearances.heat_map25`(문자 0–9,X=peak)와
`heat_tool_x/heat_tool_y`(툴좌표 중심)로 저장한다.
**이벤트 스탯도 반드시 함께 수집** (그리드와 같은 statistics 호출에서 나옴):
`xg`/`xa`/`key_passes` 컬럼 + `stats_json`(passes_total/acc, duels_won/lost, tackles,
interceptions, shots_on/off, dribbles_won, aerials_won, goals, assists 컴팩트 JSON).
선수별 집계는 `v_event_profile` 뷰. 용도: 평점 의존 축소 — 위치(그리드)+산출(스탯)의
2차원 판단 (docs/10 방법론 한계 참조).
변환: 툴x = 100 − SofaScore y, 툴y = SofaScore x. 선수별 통합본(경기 균등가중 평균)은
`player_role_map kind='measured'`에 기록하며 툴이 이를 렌더링한다.

**포지션-순수 규칙**: 가변 포지션 선수의 통합 그리드는 반드시 같은 포지션 경기끼리만
묶는다 (혼합하면 어느 역할과도 안 닮은 뭉개진 그리드가 됨 — 로저스 사례: 혼합 43% →
LW-순수 55%). 주 포지션 통합본 = `kind='measured'`, 나머지 포지션 =
`kind='measured:<class>'` (예: measured:CAM). 포지션당 표본 2경기 이상 확보 후 집계.

**맥락별 분리 집계**: 같은 (선수, 포지션)이라도 경기 지배도에 따라 풋프린트가 다르므로,
버킷당 2경기 이상이면 `@dom`(2골차 이상 승) / `@tight`(무·패·1골차 승)으로 분리 집계를
추가한다 — kind 예: `measured@dom`, `measured:CAM@tight`. 균등 평균의 "번짐"을 피하고
지배/접전 변형 프리셋의 근거가 된다. 표본 확장은 경기 수보다 **맥락 다양성**(홈/원정,
승/패)이 우선 — 균등가중 top-10 확장은 편향과 번짐만 키우므로 금지.

주요 ID (25/26 확보분): Konsa 827679, Buendía 783126, Cash 833956, Digne 96538,
Rogers 948261, Tielemans 331737, McGinn 250223, Onana 923973, Kamara 826204.
팀: Aston Villa 40. 그 외는 search로 확인하고, 자주 쓰는 ID는 여기에 추가해 갱신.

## 평점 권위 순서

SofaScore API 공식값 > SofaScore 뉴스 > 서드파티 매체 자체 평점.
하위 소스 값을 API로 교정하면 이전 값과 교정 사유를 `heat_summary` 또는
`confidence`에 남긴다 (예: 부엔디아 본머스전 9.0(Sportsdunia)→8.5(API)).

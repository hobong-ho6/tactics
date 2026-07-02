# FC 게임 시스템 분석·매핑 규칙 (FC26 → FC27…)

목적: 실측 분석 결과를 특정 FC 버전의 전술 시스템으로 번역하는 규칙.
게임 버전이 바뀌어도 "행 추가"로만 대응한다 (구조 재작성 금지).

## FC26 전술 구성요소 (기록 대상)

- **포메이션**: 툴에 45개 FC26 포메이션 등록 완료 (fc26-heatmap.html `FORMATIONS`).
- **역할(Role) + 포커스(Focus)**: 포지션 타입별 역할 세트는 `game_roles` 테이블
  (FC26: 37역할, 9개 포지션 타입). 각 역할의 기대 히트맵 커널은 툴의 `MAPS`에 있음
  — 장기적으로 DB로 이관 예정 (DESIGN.md 참조).
- **팀 전술 설정**: `game_tactic_params` 테이블이 버전별 설정 어휘를 보관.
  FC26 팀 전술 = 포메이션 + 빌드업 스타일(Short Passing/Balanced/Counter)
  + 수비 접근(Deep/Balanced/High/Aggressive) + 라인 높이(0–100, 접근 방식이 범위 제한)
  + 11명의 (역할, 포커스) + 공유용 전술 코드.

## 게임 내 전술 재현의 완전한 계약

하나의 재현 전술 = **`team_tactic_setups` 1행 (팀 설정) + `player_role_map` 11행 (선수 배치)**,
같은 (season, game_version, kind)로 조인. 이 두 테이블만 조회하면 게임에서 그대로
입력 가능한 전술 전체가 나와야 한다. 게임에서 실제로 만들었으면 `tactic_code`를
기록하고, 게임 내 히트맵과 실측 히트맵을 비교해 검증한다 (검증 전 confidence는 MEDIUM 이하).

## 실측 → 게임 매핑 방법

`player_role_map`에 (player, season, game_version, kind)별로 기록:

- `kind='measured'` — 실측 평균 히트맵을 그대로 25칸 맵(map25)으로 변환한 것.
- `kind='role'` — 실측 히트맵과 가장 유사한 게임 역할(코사인/셀합 유사도) 매핑.
- `kind='optimal'` — 평점×결과 가중으로 도출한 최적 포지션+역할 (베스트 XI + 벤치).
- `kind='match:<태그>'` — 특정 경기 단건 재현 (예: `match:LIV-4-2`).

유사도 판정 시 좌표 규약(docs/30-data-rules.md)을 반드시 맞춘 뒤 비교한다.

## 게임 버전 추가 절차 (FC27 출시 시)

1. FC27 역할/포커스 체계 조사 → `game_roles`에 `game_version='FC27'` 행 추가.
2. 역할별 히트맵 커널 작성 → 툴의 커널 라이브러리에 FC27 세트 추가
   (툴이 JSON 로딩으로 리팩터링되면 데이터 파일 추가만으로 끝나야 함).
3. 기존 실측 데이터(레이어 1)는 그대로 재사용 → FC27용 `player_role_map` 행 생성.

## 툴(fc26-heatmap.html) 규칙

### 실측 검증 모드 (헤더 메뉴)

- **왼쪽(A) = 실측 히트맵, 오른쪽(B) = 게임 역할 설정.** 헤더의 `실측 → FC26 검증` /
  `실측 로테이션` 버튼 또는 (실측) 포메이션 선택으로 진입.
- 왼쪽 데이터는 `player_role_map kind='measured'`의 선수별 정밀 그리드
  (SofaScore API 좌표를 5×5 툴 좌표계로 집계; 경기별 원본은 `appearances.heat_map25`).
- 오른쪽 로스터의 **% 뱃지 = 그 역할·포커스 커널과 같은 포지션 실측 그리드의 코사인
  유사도** (초록≥75 / 노랑≥55 / 빨강<55). 역할을 바꿔가며 실측에 가장 가까운 설정을 찾는다.
- 선수별 확인: 칩 클릭(솔로 토글)이 좌우 패널에 포지션 라벨로 동기화된다.
- 확정한 역할 조합은 `player_role_map`(kind='role')에 역기록하는 것이 완료 조건.

- 프리셋 네이밍: `아스톤 빌라 <시즌> (<종류>)` — 종류: 실측 / 역할 / 최적 / 경기 태그.
- 프리셋 JSON export는 `data/exports/`에 날짜 스탬프로 저장·커밋한다.
- 방향 규약: 툴 좌표(x=좌우, y=공격방향)와 SofaScore 좌표(x=공격방향, y=좌우 반전)가
  **다르다**. 변환 시 docs/30-data-rules.md의 규약 표를 따를 것.
- 로드맵: 하드코딩 프리셋 → `player_role_map`에서 export한 JSON 로딩으로 전환
  (DESIGN.md "Tool strategy" 참조). 새 시즌·새 버전이 코드 수정 없이 추가되는 상태가 목표.

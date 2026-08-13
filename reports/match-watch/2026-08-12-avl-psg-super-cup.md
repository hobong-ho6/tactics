# 2026-08-12 UEFA Super Cup — PSG 2-1 Aston Villa

> 수집일 2026-08-13 · SofaScore event `16260286` · 중립 경기 · 빌라 4-2-3-1

## 실측

- 빌라 점유율 **39%**, 슈팅 **15-12**, 유효슈팅 **4-6**, 빅찬스 **5-3**, 패스 **368-588**.
- 득점 국면: 0-0 20분 → 0-1 열세 25분 → 1-1 16분 → 1-2 열세 29분.
- 45분 이상 출전한 11명을 `player_matches`에 적재했다. 전원 평균 위치·히트맵·개별 스탯이 있고
  히트포인트 최저도 **33**이라 경기 단위 그리드로 유효하다.
- Brian Madjo는 72분, 1골, 6슈팅, 2키패스. John McGinn은 73분, 1도움, 4키패스.

| 선수 | 라인업 슬롯 | 평균 위치 기반 분류 | 평점 | 핵심 |
|---|---:|---:|---:|---|
| Marco Bizot | GK | GK | 6.6 | 4선방 |
| Matty Cash | RB | RB | 6.6 | 우측 수비 |
| Victor Lindelöf | RCB | RCB | 6.4 | 중앙 보호 |
| Pau Torres | LCB | LCB | 7.0 | 79분 |
| Ian Maatsen | LB | LB | 7.0 | 좌측 폭·전진 |
| Boubacar Kamara | RDM | RDM | 6.4 | 더블 피벗 |
| João Gomes | LDM | LDM | 6.1 | 더블 피벗 |
| John McGinn | RAM | RM | 7.1 | 우측 창출, 4키패스·1도움 |
| Emiliano Buendía | CAM | LDM | 6.3 | 명목 CAM이나 평균 위치는 중앙·낮음 |
| George Hemmings | LAM | LDM | 6.2 | 순수 윙어보다 좌측 하프스페이스 |
| Brian Madjo | ST | ST | 6.6 | 정통 9번·물리적 출구, 1골 |

`lineup_pos`는 실제 라인업 배열을 4-2-3-1 우→좌 순서로 사상한 원천 배치이고,
`pos_class`는 평균 위치 기반 사후 분류다. 둘이 다른 Buendía·Hemmings는 오류로 덮지 않고 나란히 보존한다.

## 전술 판정

- 명목 구조 `McGinn RAM — Buendía CAM — Hemmings LAM — Madjo ST`와
  `Kamara/Gomes` 더블 피벗은 확인됐다. 다만 세 공격형 미드필더는 유동적이었다.
- [El País 경기 분석](https://elpais.com/deportes/futbol/2026-08-12/el-psg-extiende-su-hegemonia-tras-vencer-la-supercopa-de-europa-ante-el-aston-villa.html)
  (2026-08-12)은 빌라가 중앙을 좁게 보호하고 전방에서 센터백을 압박한 뒤 짧고 직접적으로 전환했다고 서술한다.
- [AS의 Emery 경기 후 문답](https://as.com/futbol/internacional/unai-emery-habra-mas-cambios-f202608-n/)
  (2026-08-12)에서 Emery는 Madjo와 Hemmings를 해당 포지션에 맞춰 준비시켰다고 확인했다.
  따라서 두 선수의 배치는 라인업 표기 오류가 아니라 의도된 선택이다.
- Madjo는 등지고 연결하는 물리적 출구와 박스 침투를 함께 맡았고, McGinn은 오른쪽 하프스페이스에서
  반복적으로 공급했다. 경기 단위 FC 적합은 McGinn RM `wm_winger/Attack` **.882**,
  Madjo ST `st_poacher/Attack` **.725**다. 한 경기 값이므로 대표 적합으로 승격하지 않는다.

## obs#134~136 검증

- **obs#134 지지**: 자연 우측 윙어 대신 McGinn을 RAM에 세워 임시 해결했다. 그의 평균 y=15.81은
  실제로 강한 우측 편향이고 4키패스·1도움으로 기능했지만, 전문 우측 자원 영입 필요를 반증하지 않는다.
- **obs#135 검증 불가**: Endrick이 출전하지 않아 우측 적합성이나 9번 조건에 새 근거가 없다.
- **obs#136 검증 대상 아님**: 이 경기는 빌라의 수요만 보여줄 뿐 협상 단계·선수 의사를 말하지 않는다.

팬 관찰은 [r/avfc 경기 후 스레드](https://www.reddit.com/r/avfc/comments/1vmqcwz/post_match_thread_psg_21_aston_villa_uefa_super/)
(2026-08-12)에서 교차 확인했다. Madjo/Hemmings, McGinn, Kamara/Gomes 조합 호평은 반복됐지만
위치 판정에서는 SofaScore 원천값과 감독 발언보다 낮은 우선순위로만 사용했다. 경기 전 Reuters 기자회견은
영상 전체를 검토하지 못해 근거로 채택하지 않았다. 전문 전술 블로그·경기 후 전술 유튜브는 수집 시점에
검색되지 않아 미수행으로 남긴다.

## 데이터 출처와 한계

- SofaScore `/event`, `/lineups`, `/statistics`, `/incidents`, `/average-positions`,
  `/player/{id}/heatmap`, `/player/{id}/statistics`를 동일 오리진 Playwright 수집기로 사용했다.
- SofaScore가 이 경기 xG를 양 팀 모두 `0.00`으로 제공해 `team_match_stats.xg_v/xg_o`도 원천값 그대로 0이다.
  이를 실제 무위험 경기라는 뜻으로 해석하면 안 된다(빅찬스는 빌라 5, PSG 3).
- Madjo의 유효 표본은 이 경기 포함 **4경기**라 대표 역할 최소 기준 6경기에 아직 미달한다.

---

## 2026-08-13 15시 심화 업데이트 — 선수별 스탯·히트맵·영상 교차검증

### 선수별 실제 데이터

아래 `평균 위치`는 SofaScore 원좌표 `(avg_x, avg_y)`이고 `맵25`는 같은 이벤트에서 받은 5×5 히트맵을
행 우선으로 인코딩한 원천값이다(`0~9`, 최대 셀 `X`). 한 경기 커널 적합은 역할 판정을 돕는 참고값이며
대표 처방이나 선발 결론으로 승격하지 않는다.

| 선수 | 분/평점 | 평균 위치·맵25 | 실제 스탯 | 이 경기 역할·FC26 참고 적합 |
|---|---:|---|---|---|
| Marco Bizot | 90 / 6.6 | `(10.05, 51.10)` · `0000000000000000000001X10` | 4선방, 23/30패스, 40터치, 10회수 | 후방 패스 옵션·라인 수비 GK · `gk_goalkeeper/Defend .966` |
| Matty Cash | 90 / 6.6 | `(41.71, 12.64)` · `00003000250002X0004900135` | 32/42패스, 2/4경합, 2태클, 5클리어, 1키패스 | 우측 폭·회복 수비 · `fb_wingback/Balanced .907` |
| Victor Lindelöf | 90 / 6.4 | `(29.11, 36.46)` · `001000001001211018X301043` | 39/41패스, 1인터셉트, 2클리어, 8회수 | RCB 중앙 보호·안정 배급 · `cb_bpd/Aggressive .895` |
| Pau Torres | 79 / 7.0 | `(28.70, 68.14)` · `0001021000123006810024X20` | 23/26패스, 3/6경합, 2태클, 3클리어 | LCB 좌측 전진 배급 · `cb_bpd/Build-Up .798` |
| Ian Maatsen | 90 / 7.0 | `(50.02, 87.46)` · `220004200021000X000011000` | 27/35패스, 11/16경합, 4태클, 2키패스 | 좌측 폭·전진과 회복 · `fb_wingback/Balanced .759` |
| Boubacar Kamara | 72 / 6.4 | `(41.31, 38.72)` · `001000061600430009X101410` | 19/21패스, 2인터셉트, 2슈팅(1유효) | 우측 피벗·중앙 스크린 · `dm_holding/Ball-Winning .788` |
| João Gomes | 79 / 6.1 | `(46.81, 57.68)` · `0030111160616016X13301100` | 12/18패스, 3/9경합, 3태클, 1슈팅 | 좌측 피벗·경합/압박 · `dm_holding/Roaming .679` |
| John McGinn | 73 / 7.1 | `(63.70, 15.81)` · `000580001X000190014300000` | 4/10패스, 4키패스, 1도움, 4/13경합 | RAM 우측 창출·전방 압박 · `wm_winger/Attack .882` |
| Emiliano Buendía | 90 / 6.3 | `(53.43, 50.76)` · `4122115551342X40556111020` | 30/45패스, 1키패스, 6/15경합, 2태클, 2슈팅 | 명목 CAM, 실제 중앙·낮은 연결자 · `cam_playmaker/Roaming .623` |
| **George Hemmings** | **90 / 6.2** | **`(58.11, 73.31)` · `66111X4430X41009403004000`** | **20/25패스, 1키패스, 3/9경합, 1태클, 2슈팅(1유효), 6회수** | **LAM이지만 왼쪽 안쪽·낮은 지원/압박 · `wm_widemid/Support .788`** |
| Brian Madjo | 72 / 6.6 | `(64.55, 54.02)` · `13X1003334314003131101000` | 1골, 6슈팅(1유효), 2키패스, 9/14패스, 1/9경합 | 포스트 출구+배후/박스 침투 · `st_poacher/Attack .725` |

### 교체 선수 5명 보강

기존 45분+ 필터는 시즌 대표 그리드에는 맞지만 경기 리포트에서 교체 선수를 통째로 누락시켰다. 이 경기의
교체 5명은 필터를 0분+로 낮춰 같은 event의 `lineups → statistics → heatmap → average-positions`에서 다시
수집했다. 아래 히트맵은 **그 교체 시간만의 실제 위치**이며 시즌 대표 처방에는 합산하지 않는다.

| 투입 | 교체 | 분/평점 | 평균 위치·맵25 | 실제 스탯 | 종료 XI FC26 참고 |
|---:|---|---:|---|---|---|
| 72′ | 카마라 → **보가르드** | 18 / 6.8 | `(45.01, 44.14)` · `0000002622002X20804002240` | 12/13패스, 2/2경합, 1태클, 4회수 | RDM `dm_dlp/Roaming .722` |
| 72′ | Madjo → **타미 아브라함** | 18 / 6.6 | `(64.94, 40.66)` · `05005055500505X0000000000` | 5/7패스, 1/2경합, 7터치, 슈팅 0 | ST `st_false9/Build-Up .493` ⚠️ 히트포인트 9 |
| 73′ | 맥긴 → **알리송** | 17 / 6.2 | `(62.08, 19.31)` · `003850005X000580000300005` | 9/14패스, 2/3경합, 1태클, 2회수 | RM `wm_widemid/Build-Up .765` |
| 79′ | 파우 토레스 → **밍스** | 11 / 6.6 | `(35.51, 81.81)` · `50000300003000038300X5000` | 10/12패스, 12터치, 2회수 | LCB `cb_wideback/Aggressive .794` |
| 79′ | 주앙 고메스 → **바클리** | 11 / 6.8 | `(59.61, 61.11)` · `040002X400020624040000000` | 15/15패스, 2/3경합, 1태클, 18터치 | LDM `dm_dlp/Roaming .466` |

아브라함은 히트포인트가 9라 프로젝트의 대표 그리드 최소 기준 15에 못 미친다. 원천 위치를 숨기지 않기 위해
경기 화면에는 표시하지만 `.493`을 전술 판정이나 시즌 처방의 근거로 사용하지 않는다. 나머지 교체 선수도
11~18분 표본이므로 역할·포커스는 **종료 XI를 화면에서 재현하기 위한 참고값**일 뿐이다.

### 헤밍스 유스 데이터 확보 경로

- 선수 프로필의 `events/last` 경로는 유스 선수에게 비거나 404가 날 수 있다. 이번에는 프로필 이력이 아니라
  **경기 이벤트 `16260286`의 lineup → player statistics/heatmap/average-positions** 순으로 회수했다.
- 그래서 헤밍스도 90분 스탯, 평균 위치, 히트포인트 51, 5×5 원천맵까지 성인 선수와 같은 형식으로 저장됐다.
- 위치 판정은 명목 LAM을 그대로 복사하지 않았다. 평균 `y=73.31`의 좌편향은 맞지만 전진 깊이와 맵 분포가
  터치라인 고정 윙어보다 낮고 안쪽이다. 에메리의 의도된 배치 확인과 합치되, 한 경기라 대표 역할 확정은 보류한다.

### 국면별 전술

1. **0-0(20분)** — 명목 4-2-3-1. 중앙을 좁게 보호하고 전방 인원이 PSG 센터백·안쪽 통로를 압박했다.
   AS는 초반 비소유 모양을 5-4-1로 묘사했지만, 라인업·평균 위치 정본은 백4다. 따라서 이는 고정 포메이션
   변경보다 초반 수비 국면의 일시적 하강으로 기록한다.
2. **0-1 열세(25분)** — 탈취 뒤 적은 패스로 전진했다. McGinn의 우측 공급과 Madjo의 등진 떨굼·배후 침투가
   주 출구였다. Kamara도 박스 앞까지 전진해 슈팅했다.
3. **1-1(16분)** — Madjo가 McGinn의 측면 공급을 마무리했다. PSG가 후반 Dembélé를 넣고 다시 볼·공간을
   장악했으며, Villa의 전진 수비선에서 Cash가 마지막 선에 남은 틈을 Doué가 공략했다.
4. **1-2 열세(29분)** — Villa가 라인과 압박을 올려 경기를 개방했다. Gomes 슈팅, Abraham을 향한 크로스 등
   박스 접근은 늘었지만, 더 큰 후방 공간도 감수했다.

### 영상·감독 발언 확인

- [BeanymanSports 경기 후 전체 기자회견](https://www.youtube.com/watch?v=cV0xoK0gK3w)
  (2026-08-13 게시, 자동 영문 자막 직접 확인): Emery는 팀이 전술·개인 양쪽에서 응답했고, 볼을 가졌을 때의
  위치, 압박 시점, 컴팩트함, 젊은 선수의 수비·전술 규율을 준비했다고 설명했다.
- [BeanymanSports Emery 단독 클립](https://www.youtube.com/watch?v=ILFYehyhGNY)
  (2026-08-13 게시, 자동 영문 자막 직접 확인): 같은 기자회견의 Emery 구간이다. Madjo의 평가는 득점만이
  아니라 수비, 헌신, 전술 규율을 포함했다.
- [The Villa Park Podcast 경기 분석](https://www.youtube.com/watch?v=NfejEXQj3sE)
  (2026-08-13 게시, 자동 영문 자막 직접 확인): Madjo의 위치 인지·수비수와의 접촉·반복 박스 움직임,
  Hemmings의 성숙한 왼쪽 수행, Kamara/Gomes의 더 강한 경합 성격, Maatsen의 전진 뒤 회복을 평가했다.
  팬/클럽 팟캐스트이므로 감독 발언·실측보다 낮은 보조 근거로만 썼다.
- [talkSPORT Madjo 분석](https://www.youtube.com/watch?v=6_VcfCoJTmQ)
  (2026-08-13 게시, 자동 영문 자막 직접 확인): 득점 전 기회 실패 후에도 표정·움직임이 무너지지 않았고,
  수비수 앞/뒤를 바꾸는 박스 움직임과 물리적 경합을 반복했다는 스트라이커 관점 평가다.
- [TNT Sports 공식 트로피·경기 영상](https://www.youtube.com/watch?v=Kf_KjuJPvS0)
  (2026-08-13 게시): 경기 장면 확인용이며 전술 해설의 주 근거로 사용하지 않았다.

### 기사·1차 자료 교차검증

- [El País 경기 분석](https://elpais.com/deportes/futbol/2026-08-12/el-psg-extiende-su-hegemonia-tras-vencer-la-supercopa-de-europa-ante-el-aston-villa.html)
  (2026-08-12 23:26 CEST): 중앙 보호, 전방 압박, 직접 전환, Madjo의 등진 연결, 실점 후 라인 상승을 가장
  구체적으로 설명한다.
- [AS 경기 분석](https://as.com/futbol/internacional/invencible-luis-enrique-f202608-n/)
  (2026-08-12 22:59 CEST): 초반 수비 모양을 5-4-1로 묘사하고, McGinn·Buendía가 Madjo를 찾았으며
  Madjo가 등진 연결·공중볼·배후 침투를 모두 수행했다고 평가한다. 두 번째 실점은 Cash가 마지막 선에
  묶인 전진 수비의 위험으로 해석한다.
- [AS Emery 경기 후 문답](https://as.com/futbol/internacional/unai-emery-habra-mas-cambios-f202608-n/)
  (2026-08-12 23:58 CEST): Madjo와 Hemmings를 경기 전 정한 위치에서 훈련했다고 직접 확인한다.
- [UEFA 공식 경기 페이지](https://www.uefa.com/uefasupercup/match/2048319--paris-vs-aston-villa/)
  및 [공식 하이라이트 링크](https://www.uefa.com/uefasupercup/clubs/52747--paris/matches/): 대회·경기 정본과
  하이라이트 경로를 확인했다. 현재 텍스트 페이지는 세부 선수 통계를 노출하지 않아 SofaScore 수치를 대체하지 않는다.
- Aston Villa 공식 사이트의 경기 후 상세 리포트는 수집 시점 검색 인덱스에서 발견되지 않았다.
  Telegraph 원문은 유료벽으로 전체 검토하지 못했다. 이 두 유형은 **미수행 사유를 명시**하고 결론 근거에서 제외했다.

### 선수별 최종 판정

- **Bizot**: 4선방과 후방 패스 옵션은 확인. 두 실점의 개인 책임을 확정할 영상 근거는 부족하다.
- **Cash**: Kvaratskhelia를 장시간 통제했지만 두 득점 장면의 간격·마지막 선 판단은 약점으로 남았다.
- **Lindelöf/Pau**: 좁은 중앙 수비와 안정 배급. Lindelöf 39/41, Pau 23/26 패스로 빌드업 정확도가 높았다.
- **Maatsen**: 폭·전진뿐 아니라 11회 경합승, 4태클, 2키패스로 공수 활동량이 가장 선명했다.
- **Kamara/Gomes**: 더블 피벗은 확인. Kamara는 스크린·배급, Gomes는 경합·태클 쪽 신호가 강하지만
  한 경기만으로 고정 분업을 확정하지 않는다.
- **McGinn**: 자연 RW가 아닌 RAM 임시 해법이면서 실제 우측 창출자였다. 4키패스·1도움이 이를 직접 지지한다.
- **Buendía**: 명목 CAM보다 실측이 낮았다. 63터치·45패스로 연결량은 컸지만 6/15 경합과 낮은 평균 위치는
  PSG 압박 아래 전진 연결이 제한됐음을 보여준다.
- **Hemmings**: 90분을 버티며 왼쪽 안쪽 지원·압박·회수 임무를 수행했다. 유스 선수도 이벤트 경로로
  히트맵을 확보했으나, 대표 LM/LAM 역할로 승격하려면 공식전 2경기 이상 같은 위치 표본이 더 필요하다.
- **Madjo**: 1골·6슈팅·2키패스의 공격 출구. 실제 경합승은 1/9라 “물리적으로 모든 경합을 지배했다”는
  서사는 과장이다. 가치의 핵심은 등진 연결 시도, 반복 침투, 실패 뒤 재시도와 박스 점유다.

### DB 반영 원칙

- 이번 심화 회차에서 기존 `player_matches` 원천행은 덮어쓰지 않았다.
- 2026-27 역할 기록이 없던 Bizot·Lindelöf·Pau Torres·Maatsen·Hemmings·Madjo만 `player_duties`에
  추가한다. 기존 Cash·Kamara·Gomes·McGinn·Buendía 행은 보존하고 이 경기 판정은 observation으로 연결한다.
- 한 경기 커널 Δ만으로 `prescriptions`·`team_tactic_setups`는 변경하지 않는다.
- 교체 5명은 `player_matches`·`match_player_reports`·`match_player_prescriptions(starter=0)`에만 추가하고,
  누구를 몇 분에 교체했는지 `replaced_player_id`·`minute_on`으로 보존한다.

---

## 이 경기만의 FC26 재현 프리셋

> **MATCH ONLY** — 아래 설정은 PSG전 한 경기만 재현한다. 시즌 대표 전술이나 에메리 정본 설정을
> 변경하지 않으며, `match_game_setups`·`match_player_prescriptions`에 별도로 저장한다.

- 포메이션: **4-2-3-1 Wide**
- 빌드업: **Counter** — 39% 점유에서 탈취 직후 적은 패스로 Madjo와 우측 McGinn을 찾은 직접 전환.
- 수비 접근: **Balanced**, 라인 높이 **45** — 중앙을 좁게 보호한 4-2-3-1과 일시적 5-4-1을 정적 설정으로 근사.
- 전술 코드: **미검증**. 실제 게임에서 아직 저장·검증하지 않았다.
- 한계: 0-0의 낮은 블록과 1-2 열세 뒤 라인 상승을 단일 프리셋 하나가 모두 표현할 수 없다.

| 슬롯 | 선수 | FC26 역할 | 포커스 | 이 경기 적합 |
|---|---|---|---|---:|
| GK | 비조 | 골키퍼 (`gk_goalkeeper`) | Defend | .966 |
| LB | 마첸 | 윙백 (`fb_wingback`) | Balanced | .759 |
| LCB | 파우 토레스 | 볼 플레잉 센터백 (`cb_bpd`) | Build-Up | .798 |
| RCB | 린델뢰프 | 볼 플레잉 센터백 (`cb_bpd`) | Aggressive | .895 |
| RB | 캐시 | 윙백 (`fb_wingback`) | Balanced | .907 |
| LDM | 주앙 고메스 | 홀딩 (`dm_holding`) | Roaming | .679 |
| RDM | 카마라 | 홀딩 (`dm_holding`) | Ball-Winning | .788 |
| LM | 헤밍스 | 와이드 미드필더 (`wm_widemid`) | Support | .788 |
| CAM | 부엔디아 | 플레이메이커 (`cam_playmaker`) | Roaming | .623 |
| RM | 맥긴 | 윙어 (`wm_winger`) | Attack | .882 |
| ST | Brian Madjo | 포처 (`st_poacher`) | Attack | .725 |

역할·포커스는 event `16260286`의 선수별 실제 히트맵을 해당 슬롯의 FC26 커널에 비교한 단일 경기
argmax다. 이는 “그 경기에서 가장 비슷했던 움직임”이지 선수의 시즌 대표 역할이나 최적 처방이 아니다.

경기 분석 메뉴의 **재현 XI** 선택기에서 `선발 XI`와 `교체 반영 종료 XI`를 바꿔 볼 수 있다. 종료 XI는
보가르드·아브라함·알리송·밍스·바클리를 실제 교체 대상 슬롯에 넣으며, 팀 히트맵도 전체/선발/교체 및
개별 선수로 나눠 확인할 수 있다.

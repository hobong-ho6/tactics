# 2026-09-08 Club Brugge 2-3 Aston Villa — UEFA 챔피언스리그 26/27 리그 페이즈 MD1

> 수집일 2026-09-09 · SofaScore event `16938841` · FotMob `6106295` · WhoScored/Opta `2029174`
> UCL 리그 페이즈 MD1 · **원정**(Jan Breydelstadion) · 양 팀 모두 4-2-3-1
> ⛔⛔ **대회 축 분리**: 이 경기는 **챔피언스리그**다. 직전 3경기(브라이턴·아스날·헐)는 프리미어리그이며
> `team_match_stats`·시즌 시계열에 **섞지 않는다**(G13 「team_code 대회 불일치」 검사 대상).
> 경기 전 프리뷰는 `2026-09-08-avl-brugge-preview.md`(수정하지 않고 보존). 대조 결과는 §0-1에 있다.

---

## 0. 요약

**빌라가 시즌 첫 득점을, 그것도 3골을 원정에서 냈다.** PL 3경기 무득점(13슛 1유효의 헐전 포함) 뒤
브뤼헤 원정에서 **36% 점유로 21슛·유효 9·xG 3.22**를 쌓았다. 전반 43분 만에 3-1을 만들고
후반 페널티 1골을 허용해 3-2로 닫았다.

- **11분 맥긴**(파우 토레스 어시스트) → **19분 베틀레센**(비르질리 어시스트) → **22분 부엔디아**(조앙 고메스)
  → **43분 잭슨**(파우 토레스) → **61분 트레솔디 PK**. **한 번도 뒤지지 않았다**(리드 76분·동점 14분·추격 0분).
- ⭐⭐ **파우 토레스가 좌측 CB로 어시스트 2개**(키패스 4·xA 0.49)를 기록했다.
- ⭐⭐ **잭슨이 커널상 `st_false9`로 돌아왔다**(0.625 vs `st_advanced` 0.289). 헐전은 정반대였다
  — obs#446 「false9는 성향이 아니라 국면 반응」의 가장 강한 실측 지지다.
- ⭐⭐ **풀백 비대칭이 좌우 반전**됐다: 정본(좌 전진·우 절제)과 달리 이번엔 **우측 완비사카가 전진측**
  (`fb_att_wb/Support` 0.863), **좌측 마첸이 잔류측**(`fb_fullback/Balanced` 0.849).
- ⭐ **이 저장소 최초의 라인 높이 실측**: `def_x` 빌라 33.5 · 브뤼헤 42.6(n=176/147).

### 0-1. 프리뷰 예상 대비 — 적중·오류

| 프리뷰가 예상한 것 | 실제 | 판정 |
|---|---|---|
| 레코가 **홈에서 공격적으로 나온다** ⇒ 빌라가 정착 무공 블록을 세운다 | 브뤼헤 점유 **64%**·PPDA 7.08(빌라 12.84). 빌라 36% | ✅ **적중** — ②가 처음 측정됐다 |
| UTV×The Villans 예상 XI: 스즈키 / **캐시**·린델뢰프·파우·**루제리** / 카마라·조앙 고메스 / 헤밍스·맥긴·**음바예** / 잭슨 | 스즈키 / **완비사카**·린델뢰프·파우·**마첸** / 카마라·조앙 고메스 / **헤밍스·부엔디아·맥긴** / 잭슨 | ⚠️ **부분 적중** — 중앙 축(스즈키·린델뢰프·파우·카마라·조앙 고메스·헤밍스·잭슨) 7명 적중, **풀백 2명과 10번 1명이 틀렸다** |
| 린델뢰프는 「스쿼드에서 우측을 볼 수 있는 유일한 CB」 | 린델뢰프 **RCB**(avg_y 36.2) · 파우 **LCB**(62.4) | ✅ 적중 |
| **음바예 출전 가능성**(£47m, 헐전 벤치 미출전이 최대 논쟁거리) | ⛔ **또 벤치 미출전**(평점 없음). **가르나초도 미출전** | ❌ **오류** — 프리뷰가 「출전 가능 시사」로 읽은 회견이 출전으로 이어지지 않았다 |
| 조앙 고메스 복귀 가능(PL 출전정지 CL 미적용) | ✅ **90분 선발**·어시스트 1·태클 5(팀 최다) | ✅ 적중 |
| 파우 토레스 복귀 가능 | ✅ **90분 선발**·어시스트 2 | ✅ 적중 |
| 루제리·완비사카 출전 가능 | 완비사카 **선발**(68분) · **루제리 미출전** | ⚠️ 절반 |
| 고레츠카·만잠비·오나나·하우드-벨리스·마조 결장 | ✅ 전원 출전 명단 밖 | ✅ 적중 |
| 브뤼헤 예상 XI 와이드: **페틀레센·페르만트·디아콘** | 실제 **포브스(우)·베틀레센(중앙)·비르질리(좌)** | ❌ **오류** — 프리뷰가 인용한 예상 XI(Voetbalprimeur·lastwordonsports)는 전방 3명을 전부 틀렸다. obs#482 규약(예상 라인업을 형태 판정에 쓰지 않는다)이 다시 정당화됐다 |
| 브뤼헤 형태 **4-2-3-1**(포츠·바나컨 더블 피벗, 베틀레센 10번) | ⛔ **실제는 4-3-3** — clubbrugge.be 공식·Sporza 원표가 `베틀레센–포츠–바나컨` 미들 3인 + `포브스–트레솔디–비르질리` 전방 3인(**포츠 단독 6번**)으로 적었고, 실측 온볼 x가 **포츠 49.9 < 바나컨 56.5 < 베틀레센 62.9**의 계단 구조로 이를 확인한다. 79분 4-1-4-1 → 88분 4-4-2 | ❌ **오류** — 게다가 SofaScore·FotMob·WhoScored **세 제공사가 모두 템플릿 라벨 `4-2-3-1`을 냈다**(obs#552) |
| 이한범 선발 CB | ✅ **선발 90분**(패스 102건·피패스 85로 브뤼헤 최다급) | ✅ 적중 |
| 트레솔디 주시(잭슨과 프로필 중복 — 내려받아 뒤로 러너) | ✅ **1골(PK)·슛 5·유효 3·크로스바 1·xG 1.07** | ✅ 적중 |
| 「스즈키 선발 시 CL/유러피언컵 최초 일본인 GK」 | 스즈키 **90분 선발**(세이브 5·goalsPrevented +0.59) | ⚠️ 출전은 확인, **「최초」 사실은 §8에서 별도 확인** |
| **카마라 과부하** 우려 — 로테이션 카드가 조앙 고메스뿐 | 카마라 **68분**(90분 아님) → 바클리 교체. 조앙 고메스 90분 | ✅ **적중** — 카마라 부하가 실제로 관리됐다 |

---

## 1. 경기 개요와 원천 수치

| 항목 | Club Brugge | **Aston Villa** |
|---|---|---|
| 점유율 | 64% | **36%** |
| 총 슛 / 유효 / 박스 안 | 14 / 7 / 10 | **21 / 9 / 15** |
| 유효슛 비율 | 50.0% | **42.9%** |
| xG (FotMob) | 1.53 | **3.22** |
| xG 오픈플레이 / 세트피스 / non-penalty | 0.58 / 0.16 / 0.74 | **2.82 / 0.40 / 3.22** |
| xGOT | 2.59 | **3.17** |
| 빅찬스 (놓친 것) | 2 (0) | **4 (2)** |
| 패스 (정확도) | 602 (88%) | **337 (83%)** |
| 자기 진영 / 상대 진영 패스 | 269 / 263 | **162 / 118** |
| 롱볼 | 28/43 (65%) | **20/45 (44%)** |
| 크로스 | 6/27 (22%) | **2/12 (17%)** |
| 코너 | 4 | **5** |
| 공중볼 | 14/19 (74%) | **5/19 (26%)** |
| 드리블 성공 | 10/21 (48%) | **8/13 (62%)** |
| 태클 / 인터셉트 / 클리어 | 17 / 7 / 22 | **23 / 8 / 36** |
| 블록된 슛 | 3 | **7** |
| 파울 / 경고 | 17 / 3 | **14 / 3** |
| **PPDA**(core.whoscored 정의) | **7.08** (262/37) | **12.84** (411/32) |
| **def_x**(라인 높이 프록시) | **42.6** (n=147) | **33.5** (n=176) |
| 포메이션 | ⛔ **4-3-3**(포츠 단독 6번 — 제공사 3곳은 `4-2-3-1`로 라벨했으나 구단 공식·Sporza + 실측이 4-3-3이다, obs#552) → 4-1-4-1(79') → 4-4-2(88') | **4-2-3-1** (전 시간) |
| 공격 존 좌/중/우 (FotMob, 자기 공격 기준) | 32 / 29 / **39** | **34 / 33 / 33** |

**⛔⛔ PPDA 정의 경고.** 이 행의 `ppda_v/o`는 **2026-09-08 신설된 `core.whoscored.PPDA_METHOD` 정본**
정의(분자 x<60 패스 / 분모 x>40 수비액션)를 쓴다. **기존 14행(아스날 30.50·브라이턴 24.69·헐 14.67)은
분모 존이 `x>=60`이라 직접 비교할 수 없다.** 같은 구정의로 이 경기를 재계산하면
**빌라 24.29(413/17) · 브뤼헤 14.56(262/18)** 이며, **기존 시계열과 비교 가능한 값은 이쪽이다.**
⇒ 구정의 기준 빌라 압박은 **헐전 14.67보다 훨씬 약했고**(24.29) 브라이턴전 24.69와 거의 같다.
두 정의를 모두 `ppda_method`에 적어 두었다.

**xG 정합 검증** ✅ — 빌라 3.22 = 오픈플레이 2.82 + 세트피스 0.40, PK 0개로 non-penalty 3.22 = 전체.
브뤼헤 1.53 = 0.58 + 0.16 = non-penalty 0.74, + PK 1개(≈0.79) = 1.53.
⭐ **FotMob과 SofaScore가 xG·슛·패스 전 축에서 완전히 일치**했다(1.53/3.22 · 14/21 · 602/337).
제공사 간 괴리가 없는 드문 경기다. `xg_source='FotMob'`로 고정 기록.

**득점 국면**(빌라 관점) — 리드 **76분** · 동점 **14분** · 추격 **0분**.
0-11' 동점 → 11' 1-0 → 19' 1-1 → 22' 2-1 → 43' 3-1 → 61' 3-2 → 종료.

**교체** — 브뤼헤 46' 시케↔사베 / 77' 르마레샬↔바나컨 · 차와↔베틀레센 / 86' 디아콘↔비르질리 · 페르만트↔포츠.
빌라 **68' 3명 동시**(바클리↔카마라 · 알리송↔부엔디아 · 보가르드↔완비사카) / 81' 아브라함↔잭슨.

**수집 한계** — 히트맵 유효 기준(hit_points 15+)은 15명 중 **14명 통과**
(아브라함 11 → 그리드 무효, `pos_class` NULL). 45분+ 기준은 11명(선발) 통과.
`cross_att_o`·`duelpct_o`는 결손이며 0이 아니다.

---

## 2. 전술 설명

### 점유 구조·빌드업 — 「후방에서 시작해 롱볼로 1선을 넘긴다」

빌라는 점유를 포기했다(36%). 패스 337개 중 자기 진영 162 · 상대 진영 118이고,
**롱볼 45회 시도 20성공(44%)** 이다. 스즈키가 그 축이었다: **총 패스 35개 중 롱볼 15개(43%)**,
성공 5개(**33%**), 자기 진영 패스 21/21(100%)인 반면 상대 진영은 4/14(29%).
즉 **짧게 돌리는 구간은 완벽했고, 1선을 넘기는 구간에서 3분의 2를 잃었다.**

후방 순환의 실제 경로는 피패스 분포가 보여 준다(WhoScored 이벤트 인접 추정):
**린델뢰프 31 · 파우 토레스 31 · 스즈키 26**이 서로를 물려 있고
(린델뢰프→스즈키 10 · 스즈키→린델뢰프 7 · 파우→스즈키 8 · 스즈키→파우 5),
그다음이 **카마라 27**이다. 전방으로 나가는 유일한 다량 경로는 **맥긴 33**인데
그 공급자가 **완비사카 9 · 카마라 4 · 마첸 4 · 린델뢰프 4**다 — 즉 **우측 풀백–우측 와이드 축**이다.

### 비점유 구조·압박 — ⭐⭐ 「4-4-2」가 처음 측정됐다

브뤼헤가 64% 점유로 나와 준 덕에 **헐전에서 「측정 불가」였던 정착 무공 블록이 측정됐다.**
판별 지표는 프리뷰가 사전에 고정한 **「잭슨−부엔디아 수비액션 x 격차」**(0 근접 → 4-4-2 / 15+ → 4-4-1-1)다.

| 층 | 선수 | 수비액션 x 평균 (n) |
|---|---|---|
| **앞줄 2** | **부엔디아 46.0**(14) · **잭슨 45.5**(9) | **격차 0.5** |
| 와이드 2 | 헤밍스 44.7(14) · 맥긴 41.6(16) | |
| 피벗 2 | 조앙 고메스 35.8(22) · 카마라 27.1(18) | 격차 8.7 |
| 백4 | 파우 25.5(15) · 마첸 23.9(13) · 완비사카 19.9(14) · 린델뢰프 17.9(13) | |

⇒ **잭슨−부엔디아 격차 0.5. 사전 등록한 기준으로 4-4-2다.** 4-4-1-1(격차 15+)은 기각된다.
Coaches' Voice가 아스날전에서 서술한 「compact 4-4-2」의 **3번째 표본이고, 첫 실측 표본**이다.

⚠️ **단 미드필드 4는 평평하지 않다.** 와이드 2(41.6~44.7)가 피벗 2(27.1~35.8)보다 **약 10 높다.**
정확히 쓰면 **4-2-2-2에 가까운 4-4-2**이고, 압박 시작선(46)과 백4(약 22) 사이에 24의 폭이 있다.
⇒ **6-2-2 서술(Squawka 단독, 3회차 연속 독립 확인 0건)은 이 실측으로도 지지되지 않는다.**
6-2-2라면 백4+피벗2가 한 줄(6)로 붙어야 하는데 피벗과 백4 사이에 5~14의 층이 남는다.

**팀 라인 높이는 def_x 33.5**로 브뤼헤 42.6보다 **9.1 낮다** — 빌라가 더 내려섰다.
클리어 36 대 22, 블록된 슛 7 대 3도 같은 방향이다.

### 전환·rest-defense·세트피스

**3골 전부 21슛의 중앙 집중과 같은 그림**이다. 빌라 슛 21개의 존 분포는
**중앙 17 · 우 2 · 좌 2**로 극단적으로 중앙이고, 득점 좌표는
맥긴 (x85.7, y27.3 = 박스 우측) · 부엔디아 (93.3, 48.3 = 정면 근거리) · 잭슨 (87.1, 62.4 = 좌중앙).
xG 오픈플레이 2.82 대 세트피스 0.40 ⇒ **오픈플레이 전환이 압도적 산출원**이었다.

**rest-defense**는 68분 3명 동시 교체로 명시적으로 조정됐다. 보가르드가 완비사카 자리에 들어가
**수비액션 x 12.3**(완비사카 19.9보다 더 낮다)으로 내려섰다 — 3-2 리드 관리다.

---

## 3. 전술적 특성

### 반복된 강점

1. **파우 토레스의 좌측 CB 전개가 직접 득점으로 이어졌다.** 어시스트 2·키패스 4·빅찬스 창출 1·xA 0.49·
   롱볼 8/5. 좌측 CB가 한 경기에서 어시스트 2개를 하는 것은 이 저장소 표본에 없던 사건이다.
   `player_duties` id=4의 「좌 하프스페이스로 캐리·패스해 전진」이 **결과로 확인됐다.**
2. **유효슛 문제가 국면 문제였다.** 헐전 13슛 1유효(7.7%) → 이 경기 21슛 9유효(**42.9%**).
   xGOT 3.17이 xG 3.22와 거의 같다 = **슛 질과 마무리가 함께 좋았다.**
   ⇒ 프리뷰 논점 ⑤의 답: **마무리 실력 문제가 아니라 국면(정착 딥블록 vs 전환 공간) 문제였다.**
3. **더블 피벗의 역할 분담이 실측으로 갈렸다.** 카마라 def_x 27.1(남는 쪽) · 조앙 고메스 35.8(전진 쪽),
   격차 8.7. 조앙 고메스가 태클 5·빅찬스 창출 2·키패스 2·xA 0.59로 전진 기여를 담당했다.

### 반복된 취약점과 상대가 만든 교란

1. ⭐⭐ **실점 2건이 모두 빌라 우측(완비사카) 기원이다.**
   - 19분 실점: **비르질리**(브뤼헤 좌측 윙어) 어시스트 → 브뤼헤 좌측 = **빌라 우측**.
   - 61분 실점: **완비사카가 페널티를 헌납**(`penaltyConceded=1`). 68분에 교체됐다.
   ⇒ obs#502(풀백–CB 하프스페이스, 캐시=우측)가 **사람이 바뀌어도 같은 측면에서 재발**했다.
2. ⚠️ **그런데 물량 편중은 반대쪽이었다.** 브뤼헤 공격 존은 **자기 우측 39%**(= 빌라 **좌측**·마첸)
   이고 전반에는 43%였다. 빌라 좌측이 39% · 우측이 32% · 중앙 29%.
   마첸은 9분 경고, 평점 5.9(팀 최저), 볼 소유 상실 13.
   ⇒ **프리뷰의 「3경기 연속 50%+면 obs 승격」 조건은 미충족**(최대 39%)이며,
   더구나 편중 방향이 헐전(캐시=우측 52.4%)과 **반대**다. **양적 편중 가설은 기각 방향**,
   **질적 결손(실점이 나는 쪽)은 우측에서 재확인**이라는 갈림이 남는다.
3. **1선 압박 우회가 실패했다.** 스즈키 롱볼 성공률 33%(5/15) · 팀 롱볼 44% · 상대 진영 패스 118개뿐.
   ⇒ themastermindsite가 지목한 「압박받아도 무조건 후방 빌드업」·「tertiary pass 실패」는
   **실측으로 지지된다.** UTV가 말한 「1선만 넘기면 재미를 본다」는 전제는 **넘기지 못했는데도 이겼다**
   — 승리의 원천은 빌드업이 아니라 **전환과 세컨드볼**이었다.
4. **공중볼 5/19(26%)** — 브뤼헤 14/19의 반대다. 롱볼 전략과 공중 열세가 함께 있다.
5. **빅찬스 2개를 놓쳤다**(헤밍스 2). 헤밍스 슛 4·xG 0.58에 득점 0.

---

## 4. 경기 중 변화

1. **0-11분 (동점)** — 브뤼헤가 예고대로 압박해 나왔다. 마첸 9분 경고가 첫 신호.
   브뤼헤 전반 공격이 자기 우측 43%로 빌라 좌측에 쏟아졌다.
2. **11분 (리드)** — 파우 토레스 → 맥긴. 빌라가 리드를 잡고 블록을 내렸다.
3. **19분 (동점)** — 비르질리(브뤼헤 좌측) → 베틀레센. 브뤼헤가 **반대 측면**으로 들어와 되돌렸다.
4. **22·43분 (리드 확대)** — 조앙 고메스 → 부엔디아, 파우 토레스 → 잭슨. **전반에 3-1.**
   ⇒ 빌라의 전반 xG 산출은 전환에서 나왔고, HT 스코어 1-3이 그것을 확정했다.
5. **46분 브뤼헤 사베→시케** — 브뤼헤가 우측 풀백을 바꿨다(= 빌라 좌측 압력 유지).
6. **61분 (3-2)** — 완비사카 페널티 헌납, 트레솔디 성공. 브뤼헤 xG의 절반(0.79)이 이 한 장면이다.
7. **68분 빌라 3명 동시 교체** — 바클리↔카마라(부하 관리) · 보가르드↔완비사카(PK 헌납 직후) ·
   알리송↔부엔디아. 보가르드 def_x 12.3으로 우측이 더 내려앉았다.
   ⚠️ 교체 후 맥긴이 중앙으로 이동했는지는 **평균 위치만으로 확정할 수 없다**
   (알리송 avg 55.8/29.2 · 맥긴 전체 평균 58.1/28.0 — 둘 다 우측). **미확정으로 남긴다.**
8. **79·88분 브뤼헤가 4-1-4-1 → 4-4-2로** 전환하며 인원을 앞으로 올렸다(WhoScored formations).
   빌라는 **90분 내내 4-2-3-1을 유지**했다.
9. **81분 아브라함↔잭슨** — 9분 출전, 터치 4·공중볼 0/2.

---

## 5. 선수별 분석 — 출전 선수 전원 (15명)

> 평균 위치는 SofaScore(x 공격 방향, y 낮을수록 오른쪽). `def_x`/`poss_x`는 WhoScored 이벤트에서
> 계산한 **수비액션 x 평균 / 보유액션 x 평균**이다(`core.whoscored`).

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치 (def_x / poss_x) | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| **스즈키** | GK | 90 / **7.6** · 세이브 5 · 박스내 피슛 세이브 3 · 하이클레임 3 · goalsPrevented **+0.59** | 9.9 / 51.2 (— / 12.0) | 패스 35 중 **롱볼 15(43%)·성공 5(33%)**. 자기 진영 21/21, 상대 진영 4/14 | `gk_goalkeeper/Defend` **0.966** — obs#154(스위퍼 아님) 재확인 |
| **완비사카** | RB · **전진측** | 68 / 6.9 · 클리어 6 · 태클 3 · **PK 헌납 1** | 42.7 / 15.0 (**19.9** / 53.4) | 맥긴 최다 공급자(9). 실점 2건이 모두 이 측면 기원 | ⭐ `fb_att_wb/Support` **0.863** (정본 `fb_wingback/Balanced` 0.725, **Δ0.138**) |
| **린델뢰프** | RCB | 90 / 6.5 · 패스 40/37(93%) · 클리어 8 | 27.7 / 36.2 (**17.9** / 30.7) | 팀 최저 라인. 스즈키와 상호 17회로 후방 순환 축 | `cb_bpd/Aggressive` **0.892** — 정본 유지 |
| **파우 토레스** | LCB | 90 / **7.6** · **어시스트 2** · 키패스 4 · 빅찬스 창출 1 · xA 0.49 · 롱볼 8/5 · 클리어 8 | 30.6 / 62.4 (25.5 / 34.1) | ⭐⭐ 좌측 CB 전개가 2골을 만들었다. errorLeadToAShot 1 | `cb_bpd/Aggressive` 0.899 vs 정본 **Build-Up 0.887** — **Δ0.012 = 노이즈**, 정본 유지 |
| **마첸** | LB · **잔류측** | 90 / **5.9**(팀 최저) · 9분 경고 · 인터셉트 3 · 소유 상실 13 | 42.4 / 83.7 (23.9 / 49.5) | 브뤼헤 공격 39%(전반 43%)를 받았다 | ⭐ `fb_fullback/Balanced` **0.849** (정본 `fb_att_wb/Support` 0.717, **Δ0.132**) |
| **카마라** | RDM · **앵커** | 68 / 7.2 · 패스 36/34(94%) · 클리어 5 | 37.5 / 41.9 (**27.1** / 43.8) | 더블 피벗의 남는 쪽. 부하 관리 교체 | `dm_holding/Defend` **0.697** — 정본 일치 |
| **조앙 고메스** | LDM · **전진측** | 90 / **7.6** · 어시스트 1 · **태클 5**(팀 최다) · 빅찬스 창출 2 · 키패스 2 · xA 0.59 · 89분 경고 | 47.1 / 52.0 (35.8 / 54.5) | 복귀전에서 즉시 핵심. 카마라보다 def_x +8.7 | `dm_dlp/Roaming` **0.722** (정본 `dm_holding/Roaming` 0.666, Δ0.056 — 노이즈 경계 밖 아슬) |
| **맥긴** | RM | 90 / **7.8** · **1골** · 슛 3(유효 2) · 키패스 4 · 크로스 7 · 태클 4 · 소유 상실 18 · 78분 경고 | 58.1 / 28.0 (41.6 / 62.8) | 피패스 33 팀 최다. 우측 축 | `wm_widemid/Defend` 0.773 vs 정본 **Support 0.758** — **Δ0.015 = 노이즈**, 정본 유지 |
| **부엔디아** | **CAM(중앙 10번)** | 68 / 7.4 · **1골** · **슛 5 · xG 0.95** · 터치 28 | 56.0 / 59.0 (**46.0** / **63.2**) | 관여는 적고 전부 최종 국면(자기 진영 패스 3). 온볼 x가 잭슨보다 **앞** | ⚠️ **모든 조합이 0.43 이하**(argmax `cam_halfwinger/Attack` 0.426 · 정본 `cam_playmaker/Roaming` 0.365, **Δ0.061**). hp=38로 얇다 — 아래 §7 참조 |
| **헤밍스** | LM | 90 / 6.6 · 슛 4 · xG 0.58 · **빅찬스 미스 2** · 파울 유도 4 | 57.2 / 75.9 (44.7 / 60.6) | 배후를 계속 노렸으나 마무리에서 잃었다 | ⭐ `wm_wideplm/Attack` **0.798** (헐전 `wm_winger` 0.613) — **정본과 일치**. 핸드오프의 「wideplm 대안」 검토가 지지됐다 |
| **잭슨** | ST · **하강형** | 81 / 7.3 · **1골** · **xG 1.17(팀 최다)** · 슛 3(유효 2) · 키패스 3 · 빅찬스 창출 1 · 드리블 2/4 | 57.7 / 55.1 (45.5 / **60.7**) | ⭐⭐ 온볼 x가 부엔디아(63.2)보다 **뒤**. 보유액션 37건 중 **x<50이 30% · x<40이 14%**(최저 27.7) | ⭐⭐ `st_false9/Build-Up` **0.625** vs 정본 `st_advanced/Versatile` **0.289**(Δ0.336) · 헐전 `st_advanced/Support` 0.632에서 **반전** |
| 바클리 | 교체 RDM(68', 카마라↔) | 22 / 6.8 · 패스 10/9 · 태클 3 | 41.8 / 58.4 (37.0 / 44.6) | 짧은 표본 | `dm_holding/Roaming` 0.636 (hp 22) |
| 보가르드 | 교체 RB(68', 완비사카↔) | 22 / 6.6 · 패스 9/8 · 유효슛 1 | 32.0 / 20.8 (**12.3** / 32.9) | 리드 관리로 완비사카보다 더 내려섰다 | `fb_fullback/Balanced` 0.863 (hp 16) |
| 알리송 | 교체 RM(68', 부엔디아↔) | 22 / 6.7 · 슛 2(둘 다 블록) · 태클 2 · 인터셉트 1 | 55.8 / 29.2 (38.9 / 63.8) | 짧은 표본 | `wm_winger/Balanced` 0.689 (hp 24) |
| 아브라함 | 교체 ST(81', 잭슨↔) | 9 / 6.1 · 터치 4 · 공중볼 0/2 | 52.3 / 53.8 (49.4 / 50.5) | ⚠️ hp=11 → 그리드 무효 · `pos_class` NULL | fit **미산출**(표본 무효). 임무로 `st_false9/Build-Up` 기재 |

⛔ **`pos_class` 실측 결과가 논점 ①의 독립 증거다.** `core.classify`(포메이션 인식)가
**잭슨을 `CAM`으로, 부엔디아를 `LAM`으로** 분류했다 — 평균 위치만으로도 잭슨은 스트라이커 밴드에
있지 않았다. 맥긴 `RAM` · 헤밍스 `LAM`.

### 상대 대조군 — 트레솔디 (잭슨과 프로필 중복형)

| | 잭슨 | **트레솔디** |
|---|---|---|
| 분 / 평점 | 81 / 7.3 | 90 / **8.0** |
| 슛 / 유효 / xG | 3 / 2 / **1.17** | **5 / 3 / 1.07**(+ 크로스바 1) |
| 온볼 x 평균 (최저) | 60.7 (27.7) | **64.6** (27.4) |
| 보유액션 x<50 / x<40 비율 | **30% / 14%** | 23% / 10% |
| 피패스(추정) | **19** | **28** |
| 공중볼 | 0/0 집계(듀얼 2승) | **3/5 승** |

⇒ **두 하강형 9번 중 트레솔디가 더 앞에 머물고 공급도 더 많이 받았다.**
잭슨의 「배후 러너 부재」가 **선수 유형의 필연이 아니라 팀 공급 구조의 결과**라는 쪽을 지지한다.
단 브뤼헤가 64% 점유였으므로 국면 이점이 트레솔디 쪽에 있었다 — 대조는 **경향 수준**으로만 읽는다.

---

## 6. 전술 변화 판정

### 유지된 것
- **4-2-3-1 기본 형태**(90분 내내, WhoScored formations 변화 0).
- **CB 비대칭**: 린델뢰프 `cb_bpd/Aggressive` 0.892 · 파우 Build-Up 0.887(노이즈 내) — 정본 그대로.
- **더블 피벗 잔류 원칙**: 앵커(카마라 def_x 27.1) + 제한적 전진(조앙 고메스 35.8).
- **LM = 안쪽 창조형**: 헤밍스 `wm_wideplm/Attack` 0.798 — 정본과 일치(헐전 0.613에서 개선).
- **GK 스위퍼 아님**: 0.966.

### 새로 나타난 것
1. ⭐⭐ **무공 4-4-2가 실측으로 확정됐다**(잭슨−부엔디아 def_x 격차 0.5). 단 미드필드 4는
   와이드가 피벗보다 ~10 높은 **4-2-2-2형 스태거**다. **6-2-2는 기각 방향.**
2. ⭐⭐ **풀백 비대칭 좌우 반전** — 우 전진(0.863)·좌 잔류(0.849). 정본은 그 반대다.
3. ⭐ **잭슨 `st_false9` 반전** — 압박 상대에서 false9, 딥블록 상대에서 advanced.
4. ⭐ **라인 높이 실측 최초 확보** — def_x 33.5(빌라)·42.6(브뤼헤).
5. ⚠️ **부엔디아 CAM 커널 적합이 전 조합 0.43 이하로 붕괴** — 터치 28·hp 38의 얇은 표본이지만
   헐전 `cam_classic10/Attack` 0.879과 대비가 크다.

### 직전 경기(헐전) 대비 변화

| 축 | 헐전(PL, 홈 아닌 원정·74% 점유) | **브뤼헤전(CL, 원정·36% 점유)** |
|---|---|---|
| 점유 | 74% | **36%** |
| 유효슛/슛 | 1/13 (7.7%) | **9/21 (42.9%)** |
| 잭슨 역할 | `st_advanced/Support` 0.632 | **`st_false9/Build-Up` 0.625** |
| 좌측 풀백 | `fb_att_wb/Support` 0.903(마첸) | **`fb_fullback/Balanced` 0.849(마첸)** |
| 우측 풀백 | `fb_att_wb/Support` 0.91(캐시) | **`fb_att_wb/Support` 0.863(완비사카)** |
| LM | `wm_winger/Attack` 0.613(헤밍스) | **`wm_wideplm/Attack` 0.798(헤밍스)** |
| 상대 공격 편중 | 캐시(우측) 52.4% | **마첸(좌측) 39%** |
| 무공 형태 | 측정 불가 | **4-4-2 (격차 0.5)** |
| PPDA(구정의) | 14.67 | **24.29** |

### `manager_profiles`·`observations` 반영
- `observations` 신규 7건(§9). ⛔ 기존 obs는 **덮어쓰지 않았다**(불변규칙 2·G14).
- `manager_profiles`(regime 1) 갱신 axis: **formation · pressing · situational · role_demands** —
  §9에 덧붙임 문장을 기록했다.
- ⛔ `prescriptions`·`slot_canon_roles`·`team_tactic_setups` **미변경**(단일 경기 + 대회 축 상이).

---

## 7. 게임 구현 판정

### 결론: **추가 관찰** (정본 변경 없음)

근거: ⑴ 단일 경기다. ⑵ **대회 축이 CL로 달라** PL 시즌 시계열과 직접 합칠 수 없다.
⑶ 36% 점유는 이 체제의 정착 국면이 아니다. ⑷ 반전이 큰 두 축(풀백 비대칭·잭슨 역할)이
**모두 점유율과 함께 뒤집혀** 체제 변화보다 **국면 반응**으로 읽힌다.

### 이 경기 전용 팀 설정 (`match_game_setups`, MATCH ONLY)

| 항목 | 값 |
|---|---|
| 게임 버전 | FC26 |
| 포메이션 | **4-2-3-1 Wide** |
| 빌드업 | **Counter** |
| 수비 접근 | **Balanced** |
| 라인 높이 | **48** |
| tactic_code | (없음) |
| rule_note | **RULE** |

`core.team_settings.suggest(점유 36.0, 패스 337, 롱볼 45, PPDA 12.84)`
→ `Counter / Balanced / 48~58` ⇒ **규칙과 일치**(`RULE`).
라인 높이는 밴드의 **하한 48**을 택했다. 이유 두 가지를 rationale에 남겼다:
⑴ 기존 시계열과 비교 가능한 **구정의 PPDA 24.29**를 넣으면 규칙은 `Deep / 0~45`를 낸다.
⑵ **def_x 실측 33.5**가 상대 42.6보다 9.1 낮다.
⚠️ **def_x → 라인 높이 환산표가 아직 없다**(이 행이 최초 실측). 보정은 표본이 쌓인 뒤로 미룬다.

### 이 경기 선발 11명 (`match_player_prescriptions`, MATCH ONLY)

| 슬롯 | 선수 | 역할 / 포커스 | 단일 경기 fit | 선택 이유 |
|---|---|---|---|---|
| GK | 스즈키 | `gk_goalkeeper` / Defend | **0.966** | 정본·실측 일치 |
| RB | 완비사카 | `fb_att_wb` / **Support** | **0.863** | 정본(`fb_wingback/Balanced` 0.725)과 Δ0.138 — 노이즈 밖. 같은 쪽 맥긴이 `widemid`(복귀형)이라 docs/20 ⑨ 규칙대로 풀백이 전진했다 |
| RCB | 린델뢰프 | `cb_bpd` / Aggressive | **0.892** | 정본 일치 |
| LCB | 파우 토레스 | `cb_bpd` / **Build-Up** | 0.887 | argmax는 Aggressive 0.899이나 **Δ0.012 = 노이즈** ⇒ 정본(Build-Up) 유지 |
| LB | 마첸 | `fb_fullback` / **Balanced** | **0.849** | 정본(`fb_att_wb/Support` 0.717)과 Δ0.132. 같은 쪽 헤밍스가 `wideplm/Attack`(높고 안쪽)이라 풀백이 잔류 |
| RDM | 카마라 | `dm_holding` / Defend | **0.697** | 정본 일치 (def_x 27.1 = 앵커) |
| LDM | 조앙 고메스 | `dm_dlp` / **Roaming** | **0.722** | 정본(`dm_holding/Roaming` 0.666)과 Δ0.056 — 노이즈 경계 바로 밖. 태클 5·xA 0.59의 전진 기여와 정합 |
| RM | 맥긴 | `wm_widemid` / **Support** | 0.758 | argmax는 Defend 0.773이나 **Δ0.015 = 노이즈** ⇒ 정본(Support) 유지 |
| CAM | 부엔디아 | `cam_playmaker` / **Roaming** | **0.365** | ⚠️ argmax는 `cam_halfwinger/Attack` 0.426(Δ0.061). **그런데 hp=38·터치 28로 표본이 얇고**, obs#464의 짝짓기 규칙(halfwinger 옆은 `insidefwd`, playmaker 옆은 `wideplm/widemid`)에서 **와이드 두 칸이 `wideplm`·`widemid`로 강하게 측정**됐다(0.798·0.758) ⇒ 세트 B가 정합적이다. **정본(playmaker/Roaming) 유지**하고 halfwinger는 대안으로 기록 |
| LM | 헤밍스 | `wm_wideplm` / Attack | **0.798** | 정본 일치 (헐전 0.613 → 0.798) |
| ST | 잭슨 | `st_false9` / **Build-Up** | **0.625** | 정본(`st_advanced/Versatile` 0.289)과 Δ0.336. `pos_class=CAM`·온볼 x 60.7(부엔디아 63.2보다 뒤)이 독립 지지 |

교체 4명: 바클리 `dm_holding/Roaming` 0.636(68') · 보가르드 `fb_fullback/Balanced` 0.863(68') ·
알리송 `wm_winger/Balanced` 0.689(68') · 아브라함 `st_false9/Build-Up` **fit 미산출**(hp 11, 81').

### 변경 여부
- ⛔ `slot_canon_roles`·`prescriptions`·`team_tactic_setups` **변경 없음.**
- 근거: 단일 경기 · 대회 축 상이 · 두 반전 축이 점유율과 동시 이동.

### 다음 경기 재검증 항목 (2026-09-12 포레스트전, PL 홈)

| # | 항목 | 판별 기준 |
|---|---|---|
| ① | **잭슨 국면 반응 가설** | 포레스트 상대로 점유가 55%+면 `st_advanced` 쪽으로 되돌아가야 한다. 되돌아가면 obs#446 확정, 그대로 false9면 **체제 변화** |
| ② | **풀백 비대칭 좌우** | 점유 55%+에서 좌 전진·우 절제로 복귀하는가. 복귀하면 obs#449 ⓑ(국면 혼입) 확정 |
| ③ | **무공 4-4-2** | 4번째 표본. 잭슨−(그 자리 10번) def_x 격차. 이번 격차 0.5가 재현되는가 |
| ④ | **부엔디아 CAM 적합 붕괴** | hp 45+ 표본에서도 0.43 이하인가. 그렇다면 CAM 슬롯 기하 재검토 |
| ⑤ | **우측 실점 편중** | 실점·피빅찬스의 발생 측면. 3경기 연속 우측이면 obs#502 승격 |
| ⑥ | **잭슨 피패스 공급자** | 4번째 표본. 두 10번 합이 계속 5 미만인가 |
| ⑦ | **def_x 환산표** | 2번째 라인 높이 실측. 점유·PPDA와의 관계가 보이면 docs/20 규칙에 def_x 축 추가 검토 |

---

## 8. 영상·기사·감독 발언 (§2-1 D+0 회차)

> D+1~D+3 추적은 예약된 후속 회차(`-followup-d1/-d2/-d3`)가 이어서 채운다.
> ⚠️ 유튜브 전사는 **전부 auto-caption**이다 — 단어 단위 인용은 육성 재확인이 필요하다.

### 8-1. ⭐⭐ 에메리 경기 후 회견 (원문 + 번역)

**소스**: `avfc.co.uk` 공식 「Emery: We took a big step forward」·「McGinn hails 'huge' Brugge win」
(2026-09-08, **브라우저 경로로 본문 확보 — WebFetch/curl은 CSR 때문에 빈 응답**) +
BeanymanSports 회견 전체 영상 `dlQTpbG_mxk`(auto-caption 전사) + BBC · Sky · Guardian.

#### ⓐ 잭슨의 임무 — 그리고 가르나초·음바예 미출전에 가장 가까운 답

> 「Of course, he's a striker. **He likes to drop and sometime he needs someone running more than him**
> as well. And we were pushing him the last training session: **"You must try to be the last player
> running in behind"** … and then when we are going to join maybe **Manzambi** as well, when they are
> getting better, **Garnacho, Ibra, they can run as well**, and this is the process we have. But now with
> the player we have on the field, **George is running, he's running in behind, George is helping so so
> much to run in behind with Jackson**.」
> (번역: 물론 그는 스트라이커다. **그는 내려받기를 좋아하고 때로는 자기보다 더 뛰어주는 누군가가
> 필요하다**. 그리고 우리는 지난 훈련에서 그를 밀어붙였다 — **「너는 배후로 뛰는 마지막 선수가 되려고
> 해야 한다」** … 그리고 **만잠비**가 합류하고 **그들이 좋아지면 가르나초, 이브라(음바예)도 뛸 수 있다**.
> 이것이 우리가 가진 과정이다. 그러나 지금 필드에 있는 선수로는 **조지(헤밍스)가 뛴다, 그가 배후로
> 뛴다, 조지가 잭슨과 함께 배후로 뛰는 걸 아주 많이 돕고 있다**.)

⇒ ⭐⭐ **회견 어디에도 「왜 가르나초를 안 쓰나」라는 직접 질문은 없었다**(영어·스페인어 모두 확인).
그런데 에메리가 **잭슨 질문에 답하다 두 이름을 스스로 호명**했고, 프레임은 **전술 부적합이 아니라
「배후 러너 자원, 준비 중」**이다. ⇒ obs#553. 또 이것은 **obs#440(헤밍스의 최종라인 와이드 기능은
지정 설계인가 대안 부재인가)에 감독 본인이 「둘 다」로 답한 것**이다.

#### ⓑ 설계 자기진단 — 헐전과의 차이를 「배후 러닝」으로 특정

> 「We needed a lot of duels offensively, **run in behinds. We were lack of running behind as well the
> last match in Hull City and today we did more**, and we crafted chances, we have got their box and we
> score goals.」
> (번역: 우리는 공격적으로 많은 듀얼과 **배후 침투가 필요했다. 지난 헐 시티 경기에서도 배후 러닝이
> 부족했고 오늘은 더 많이 했다**. 그리고 기회를 만들었고, 그들의 박스에 들어갔고, 골을 넣었다.)

> 「Yesterday we were in the training session and we were being demanding even in the training session
> playing a small match. **We are lack of goals and we must even score here goals** — please, each one be
> demanding yourself to score here in the training session with the small goals.」
> (번역: 어제 훈련에서 우리는 작은 경기를 하면서도 요구 수준을 높였다. **우리는 골이 부족하고 여기서라도
> 골을 넣어야 한다** — 각자 이 훈련에서 작은 골문에라도 득점하도록 자기 자신에게 요구하라.)

#### ⓒ 개인 이름 평가 — obs#484가 반증 방향으로 움직인다

> 「**All the players were giving to the team: John McGinn, Emiliano Buendía, Pau [Torres], Victor
> Lindelöf, and the young players as well like [George] Hemmings, who is new and progressively getting
> better and understanding everything we demand.** So are Aaron Wan-Bissaka, Ian Maatsen, Boubacar
> Kamara.」 (avfc.co.uk 공식)
> (번역: **모든 선수가 팀에 기여했다 — 존 맥긴, 에밀리아노 부엔디아, 파우 토레스, 빅토르 린델뢰프,
> 그리고 새로 와서 점점 나아지고 우리가 요구하는 모든 것을 이해해 가는 조지 헤밍스 같은 젊은 선수들도.**
> 애런 완비사카, 이안 마첸, 부바카르 카마라도 그렇다.)

> 「And Aaron Wan-Bissaka, after the injury of Cash, very important — **but he was so, so tired. This is
> the first match after a long time.**」
> (번역: 그리고 캐시의 부상 이후 완비사카는 매우 중요했다 — **그러나 그는 몹시, 몹시 지쳐 있었다.
> 오랜만의 첫 경기다.**)

⇒ **8명을 호명해 수행을 평가**했다. obs#484(「개인 이름 평가 0건 = 구조적 부재」)는 **폐기가 아니라
조건 축소 후보**로 올렸다(obs#554) — 표본이 1경기이고 **원정 UCL 승리**라는 특수 국면이다.

#### ⓓ 교체 준비성 — 본인이 인정한 반복 문제

> 「In the dressing room the first half we were speaking about some players — they were tight, **Kamara,
> Wan-Bissaka, both especially**. I tried to keep 50 minutes how we were, but when I asked the players to
> replace them **they were with the set pieces, with their individual issues — but I needed quick their
> impact on the field**, and they did it after.」
> (번역: 하프타임 라커룸에서 우리는 몇몇 선수에 대해 이야기했다 — 그들은 뻣뻣했다, **특히 카마라와
> 완비사카 둘**. 나는 50분까지 그대로 가려고 했지만, 교체할 선수들을 불렀을 때 **그들은 세트피스를
> 보고 있었고 개인 문제를 처리하고 있었다 — 나는 그들의 임팩트가 즉시 필요했다**. 이후엔 해줬다.)

⭐ **Guardian(Ben Fisher, 현지 취재)이 이를 계열화했다**: 「At Hull last weekend, it was Tammy Abraham
and Wan-Bissaka, and a few days earlier **Alejandro Garnacho against Arsenal**. This time the culprits
were Alysson, Ross Barkley and Lamare Bogarde.」
⇒ **가르나초·음바예 미출전에는 세 갈래 설명이 병존한다**: ⓐ 감독 = 러너 자원·준비 중 ⓑ Guardian =
**교체 준비 미비** ⓒ 팬·분석 채널 = **국면 논리**(수세 국면 교체는 피지컬·시스템 숙지 우선).
⛔ 어느 하나로 단정하지 않았다(obs#553).

#### ⓔ 그 외

> 「We had a fantastic first half. We had so many chances to get more of an advantage. … When we were 2-0
> ahead the confidence was very good, but Brugge scored and we could feel a little bit less confidence.
> But we finished well, **controlling the game like we planned**.」
> (번역: … 우리는 잘 마무리했고 **계획대로 경기를 통제했다**.)

⭐ **맥긴 본인의 마무리 설명**(avfc.co.uk, UCL Player of the Match):
> 「**Pau Torres made a great run through the middle** and I just tried to **use the defender to elevate
> the goalkeeper's sight line**, so I just passed it in the corner. **As I've got older, I've tried to use
> that finish a lot more and just place it in the corner rather than smashing it.**」
> (번역: **파우 토레스가 중앙으로 훌륭하게 침투했고** 나는 **수비수를 이용해 골키퍼의 시야선을
> 들어올리려** 했다 — 그래서 그냥 구석으로 패스했다. **나이가 들면서 이 마무리를 훨씬 더 많이 쓰려
> 한다 — 세게 때리는 대신 구석에 놓는 것이다.**)
> ⭐ 맥긴은 이 골로 **구단 유럽 대회 역대 최다 득점자**가 됐다(12골, 왓킨스 11 추월).

### 8-2. ⭐⭐ 이반 레코 경기 후 회견 — **프리뷰의 미결 과제가 닫혔다(단, 언어가 예상과 달랐다)**

⭐⭐ **프리뷰는 「레코 회견 원문 전문 미확보(🇳🇱 네덜란드어 요약 경유, confidence LOW-MEDIUM)」를
과제로 남겼다. 실제로는 레코가 사후 회견을 영어로 진행했다** — 구단 공식 유튜브 라이브
`B-9hoJZf9rQ`(Club Brugge, 「LIVE | PERSCONFERENTIE NA CLUB BRUGGE - ASTON VILLA」, 2026-09-08)의
자막 트랙이 **`en-orig`(영어 원본)** 이고 네덜란드어는 번역 트랙이다.
⇒ **이 과제는 네덜란드어가 아니라 영어로 닫힌다.** 어떤 네덜란드어 매체에도 회견 전사는 없었고,
`clubbrugge.be` 공식 반응 기사는 **레코를 아예 싣지 않고** 세이스·바나컨·트레솔디·메헬레만 실었다.

> 「For me it was **not bad first half**. It was so much **cadeaus** [gifts] — it was never a game how I
> see football. It was not a game that our opponent was smashing us, we couldn't give two passes, we
> couldn't pass the middle line. **But I agree with you absolutely that three, four or even five
> situations what we gave it away create this feeling that we are really bad first half.**」
> (번역: 내게 전반은 **나쁘지 않았다**. **선물**이 너무 많았다 — 내가 보는 축구로는 결코 그런 경기가
> 아니었다. 상대가 우리를 짓밟아 패스 두 개도 못 하고 하프라인도 못 넘긴 경기가 아니었다.
> **그러나 우리가 내준 3, 4, 심지어 5개의 상황이 「우리가 전반 정말 나빴다」는 느낌을 만들었다는 데는
> 절대적으로 동의한다.**)

> ⭐ 「Especially in second half, if we now want to say — this was in a lot of moments **like handball**:
> we put them **in close to their box that they couldn't go out except counter attacks**. … Expensive
> lesson, I would say. I think also **Villa they deserve to win because they had better chances**.」
> (번역: 특히 후반은 많은 순간 **핸드볼 같았다** — 우리는 그들을 **자기 박스 근처에 몰아넣어 역습
> 말고는 나올 수 없게 했다**. … 값비싼 수업료라 하겠다. **빌라가 이길 자격이 있었다고 생각한다,
> 더 좋은 기회를 가졌으니까.**)
> ⇒ ⭐ **상대 감독이 「빌라의 후반 자발적 딥블록」을 바깥에서 확인해 준 진술**이다.

> 「When it is to read the game, we are saying before the game two words: **brave and smart** — and this
> balance between brave and smart. Yeah, it was sometimes not perfect today.」
> (번역: 경기를 읽는 문제라면, 우리는 경기 전에 두 단어를 말한다 — **용감하게, 그리고 똑똑하게**.
> 그리고 그 둘 사이의 균형. 오늘 그것이 때때로 완벽하지 않았다.)

> ⛔ **선제골에 대한 레코의 인과 주장(자기 변호 가능성)**:
> 「What I saw in the first goal … **my two, three players stopped to play because it was one player
> down**, and then they were expecting that the opponent will wait … **Those are when I was saying brave
> and smart — I was thinking about this first goal.**」
> (번역: 첫 골에서 내가 본 것은 … **내 선수 두세 명이 한 선수가 쓰러져 있었기 때문에 플레이를
> 멈췄다**는 것이고, 그들은 상대가 기다릴 거라고 예상했다 … **내가 「용감하고 똑똑하게」라고 말한 게
> 바로 이런 것 — 나는 이 첫 골을 생각하고 있었다.**)
> 메헬레(CB)가 🇳🇱 네덜란드어로 구체화했다(Voetbalkrant 현장, 2026-09-08 21:18):
> 「Volgens ons werd het spel stilgelegd door een hoofdblessure. **Vetlesen raakte het hoofd van
> Buendia**, waardoor we dachten dat het spel zou worden stilgelegd. Maar de scheidsrechter fluit niet en
> het gaat door. Dan wordt het te gemakkelijk.」 / 「**Het kan niet dat hij helemaal kan indribbelen.**」
> (번역: 우리 생각엔 머리 부상으로 경기가 중단될 상황이었다. **베틀레센이 부엔디아의 머리를 맞혔고**
> 그래서 중단될 줄 알았다. 그런데 주심이 불지 않고 계속됐다. 그러면 너무 쉬워진다. /
> **그가 그렇게 끝까지 드리블해 들어올 수 있다는 건 있을 수 없다.**)
> ⚠️ FotMob은 이 골을 그냥 `RegularPlay`로 분류했다. **미해소 — 영상 확인 항목**(obs#555).

> 조머 옹호: 「**He's for me probably in this moment the best transfer what we had — not only on quality
> but on mentality, on leadership.** So if you will have more Yann Sommers in the dressing room I would be
> very happy.」 (번역: 그는 지금 우리가 한 최고의 이적일 것이다 — 품질만이 아니라 멘털리티, 리더십에서.
> 라커룸에 얀 조머가 더 있다면 아주 기쁠 것이다.)

> ⭐ 포츠(단독 6번) 진단 — 🇳🇱 네덜란드어판이 더 전술적이다(Voetbalkrant, 2026-09-08 23:30):
> 「Freddie maakt één of twee **dure fouten**. Hij komt ook uit een zware competitie waar er anders wordt
> gespeeld. **Hij is goed met de bal, maar kiest te veel voor een tikje breed.** Hier moet je totaal
> anders spelen en daar moet hij zich aan aanpassen, net als andere nieuwe spelers zoals **Lee** en Jan
> Virgili.」
> (번역: 프레디는 **값비싼 실수** 한두 개를 했다. 그는 다르게 플레이하는 힘든 리그에서 왔다. **그는 볼을
> 잘 다루지만 옆으로 짧게 빼는 선택을 너무 많이 한다.** 여기서는 완전히 다르게 플레이해야 하고 그가
> 적응해야 한다 — **이(한범)**와 얀 비르질리 같은 다른 새 선수들도 마찬가지다.)

🇫🇷 벨기에 프랑스어권(L'Avenir, Louis Janssen, 2026-09-08 22:28)이 같은 회견의 프랑스어판을 실었다:
> 「**À un moment, nous jouions au handball autour de leur grand rectangle.** Un point aurait été beau
> pour les gars, mais Villa a mérité de gagner. **La leçon était chère.**」
> (번역: **한때 우리는 그들의 박스 주변에서 핸드볼을 하고 있었다.** 승점 1은 선수들에게 훌륭했겠지만
> 빌라가 이길 자격이 있었다. **수업료가 비쌌다.**)

⚠️ **미확보**: `hln.be`·`nieuwsblad.be`·`gva.be` 3개 도메인은 크롤러 차단 + JS-only 렌더링으로 본문
직접 확보 실패. HLN 취재분은 voetbalnieuws.be 재인용 경로로만 확보했다(「Het gevoel dat overheerst, is
dat **we gefaald hebben**」 = 지배적 감정은 우리가 실패했다는 것이다). confidence MEDIUM.

### 8-3. 영상 (채널 · 제목 · 게시일 · URL/ID · 확인 방식)

| 채널 | 제목 | 게시일 | ID | 확인 방식 |
|---|---|---|---|---|
| ⭐⭐ **Club Brugge**(공식) | LIVE \| PERSCONFERENTIE NA CLUB BRUGGE - ASTON VILLA | 2026-09-08 | `B-9hoJZf9rQ` | **auto-caption(en-orig) 전사** |
| ⭐⭐ BeanymanSports | EMERY: "I AM SO, SO HAPPY TODAY!" — Club Brugge 2-3 Aston Villa | 2026-09-08 | `dlQTpbG_mxk` | **auto-caption 전사** |
| ⭐⭐ Bains Analysis | Unai Emery Found Aston Villa's Cheat Code (5:22) | 2026-09-08 | `z3QtUD65Jiw` | **auto-caption 전사 · 전술 그래픽 포함** |
| ⭐ **UTV \| Aston Villa Fan Channel** | CLUB BRUGGE 2-3 ASTON VILLA \| MATCH REACTION (25:45) | 2026-09-08 | `mlw5BA0WlyM` | auto-caption 전사 |
| ⭐ **1874 : The Aston Villa Channel** | Match Reaction: Aston Villa See Off Club Brugge in CL Opener! (18:46) | 2026-09-08 | `c6oW6AHlnBM` | auto-caption 전사 |
| **The Villans**(@TheViIIans) | — | — | — | ⛔ **사후 영상 0건**. 채널 업로드 8건을 직접 열거해 확인(최신 = 09-07 프리뷰) |
| CBS Sports Golazo | Nicolas Jackson discusses FIRST GOAL (에메리·맥긴·잭슨·레코·조머 통합) | 2026-09-08 | `zK8FAlqDTnQ` | **설명란 챕터 기준 — 미시청** |
| Virgin Media Sport | Highlights: Club Brugge vs Aston Villa | 2026-09-08 | `EA11nWmEUPs` | 미시청 |
| Justin Talks Villa / For The Love of Paul McGrath / The Holy Trinity Show / Shouts From The Stands | 각 사후 리액션 | 2026-09-08 | `w6qr6jijVgg`·`vAbbatV61zM`·`UDRx19AGtL0`·`VQTPenq7xbc` | 미시청 |

⛔ **브뤼헤 쪽·벨기에 전술 분석 채널 0건.** 시도한 검색어(전부 유튜브 사이트 내부 검색
`&sp=EgIIAw%3D%3D` = 이번 주 업로드): `Club Brugge Aston Villa analyse Leko` ·
`Club Brugge Aston Villa nabeschouwing` · `Club Brugge Champions League Leko persconferentie` +
`ytsearch`로 `Club Brugge Aston Villa reactie` / `analyse` / `Brugge Aston Villa Leko`.
결과는 하이라이트 스팸·eFootball 시뮬레이션·18/19 오염 영상이었다. **@clubbrugge 채널 업로드 8건을
직접 열거**한 결과 관련은 「EUROPEAN TOUR」 브이로그 2편 + 위 회견 라이브뿐이며 전술 분석은 없다.

#### 핵심 전술 서술

⭐ **Bains Analysis — 브뤼헤 압박 도식을 그래픽으로 특정**
> 「Club Brugge's press was very, very poor. … essentially **Forbs — the Club Brugge right winger —
> trying to jump onto Pau Torres, which kind of forced the Club Brugge right back to jump onto Maatsen.
> The right centre-back was trying to go on to Hemmings — but they were just so slow in that jump**, and
> Pau Torres just found it so easy to get the ball and drive.」
> (번역: 브뤼헤의 압박은 매우 형편없었다. … 요컨대 **브뤼헤 우측 윙어 포브스가 파우 토레스에게
> 점프하려 했고, 그것이 브뤼헤 우측백을 마첸에게 점프하게 만들었다. 우측 센터백은 헤밍스에게 나가려
> 했다 — 그런데 그 점프가 너무 느렸다.**)
> 「**Pau Torres, instead of going towards the left, takes it the other direction and Club Brugge did not
> know how to deal with him**, and then finds a pass to McGinn.」

> ⭐ 「Suzuki — **he's an absolute cheat code**. … **you don't know which direction he's going to go.** …
> **He's both-footed. He is a cheat code when it comes to build-up. … Emiliano Martínez could not do
> this.**」 (번역: 스즈키는 **완전한 치트코드**다 … **어느 방향으로 갈지 알 수 없다** … **그는 양발이다.
> 빌드업에 관해선 치트코드다 … 에밀리아노 마르티네스는 이걸 못 했다.**)

> ⭐⭐ 「one of the midfielders pushing on to the final line was **Vanaken. He's 34, he's not the most
> athletic** … he's not going to get back. … **You can see the average position, especially in the first
> half: look at the midfielders — Kamara was the one holding, João Gomes was clearly the one pushing
> forward**, and he found it so easy.」
> (번역: 최종라인까지 올라간 미드필더 중 하나가 **바나컨이었다. 34세이고 운동능력이 가장 좋지 않다** …
> 돌아오지 못한다. … **평균 위치를 보라, 특히 전반 — 미드필더를 보면 카마라가 잔류한 쪽이고,
> 조앙 고메스가 분명히 전진한 쪽이었다.**)
> ⇒ ⭐⭐ **우리 def_x 실측(카마라 27.1 / 조앙 고메스 35.8, 격차 8.7)과 독립적으로 일치한다.**

> 「Especially in the second half [Wan-Bissaka] really struggled. **Virgili was really causing him a lot
> of problems. Seys was making those overlapping runs** … You saw **Kamara trying to get close to
> Wan-Bissaka to help him out**. … Wan-Bissaka back post — **he will be caught sleeping. That's just
> Wan-Bissaka's game.**」

⭐ **UTV — 스즈키 롱볼의 2차 효과**
> 「those long ones that loop over with pace: **when these defenders are getting under it, it's spraying
> off their head, going out for a throw-in — and then we're able to pin them in a zone again.**」
> (번역: 페이스를 얹어 넘기는 롱볼들은 **수비수가 밑으로 들어가려 하면 머리에서 튀어 스로인이 되고 —
> 그러면 우리는 다시 그들을 한 존에 몰아넣을 수 있다.**)
> ⇒ 팀 공중볼 승률 **26%**와 함께 읽으면 제공권이 아니라 **2차볼 위치**를 노린 설계다.
> 잭슨 처방: 「**you get the best out of Jackson: you feed him the ball, you have runners running off
> him**」 / 완비사카: 「**he failed to block a cross for the goal we conceded — he got his feet all
> wrong**」 / 가르나초·음바예: 「**When we were defending like that under the kosh, was Mbaye the right
> sub? I don't think so.**」

⭐ **1874 — 잭슨 하강을 3골 모두에 연결**
> 「Everything good Villa did, **he was involved in every goal**. … **Jackson just giving that option,
> drops deep for the first goal, [and for] the third goal, the one he scored.** He gives Pau Torres that
> angle to play a kind of mini-diagonal and puts him through on goal. … **Pau's picked up two assists
> tonight — I don't even know if he's ever had an assist for Villa before.**」
> 맥긴 골: 「**his hold-up play, playing the back-heel that led to the goal, was absolutely amazing**」
> 보가르드 투입: 「**he's much more aware of Unai's system, he knows that right-back role**」

### 8-4. 전술 블로그 — 사이트 내부 색인을 직접 열어 확인

| 사이트 | 확인 경로 | 결과 |
|---|---|---|
| **Coaches' Voice** | `learning.coachesvoice.com/category/analysis/` 1페이지 육안 | ⛔ MD1 분석 없음. ⭐⭐ **다만 과거 3회 「0건」은 경로 오류였다 — `/analysis/`는 404이고 정본은 `/category/analysis/`다.** 26/27 빌라 자료는 실재한다(아래) |
| The Football Analyst | 홈 최신 피드 | ⛔ 최신 글 2026-01-28 |
| Breaking The Lines | `/`, `/arena/` | ⛔ **공개 아카이브 소멸** — B2B로 전환, 공개 분석 피드 자체가 없다 |
| Spielverlagerung | .com 홈 | ⛔ 최신 글 2026-07-19 |
| themastermindsite | `?s=Aston+Villa`(결과 8건) | ⛔ 최신 빌라 글 **2025-12-29** — 티엘레망스 10번·로저스·왓킨스 기준이라 **현재 적용 불가** |
| Between The Posts | 홈 최신 5건 | ⛔ 없음 |
| Total Football Analysis | `/teams/club-brugge` · `/teams/aston-villa` 색인 전문 | ⛔ 양쪽 26/27 없음. 브뤼헤 최신 = 2026-04-18 **포브스 스카우트 리포트**(하옌 체제이나 개인 프로필은 유효) |
| 🇧🇪 Lange Bal | 홈 | ⛔ 휴면(최신 2019-08-16) |
| 🇧🇪 **VoetbalPrimeur.be** | `/zoeken?q=Aston Villa` | ✅ **이 경기 유일한 전용 전술 분석** |

⭐ **VoetbalPrimeur.be 「Potts zoekt zichzelf, Tresoldi blijft scoren: drie lessen na Club Brugge -
Aston Villa」**(2026-09-08 22:18) — 우리 대조군 질문의 직답이 교훈 ②다:
> 「Toch oogt de Duitser dit seizoen een stuk vaker **geïsoleerd**. Club vindt hem **minder gemakkelijk
> in de opbouw** en ook vanaf de flanken komt er **minder constante aanvoer**. … Met hen had Tresoldi
> **automatismen**… Club moet er vooral opnieuw in slagen om zijn spits **vaker en beter in stelling te
> brengen**.」
> (번역: 그럼에도 이 독일인은 올 시즌 훨씬 자주 **고립되어** 보인다. 브뤼헤는 **빌드업에서 그를 덜 쉽게
> 찾고**, 측면에서의 **공급도 덜 일정하다**. … 그들(촐리스·스탄코비치)과는 트레솔디에게 **자동화된
> 패턴**이 있었다… 브뤼헤는 무엇보다 자기 스트라이커를 **더 자주, 더 잘 슈팅 위치에 놓는 데** 다시
> 성공해야 한다.)
> 교훈 ③: 「Bij de 0-1 mocht Pau Torres **haast ongehinderd vanuit zijn eigen helft richting de Brugse
> zestien oprukken. Niemand voelde zich geroepen om uit te stappen**」(0-1 때 파우 토레스는 자기 진영에서
> 브뤼헤 박스까지 **거의 방해 없이 전진할 수 있었다. 아무도 나가서 막을 책임을 느끼지 않았다**)
> ⇒ ⭐ **레코의 「선수들이 플레이를 멈췄다」와 자기 매체의 「구조 결손」이 같은 장면에서 갈린다.**

⭐ **Coaches' Voice 26/27 빌라 자료**(경로 정정으로 확보) — 「Aston Villa 0 Arsenal 1: Tactical
analysis」(2026-09-01), `learning.coachesvoice.com/cv/aston-villa-arsenal-tactics-august-2026/`
> 부엔디아 = 「**arriving from deeper positions to combine and create, or attack crosses from Jackson**」
> (**더 깊은 위치에서 도착해** 연계·창출하거나 잭슨의 크로스를 공격)
> 스즈키 = 「**a high level of quality with his distribution to drive the ball into these areas,
> bypassing Arsenal's aggressive pressing structure**」(그 지역으로 볼을 밀어 넣는 배급의 질이 매우
> 높았고, **아스날의 공격적 압박 구조를 우회했다**)
> ⇒ ⭐ **스즈키 롱볼 = 압박 우회 해법의 2번째 독립 표본**이고, 부엔디아는 **「박스 도착형」 쪽 서술**이다.

### 8-5. 기사·전담 기자

- **John Townley**(birminghammail, 2026-09-08) — 스즈키 6 「**Outstanding distribution again**」 /
  ⭐ 카마라 7 「**He allowed Gomes to venture further forward tonight**」 / 마첸 7 「**Defended well
  against the tricky Forbs** despite being on a yellow card」 / 부엔디아 7 「**gobbling up Gomes' ball
  across the box**」 / ⭐ 2분 첫 기회의 시발점을 스즈키 롱볼로 특정 「goalkeeper Zion Suzuki **pinged a
  perfect long ball to Aaron Wan-Bissaka**」
- **Ben Fisher**(Guardian, 현지 취재) — 「McGinn's opener was a product of the **centre-back roaming
  unchallenged to the edge of the box**」 / 잭슨 골 「**Jackson got in between the opposition
  centre-backs, Lee Han-beom and Brandon Mechele. Enter Sommer, who raced about 40 yards from goal.**」 /
  19분 실점 「the lively **Jan Virgili found a way past Wan-Bissaka** … and located Hugo Vetlesen in the
  box」
- **BBC**(Nick Mashiter) — 카마라 7 「**made more passes than any other Villa player**」 / 완비사카 5
  「**He could not stop the cross for Brugge's equaliser**」
- **Sky Sports** — 「**Nicolas Jackson thrives on running in behind, which is how he scored his goal**」
- **Opta / theanalyst**(Harry Carr) — 「Buendía **ghosted in** and clipped João Gomes' cutback past
  Sommer」. 빌라 xG **3.00**(FotMob 3.22 대비) · **CL·유러피언컵 하프타임 리드 시 9승 0패** ·
  CL 통산 28경기 18승(승률 64.3%, 10경기 이상 팀 중 역대 최고)
- **avfc.co.uk 공식 리포트** — ⭐ 「Zion Suzuki, who became the **first Japanese goalkeeper to play in the
  competition**」(구단 공식 확인)

### 8-6. ⭐⭐ 언어축별 수확 (불변규칙 10) — 쓰지 않은 언어권은 사유를 남겼다

| 언어 | 대표 검색어 | 결과 | 0건 사유 / 제약 |
|---|---|---|---|
| 🇳🇱 **네덜란드(1차축)** | `Leko reactie` · `"gefaald" "dure les" cadeaus` · `spelersbeoordelingen rapport` · `tactische analyse pressing halfruimte` 외 13건 | ⭐⭐ **최대 수확** — clubbrugge.be 공식 선수 반응 4인 · Sporza 실황 전문 · Voetbalkrant 현장 4건 · **VoetbalPrimeur 「3가지 교훈」** · 평점표 12인 | ⛔ hln.be·nieuwsblad.be·gva.be **크롤러 차단 + JS-only** → 재인용 경로만. ⛔ **레코 전사는 네덜란드어에 없다 — 영어 회견이 정본** |
| 🇯🇵 **일본** | `鈴木彩艶 チャンピオンズリーグ ブルージュ` · `日本人GK 初 CL` · `ロングキック` | ⭐⭐ **최대 수확** — 「**일본인 GK 사상 첫 CL 출전**」 3개 독립 매체 확정(게키사카·스포니치·사커다이제스트) + **롱패스 압박 회피 메커니즘 직접 서술** + 세이브 로그 | 본인 경기 후 코멘트 0건 |
| 🇰🇷 **한국** | `이한범 챔피언스리그` · `이한범 평점` · `스즈키 젠 챔피언스리그` | ⭐ **실질 수확**(헐전 0건에서 반전) — 이한범 평점 3종·터치 114 양팀 최다·공중볼 4/4·**드리블 돌파 허용 0**·실점 무과실 정리 (머니투데이·MHN·스포츠경향·서울경제) | ⛔ 「일본인 GK 최초」를 다룬 한국 기사 0건 |
| 🇩🇪🇨🇭 **독일·스위스** | `Sommer Brügge Fehler` · `Goretzka Verletzung` · `Tresoldi Hannover` | ⭐⭐ **최대 수확** — 조머 원문 + ⭐ **잭슨 본인 원문**(아래) + **고레츠카 = 왼쪽 무릎 자극(Reizung), 10월 복귀** (Blick·Tagesanzeiger) | ⛔ Kicker·NDR·HAZ의 트레솔디 이 경기 기사 0건. ⚠️ Blick 요약에 「KI-generiert」 라벨 — **본문(기명)만 인용** |
| 🇫🇷 **프랑스** | `Kamara L'Équipe` · `Leko` | ⭐ **초과 달성** — 벨기에 프랑스어권 **L'Avenir이 최고 품질 소스**(레코 회견 프랑스어 전문 + 「Potts a laissé Torres **transpercer l'entrejeu d'une course de 40 mètres**」) | ⛔ **L'Équipe·RMC·Foot Mercato의 카마라 기사 0건** |
| 🇮🇹 **이탈리아** | `Tresoldi rigore` · `pagelle` | **서사 성공 / 경기 부분** — ⭐ **국적 스위치**(독일 U21 24경기 12골 → 이탈리아 A대표 선택, FIFA 절차 개시) · 부친 에마누엘레 = 전 아탈란타 LB · 브뤼헤 호가 €50m, **로마 €35m 거절** | ⛔ Gazzetta·Corriere **페이월+JS**(브라우저도 빈 body). 린델뢰프 이탈리아 링크 0건 |
| 🇪🇸 **스페인** | `Emery Brujas rueda de prensa` · `Garnacho suplente` · `Buendía` · `Virgili` | **부분** — EFE 통신 전문(브뤼헤 좌측 편향 명시) · 비르질리 **마요르카 출신** 확정(€12m) | ⛔⛔ **MARCA·AS·Relevo·MD·Sport.es·El Desmarque가 크롤러를 도메인 차단**(API 400). 「기사 없음」이 아니라 **접근 불가** — 사람이 직접 열어야 닫힌다 |
| 🇦🇷 아르헨티나 | `Buendía Brujas Champions` | 성공 — 득점·교체·빌라 유럽 통산 5골 (Diario Río Negro) | Olé·TyC·Clarín 미노출 |
| 🇸🇳 세네갈 | `Jackson wiwsport` | 성공 — 잭슨 본인 발언. ⭐ **25/26 바이에른 임대 때도 브뤼헤 상대 CL 득점** = 두 클럽으로 같은 상대 득점 | ⚠️ Wiwsport이 잭슨을 「교체 투입」으로 오기 |
| 🏴󠁧󠁢󠁳󠁣󠁴󠁿 스코틀랜드 | `McGinn record` | 성공 — 유럽 12골 역대 1위, 별명 「**McGinnedine Zidane**」 (The Scotsman·Sky) | Daily Record·Herald·BBC Scotland 직접 노출 0 |
| 🇵🇹 포르투갈 | `Forbs` · `João Gomes` | 부분 — 포브스 90분, 후반 트레솔디에게 크로스 2회 (Record 라이브) | ⛔ O Jogo 403 + 브라우저 추출 실패, A Bola·Maisfutebol 0건 |
| 🇸🇪 **스웨덴** | `Lindelöf Aftonbladet` · Expressen · Fotbollskanalen · SVT | ⛔ **실패(0건)** | 4대 매체 전부 이 경기 노출 0. 대체 노출은 **콘텐츠팜(hurbra.se, AI 생성 의심)이라 폐기**. ⇒ **다음 회차 우선순위 하향**(단 결장·이적 국면에서는 재개) |
| 🏴 바스크 | `euskara Emery` · Naiz · Berria | ⛔ **0건** | 바스크어 매체 이 경기 취재 미노출 |

⭐ **선수 1차 발언 — 잭슨의 43분 골은 「롱볼 운」이 아니라 조건부 트리거였다**(🇩🇪 Blick, Alain Kunz):
> 「**Ich hatte den Goalie schon das ganze Spiel über weit vor der Linie stehen sehen. Als Pau mich
> lancierte, lief alles perfekt.**」
> (번역: 나는 **경기 내내 골키퍼가 라인에서 한참 앞에 서 있는 것을 봐 왔다**. 파우가 나를 발사했을 때
> 모든 것이 완벽하게 진행됐다.)
> ⇒ ⭐ **빌라의 롱패스 트리거가 상대 GK 라인 높이에 조건화**돼 있다는 1차 증거다.
> 「우연한 GK 실책」으로 감쇠 처리하면 이 설계를 놓친다.

조머(🇩🇪 Blick): 「**Ich muss im Tor bleiben!** Ich dachte, der Ball komme schneller. Aber er kam nicht
schneller. **Zudem standen zwei unserer Verteidiger gegen nur einen Stürmer.**」
(번역: **나는 골문에 머물러야 했다!** 공이 더 빨리 올 거라 생각했는데 아니었다. **게다가 우리 수비수
두 명이 공격수 한 명을 상대하고 있었다.**)

### 8-7. ⛔ 서사 회차가 남긴 「신뢰도 경고」와 정정

1. ⛔ **브뤼헤 형태는 4-3-3이다** — 제공사 3곳의 라벨이 틀렸다. `formation_o`를 정정하고 obs#552에 기록.
   §0-1 대조표도 ❌로 고쳤다.
2. ⛔ **이 경기의 커널·전술 판정 신뢰도를 낮춰 잡아야 한다**(obs#555) — 브뤼헤 선수단 4인이 「구조가
   뜯긴 게 아니라 개인 실책」이라고 진술했고, **조머가 3실점 중 2개에 직접 연루**됐다
   (`errorLeadToAGoal=1`).
3. ⭐ **obs#544 정밀화**(obs#551) — 무공 4-4-2 앞줄 2인은 **「서 있되 따내지 않는」 차단·유도형**이다.
   광의 수비액션 23건 중 **협의(태클·인터셉트·클리어·블록패스)는 3건**뿐이고 볼 탈취는 뒤에서
   일어났다(조앙 고메스 12·카마라 8). ⚠️ **FotMob의 「수비액션」 지표는 협의 정의라 부엔디아 0·잭슨 1로
   보이며, 그 값만 보면 「6-3-1 저블록」으로 오독된다** — 두 지표는 모순이 아니라 서로 다른 것
   (위치 대 탈취량)을 측정한다. 위치 실측이 6-3-1을 기각한다.
4. ⚠️ **완비사카 실점 2건의 메커니즘 재기술**: obs#502의 「풀백–CB 하프스페이스 침투」가 아니라
   **「RB 대인 1대1 돌파 + 박스 내 마킹 상실」**이다. 감쇠 요인 3건(캐시 결장 대체 첫 선발 · 감독이
   인정한 하프타임 피로 · 카마라의 보조 이동).
5. ⚠️ **완비사카 평점이 소스 간 극단적으로 갈린다**(FotMob 7.19 vs BBC 5·UTV 5) — **평점을 근거로 쓰지
   말고 실점 좌표·역할로만 판정**한다.
6. ⚠️ **부엔디아 롤은 텍스트로 결정할 수 없다** — 전 소스가 「박스 도착형」인데 DB 기존 서술은
   「라인 사이 수신형」이다. 25/26 로저스 기준 서술을 26/27 부엔디아에 승계한 것이 아닌지 재검증 필요.
7. ⚠️ **영상 육성 확인 3건 미해소**: ⑴ 에메리 「he's not the player with qualities to running behind」의
   지칭 대상(부엔디아 vs 잭슨) ⑵ 세이스 침투가 오버랩인지 언더랩인지 ⑶ 11분 골 직전 브뤼헤가 실제로
   플레이를 멈췄는지.
8. ⚠️ **점유·xG 제공사 충돌**: 점유 FotMob 36% / Sky 35% / readastonvilla 39%. xG FotMob 3.22 /
   Opta 3.00. ⇒ **FotMob 원값을 정본으로 고정**(`xg_source='FotMob'`), Opta는 대조.

### 8-8. 미수행·미도달 소스와 사유

- ⛔ **스페인어 정본 미확보** — 스페인 주요 6개 매체가 **크롤러를 도메인 차단**. 에메리 회견의 스페인어
  원문과 「가르나초 직접 질문 여부」는 이 축에서만 닫힌다. **사람이 직접 열어야 한다.**
- ⛔ 🇧🇪 `hln.be`·`nieuwsblad.be`·`gva.be` 동일 차단 + JS-only(재인용 경로만, MEDIUM).
- ⛔ 🇮🇹 Gazzetta·Corriere의 트레솔디 pagelle — 페이월 + JS.
- ⛔ **UEFA.com 공식 리포트 미획득**(matchId 미확보, 404).
- ⚠️ **전사 5건이 임시 디렉터리에만 있다**(`/tmp/ytsub/`: `B-9hoJZf9rQ`·`dlQTpbG_mxk`·`z3QtUD65Jiw`·
  `mlw5BA0WlyM`·`c6oW6AHlnBM`). **전부 auto-caption**이며 `reports/transcripts/`로 정식 보존하는 것은
  별도 작업으로 남긴다(D+1 회차 후보).
- ⛔ 🇸🇪 스웨덴어·🏴 바스크어 0건(위 표에 검색어 기록).

---

## 9. 데이터 반영과 한계

### DB에 추가한 행

| 테이블 | 행 | 비고 |
|---|---|---|
| `matches` | **1** (id=99) | event_id **16938841**(SofaScore) · competition **UEFA Champions League** · stage `League Phase MD1` · venue A · result `2-3`(홈-원정 순) · possession 36.0 |
| `team_match_stats` | **1** | `xg_source='FotMob'` · `ppda_v` 12.84 / `ppda_o` 7.08 · **`def_x_v` 33.5 / `def_x_o` 42.6**(저장소 최초) |
| `player_matches` | **15** | 출전 전원. `cells_poss`/`cells_def`/`map25_poss`/`map25_def`/`phase_source` **최초 적재**(2026-09-08 신설 축) |
| `match_reports` | **1** | status `complete` |
| `match_player_reports` | **15** | |
| `match_game_setups` | **1** | `match_only=1` · `rule_note='RULE'` |
| `match_player_prescriptions` | **15** | 선발 11 + 교체 4 |
| `observations` | **13** | 실측 회차 7(#544~550) + 서사 회차 6(#551~556). §아래 |
| `player_duties` | **11 덧붙임** | 선발 11명 전원(#121·87·199·22·29·89·27·25·96·88·86) — ⛔ 새 행이 아니라 **기존 행 뒤에 덧붙임**(G14 prefix 보존) |
| `manager_profiles` | **6 axis 덧붙임** | formation·pressing·situational·role_demands(실측) + buildup·rotation(서사) |

### 한계

1. ⛔⛔ **대회 축.** CL 1경기다. PL 3경기 추세(무득점·헐전 13슛 1유효)와 **같은 시계열로 읽으면 안 된다.**
2. **36% 점유는 이 체제의 정착 국면이 아니다.** 브라이턴전 27%·아스날전 39%와 같은 대역이고,
   헐전 74%와는 반대 극이다. 역할 반전 2건이 이 축과 함께 움직였다.
3. ⚠️ **피패스(공급자) 수치는 추정이다.** WhoScored 이벤트에서 **성공 패스의 직후 이벤트 주체를
   수신자로 본** 근사이며, 헐전의 14회(영상 낭독 경유)와 **측정 방법이 다르다.**
   두 값을 같은 시계열로 쓰지 말고 방법 표기와 함께 읽는다. confidence MEDIUM.
4. ⚠️ **PPDA 정의가 갈렸다.** `core.whoscored` 정본(신)과 기존 14행(구)의 분모 존이 다르다.
   저장 컬럼은 신정의이고, 구정의 값(24.29/14.56)은 `ppda_method`에 병기했다.
5. **부엔디아·아브라함 표본이 얇다**(hp 38 · 11). 아브라함은 그리드 무효로 fit 미산출.
6. **def_x → 라인 높이 환산 근거가 없다**(첫 실측). 팀 설정 라인 값은 규칙 밴드 내에서 정했다.
7. 68분 3명 동시 교체 후의 **맥긴 위치 이동은 미확정**으로 남겼다.

### 새 observations

| obs | scope | 요지 |
|---|---|---|
| **#544** | defence | ⭐⭐ **무공 4-4-2 실측 확정** — 잭슨−부엔디아 def_x 격차 0.5. 6-2-2 기각 방향, 단 미드필드 4는 4-2-2-2형 스태거 |
| **#545** | in_possession | ⭐⭐ **잭슨 st_false9 반전** — obs#446(국면 반응) 강한 지지, obs#505 재검증 지표로 판정 |
| **#546** | in_possession | ⭐⭐ **풀백 비대칭 좌우 반전** — obs#449 ⓑ(국면 혼입) 지지 |
| **#547** | defence | **실점 2건 모두 우측 기원 · 물량 편중은 좌측 39%** — obs#502의 양·질 분리 |
| **#548** | build_up | **1선 압박 우회 실패 실측** — 스즈키 롱볼 33%, 상대 진영 패스 118 |
| **#549** | verdict | **유효슛 문제는 국면 문제였다** — 7.7% → 42.9%, xGOT 3.17 |
| **#550** | reference | ⛔ **PPDA 신·구 정의 비교 불가** — 분모 존 x>40 vs x>=60 |
| **#551** | defence | ⭐ **obs#544 정밀화** — 4-4-2 앞줄 2인은 「서 있되 따내지 않는」 차단·유도형(협의 수비액션 3건/23건). FotMob 협의 지표로 보면 「6-3-1」로 오독된다 |
| **#552** | reference | ⛔⛔ **브뤼헤 형태는 4-3-3** — 제공사 3곳 라벨 오류, 구단 공식·Sporza + 실측 계단(포츠 49.9<바나컨 56.5<베틀레센 62.9)이 일치 |
| **#553** | role_demands | ⭐⭐ **에메리 1차 발언** — 하강형 9번의 배후 러너 요구는 임시 부하이며 러너 자원(만잠비·가르나초·음바예)이 준비되면 이전된다. obs#440에 「둘 다」로 답 |
| **#554** | verdict | ⚠️ **obs#484 반증 방향** — 8명 호명 평가. 「승리·유럽 국면」으로 조건 축소 후보 |
| **#555** | reference | ⛔ **상대 선수단 4인이 「개인 실책」으로 진술** — 이 경기 커널 판정 신뢰도 하향 사유 |
| **#556** | in_possession | ⭐ **트레솔디 대조군 확정** — 하강형 9번의 산출은 러너 구조의 함수(같은 경기 A/B) |

`manager_profiles`(regime 1) 덧붙임 axis 6종: 실측 회차 **formation · pressing · situational ·
role_demands** + 서사 회차 **buildup · rotation** (`content || '\n\n[2026-09-08 …]'`,
`updated`=2026-09-09). ⛔ 덧붙임만 — 기존 문장 미변경(G14 통과).
`player_duties` 11행도 **덧붙임만**이며 prefix를 보존했다(G14 보호 테이블).

### G12·게이트

- `python3 scripts/gates.py` — §종료 보고 참조.

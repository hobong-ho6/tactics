# 2026-09-19 Tottenham Hotspur 2-3 Aston Villa — 원정 승, 시즌 최저 라인(def_x 30.6)

> 수집일 2026-09-19 · SofaScore event `16363870` · WhoScored matchId `1983589` · FotMob matchId `5795464`
> 프리미어리그 2026-27 R5 · 원정 · 4-2-3-1 Wide (90분 불변)

---

## 1. 경기 개요와 원천 수치

| 항목 | 빌라 | 토트넘 |
|---|---|---|
| 점유율 | **36%** | 64% |
| xG (전체) | **1.16** | 1.22 |
| xG 오픈플레이 | **1.16** | 0.65 |
| xG 세트피스 | **0.00** | **0.57** |
| xGOT | 1.76 | 1.90 |
| 슈팅 (유효) | 15 (6) | 20 (7) |
| 박스 안 슈팅 | 9 | 12 |
| 빅찬스 (실패) | 2 (1) | 3 (1) |
| 패스 (정확) | 331 (278·84%) | 571 (497·87%) |
| 상대 진영 패스 | **102** | **308** |
| 롱볼 시도(성공) | 48 (24·50%) | 33 (15·45%) → **롱볼 비율 14.5%** |
| 코너 | **1** | **11** |
| 클리어 | **37** | 10 |
| 태클 / 인터셉트 | 18 / 14 | 35 / 9 |
| 지상경합 승 | 37 (40%) | 56 (60%) |
| 상대 박스 터치 | 18 | 31 |
| **PPDA** | **13.24** (331/25) | 6.17 (284/46) |
| **def_x (라인 프록시)** | **30.6** (표본 160) | 45.5 (표본 149) |
| 파울 / 경고 | 13 / 2 | 9 / 1 |

**득점 국면**

| 분 | 팀 | 득점 | 어시스트 | xG | 국면 | 이후 스코어 |
|---|---|---|---|---|---|---|
| 45+4′ (49′) | AVL | 만잠비 | 카마라 | 0.316 | assisted, 박스 안 좌측 | 0-1 |
| 67′ | AVL | 잭슨 | 만잠비 | 0.060 | assisted | 0-2 |
| 79′ | AVL | 부엔디아 | 맥긴 | **0.024** | assisted, **박스 밖 26.2** | 0-3 |
| 86′ | TOT | 갤러거 | 쿠두스 | 0.172 | 오픈플레이 | 1-3 |
| 90+8′ (98′) | TOT | 판 헤케 | 로버트슨 | 0.213 | **set-piece 헤더** | 2-3 |

킥오프 직전 **에메리 경고**(벤치, 이벤트상 −5′ 표기). 교체: 46′ 완비사카→캐시 · 72′ 만잠비→헤밍스 ·
84′ 카마라→음바예, 맥긴→바클리 · 88′ 잭슨→아브라함. 토트넘 교체 19′ 포로→그레이(부상 추정),
46′ 페르난데스→쿠두스, 66′ 솔란케→매디슨, 84′ 토날리→갤러거·벤탄쿠르→베리발.

**수집 엔드포인트·결손**

- SofaScore `/api/v1/event/16363870/{lineups,average-positions,incidents,statistics,shotmap}` — 출전 16명 전원 실측, `match_events` 19건, `match_shots` 35건.
- FotMob `/api/data/matchDetails?matchId=5795464` — **xG 4종(전체·오픈플레이·세트피스·xGOT)을 한 응답에서 동시 수집**(`xg_source='FotMob'`). SofaScore 전체 xG와 소수 둘째 자리까지 일치해 스냅샷 혼합 없음.
- WhoScored matchCentreData `matchId=1983589`(Opta, 이벤트 1,583건) — **PPDA·def_x·국면 분리 그리드**. 파생 대상 이벤트 1,464건을 `core.whoscored`로 처리.
- 유효 히트맵 기준(45분+ · hit_points 15+): **통과 12명**. 캐시(45′, hp 13)·헤밍스(18′, hp 9)·음바예(15′, hp 5)·아브라함(11′, hp 6)은 리포트 근거로만 쓰고 시즌 처방 집계에서 뺐다.
- 결손: 없음(dribbles·clearances까지 FotMob에서 보충). 토트넘 선수 개인 실측은 수집 범위 밖(관리 4팀 축 밖 — 불변규칙 7).

---

## 2. 전술 설명

### 점유 구조·빌드업

점유 36%·패스 331(84%)·**롱볼 비율 14.5%**로 시즌 최고 다이렉트 수치다(종전 최고는 브라이턴 원정 15.4%,
브뤼헤 원정 13.4%). 상대 진영 패스가 **102회**에 그쳤다 — 토트넘 308회의 3분의 1이다.
즉 빌라는 90분 중 대부분을 자기 진영에서 보냈고, 전진은 패스 축적이 아니라 **한 번에 넘기는 전달**로 했다.

스즈키가 볼 터치 57·패스 38회로 백4와 함께 1차 순환에 참여했지만, 성공률 22/38(58%)이 말해주듯
그 참여의 대부분은 **의도적 롱킥**이었다. 브뤼헤전에서 정식화된 「상대 맨투맨 하이프레스 → 의도적 GK
백패스 → 스즈키 롱킥」 경로(manager_profiles.buildup, 2026-09-09)가 그대로 재현됐다.
토트넘의 PPDA 6.17은 이 시즌 빌라가 만난 압박 중 가장 강한 축이다(브뤼헤 7.08, PSG 8.5, 아스날 8.17).

좌우가 비대칭이었다. **루헤리(LB)가 보유 국면 셀 22개를 상대 진영 좌측(행0~2·열0)에 찍은 반면**
완비사카·캐시(RB)는 전반 내내 자기 진영 우측에 머물렀다(완비사카 보유 셀의 절반이 행3·열4).
즉 「풀백은 한 번에 한 명만 전진한다」는 잔류 수비 원칙(manager_profiles.rest_defense)이
**좌측 고정 전진**으로 나타났다. 밍스가 좌측 열0~1에서 보유 셀 19개를 찍은 것도 같은 축이다 —
좌측 3인(밍스·루헤리·부엔디아)이 전진 통로였다.

### 비점유 구조·압박

**def_x 30.6은 26/27 시즌 빌라의 최저치다**(종전 최저 브뤼헤 원정 33.5, 홈 포레스트전 43.0).
수비 액션 평균 지점이 자기 골문에서 30.6% 지점이라는 뜻으로, `optimal:vs-strong` 프리셋의
라인 43보다도 낮다. PPDA 13.24는 중간 대역(8~18)이지만 상단이다 — **압박하지 않고 물러서서 닫았다.**

클리어 37회(토트넘 10회)와 코너 허용 11회(빌라 1회)가 같은 구조의 결과다. 블록이 깊으니
박스 안 경합이 늘고, 걷어내면 다시 코너가 됐다. 토트넘 슈팅 20개 중 **코너 국면에서 나온 것이 8개**
(포로 11′·사비우 21′·토날리 34′·솔란케 34′·솔란케 66′·토날리 70′·쿠두스 76′·판 더 펜 95′)로,
xG 세트피스 0.57의 출처다.

국면 분리 그리드가 4-4-2 블록을 다시 확증한다: 수비 액션이 **잭슨 행0~1 / 부엔디아·맥긴 행1~3 /
피벗 2 행3 / 백4 행3~4**로 층이 뚜렷하다. 특히 **맥긴의 수비 셀 11개 중 9개가 우측 열3~4**,
**루헤리의 수비 셀 28개 중 18개가 좌측 열0~1의 행3~4**에 몰렸다 — 측면을 각자 막고 중앙은 피벗이 닫는,
브뤼헤전과 같은 4-2-2-2형 스태거다.

### ⭐⭐ 후반 우측 편중 백5 — 감독 자인 + 실측 (2026-09-19 D+0 서사 반영, 당일 판정 정정)

**처음 이 리포트는 「5-3-2 전환은 관측되지 않았다」고 적었다. 그것은 틀렸다.**
경기 후 회견에서 **에메리 본인이 후반 백5를 인정**했고, WhoScored 이벤트를 전·후반으로 나누니 실측도 맞는다.

> 원문 「sometimes with back four is not enough to defend completely the … side of the field,
> and someday we are the first half we use it more **[Kamara] dropping dropping**, and someday is
> **a five center back** being in the back four inside, and **the second half we needed more with John McGinn**.」
> (때로는 백4로는 측면을 완전히 수비하기에 충분하지 않다. 어떤 날은 전반처럼 **카마라를 더 내려서** 쓰고,
> 어떤 날은 **센터백 5명**이 백4 안쪽에 들어가는 형태가 된다. 그리고 **후반에는 존 맥긴으로 더 필요했다**.)
> — TNT Sports `k6dbBj7Tz7w` (2026-09-19), ⚠️ **auto-caption** — 「camera」는 Kamara의 오인식.

**실측(WhoScored matchId 1983589, 수비액션 159건을 전·후반으로 분리)**

| | 전반 | 후반 | Δ |
|---|---|---|---|
| **맥긴 수비액션 x** | 56.3 (n3) | **32.1** (n8) | **−24.2** |
| 맥긴 수비액션 y | 32.8 | **18.2** (우측 터치라인) | −14.6 |
| 부엔디아 수비액션 x | 35.6 (n6) | **47.6** (n14) | **+12.0** |
| 팀 def_x | 32.3 (n69) | 29.5 (n90) | −2.8 |

맥긴은 **후반 57′·58′·77′에 x 11.8 · 14.1 · 16.2에서 수비**했다 — 같은 시간대 백4 라인
(캐시 17.4 · 린델뢰프 16.5 · 밍스 15.2 · 루헤리 21.4)과 **같은 깊이**다. 전반에는 그 대역 수비액션이 0건이었다.

다만 **대칭 5-3-2가 아니다.** 좌측의 부엔디아는 반대로 12점 올라갔다. 즉 이 경기의 후반 형태는
**우측만 5로 만든 편중 백5**(캐시 + 맥긴이 우측 채널을 겹쳐 막고, 좌측은 4를 유지)다.
에메리 발언의 「side of the field」(측면)가 단수인 것과 정합한다.

⭐ 가장 깊었던 구간은 **경기 막판이 아니라 50~86′(def_x 26.1)**이다. 교체 4장 이후(87′~)는 오히려 34.6으로
올라간다 — 「리드를 지키려 더 내려앉았다」는 통상 서사와 반대이고, 두 실점이 그 올라간 구간에서 나왔다.

주앙 고메스가 태클 5·경합 8승8패로 피벗의 파괴 몫을 전담했고(파울 13회 중 상당수가 이 축),
카마라는 42패스·터치 48로 배급 쪽에 섰다. **피벗 두 명의 역할이 갈렸다** — 종전 「둘 다 dm_holding 계열」
서술과 어긋나는 첫 실측 신호다(§6에서 판정).

### 전환·rest-defense·세트피스

3골 전부 **오픈플레이**이고(빌라 세트피스 xG 0.00), 이 중 2골이 상대 진영 회수 직후 3~5초 안에 끝났다.
fast-break로 분류된 슈팅도 3개(만잠비 31′·잭슨 56′·58′)다. 즉 이 경기의 공격 산출은
**빌드업이 아니라 전환**에서 나왔다 — 오픈플레이 xG 1.16이 전체 xG와 같다는 사실이 그것을 단독으로 증명한다.

79′ 부엔디아의 세 번째 골은 **박스 밖 26.2 지점 xG 0.024**다. 25/26 시즌 「중거리 슈팅을 의도적 무기로
편입(박스 밖 9골 리그 1위)」한 패턴(manager_profiles.situational)의 26/27 첫 재현이다.

rest-defense는 리드 국면에서 의도적으로 더 내려앉았다. 다만 대가가 명확했다 —
**86′·90+8′ 두 실점이 모두 리드 3-0 이후**에 나왔고, 마지막 실점은 세트피스 헤더였다.
90+8′까지 갔다는 것은 전반에 쌓인 파울 13회·경고 2장의 시간 소모가 마지막에 되돌아왔다는 뜻이다.

---

## 3. 전술적 특성

**반복된 강점**

1. **저점유 원정 전환 승리의 재현.** 브뤼헤 원정(36% 점유·롱볼 13.4%·2-3 승)과 이 경기(36%·14.5%·2-3 승)는
   점유율·다이렉트 비율·스코어까지 같다. 강팀·원정에서 에메리는 **점유를 포기하고 전환을 산다** —
   상황 대응 진폭(PPDA 4.99~30.5)의 하단 운용이 두 번 연속 성공했다.
2. **좌측 고정 전진.** 루헤리·밍스·부엔디아 3인이 전진 통로를 전담하고 우측은 잠갔다. 우측 전진을
   포기한 대가로 rest-defense 인원이 유지됐고, 역습 실점은 0이었다(두 실점 모두 정지 국면·세트피스).
3. **부엔디아의 양면 부하.** 태클 6·경합 10승·키패스 3·골 1로 공수 양쪽 최다다. LM 슬롯에서
   수비 셀 20개를 찍으면서도 공격 3선에 남았다.

**반복된 취약점**

1. **세트피스 수비.** 코너 11개 허용, 코너 국면 피슈팅 8개, 세트피스 실점 1. 리그 4R 포레스트전
   후반 붕괴와 같은 계열의 문제다(그때도 후반 2실점). **저블록 → 클리어 37회 → 코너 → 세트피스 실점**은
   구조적으로 연결된 사슬이지 우연이 아니다.
2. **리드 후 관리.** 3-0에서 2골을 내줬다. 시즌 들어 리드 국면 실점이 반복된다.
3. **빌드업 정확도.** 패스 성공률 84%·상대 진영 패스 102회는 리그 하위권 수치다. 압박을 벗어나는 수단이
   롱킥 하나뿐이면 상대가 세컨볼을 정리할 때 되돌릴 방법이 없다(지상경합 40% 승률).

**상대가 만든 교란** — 토트넘은 PPDA 6.17의 강한 전방 압박과 11코너로 빌라를 자기 진영에 묶었다.
빌라의 def_x 30.6은 「선택」이면서 동시에 「밀려난 결과」다. 두 해석이 공존하며, 구분 근거는
**리드 이전(0-0 국면)에도 이미 깊었는가**인데 전반 슈팅 6-9·코너 0-6으로 **리드 전부터 깊었다** —
선택 쪽에 무게가 실린다.

---

## 4. 경기 중 변화

1. **0-0 (1′~45+3′)** — 토트넘이 코너 6개·슈팅 9개로 몰아쳤고 빌라는 슈팅 5개·xG 0.28에 그쳤다.
   스즈키 선방 2회(사비우 11′ 두 차례)가 스코어를 유지했다. 빌라의 유일한 위협은 전환(만잠비 15′·31′,
   잭슨 28′ xG 0.126).
2. **리드 전환 (45+4′)** — 카마라의 전진 패스에서 만잠비가 박스 좌측에서 마무리(xG 0.316, 이 경기 최대).
   하프타임 직전 득점으로 후반 운용 선택지가 통째로 바뀌었다.
3. **교체·역할 변화**
   - **46′ 완비사카 → 캐시 (RB)**: 하프타임 교체. 완비사카 45분 hp 37 → 캐시 45분 hp 13으로
     **우측 관여가 3분의 1로 줄었다**(터치 33 → 10). 우측을 아예 봉쇄 모드로 돌린 조정이다.
   - **72′ 만잠비 → 헤밍스 (CAM)**: 득점·어시스트를 모두 기록한 만잠비를 2-0 리드에서 뺐다.
   - **84′ 카마라 → 음바예 · 맥긴 → 바클리**: 음바예가 RM으로 들어가고 **바클리가 맥긴 자리가 아니라
     카마라의 피벗 자리로 내려갔다**(평균 위치 x 35.1 — 맥긴 52.4가 아니라 카마라 40.3 쪽). 3-0에서
     중앙 2를 새로 세우는 잠금 교체다.
   - **88′ 잭슨 → 아브라함 (ST)**: 시간 소모·공중 경합 교체.
4. **마지막 국면 (84′~90+8′)** — 교체 4장 직후 2실점. 갤러거 86′(오픈플레이)·판 헤케 90+8′(세트피스 헤더).
   교체로 들어간 4명의 합산 터치가 27회뿐이고 경합 패가 11회다 — **새로 들어간 인원이 볼을 지키지 못했고,
   그 결과 마지막 10분이 통째로 토트넘 진영이 아니라 빌라 진영에서 진행됐다.**
   ⚠️ 단 **수비액션 def_x는 이 구간에 26.1 → 34.6으로 올라간다.** 「더 내려앉아서 실점했다」가 아니라
   **블록이 오히려 풀렸다**는 뜻이다. 갤러거의 슛은 캐시를 맞고 굴절됐고(Reuters·NBC), 판 헤케는
   로버트슨 배급을 받은 파포스트 헤더다.

---

## 5. 선수별 분석 — 출전 선수 전원

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치·히트맵 | 특성·수행 | FC 역할/포커스 함의 (단일 경기 fit) |
|---|---|---|---|---|---|
| 스즈키 지온 | GK — 롱킥 출구 겸 최종 수비 | 90′ 7.0 · 선방 5 · 패스 38(22·58%) · 터치 57 · 회수 12 · 클리어 4 | (9.8, 51.4) · 자기 박스 행4 중앙 46셀 집중 | 전반 사비우 2연속 선방으로 0-0 유지. 패스 성공률이 낮은 것은 실책이 아니라 **의도적 롱킥 58%** | `gk_goalkeeper/Defend` **0.9876** (2위 Balanced 0.9774, **Δ0.010 — 실측 무결정**) |
| 린델뢰프 | RCB — 우측 잠금, 전진 최소 | 90′ 6.2 · 패스 28(26·93%) · 클리어 4 · 인터셉트 1 · 터치 37 | (25.7, 35.9) · 자기 진영 우중앙 | 터치 37회로 백4 최소. 우측을 전진 통로에서 뺀 설계의 결과이지 부진이 아니다 | `cb_bpd/Aggressive` **0.9496** (2위 Build-Up 0.9172, Δ0.032 — 무결정) |
| 밍스 | LCB — 좌측 전진 통로의 출발점 | 90′ 7.0 · **클리어 10** · 패스 45(41·91%) · 터치 58 · 회수 3 | (26.1, 68.9) · 좌측 열0~1 보유 19셀 + 자기 박스 수비 9셀 | 저블록의 공중·박스 방어를 전담하면서 좌측 빌드업 첫 패스도 맡았다 | `cb_bpd/Build-Up` **0.9269** (2위 Defend 0.8878, Δ0.039 — 무결정) ⚠️ 시즌 정본은 `Aggressive` |
| 마테오 루헤리 | LB — 좌측 고정 전진 + 저블록 좌측 수비 | 90′ 6.4 · **인터셉트 5 · 클리어 8 · 회수 9** · 패스 33(30·91%) · 터치 66 · hp **80(최다)** | (33.1, 85.6) · 보유 셀 22개가 상대 진영 좌측, 수비 셀 28개 중 18개가 자기 진영 좌측 | 공수 양방향 최다 관여. **한쪽 풀백만 전진** 원칙의 그 한쪽 | `fb_fullback/Balanced` **0.9247** (2위 Versatile 0.8804, Δ0.044 — 무결정) ⚠️ 시즌 정본은 `fb_att_wb/Support` |
| 주앙 고메스 | LDM — 파괴 전담 피벗 | 90′ 6.8 · **태클 5 · 경합 8승8패** · 인터셉트 3 · 패스 25(23·92%) | (38.3, 64.3) · 중앙~좌측 행1~3 | 피벗 중 파괴 몫. 볼 배급은 카마라에게 넘기고 앞으로 나가 끊는 역할 | `dm_holding/Roaming` **0.7759** (2위 Defend 0.7253, Δ0.051 — 유일하게 무결정 밖) |
| 부엔디아 | LM — 공수 양면 최다 부하 | 90′ **8.2** · **골 1 · 태클 6 · 경합 10승** · 키패스 3 · 슈팅 3(유효 2) · 터치 58 | (46.4, 72.1) · 5×5 전 구간 분산(행0~4 모두 기록) | 79′ 박스 밖 26.2 지점 결승골(xG 0.024). 수비 셀 20개로 LM 중 최다 | `wm_widemid/Defend` **0.6252** (2위 Support 0.6129, **Δ0.012 — 무결정**) ⚠️ 시즌 정본은 `wm_wideplm/Attack` |
| 잭슨 | ST — 전환 출구 + 1선 압박 유도 | 88′ 7.7 · **골 1 · 슈팅 6(유효 2) xG 0.44** · 경합 6승10패 · 패스 12(12·100%) | (65.6, 55.1) · 행0~1 좌우 분산, 중앙 고정 아님 | 최전방 고립을 넓게 움직여 풀었다. 경합 10패는 저점유 최전방의 구조적 비용 | `st_advanced/Support` **0.7022** (2위 `st_false9/Build-Up` 0.6648, Δ0.037 — 무결정) ⚠️ 시즌 정본은 `st_false9/Attack` |
| 카마라 | RDM — 배급 전담 피벗 | 84′ 7.0 · **어시 1** · 패스 42(35·83%) · 터치 48 · 태클 2 | (40.3, 41.4) · 중앙~우측 행2~3 | 45+4′ 선제골의 시발 패스. 파괴는 고메스에게 넘기고 전진 패스를 맡았다 | `dm_holding/Roaming` **0.8453** (2위 `dm_dlp/Roaming` 0.819, Δ0.026 — 무결정) ⚠️ 시즌 정본은 `dm_dlp/Roaming` |
| 맥긴 | RM — 우측 봉쇄 + 세 번째 골 어시스트 | 84′ 6.6 · **어시 1** · 키패스 3 · 패스 19(12·63%) · 경합 1승6패 | (52.4, 28.5) · 우측 열3~4, 수비 셀 11개 중 9개가 우측 | 패스 성공률 63%는 우측이 전진 통로가 아니었음을 보여준다. 대신 79′ 결정적 컷백 | `wm_widemid/Defend` **0.6915** (2위 Support 0.6573, Δ0.034 — 무결정) ⚠️ 시즌 정본은 `wm_winger/Attack` |
| 만잠비 | CAM — 전환 국면 1차 출구 | 72′ **7.8** · **골 1 · 어시 1 · 슈팅 4(유효 2) xG 0.44 · xA 0.156** · 키패스 2 | (55.6, 46.6) · 행0~2 중앙~우측 | 선제골(xG 0.316)과 두 번째 골 어시스트. 이 경기 산출 최다 기여 | `cam_playmaker/Build-Up` **0.6314** (2위 Roaming 0.6219, **Δ0.010 — 무결정**) ⚠️ 시즌 fc26:opt는 `cam_halfwinger/Balanced` |
| 완비사카 | RB — 우측 봉쇄(전반) | 45′ 6.8 · 태클 2 · 인터셉트 2 · 패스 17(16·94%) · 터치 33 · hp 37 | (40.6, 17.7) · 우측 열4 집중 | 전반 우측을 단독으로 닫았다. HT 교체는 부상 여부 미확인(§8) | `fb_wingback/Balanced` **0.8405** (2위 `fb_att_wb/Support` 0.8035, Δ0.037 — 무결정) |
| 캐시 | RB — 우측 봉쇄(후반), 극단 저관여 | 45′ 5.8 · 터치 **10** · 패스 4(2) · 클리어 3 · 92′ 경고 · hp 13 | (27.8, 16.8) · 우측 열4 자기 진영만 | 터치 10회는 45분 필드 플레이어로는 극단값. 봉쇄 지시로 읽히지만 볼 지연·경고까지 포함된 결과 | `fb_wingback/Support` 0.7768 (2위 Balanced 0.7722, **Δ0.005 — 무결정**) ⚠️ hp 13 — 대표 그리드 제외 |
| 헤밍스 | CAM — 72′ 교체, 시간 관리 | 18′ 6.2 · 터치 7 · 패스 2(2) · 태클 1 · 경합 1승3패 · hp 9 | (48.2, 42.2) · 표본 부족 | 표본이 리포트 근거 수준에 못 미친다 | `cam_playmaker/Roaming` 0.4428 (Δ0.010) — **표본 부족, 처방 근거로 쓰지 않는다** |
| 음바예 | RM — 84′ 교체 | 15′ 6.3 · 터치 3 · 경합 0승4패 · hp 5 | (64.0, 20.0) · 표본 부족 | 15분 터치 3회·경합 4패. 마지막 10분 볼 유지 실패의 일부 | `wm_winger/Attack` 0.7569 (Δ0.050) — **표본 부족** |
| 바클리 | 명목 RM 교체이나 실제 **피벗** | 15′ 6.2 · 터치 12 · 패스 7(7·100%) · 회수 3 · 클리어 2 · hp 17 | (35.1, 58.2) · 자기 진영 중앙 — **맥긴(52.4)이 아니라 카마라(40.3) 자리** | 교체 명목과 실제 위치가 다르다. 3-0 잠금 교체의 축 | `dm_holding/Defend` 0.5564 (RDM 슬롯 기준, Δ0.020) — **표본 부족** |
| 타미 아브라함 | ST — 88′ 교체 | 11′ 6.6 · 터치 5 · 패스 5(5) · 경합 1승 · hp 6 | (57.7, 61.8) · 표본 부족 | 시간 소모·공중 경합용 | `st_false9/Build-Up` 0.473 (Δ0.087) — **표본 부족** |

⚠️ 45분 미만·hp 15 미만 선수(캐시 제외 4명 + 캐시)는 대표 그리드·시즌 처방 집계에서 뺐다.
⚠️ 토트넘 선수 개인 실측은 이 저장소의 수집 범위가 아니다(관리 4팀 축 — 불변규칙 7).

---

## 6. 전술 변화 판정

**유지된 것**

- 4-2-3-1 Wide 90분 불변(WhoScored 포메이션 변화 0). 시즌 내 포메이션 불변 서술 유지.
- 무공 정착 블록 4-4-2(잭슨 1선, 부엔디아·맥긴이 미드 4의 와이드) — **전반 한정**. 브뤼헤전 실측의 두 번째 사례.
- 「풀백은 한 번에 한 명만 전진」 — 좌측(루헤리) 전진·우측(완비사카/캐시) 고정.
- 상대 맨투맨 하이프레스 → 의도적 GK 롱킥 경로(스즈키 패스 성공률 58%).
- 역습 실점 0(두 실점 모두 정지 국면·세트피스).

**새로 나타난 것**

0. ⭐⭐ **후반 우측 편중 백5 — `manager_profiles.formation` 정정 대상.** 현 프로필은
   「4-2-3-1 고정, 국면 변형은 라인·역할로만 / 5-3-2 전환은 브뤼헤전에서 관측되지 않았다」인데,
   이 경기는 **감독 자인 + 실측**이 동시에 성립한 첫 사례다(맥긴 수비 x 56.3 → 32.1). 다만 대칭 5-3-2가
   아니라 **한쪽만 5로 만드는 변형**이므로, 프로필에는 「5-3-2 전환」이 아니라
   「**국면·측면 의존 편중 백5**」로 적어야 한다. D+3 회차에서 `formation` 축에 덧붙인다.

1. ⭐ **def_x 30.6 — 26/27 최저이자 `optimal:vs-strong`(라인 43)보다 낮다.** 강팀 원정에서
   기존 프리셋보다 더 내려앉는 대역이 실측으로 열렸다. PPDA 13.24와 짝지으면
   「깊되 압박은 중간」이라는 새 조합이다(브뤼헤: 33.5/12.84와 근접, 방향 동일).
2. ⭐ **피벗 2의 역할 분화.** 주앙 고메스 태클 5·경합 16회 vs 카마라 패스 42·어시 1.
   종전 rest_defense 서술의 「더블 피벗 둘 다 dm_holding 계열 유지」와 어긋난다.
   단 **단일 경기 표본**이고 커널 적합은 둘 다 `dm_holding/Roaming`으로 같게 나왔다 —
   기하로는 분화가 보이지 않고 **행동 스탯에서만 보인다**. 누적 관찰 대상.
3. ⭐ **중거리 무기의 26/27 첫 재현**(부엔디아 79′, 박스 밖 26.2, xG 0.024).
4. **저블록 → 클리어 37 → 코너 11 → 세트피스 실점**의 사슬이 두 경기 연속 확인됐다
   (포레스트전 후반 붕괴와 같은 계열).

**직전 경기 대비 변화** — 코번트리전(EFL컵, 점유 57%·PPDA 9.86·def_x 36.4, 대폭 로테이션)과는
정반대 국면이다. 두 경기를 나란히 두면 에메리의 상황 대응 진폭이 **한 주 안에** 다시 확인된다.

**`manager_profiles` 반영** — 다음 축에 덧붙인다(D+3 회차에서 실행):
**`formation`(우측 편중 백5 — 감독 자인 + 실측, 「5-3-2 미관측」 서술 정정)** ·
`pressing`(PPDA 13.24 + def_x 30.6 대역 추가) · `situational`(강팀 원정 저점유 전환 승리 2회 연속) ·
`buildup`(⭐ 데 제르비의 「빌라 롱볼 전 시즌 대비 +86%」 — 상대 감독의 정량 사전 스카우팅이 우리 축 갱신을 독립 확인) ·
`rest_defense`(피벗 역할 분화 관찰 + 리드 후 2실점 · def_x가 막판에 오히려 26.1 → 34.6으로 풀린다) ·
`set_pieces`(코너 허용 11·세트피스 실점).

---

## 7. 게임 구현 판정

- **결론: 추가 관찰.** 단일 경기이고 선발 11명 중 **10명이 커널 Δ≤0.05(실측 무결정)**다.
  이 경기만으로 시즌 정본 처방을 바꾸지 않는다.

**이 경기 전용 팀 설정** (`match_game_setups`, `match_only=1`)

| 항목 | 값 |
|---|---|
| 게임 버전 | FC26 |
| 포메이션 | 4-2-3-1 Wide |
| 빌드업 | **Counter** |
| 수비 접근 | **Balanced** |
| 라인 높이 | **48** |
| rule_note | `RULE` — `core.team_settings.suggest(점유 36, 패스 331, 롱볼 48, PPDA 13.24)` → Counter / Balanced / 48~58(롱볼 14.5%). 기록 Counter/Balanced/48 — 규칙 일치. 라인은 제안 대역의 **하단**을 택했다(def_x 30.6이 26/27 최저이므로). |

**이 경기 선발 11명** (`match_player_prescriptions`)

| 슬롯 | 선수 | 역할 | 포커스 | 단일 경기 fit | 선택 이유 |
|---|---|---|---|---|---|
| GK | 스즈키 지온 | gk_goalkeeper | Defend | 0.9876 | Δ0.010 무결정 — 시즌 정본과 같아 유지 |
| RB | 완비사카 | fb_wingback | Balanced | 0.8405 | 우측 고정. 시즌 정본 `fb_att_wb/Support`(0.932)보다 이 경기 기하는 덜 전진 |
| RCB | 린델뢰프 | cb_bpd | Aggressive | 0.9496 | 시즌 정본과 동일 |
| LCB | 밍스 | cb_bpd | Build-Up | 0.9269 | 좌측 첫 패스 담당. Δ0.039 무결정 — 시즌 정본 `Aggressive`(0.9369)와 병기 |
| LB | 마테오 루헤리 | fb_fullback | Balanced | 0.9247 | 전진과 저블록 복귀를 모두 했다. 시즌 정본 `fb_att_wb/Support`는 전진 쪽에 치우친다 |
| RDM | 카마라 | dm_holding | Roaming | 0.8453 | 배급 몫이었으나 기하는 holding. Δ0.026 무결정, 2위 `dm_dlp/Roaming`(0.819)이 시즌 정본 |
| LDM | 주앙 고메스 | dm_holding | Roaming | 0.7759 | **Δ0.051 — 이 경기에서 유일하게 무결정 밖**. 파괴 전담과 정합 |
| RM | 맥긴 | wm_widemid | Defend | 0.6915 | 우측 봉쇄. 시즌 정본 `wm_winger/Attack`(0.7295)과 명확히 다른 국면 역할 |
| LM | 부엔디아 | wm_widemid | Defend | 0.6252 | Δ0.012 무결정. 태클 6·수비 셀 20 — 공격 역할명(wideplm/Attack)이 이 경기를 설명하지 못한다 |
| CAM | 만잠비 | cam_playmaker | Build-Up | 0.6314 | Δ0.010 무결정. 전환 1차 출구 |
| ST | 잭슨 | st_advanced | Support | 0.7022 | 넓게 움직이며 전환 출구. 시즌 정본 `st_false9/Attack`보다 전진·지원형 |

- **`prescriptions`·`slot_canon_roles`·`team_tactic_setups` 변경 없음.** 무결정 구간 10/11이고
  단일 경기다. 단 §4-1 T1로 `refresh_eval_samples.py`는 실행했고, 이 경기가 포함되며
  **시즌 measured 처방 4건**(맥긴 RM · 스즈키 GK · 완비사카 RB · 밍스 LCB)이 재집계됐다.
- **다음 경기 재검증 항목**
  1. **피벗 역할 분화**가 반복되는가(고메스 태클 ≫ 카마라 패스). 2경기 더 쌓이면 `dm_holding` vs `dm_dlp` 분리 처방을 검토한다.
  2. **def_x 30 대역**이 강팀 원정에서 재현되는가(다음 강팀 원정: 뉴캐슬). 재현되면 `optimal:vs-strong` 라인 43 → 하향 검토.
  3. **부엔디아 LM의 수비 부하**가 유지되면 시즌 정본 `wm_wideplm/Attack` 재검토(현재는 국면 차이로 본다).
  4. **세트피스 수비** — 코너 허용과 실점의 연결이 3경기째 이어지는지.

⚠️ 이 설정은 `MATCH ONLY` 프리셋이다. 시즌 전술·대표 선수 역할에 자동 병합하지 않는다.

---

## 8. 영상·기사·감독 발언

> D+0 회차(경기 종료 ~10시간 후) 수집분. **외국어 인용은 원문 + 한국어 번역 병기**(불변규칙 11).
> 전사 기반 인용은 **auto-caption**이며 인물명·수치는 실측과 교차검증했다.

### 8-1. 에메리 경기 후 회견

**① 후반 백5 — 본인 확인** · TNT Sports Football, 「Unai Emery REACTS after Aston Villa end winless run」,
2026-09-19 게시, `k6dbBj7Tz7w` · 전사 `reports/transcripts/k6dbBj7Tz7w.en.md` (자막 기준, auto-caption)
→ 인용·실측 대조는 §2 「후반 우측 편중 백5」 참조.

**② 게임 플랜 = 수비 → GK → 전환** · Aston Villa FC 공식, 2026-09-19, `Jp52xd-xLt8`

> 원문 「**The game plan we planned** … **We were defending collectively strong the first half. We needed the keeper.
> We needed defend a lot of corners defensively and we were resilience, but as well when we could get some transition
> we were trying to threaten them.**」
> (**우리가 세운 게임 플랜** … **전반에 집단적으로 강하게 수비했다. 골키퍼가 필요했다. 코너를 수비적으로 많이
> 막아내야 했고 우리는 회복력이 있었다. 동시에 전환을 얻을 수 있을 때는 그들을 위협하려 했다.**)

> 원문 「keeping the result with nil nil was **out of process to try to grow up during the match**」
> (0-0으로 결과를 유지하는 것이 **경기 중 성장하려는 과정의 일부**였다.)

⇒ **36% 점유는 사고가 아니라 사전 설계다.** 「수비 · 골키퍼 · 코너 · 전환」 네 낱말이 그대로 실측이 됐다
(def_x 30.6 · 스즈키 선방 5 · 코너 1-11 · 오픈플레이 xG가 전체 xG와 동일).

**③ 만잠비 — 「구조 안에서의 자유」** · Jacob Tanswell(The Athletic) Bluesky, 2026-09-19T14:34Z verbatim

> 원문 「**Manzambi played a good match but not understanding yet everything with his position.** But
> **his qualities are over the tactical idea of what we are achieving** … **he must feel free to exploit his
> qualities but always under our structure**.」
> (**만잠비는 좋은 경기를 했지만 자기 포지션에 관해 아직 모든 것을 이해하지는 못했다.** 다만 **그의 자질은
> 우리가 구현하려는 전술적 아이디어를 넘어선다** … **자기 자질을 자유롭게 발휘해야 하지만 언제나 우리 구조 안에서**여야 한다.)

⇒ `role_demands` 축(「지시를 이행하고 구조 안에서 판단하는 선수 선호」)의 **가장 명료한 1차 문장**이다.

**④ 잭슨 — 「힘을 처음 보여준 경기」** · Read Aston Villa, 2026-09-19 15:55 발행

> 원문 「**Maybe it is the first match where Jackson showed his power**, because before he didn't completely show
> that he understood everything we wanted from him in the previous games.」
> (**아마 잭슨이 자기 파워를 보여준 첫 경기일 것이다.** 이전 경기들에서는 우리가 그에게 원하는 걸 전부
> 이해했다는 걸 완전히 보여주지 못했으니까.)

⇒ 코번트리전 「잭슨 5.9 = 접점 부재, 감독 언급 0건」(obs#815)의 **후속이 닫혔다**.

**⑤ 경기 전 회견(D-1, 2026-09-18) — 인선 맥락**
결장 7명(비조·오나나·시세·마첸·고레츠카·마조 + 아센시오·파우 토레스). 고메스·캐시는 「more or less with the
group but I must be sure they are 100%」(대체로 그룹과 함께 있지만 100%인지 확인해야 한다) → 둘 다 가용.
⚠️ 같은 회견에서 **음바예·헤밍스·마조 3인 공개 지적** — 「until now, have not been good enough in the Premier
League」(지금까지 프리미어리그에서 충분히 좋지 않았다). 직후 경기에서 **음바예 선발 제외(84′ 투입)** ·
**헤밍스 72′ 투입**. obs#826 「원정 수비 게이트」 가설이 **기각되지 않았다**(단 감독의 직접 설명은 0건 — HELD 유지).

### 8-2. 데 제르비(토트넘) 경기 후 회견 — ⭐⭐ 빌라 롱볼을 수치로 사전 스카우팅

BeanymanSports, 2026-09-19, `kJZ0G7WvLWY` · 전사 `reports/transcripts/kJZ0G7WvLWY.en.md` (auto-caption)

> 원문 「we conceded **one unacceptable goal from long goal kick with a long ball**, and **we knew before the game
> because this season Aston Villa are playing 86% more long balls than last season**, and **we spoke in many many
> meetings yesterday and two days ago**.」
> (우리는 **롱 골킥에서 롱볼로 용납할 수 없는 골을 하나 내줬다**. 그리고 **경기 전에 알고 있었다 — 올 시즌
> 아스톤 빌라는 지난 시즌보다 롱볼을 86% 더 많이 하고 있으니까**. **어제와 이틀 전 수많은 미팅에서 그 얘기를 했다**.)

⇒ **이번 회차 최대 발견.** `manager_profiles.buildup`의 26/27 갱신(「상대 의존 폭이 저점유·고다이렉트로 확장」)을
**상대 감독이 「전 시즌 대비 +86%」라는 정량 수치로 독립 확인**했다. 더 중요한 것은 **대비했는데도 그 루트로
실점했다**는 점이다 — 67′ 잭슨 골의 경로(스즈키 롱킥 → 만잠비 플릭 → 잭슨)는 🇫🇷 wiwsport · 🇯🇵 footballchannel ·
🇮🇹 Sky Sport Italia 3개 언어권이 동일하게 서술했고, 브뤼헤전에서 정식화한 GK 롱킥 경로의 **3번째 표본이자
첫 득점 전환**이다.

> 원문 「**Aston Villa is not a so bad team, it's good team, good players.**」(아스톤 빌라는 나쁜 팀이 아니다.
> 좋은 팀이고 좋은 선수들이다.) / 「**Too easy for them to score, no? To score one goal we have to create 20 chances
> and the others, just one half chance — no, not even, because the goal kick is not a chance.**」
> (**저들은 너무 쉽게 득점하지 않았나? 우리는 한 골 넣으려면 20번의 기회를 만들어야 하는데, 상대는 반쪽짜리
> 기회 하나 — 아니 그것도 아니다, 골킥은 기회가 아니니까.**)

⚠️ 데 제르비의 빌라 인식은 **구조 분석이 아니라 효율**로 수렴한다 — 회견 전체에서 빌라의 블록·압박 구조를
전술적으로 서술한 대목은 **0건**이다.

### 8-3. 선수별 새 서사 (다국어)

- **만잠비** · 🇩🇪 watson.ch(2026-09-19 15:33): 「**Ursprünglich im Zentrum aufgestellt, ist Manzambi überall
  anzutreffen, presst, erobert Bälle und lanciert Angriffe.**」(원래 중앙에 배치됐지만 만잠비는 **어디에서나
  발견되며, 압박하고, 볼을 탈취하고, 공격을 개시한다**.) · 🇩🇪 kicker 제목 「**Manzambi krönt seine
  Startelfpremiere noch vor der Pause**」(만잠비, **하프타임 전에** 선발 데뷔전을 장식하다).
  ⭐ Tanswell 현장 관찰: 「**Kamara is dropping between the CBs**, so #AVFC can keep building in a **back three** …
  **Manzambi dropping deeper and alongside Gomes — far deeper than Rogers would pick the ball up**」
  (카마라가 CB 사이로 내려가 빌라는 백3로 빌드업을 유지한다 … **만잠비는 더 깊이, 고메스 옆까지 내려온다 —
  로저스가 볼을 받던 높이보다 훨씬 깊다**.) ⇒ `player_duties`의 「LDM(클럽 실측) / CAM(빌라 배치)」 **양쪽이
  한 경기에서 동시 관측**됐다. Opta: PL 첫 선발 골+도움은 **빌라 역사상 2번째**(2005 케빈 필립스 이후).
  ⚠️ 18′경 물리치료진 투입 기록이 있고 72′ 교체됐다 — **교체 사유 설명 0건**(D+1 조회 항목).
- **부엔디아** · Opta: **토트넘 상대 4경기 연속 골** · 최근 PL 6골 중 4골이 **박스 밖**(리그 2위).
  Tanswell 골 장면: 「Spurs are ragged and **Gomes drives straight through**. After the ball goes back inside the
  pitch, **Buendia lets fly. Top left corner.**」(스퍼스가 너덜너덜해졌고 **고메스가 곧장 뚫고 들어간다**.
  볼이 안쪽으로 돌아오자 **부엔디아가 때렸다. 왼쪽 상단 구석.**)
- **스즈키 지온** · 🇯🇵 footballchannel: 11′ 사비우 근거리 반응 세이브 → 세컨볼 한 손 차단, 20′ 아치 그레이
  중거리 저지, **67′ 롱패스가 추가골 기점**. 총평 「**高精度キック**」(고정밀 킥).
  ⚠️ Tanswell은 반대 방향도 기록했다: 「**Double save from Suzuki after a really poor, lax giveaway between him
  and Wan-Bissaka**」(스즈키와 완비사카 사이의 아주 나쁘고 느슨한 볼 로스트 뒤 스즈키의 더블 세이브)
  — 빌드업 실수가 세이브의 원인이었다는 뜻이다.
- **잭슨** · 골 체인 3개 언어 교차 확인: 🇫🇷 wiwsport 「Jackson … reçoit une passe de Manzambi qui avait récupéré
  **un long dégagement de Suzuki**, **contrôle de la poitrine**」(잭슨이 **스즈키의 롱 클리어런스**를 회수한
  만잠비의 패스를 받아 **가슴 트래핑**) · 🇯🇵 footballchannel 「**鈴木のロングパスが2点目の起点**」(스즈키의
  롱패스가 두 번째 골의 기점) · 🇮🇹 Sky Sport Italia 「**destro rasoterra da 20 metri su assist di Manzambi**」.
  ⚠️ 후반 시작 30초 만에 경고 — Tanswell: 「Emery talked yesterday about **Jackson not picking up unnecessary
  bookings**. **30 seconds into the second half, he gets one.**」 ⇒ obs#845(포레스트전 45분 교체 = 퇴장 리스크
  관리)의 **연속 관리 대상** 재확인.
- **루헤리** · ⚠️ **양 진영 평가가 정면 충돌한다.** 빌라 쪽 Aston Villa Review 4점 「struggled with the evolving
  challenge of Spurs' right flank」(변화하는 스퍼스 우측의 도전에 고전했다) + Tanswell 「**Spurs targeting
  Ruggeri** … **#AVFC getting overloaded down their left.**」(스퍼스가 루헤리를 노린다 … 빌라가 좌측에서
  과부하를 당하고 있다). 반대로 토트넘 쪽 HotspurHQ는 **사비우에게 4점**을 주며 「**quickly contained by
  Matteo Ruggeri**」(루헤리에게 빠르게 봉쇄됐다)라고 적었다. 🇮🇹 TMW 「**Ruggeri debutta dal 1′ contro
  De Zerbi**」(루헤리, 데 제르비 상대로 선발 데뷔) — **PL 첫 선발**. **판정 보류**(D+1~D+3 재검토).
- **주앙 고메스** · Tanswell 사전 임무: 「Spurs a threat with Savio's pace against Ruggeri … so **Gomes will need
  to keep coming across to cover**」(사비오의 스피드가 루헤리를 상대로 위협적이므로 **고메스가 계속 건너와
  커버해야 할 것이다**.) ⇒ §2의 「피벗 역할 분화」와 정합한다 — 고메스의 파괴 몫은 성향이 아니라 **좌측 커버
  지시**였을 수 있다. 수비액션 y가 전반 72.5(좌측) → 후반 50.3(중앙)으로 이동한 것도 같은 방향이다.
- **카마라** · ⭐ Tanswell: 「**Kamara is dropping between the CBs, so #AVFC can keep building in a back three.**」
  + 에메리 본인의 「first half we use it more [Kamara] dropping dropping」. ⇒ `manager_profiles.buildup`의 기존
  백3 경로(3-2-5 · 콘사 RB 변환)와 다른 **피벗 하강형 백3** 후보. **HELD** — 재판정 조건은 §8-5 참조.
- **맥긴** · Tanswell: 「#AVFC happy for **McGinn to slide along Cash, be in a back five mid-block (5-3-2)**」
  (빌라는 **맥긴이 캐시 옆으로 미끄러져 백5 미드블록(5-3-2)**을 이루는 형태에 만족한다.) ⇒ 실측으로 확인됐고
  obs#151(맥긴 RM 인사이드 포워드 기각)과 충돌하지 않는다 — **무보유 국면 임무**이기 때문이다.
- **완비사카 → 캐시** · AVR 완비사카 5점 「Showcased his one-on-one defending in the early minutes but **took a few
  risks with his physicality** and was substituted at half time.」(초반에 1대1 수비를 보여줬지만 **자기 피지컬로
  몇 번 위험을 감수했다**. 하프타임에 교체됐다.) — **감독 설명 0건, 부상/전술 미확정**(D+1 최우선 조회).

### 8-4. 실측과의 충돌·정정

| # | 항목 | 외부 | 우리 값 | 판정 |
|---|---|---|---|---|
| ① | 만잠비 득점 시각 | 45+4′ (Opta·kicker·Sky It 등 6개 언어권) | `minute=49, added=4` | 🟢 **충돌 아님** — 우리 규약이 「90+3은 93」이므로 45+4 = 49다. 서사 회차가 규약을 모르고 충돌로 올린 건이며 DB는 정확하다. |
| ② | 갤러거 / 판 헤케 | 85′ / 90+5′ (Opta) | 86′ / 90+8′ (SofaScore·구단) | 🟡 제공사 1~3분 차 — 서사 판단에 영향 없음, 병기만 한다. |
| ③ | 「판 데 벤 부상 교체」 | — | — | 🔴 **교체되지 않았다.** 45′경 치료로 일시 이탈 후 복귀해 풀타임. 데 제르비 본인 「we concede the first goal … **in 10 players just for one minute**」(단 1분간 10명이던 상황에서 첫 골을 내줬다). 전반 부상 교체는 **포로(19′ → 아치 그레이)**다. |
| ④ | 「무공 4-4-2 고정」 | — | 리포트 초판 서술 | 🔴 **정정됨** — 후반은 우측 편중 백5(§2). |
| ⑤ | 소스 오류 2건 | HotspurHQ가 빌라 GK를 「Emiliano Martínez」로 오기 · wiwsport 본문이 스코어를 3-1로 오기 | — | 인용에서 배제했다. |

### 8-5. 구현 주장 (`video_impl_claims` 5행 — G17)

| 영상 | axis · field | value | verdict |
|---|---|---|---|
| `Jp52xd-xLt8` | instruction · `away_vs_top_game_plan` | `defend_deep_then_transition` | **APPLIED** |
| `k6dbBj7Tz7w` | instruction · `defensive_shape_second_half` | `back_five_right_side_shift` | **APPLIED** |
| `k6dbBj7Tz7w` | instruction · `buildup_back_three_source` | `pivot_drop_kamara` | **HELD** |
| `kJZ0G7WvLWY` | team_axis · `build_up_style` | `Counter` | **APPLIED** |
| `kJZ0G7WvLWY` | instruction · `gk_long_kick_route` | `goal_kick_to_ten_flick_to_nine` | **APPLIED** |

⛔ HELD 1건의 **재판정 조건**: 이번 수집은 WhoScored **보유 이벤트를 분(分) 없이** 받아 전반만 분리할 수
없었다. 다음 회차에 보유 이벤트를 `expandedMinute` 포함으로 재수집해 **전반 카마라 보유 x와 CB 라인 x
(린델뢰프·밍스)를 대조**한다. 격차가 8 이하로 좁혀지면 APPLIED, 아니면 REJECTED.
(경기 전체 평균 카마라 40.3 vs CB 25.7·26.1만으로는 판정할 수 없다.)

### 8-6. 소스 커버리지 (D+0)

| 종류 | 상태 | 내용 / 미수행 사유 |
|---|---|---|
| 1. 유튜브 전술 분석 | ◐ 부분 | ⭐ **AVL 필수 3채널 전부 이 경기 영상 0건**(D+0 ~10h 시점) — UTV `fKDbTccRjGk` · The Villans `JmmZ2jzDzJQ`(제목 「Mbaye To Start」 — 실제로는 선발 제외) · 1874 `WajH4NOz_D0` 모두 **프리뷰**다. 대신 **회견 원본 3편 전사 확보**. 리뷰 영상은 D+1 예상. |
| 2. 전술 블로그 | ⛔ **0건** | TFA · Between the Lines · Spielverlagerung · Coaches' Voice 전부 D+0 미발행. 대체로 The Analyst(Opta) 데이터 기사 1편. |
| 3. 기사 | ✅ | ⭐⭐ **Tanswell 확보** — Bluesky `jacobtanswell.bsky.social` 공개 API로 경기 전~중 22건 + 경기 후 에메리 인용 1건. The Athletic 본문·Birmingham Mail·football.london·BBC·Guardian은 **크롤러 차단**. 대체: Read Aston Villa 3편 · Aston Villa Review · Yardbarker · Goal · NBC · Reuters. |
| 4. 본인 발언 | ✅ | **양 팀 감독 회견 전문 전사 확보** + 에메리 D-1 회견. ⛔ 미확보: avfc.co.uk 회견 본문(클라이언트 렌더링) · tottenhamhotspur.com 「Every word」(D+0 미발행). |

**언어별 시도 검색어(0건 포함)**

| 언어 | 결과 |
|---|---|
| 🇪🇸 스페인어 | EFE 크로니카 2건 + 🇦🇷 Vermouth Deportivo 1건. **회견 verbatim 0건**(Marca·AS·Relevo·El Desmarque 미발행). 검색어 `Emery Aston Villa Tottenham crónica rueda de prensa` · `Buendía golazo Tottenham rueda de prensa post partido` · `Emery declaraciones tras ganar Tottenham 19 septiembre 2026` |
| 🇯🇵 일본어 | **3건**(soccer-king 2 · footballchannel 1) — 스즈키 세이브 타임스탬프 + 에메리 평가 재번역. 검색어 `鈴木彩艶 トッテナム アストン・ヴィラ` · `鈴木彩艶 セーブ プレミアリーグ` |
| 🇩🇪 독일어/스위스 | **4건**(watson.ch · kicker · Tages-Anzeiger · bluewin) — 만잠비 전술 묘사 verbatim |
| 🇮🇹 이탈리아어 | TMW 1 + Sky Sport Italia 1. **pagelle 0건 · 데 제르비 이탈리아어 인용 0건**. 검색어 `Ruggeri Aston Villa Tottenham pagelle` · `De Zerbi Tottenham Aston Villa conferenza stampa` · `Tuttosport Gazzetta De Zerbi 3-2 dichiarazioni` |
| 🇸🇪 스웨덴어 | 1건(Fotbollskanalen, 라인업·골 묘사만). **린델뢰프 개별 평가 0건** |
| 🇫🇷 프랑스어/세네갈 | wiwsport 2건. **음바예 84′ 투입 전용 기사 0건**(L'Équipe·RMC·Senego) |
| 🇧🇷 포르투갈어 | ⛔ **0건** — Trivela·GE·Lance·UOL 전부 미커버. 검색어 `João Gomes Aston Villa Tottenham atuação` · `Aston Villa vence Tottenham João Gomes Kamara meio-campo crônica` |
| 🏴 상대팀 관점 | **4건**(Cartilage Free Captain · HotspurHQ · Read Tottenham · 팬채널 리액션). Spurs Web·The Fan Debate·LWOS는 D+0 미발행 |

**D+1 이후 과제**: ① 필수 3채널 리뷰 영상 ② 전술 블로그(TFA·Between the Lines) ③ **완비사카 HT 교체 사유**
④ **만잠비 72′ 교체가 부상인지** ⑤ 후반 2실점에 대한 에메리 진단(회견 2편 어디에도 **0건**) ⑥ avfc.co.uk·
tottenhamhotspur.com 회견 전문 ⑦ 🇮🇹 pagelle · 🇸🇪 린델뢰프 평점 ⑧ 루헤리 평가 충돌 판정.

---

## 레퍼런스·한계

- SofaScore `/api/v1/event/16363870/{lineups,average-positions,incidents,statistics,shotmap}` (2026-09-19 수집)
- FotMob `/api/data/matchDetails?matchId=5795464` — xG 4종 동시 스냅샷 (2026-09-19)
- WhoScored matchCentreData `matchId=1983589` (Opta) — PPDA·def_x·국면 분리 그리드
- 한계: 토트넘 선수 개인 실측 미수집(관리 4팀 축 밖). 빌라 세트피스 수비의 개인 마킹 배치는
  이벤트 데이터로 특정되지 않아 영상 확인 대상으로 남겼다.

---

## D+1 추적 (2026-09-20)

> 수집 방식: 서브에이전트 3축 병렬(AVL 필수 3채널·Tanswell / 전술 블로그·토트넘 관점 / 다국어 7개 언어권) + 메인 세션의 WhoScored 재수집·실측 판정.
> ⛔ **당일(D+0) 절은 수정하지 않았다.** 뒤집힌 판정은 아래 「당일 판정 정정」에 적는다(불변규칙 2·3).

### D+1-1. ⭐⭐ HELD 1건 종결 — 「카마라 피벗 하강형 백3」 REJECTED

D+0이 건 재판정 조건(전반 카마라 보유 x와 CB 라인 x의 격차가 8 이하면 APPLIED)을 집행했다.
WhoScored matchCentreData `1983589`를 **`period`·`minute` 포함으로 재수집**(이벤트 1,627건 · 빌라 692건)해 `core.whoscored`로 재집계했다.

| 전반 보유 국면 | x | n |
|---|---|---|
| 카마라 | **41.3** | 37 |
| 린델뢰프 | 28.0 | 20 |
| 밍스 | 31.6 | 30 |
| **CB 라인(2인 합산)** | **30.2** | 50 |

**Δ = 11.1** → 임계 밖. 자기 진영(x<50)으로 좁혀도 **8.8**로 여전히 밖이다. 후반은 Δ 14.8로 더 벌어진다.

⭐ **기각의 범위를 좁혔다**: 좌우로는 카마라(y 43.0)가 린델뢰프(32.5)와 밍스(70.7) **사이**에 있고, 전반 보유 37건 중 **7건(19%)이 CB 라인 깊이 이하**이며 그중 6건은 두 CB 사이였다.
⇒ 「내려오는 장면이 있다」는 참이고 「백3로 **상시** 빌드업한다」는 거짓이다. 에메리 회견 원문의 「**someday** we are the first half we use it more dropping」(어떤 날은 전반처럼 더 내려서 쓴다)도 상시가 아니라 **선택적**이라고 말한다. obs#866.

⛔⛔ **단 이 판정은 같은 회차에 철회됐다 — 임계 설계 자체가 잘못됐다.** `video_impl_claims` #139는 **REJECTED → HELD**로 되돌렸다.
계기는 Jacob Tanswell(The Athletic) 2026-09-20 정식 기사 본문이다 — 원문 「A quarter of an hour into the match, **when Villa built from the back**, Manzambi dropped deep, occasionally alongside Joao Gomes, as **Boubacar Kamara moved into a back three**.」(경기 15분 무렵 **빌라가 후방 빌드업을 할 때** 만잠비가 깊게 내려왔고 때때로 주앙 고메스 옆에 섰으며, **카마라는 백3로 이동했다**.)
이 서술은 **국면(후방 빌드업)·시점(15분 무렵)을 명시적으로 한정**한다. 그런데 D+0이 건 조건은 「전반 보유 **전체**의 평균 격차」였다 — **국면 한정 행동을 전체 평균으로 검정하면 구조적으로 기각된다**(카마라 전반 보유 최대 x는 87.8이다 · 희석). 실제로 국면을 좁히면 19%라는 신호가 보인다.
⇒ **새 재판정 조건**: 골킥·자기 진영 시작 시퀀스만 추려 **빌드업 국면 한정**으로 대조한다. 격차 8 이하면 APPLIED. obs#879(방법론).

### D+1-2. 당일 판정 정정·보강

| # | 항목 | D+0 | D+1 | 판정 |
|---|---|---|---|---|
| ⑥ | **필수 3채널 리뷰** | 「0건 — D+1 예상」 | **3채널 전부 확보** | 🔴 **정정.** 1874 `ahxMgX0BH2c`는 **게시 시각이 09-19 14:09Z로 D+0 회차보다 앞선다** — 「안 올라왔다」가 아니라 **우리가 보는 탭에 없었다**(「실시간 스트림」 탭 전용). obs#876 |
| ⑦ | **86% 롱볼 수치 출처** | auto-caption 전사 1건 | 구단 공식 회견 전문 + 🇮🇹 서면 2매체 | 🟢 **보강 + 한정.** auto-caption 의존 해소. ⛔ 단 **Opta 공표 수치가 아니다** — 토트넘 내부 스카우팅이며 제공사 미상. 「Opta에 따르면」은 허위 귀속. obs#875 |
| ⑧ | **루헤리 평가 충돌** | 판정 보류(AVR 4 ↔ 타 소스) | 「전반 고전 → 후반 개선」 | 🟢 **해소.** 평점 분열은 평가자가 본 **구간**의 차이였다. obs#874 |
| ⑨ | 완비사카 HT 교체 | 사유 0건 | ✅ **종결** | 🟢 **닫혔다.** Birmingham Live(John Townley, 빌라 전담 1티어) 원문 「**Wan-Bissaka continued at right-back while Cash wasn't quite ready to start today. He wasn't effective enough in possession and was replaced by Cash at the break.**」(완비사카는 캐시가 선발할 만큼 준비되지 않아 계속 우측 풀백으로 나섰다. 볼 소유에서 충분히 효과적이지 못해 하프타임에 캐시로 교체됐다.) ⇒ **가용성 + 경기력**. obs#867·#872·#880 |
| ⑩ | 만잠비 72′ 교체 | 부상 여부 미확정 | **부상 아님 사실상 확정** | 🟢 **부상설 종결**(스위스 대표팀 소집 명단 포함 — obs#873 재판정 조건 충족). 사유는 **체력 관리** 가설(「he looked spent」·「65% 정도로 뛰고 있다」)이나 직접 진술 0건. ⚠️ 치료 시점 18′ vs 30′ 충돌은 미해결. obs#873·#885 |
| ⑪ | 후반 2실점 감독 진단 | 0건 | **0건 유지** | 🔴 **영구 0건 처리.** 회견 2편 + D+1 기사 9편 전수 확인. UTV 프레임 분석으로 대체. obs#878 |
| ⑫ | 선제골 경로 | 만잠비 / 어시스트 카마라 | 상대팀 채널 「로버트슨 → **맥긴** → 박스 패스」 | 🟡 **실측 유지.** 3티어 팬 회상 vs Opta. 만잠비 본인도 「부바카르(카마라)가 슈팅하려는 걸 봤다」고 말해 우리 기록과 정합 |
| ⑬ | 86′ 실점 최종 굴절 | 미기록 | TNT 「매티 캐시의 굴절」 | 🔴 **미검증.** Opta 골 시퀀스에 **캐시 터치가 없다**. DB에 반영하지 않았다. obs#871 |

### D+1-3. 새 실측 — 후반 우측은 「이중 하강」이었다

§2의 「후반 우측 편중 백5」에 성분이 하나 더 붙었다. 미드필더만 내려간 것이 아니라 **풀백도 함께 내려갔다.**

| 우측 | 전반 | 후반 | Δ |
|---|---|---|---|
| 미드필더(맥긴) 수비액션 x | 56.3 | **32.1** | −24.2 |
| 풀백 수비액션 x | 33.1 (완비사카, n=6) | **17.2** (캐시, n=7) | −15.9 |

⭐ **상대팀 채널이 이 구조를 독립 서술**했다 — 원문 「They started bringing their midfield very deep to protect the sides … **McGinn was dropping in on the right as well to protect us against Marmoush**」(측면을 보호하려고 미드필드를 아주 깊이 내리기 시작했다 … 맥긴도 우측으로 내려앉아 마르무시에 대비했다). **의도(측면 보호)까지 붙은 서술**이라 def_x 26.1이 강요가 아니라 지시였다는 쪽 근거가 세졌다. obs#868.

**좌측은 내려가지 않았다.** 부엔디아 수비액션은 **건수만** 늘었다 — 전반 9건 → 후반 16건(+78%)이고 평균 깊이 x는 **전반 44.1 → 후반 42.7로 사실상 불변**이다.
⭐ 영상 서술의 「helping out a lot more(훨씬 더 많이 돕는다)」도 **빈도** 진술이고 실측도 빈도에서만 움직인다 — 두 축이 일치한다.
⛔ **「좌측이 더 내려앉았다」로 읽으면 오독**이다. 내려간 것은 우측뿐이고, 그래서 **대칭 5-3-2가 아니라 우측 편중 백5**다. obs#870.

> ⚠️ **당일 수치 정정(값은 덮지 않는다 — 불변규칙 2)**: §2 표의 부엔디아 행 「전반 35.6 → 후반 47.6(Δ+12.0)」은 **전수 탐색에서 재현되지 않았다**(필터 × 분할 × 선수 × 축 전 조합 0건).
> 같은 표의 맥긴 행은 소수점까지 재현된다. 재계산값은 **44.1 → 42.7(Δ−1.4)**이다. **결론(「좌측은 안 내려갔다」)은 살아남고, 틀린 것은 「반대로 12점 올라갔다」 부분**이다.
> 원인 후보: 이 경기 전반은 `expandedMinute` 기준 **52분까지** 이어지는데(만잠비 골 49′) D+0 스냅샷에는 `period`도 `minute`도 없었다(필드 5개뿐). obs#884.
> ⇒ ⭐ **파생 수치를 적을 때는 산출 경로(필터·분할 기준·스냅샷)를 함께 적는다.**

⛔ **「전반 20~25분에 이미 5-3-2」(Bains)는 기각**했다 — 맥긴 수비액션 x가 전반 0~20′ 55.7 · 20′~HT 58.4로 **오히려 올라가고**, 전반에 백라인 깊이(x<20) 수비액션은 **0건**이다. obs#869.

### D+1-4. 86′ 실점의 성격 — 구조 붕괴가 아니라 2차 처리 실패

UTV의 프레임 분석을 **Opta 이벤트 시퀀스로 검증했고 일치한다.**

> 루헤리 Aerial → 루헤리 Interception ×2 → 밍스 Clearance(x 13.8) → **루헤리 BallRecovery(x 21.7) → 루헤리 Dispossessed**(쿠두스 Tackle) → 루헤리 BlockedPass → **부엔디아 TakeOn 실패**(그레이 Tackle) → 쿠두스 → 마르무시 → 쿠두스(어시스트) → 갤러거 Goal

원문 「We have one opportunity to deal with it here. **Rejieri**, clear it. We then have another opportunity here. **Buendía, win the ball. Clear it. We don't.**」(여기서 처리할 기회가 한 번 있었다. 루헤리, 걷어내라. 또 한 번 기회가 있었다. 부엔디아, 볼을 따내라. 걷어내라. 우리는 못 했다.) ※ `Rejieri`=Ruggeri auto-caption 오인식

⇒ **구현 함의는 라인·수비접근 축이 아니라 세컨볼 대응이다.** obs#865(87′~ 블록이 풀렸다)와 합치면 「리드 관리 실패」의 내용이 **라인 하강이 아니라 2차 처리**로 좁혀진다. obs#871.

### D+1-5. 신규 구현 주장 (`video_impl_claims` 9행 — G17)

| 영상 | axis · field | value | verdict |
|---|---|---|---|
| `BTW1C1UCPN0` UTV | instruction · `concession_second_ball_clear` | `second_clear_fail_ruggeri_buendia` | **APPLIED** (Opta 시퀀스 일치) |
| `BTW1C1UCPN0` UTV | instruction · `set_piece_defending_marking` | `mark_drop_under_flight_fail` | **HELD** |
| `BTW1C1UCPN0` UTV | instruction · `gk_role_in_buildup` | `gk_as_eleventh_outfield` | **HELD** |
| `kj4gz1QXrl8` The Villans | instruction · `halftime_left_side_cover` | `winger_tucks_to_support_lb` | **APPLIED** |
| `noampLJzxn0` Bains | instruction · `defensive_shape_first_half` | `mid_block_to_532_at_20min` | **REJECTED** (실측 기각) |
| `XRJgUjer1cc` Blueprint(상대팀) | instruction · `defensive_shape_second_half` | `back_five_right_side_shift` | **APPLIED** (제3자 독립 확인) |
| `ahxMgX0BH2c` 1874 · `yn-UvcWhAio` 구단 · `FP7obsFLxRQ` 미상 | none | — | NA |

⛔ **HELD 2건의 재판정 조건** — ⑴ 세트피스 마킹: 개인 마킹 배치는 우리 이벤트 데이터로 특정되지 않는다(프레임 1소스). **독립 2번째 프레임 소스** 또는 **세트피스 실점 2경기째 누적** 중 하나가 생기면 재판정.
⑵ GK 빌드업: 제시된 수치(론치 성공률 47% · 골킥 9회 · 패스 32회 중 롱 15)가 **우리 실측(패스 38회·성공 22)과 총계부터 어긋난다** — 같은 스냅샷으로 골킥 숏/롱 분해를 받아 대조한 뒤 판정.

⚠️ **가설 후보(인과 아님)**: 세트피스 코치 **오스틴 맥피가 2026-07 첼시로 이적**했고 25/26 빌라는 세트피스 득점 유럽 공동 1위(29골)였다. **이번 경기를 맥피 부재와 연결한 분석은 0건**이므로 시즌 누적 추적 대상으로만 남긴다.

### D+1-6. 소스 커버리지 (D+1)

| 종류 | 상태 | 내용 / 미수행 사유 |
|---|---|---|
| 1. 유튜브 전술 분석 | ✅ | **필수 3채널 전부 + 4편 추가, 전사 7편 등재**(`match_videos` 197~203). ⭐ 1874는 **`/streams` 탭에서만** 발견 — 스윕 규칙에 ㉣ 추가(obs#876) |
| 2. 전술 블로그 | ◐ 부분 | Read Aston Villa(09-20) 1건 + The Analyst(Opta) 1건. ⛔ **TFA · Between the Lines · Spielverlagerung · Coaches' Voice는 D+1에도 0건**(Coaches' Voice는 보통 며칠 뒤 발행 — D+2~D+3 재시도) |
| 3. 기사 | ✅ | VAVEL 2 · Claret Villans · ESPN · TNT · Read Aston Villa 3 · **Birmingham Live(John Townley) 평점 기사·회견 전문** · Spurs Web · Spurs Odyssey · Football Italia. ⛔ **The Athletic 본문·가디언은 도메인 차단**(단 Tanswell 정식 기사 인용문은 확보). ⚠️ **소스 판정 2건 정정** — Birmingham Live는 **URL 직접 접근으로 열린다**(검색 인덱싱 0건을 「접근 불가」로 승격하지 말 것) · avfc.co.uk는 **같은 URL로 1회 재navigate하면 본문이 뜬다**(쿠키 배너 우회, 2회 재현). obs#881 |
| 4. 본인 발언 | ✅ | ⭐ **tottenhamhotspur.com 공식 회견 전문 D+1 발행분 확보**(D+0 미발행 해소) · **avfc.co.uk 에메리 회견·맥긴 인터뷰·콘사 이적 공지 본문 확보**(재navigate 경로) · 구단 만잠비 인터뷰. ⭐⭐ **에메리가 「롱볼은 설계」를 1차 진술로 확인**(obs#882) · **맥긴이 67′ 골을 「훈련된 패턴」으로 확인**(claim #141 보강) |

**언어별 D+1 결과 (0건은 검색어를 남긴다 — D+2가 반복하지 않게)**

| 언어 | 결과 |
|---|---|
| 🇮🇹 | **3건(D+0 0건 → 반전)** — ilnapolista · Napoli Magazine(데 제르비 회견 verbatim, 86% 독립 확인) · Football Italia(루헤리 FotMob 7.5). ⛔ **Gazzetta·Tuttosport·CdS·TMW 자체 숫자 pagelle는 0건**(「italiani all'estero」 코너는 월~화 발행 — D+2~3 재시도). 검색어 `Ruggeri pagelle Tottenham Aston Villa voto` · `"italiani all'estero" Ruggeri Tonali voti quinta giornata TMW` |
| 🇯🇵 | **3건 신규** — 東スポWEB(09-20, 롱킥 루트 독립 보도 · BBC 평가 재번역). ⛔ **스즈키 본인 코멘트 0건 유지**. 검색어 `鈴木彩艶 アストンヴィラ トッテナム 戦 ロングキック 起点 コメント` |
| 🇩🇪🇨🇭 | 1건 검증(Blick — 만잠비 「Feierabend」). ⛔ **72′ 교체 사유 직접 서술 0건** · SRF·Nau.ch·20 Minuten 원문 미검증(D+2 과제). 검색어 `Manzambi Auswechslung 72. Minute Verletzung Aston Villa Tottenham` |
| 🇫🇷🇸🇳 | 2건(Seneweb·wiwsport). ⛔ **음바예 전용 기사 0건 유지**(L'Équipe·RMC·Foot Mercato·Senego 미커버) |
| 🇪🇸🇦🇷 | 아르헨 5건(부엔디아 골라소, **미검증**). ⛔ **에메리 회견 verbatim 스페인어 0건 — 3회차 연속**(Marca·AS·Relevo·El Desmarque·MD) |
| 🇧🇷 | ⛔ **본토 매체 0건 — 2회차 연속**(GE·Lance·UOL·Trivela·ESPN Brasil). 고메스 분석은 영문 Read Aston Villa가 유일(태클 5·인터셉트 3·11.5km·라인브레이킹 패스 7) |
| 🇸🇪 | ⛔ **린델뢰프 개별 평가 0건 — 2회차 연속**. ⚠️ **연도 함정**: Fotbollskanalen 「Godkända Lindelöf-betyg」는 **2026-05-10 번리전** 기사다 |
| 🏴 상대팀 | ✅ 공식 전문 + HotspurHQ · Spurs Web · To The Lane And Back · The Tottenham Blueprint. ❌ Cartilage Free Captain 도메인 차단 · Last Word on Spurs·The Fan Debate 0건 |

⚠️ **소스 품질 — 상시 배제 목록에 추가**(obs#877): **빌라 GK를 「Martinez」로 오기하는 소스군**이 2회차 연속 나왔다(D+0 HotspurHQ · D+1 Yahoo/The 4th Official). 둘 다 **선수 평점 기사**다.
⇒ **평점 기사는 GK 이름으로 신선도를 먼저 검사한다**(저비용 판별자). 연도 함정 2건도 함께 걸렀다(위 🇸🇪 · soccerway.es 2024-10-19).

**D+2 이후 과제**: ① 🇮🇹 「italiani all'estero」 pagelle(월~화 발행) ② 🇨🇭 SRF·Nau.ch·20 Minuten 원문 — 만잠비 72′ 종결용 ③ Coaches' Voice·StatsBomb/Tifo 재시도 ④ 유튜브 `KCsvWv_eDeg`·`4J67XYRC8Uk` 회견 리액션 전사 — 완비사카 HT·후반 2실점의 남은 경로 ⑤ **The Athletic 09-20 기사(67′ 골 전용 해부)는 사용자 브라우저로만 접근 가능** ⑥ 만잠비 치료 시점(18′ vs 30′) 영상 확인 ⑦ 루헤리 인터셉트 6·클리어런스 8을 **좌측 피침투 실측과 대조**해 「많이 막음 = 많이 당함」 해석 닫기 ⑧ GK 골킥 숏/롱 분해 제공사 대조.

### D+1-8. 미확보·제외 판단 (병렬 세션 메모 흡수분 — 메모는 삭제됨)

**🟡 미확보로 남은 것 3건**
1. **The Athletic 본문**(nytimes.com 도메인 차단) — 09-20 Tanswell 전술 기사 「Three passes and a goal」(67′ 골 전용 해부). 인용문은 확보했으나 본문은 **사용자 브라우저로만** 접근 가능.
2. **Tanswell X 부엔디아 포스트의 「Emery wanted …」 이후 문장** — 비로그인 X에서 잘렸다(로그인 세션 필요). ⭐ 확보분: 「**Ran over 12km today. 0.6km more than any other #AVFC player**」(오늘 12km 이상 주행, 다른 어떤 빌라 선수보다 0.6km 많다) — **부엔디아의 무보유 주행량은 우리 실측에 없는 축**이다.
3. **The Athletic 라이브블로그 58′ 루헤리 항목**(「Cheeky nutmeg from Ruggeri」) — 페이월로 전문 미확인, **인용 보류**.

**⛔ 등재에서 제외한 전사 1편** — `ofp0s7RaNoc`(Cash talk's Football)은 **PL 전 경기 골 모음 포맷**이라 이 경기 비중이 서두 ~2분뿐이고 본문에 타 경기 내용이 섞여 있다.
⇒ 등재하면 경기 화면 「이 경기 영상 분석」 패널이 오독을 부른다. **다음 회차가 같은 영상을 재후보로 올리지 않도록 여기에 사유를 남긴다.**
⏰ 미등재 2편(`U4OewDAQMCk` MAH · `QkA0fScs5s8` Chris Cowlin: Spurs Chat, 둘 다 상대팀 축)은 **등재 가치가 있다** — G17상 `impl_claims` 1행(주장 없으면 `axis:none`)이 필요하다.

### D+1-7. ⚠️ 병렬 세션 병합 기록 (2026-09-20)

이 경기 D+1 추적을 **두 세션이 병렬로** 수행했다. 다른 세션은 **DB를 건드리지 않고** 인계 메모
`reports/match-watch/2026-09-19-avl-tottenham.D1-findings.md`만 남겼고, 이 절이 그것을 병합한 결과다.
(HANDOFF 「공유 DB에 동시 세션이 붙으면 내 것만 명시 스테이징한다」의 정상 동작 사례 — 충돌 0건.)

병합으로 **내 판정 1건이 철회되고 2건이 정정**됐다:

| 항목 | 내 D+1 초판 | 병합 후 | 근거 |
|---|---|---|---|
| claim #139 카마라 백3 | **REJECTED** | **HELD**(철회) | The Athletic 정식 기사가 **국면 한정**으로 서술 — D+0 임계가 「전체 평균」이라 오설정. obs#879 |
| obs#870 하프타임 좌측 조정 | 「수비 가담이 늘고 **깊어졌다**」 | 「**빈도만** 늘었다, 깊이는 불변」 | 전반 전체 44.1 → 후반 42.7. 하위 구간 비교(n=3)가 과대 해석을 낳았다 |
| 소스 접근성 | Birmingham Live·avfc.co.uk **접근 불가** | **둘 다 접근 가능** | URL 직접 접근 / 재navigate 경로. obs#881 |

⭐ **추가로 얻은 1차 진술 3건**(내 3축 스윕이 도메인 차단으로 놓친 것): 에메리의 「롱볼은 설계」 자백(obs#882) ·
맥긴의 「67′ 골은 훈련된 패턴」(claim #141 보강) · Townley의 완비사카 교체 사유(obs#880).

⭐⭐ **방법론 수확 2건**: ⑴ **Opta는 이벤트 자체도 사후 개정한다**(양방향 차분 60/44건 — 종전 규약은 「xG만 개정」)
⑵ **국면 한정 행동을 전체 평균으로 검정하면 구조적으로 기각된다**. obs#883·#879.

⚠️ **미해결로 남긴 것**: 만잠비 치료 시점(18′ vs 30′) · 루헤리 86′ 볼 로스트 책임의 영상 확인 ·
GK 골킥 숏/롱 분해 제공사 대조 · PPDA·def_x·국면 그리드에 **수집 시각·범위를 남기는 규약**의 docs/30 반영 여부(사용자 판단).

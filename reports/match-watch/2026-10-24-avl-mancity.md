# 2026-10-24 AVL vs Manchester City — 2-1

> 수집일 2026-10-25(00:32 예약 회차 · 경기 다음 날 D+1 · FT 22:20 KST 뒤 약 2시간) · SofaScore event `16363892` · 프리미어리그 MD8 · **홈(빌라 파크)** · 기본 포메이션 4-2-3-1(SofaScore 표기 · 상대 4-2-3-1)
> FotMob matchId `5795486` · WhoScored matchId `1983617`(Opta · scope=full · 이벤트 1,464건 · pulled=2026-10-25 · ⭐ **matchCentreData 전체 JSON 보존** [data/2026-10-24-avl-ws-1983617.json](data/2026-10-24-avl-ws-1983617.json) — headful Playwright로 Cloudflare 통과) · **match_reports #63** · matches #127
> 맨시티 감독 **엔초 마레스카**(SofaScore managers) · 주심 Peter Bankes · 게임 버전 **FC27**(`core.game_version.live_on(con,'2026-10-24')`)
> ⚠️ 예약 프롬프트는 「Manchester City vs Aston Villa」로 적었지만 SofaScore·WhoScored·FotMob 모두 **빌라 홈**이다(home=Aston Villa · venue Villa Park).
> 관전 메모: `reports/match-watch/notes/`에 이 경기 메모(2026-10-24-avl-mancity*) **없음** — 사용자 가설 대조 대신 직전 경기(바이킹전 D+3)가 넘긴 확인 항목 6개를 「이월 확인 대조표」로 판정했다.

## 요약

- **결과는 2-1, 내용은 맨시티가 앞섰다.** xG **0.61 대 1.79**(FotMob · 오픈플레이 0.48/1.43 · 세트 0.13/0.36 · PK 0), 슈팅 8–15, 박스 안 터치 **12 대 53**, 점유 **37%**(1H 41 · 2H 33). 빌라 두 골은 모두 **맨시티 실책에서** 나왔다(SS `errorLeadToGoal` 2 — 6′ 게히 첫 터치 → 잭슨 · 60′ 돈나룸마 위치 선정 → 잭슨). 스즈키 선방 6 · 막은 실점 **+1.74**(SS goals prevented).
- **바이킹전 「보유 3백 + 오른쪽 과부하」는 유지되지 않았다 — 4백 + 왼쪽 쏠림.** 볼 소유 평균 위치(WS): 린델뢰프 (25, 26) · 토레스 (24, 66)가 CB 2, **캐시 (40, 17) · 마트센 (45, 88)이 양쪽 폭**, 그 앞 **카마라 (38, 38) · 고메스 (44, 68)** 더블 피벗, 맥긴 (61, 47) 중앙 10번, 알리송 (63, 22) 오른쪽, 만잠비 (58, 67) 왼쪽 안쪽, 잭슨 (61, 63). 중앙·상대 진영 볼 소유 레인 **왼쪽 44% · 중앙 26% · 오른쪽 30%**(바이킹전 오른쪽 46%의 반대).
- **비보유는 4-4-1-1 중·저블록.** 팀 수비 액션 높이 def_x **34.9**(맨시티 45.3) · 6′ 득점 뒤 6–30′ **31.8~32.2** · 2-1 리드 뒤 60–66′ **20.4**. 맥긴의 수비 액션 평균 (34, 38)은 카마라 (33, 34) 바로 옆 — 공이 없을 때는 CAM이 아니라 중원 셋째 자리로 내려왔다.
- **주앙 고메스는 RB가 아니라 LDM(카마라 왼쪽)** — 바이킹전 RB는 부상 강제 1회성(obs#1129 확정과 일치). 패스 **27/28**(96%) · 가로채기 3 · 볼 소유 레인 왼쪽 58%.
- **「맥긴·고메스 중원 축」은 이 경기에서는 성립하지 않았다.** 연결 상위 쌍은 **토레스→스즈키 20 · 린델뢰프↔토레스 11/10 · 마트센→고메스 10 · 마트센→토레스 10** — 후방 순환과 왼쪽(마트센–고메스)이다. 맥긴은 볼 소유 18 · 패스 8/15(WS)로 연결보다 **압박·탈취·마무리 공급**(선제골 도움 · 기회 창출 4 · FM 7.98)이었다.
- **교체 서열**: 59′ 음바예(알리송 자리 · **오른쪽**) → 1분 뒤 결승골 도움 · 66′ 바클리←맥긴 · 부엔디아←만잠비 · 82′ 고레츠카←고메스 · 마조←잭슨. **가르나초는 소집 명단 밖**(PL 2경기 연속 · 사유 공식 확인 0 · 계약 조항 루머 LOW). 밍스는 벤치 미출전.
- **게임 구현: 추가 관찰.** 이 경기 전용 프리셋 4-2-3-1 Wide · **Counter**/Balanced/48(규칙 Counter/Balanced/55~62 — 라인만 DIVERGE: def_x 34.9). 시즌 정본 변경 없음.

## ⭐ 이월 확인 대조표 (바이킹전 D+3 → 이 경기)

관전 메모가 없어 사용자 가설 대신 바이킹전 리포트 「D+3 ⑷」와 예약 프롬프트가 넘긴 항목을 판정했다. `match_hypotheses` #63 C1~C6.

| # | 이월 항목 | 실측 | 판정 |
|---|---|---|---|
| C1 | 주앙 고메스 RB 재기용 여부 | SS 라인업 M(LDM 칸) · 볼 소유 (44, 68) 왼쪽 58% · RB 존(x<40·y<25) 수비 액션 **0** · RB는 캐시 90분 · BBC 「Worked alongside Kamara」(카마라 옆에서 뛰었다) · 포르투갈어 hoop78 「O volante João Gomes」(볼란치 주앙 고메스) | **불일치(RB 재기용 없음)** — 바이킹전 RB는 부상 강제 1회성 |
| C2 | 만잠비 복귀 | 선발 66′ · LM 칸 · 볼 소유 (58, 67) 왼쪽 71% · 수비 액션 (31, 65) · 54′ 경고(지연) · watson.ch 「주중 CL은 가벼운 종아리 문제로 쉬었다」 · SS missingPlayers엔 「Physical Discomfort」가 그대로 남음(경기 전 표기 잔존) | **일치(복귀)** — 위치는 CAM이 아니라 왼쪽 안쪽 |
| C3 | 마트센(LB) 복귀·기능 | 선발 90′ · 볼 소유 (45, 88) · 상대 진영(x≥66.7) 볼 소유 **11**(팀 공동 1위 · 잭슨 11) · 운반(SS) 전진 2·81.8m · 수비 액션 15 (37, 90) · 막판 홀란 헤더 골라인 클리어 · 평점 AVN 4 ~ SportsDunia 7(가장 크게 갈림) | **일치(복귀 · 높은 LB)** |
| C4 | 가르나초 서열(교체 순번) | 소집 명단 제외(벤치 9명: 비조·밍스·바클리·부엔디아·음바예·보가르드·고레츠카·마조·헤밍스) · 첫 교체는 59′ 음바예 | **판정 불가** — 명단 밖이라 순번 없음. 사유: 공식 0 · OneFootball(AI 보조 표기)·Football Insider 「구매 의무 조항 회피」 루머 LOW(obs#1129와 같은 축) |
| C5 | 보유 3백(밍스·토레스·린델뢰프) + 오른쪽 과부하 유지 여부 | 밍스 벤치 · 4백(캐시·린델뢰프·토레스·마트센) · 양 풀백 보유 x 40~45(바이킹전 밍스 42·고메스 55와 달리 둘 다 폭) · 중앙·상대 진영 레인 **왼쪽 44**/중 26/오른 30 · Sports Mole 「recognised back four」(익숙한 4백) | **불일치(변화)** — 4백 + 왼쪽 쏠림 · 강팀 상대 37% 점유라 3백 빌드업 국면 자체가 적었다 |
| C6 | 맥긴·고메스 중원 축(바이킹전 가설 최종 일치) | 이 경기 연결 상위 = 후방 순환(토레스→스즈키 20 · CB 상호 21) · 마트센→고메스 10 · 맥긴 볼 소유 18 · 패스 8/15(WS) · 고메스 패스 27/28이지만 대상은 토레스·마트센 | **불일치(이 경기 한정)** — 37% 점유·롱볼 22%에서는 중원 연결 국면이 짧았다. 바이킹전 판정을 뒤집지 않는다(경기 성격이 다름) |

## ⭐ 중점 4인 전용 절

### 알리송 (#47 · 브라질 · 전 그레미우)
- **실측**: 선발 RM 59′ · SS 6.4 · FM 6.66 · 볼 소유 16 (63, 22) 오른쪽 75% · 깊은 수신(x≥66.7) 5 · 드리블 1/2 · 슈팅 3(블록 2 · xG 0.10) · 수비 액션 14 (48, 23) · **스프린트 거리 310m**(SS 피지컬 · 팀 최다 · 횟수 13 — 횟수 최다는 잭슨 15) · 상대 진영 볼 소유 7. 바이킹전(SS 8.4 · 깊은 수신 15)과 달리 고립된 1대1 장면이 적었다.
- **에메리 발언**: 이 경기 알리송 언급 **0건**(영어 회견·공식 인터뷰 · 스페인어 0).
- **평점**: BBC 7(「또 눈에 띄는 경기」) · The National 7 「full of running up and down pitch」(피치를 위아래로 쉼 없이 뛰었다) · AVN 6 · EPL Index 6 · dave.sport 6.5(AI 보조 표기) · SportsDunia 6.5.
- **장면**: A Bola 39′ 「Alysson entra na área, dribla para um lado e para o outro e tira o central da frente」(알리송이 박스에 들어가 좌우로 드리블해 센터백을 제쳤다) → 디아스 블록(BBC 서술 · WS 39′ 블록 슈팅). SI 「desperate to dribble at every opportunity」(기회마다 드리블하려 안달했다).
- **모국어(포르투갈어)**: hoop78 「O ponta Alysson, revelado pelo Grêmio, saiu aos 14 do segundo tempo」(그레미우 출신 윙어 알리송은 후반 14분에 나갔다) — 위치는 「ponta」(윙어). ge.globo·GZH·UOL·Lance! 0건(차단·미게재).
- **FC 함의**: 커널 RM 1위 wm_insidefwd/Attack **.455**(Δ.002 무결정 · 2위 wm_wideplm/Attack .454) — 바이킹전 wm_winger/Attack .809와 크게 다르다. 수비 국면 비중이 컸던 경기라 히트맵이 안쪽·아래로 번졌다. 쟁점 #14(알리송 수비 복귀형 vs 윙어 · 「판정할 차례」)의 표본 1경기 — 이 경기 단독으로 닫지 않는다(§7).
- **D+1 보강(10-25 13:00)**: Express & Star(George Bennett · 403 → 검색요약 2회 일치) **7** 「He showcased his attacking qualities in glimpses and never neglected his defensive duties, cutting out a number of attacks.」(공격 자질을 간간이 보여줬고 수비 임무를 결코 소홀히 하지 않아 여러 공격을 끊었다) — 수비 액션 14 실측과 같은 방향 · The Independent(Jolly) 「looking reminiscent of Morgan Rogers」(모건 로저스를 떠올리게 했다) · 1874 사후 라이브 「with Allison obviously high and wide on the right」(알리송은 오른쪽에 높고 넓게 · auto-caption) — 볼 소유 (63, 22)와 일치. 에메리 발언 여전히 **0건**. 포르투갈어 0건(시도: 「Alysson Aston Villa Manchester City ex-Grêmio atuação」 · 「Alysson nota … ge globo OR GZH OR Lance」 · 「Alysson Edward … vitória titular Grêmio Info」). 쟁점 #14 표본에 「수비 임무」 서술 1건 + 「높고 넓게」 1건 — 양쪽 서술이 공존(닫지 않음).
- **13:00 실행 회차 덧붙임**: Yardbarker(상대 관점) 「Alysson was quick, but Gvardiol was quicker」(알리송은 빨랐지만 그바르디올이 더 빨랐다) — WS상 그바르디올 맨시티 왼쪽(ȳ 76~78) · 둘의 파울 경합 4회(알리송 반칙 3) → 측면 돌파 실패는 실측과 같은 방향(obs#1139 · 「D+1 보강 ⑻」).

### 주앙 고메스 (#35 · 브라질)
- **실측**: 선발 **LDM** 82′ · SS 6.7 · FM 7.05 · 패스 27/28 · 볼 소유 31 (44, 68) 왼쪽 58% · 수비 액션 13 (36, 65) · 가로채기 3 · 운반(SS) 8회 69m(전진 0) · 수신 22(x̄ 45.5). 60′~ 볼 소유 (38, 74)로 더 왼쪽·아래.
- **에메리 발언**: 0건. 바이킹전 회견 「고메스는 늘 8번」(obs#1083 맥락)과 충돌 없음 — 이 경기는 6번 짝.
- **평점**: BBC 6 · The National 7 · AVN 7 · EPL Index 6 · SportsDunia 7 · dave.sport 6.5(82분 패스 96%).
- **모국어**: hoop78 「O volante João Gomes jogou até os 37 minutos do segundo tempo」(볼란치 주앙 고메스는 후반 37분까지 뛰었다). 브라질 대형 매체 평점 0건.
- **FC 함의**: LDM 1위 dm_dlp/Build-Up **.811**(Δ.018 무결정 · 2위 dm_holding/Defend .792) · 보유 그리드 1위 dm_dlp/Defend .855. 쟁점 #20(더블 피벗 분업: 고메스 궂은일 vs 카마라 전진)은 이 경기에서 **반대 방향** — 카마라 수비 액션 27(팀 1위) · 고메스 13.
- **D+1 보강(10-25 13:00)**: ⭐ **본인 발언(포르투갈어)** somosfanaticos BR(Sidney Araujo · 10-24) 「Uma vitória muito especial. Sabíamos do desafio que seria enfrentar o líder do campeonato.」(아주 특별한 승리다. 리그 선두를 상대하는 게 어떤 도전인지 알고 있었다) — 발언 매체 미표기 · 기사는 「volante」(볼란치)로 서술 · 전술 내용 없음. Express & Star **7** 「showed good coordination with Kamara, as the pair complimented each other well」(카마라와 호흡이 좋아 서로를 잘 보완했다 · 검색요약) · 1874 「Kamara and Gomez jumped on those two」(카마라·고메스가 상대 두 미드필더에게 달려들었다 · auto-caption) — LDM 실측과 일치. 에메리 발언 0건.

### 맥긴 (#7 · 주장 · 스코틀랜드)
- **실측**: 선발 **CAM** 66′ · SS 7.3 · FM 7.98 · **선제골 도움**(6′ — 게히 실책 직후 컷백) · 기회 창출 4(FM) · 키패스 4(SS) · 볼 소유 18 (61, 47) · 패스 8/15(WS · FM 8/12) · 수비 액션 13 **(34, 38)** · 운반 전진 2(47m).
- **에메리 발언**: 0건. 66′ 교체 사유 언급 없음(UTV 팬 「bold move」(대담한 결정)).
- **평점**: BBC 7(「경기장 전체 최다 기회 창출」) · The National 7 「constant harrying of opponents」(상대를 끊임없이 괴롭혔다)·카마라와 「dovetailing」(잘 맞물렸다) · AVN 7 · EPL Index 7 · SportsDunia 8 · dave.sport 7.5.
- **스코틀랜드 매체**: Daily Record·Herald·Scottish Sun·BBC Scotland **차단**, Scotsman 0건 — 미확보(사유: 검색 도구 차단).
- **FC 함의**: CAM 1위 cam_playmaker/Build-Up .540(Δ.069) · 보유 그리드 1위 cam_halfwinger/Roaming .687. 비보유 위치가 카마라 옆이라 **FC 4-2-3-1 CAM 칸 그대로는 수비 형태를 재현하지 못한다**(FC CAM은 비보유에 내려오지 않는다 — D등급 통설 · 미검증).
- **D+1 보강(10-25 13:00)**: ⭐ **위치 서사 2건이 실측과 일치**(obs#1138) — Express & Star talking points 「Emery deployed him [Manzambi] on the left, rather than as the No 10. Instead, Villa skipper McGinn took up a central role」(만잠비를 10번이 아니라 왼쪽에, 대신 맥긴이 중앙 역할 · 403 → 검색요약) · 상대 관점 Esteemed Kompany 「McGinn would start up front then drift into midfield」(앞에서 시작해 미드필드로 흘러 내려왔다) · 「Ruben Dias was getting drawn out of position … leaving a big hole for Nicolas Jackson」(디아스가 끌려나와 잭슨에게 큰 구멍이 생겼다) — 보유 (61, 47)↔비보유 (34, 38) 이동을 행동으로 서술한 유일 대목. 1874는 보유 시 「가짜 공격수」로 봤고 66′ 교체엔 아쉬움(auto-caption). Express & Star 평점 8은 요약 간 불일치(원문 403). 경기 전 Sports Mole 「McGinn remaining on the right」(맥긴 오른쪽 유지)는 명단 해석 — 실측과 불일치 → 기각. 스코틀랜드 매체 이 경기 0건(시도: 「McGinn … Scotland captain Daily Record」 · 「Scotsman OR Daily Record McGinn Villa City assist Guehi」 · 「heraldscotland OR scottishsun McGinn …」).

### 가르나초 (#17 · 아르헨티나 · 첼시 임대)
- **출전 없음 — 소집 명단 제외**(PL 2경기 연속 · UCL 바이킹전은 72′ 교체 출전). SS missingPlayers에도 없음 = 부상 표기 아님.
- **사유**: 구단·에메리 공식 0건. 영어 OneFootball(필진 「OffsAIde」 · AI 보조 작성 명시)·Football Insider 경유 「구매 의무 조항 발동을 피하려 출전을 제한」 — **LOW**(익명 소스 · obs#1129와 같은 루머). 에메리 최근 직접 발언은 9월 「Garnacho is a little bit behind, because of some circumstances we had in pre-season」(가르나초는 프리시즌의 사정 때문에 조금 뒤처져 있다 · 검색요약 경유).
- **스페인어(아르헨티나)**: La Nación 경기 기사에 가르나초 언급 0 · Olé·TyC·Clarín 차단.
- **함의**: 쟁점 #9(가르나초 LM 기용 시 좌측 구조)·#47 표본 0 유지.
- **D+1 보강 — 당일 판정 정정(obs#1136 · C4 D1 정정 행)**: 사유 「공식 0」 → **에메리 직접 발언 확보** — Hayters(Dan Bennett · 10-24 17:42) 「He's progressing. He played fantastic 20 minutes on Wednesday in Champions League, but today as well we have players as well now ready, available.」(그는 나아지고 있다. 수요일 CL에서 환상적인 20분을 뛰었지만 오늘은 이제 준비된·출전 가능한 선수들이 있다) · 「of course will have as well minutes」(물론 출전 시간도 받을 것이다) · 요약 경유. Football365 「BirminghamLive 인용」은 같은 회견 같은 문장(교차검증 아님). ⇒ 사유 = 복귀 선수(마트센·만잠비·카마라·캐시)로 인한 명단 경쟁. 「구매 의무 조항 회피」 루머(GOAL 「freeze out」·SportBible·TeamTalk — 전부 Football Insider 재가공)는 LOW 유지. 스페인어(아르헨티나) 이 경기 0건 — Olé 「Está progresando」(나아지고 있다)는 10-09경 A매치 휴식기 회견(이 경기 아님 · 영어 번역 가능성).

## 1. 경기 개요와 원천 수치

| 항목 | 빌라 | 맨시티 | 원천 |
|---|---|---|---|
| 점유 | 37% (1H 41 · 2H 33) | 63% | FM(=SS) |
| xG | **0.61**(오픈 0.48 · 세트 0.13 · PK 0) | **1.79**(오픈 1.43 · 세트 0.36) | FM 한 응답(xg_source=FotMob) · SS statistics 0.61/1.79 · SS 슛맵 합 0.61/1.79 일치 |
| xGOT | 0.32 | **2.74** | FM |
| 슈팅 / 유효 / 블록 / 골대 | 8 / 2 / 3 / 0 | 15 / 7 / 4 / 2 | SS·FM |
| 빅찬스(미스) | 1 (0) | 4 (3) | SS |
| 박스 안 터치 | 12 | 53 | SS |
| 패스(성공) | 314 (254 · 81%) | 528 (472 · 89%) | SS |
| 롱볼 | 19/53 | 17/32 | SS |
| 크로스 | 0/5 | 9/22 | SS |
| 파이널서드 진입 | 27 | 49 | SS |
| 태클 / 가로채기 / 클리어 | 31 / 10 / 22 | 13 / 8 / 16 | SS |
| 드리블 | 3/10 | 17/39 | SS |
| 코너 / 파울 / 경고 | 4 / 21 / 4 | 7 / 17 / 4 | SS |
| PPDA | **8.55**(325/38) · 1H 7.58 · 2H 9.53 | 7.5 · 1H 12.08 · 2H 5.38 | WS · `core.whoscored.ppda` |
| def_x(수비 액션 높이) | **34.9**(n=170) | 45.3(n=132) | WS · `core.whoscored.def_x` |
| GK 선방 · 막은 실점 | 6 · **+1.74** | 0 · −1.68 | SS |
| 실책→실점 | 0 | **2** | SS |
| 뛴 거리 · 스프린트 | 113.2km · 70 | 112.1km · 83 | SS |

- **득점·국면**: **6′ 잭슨**(맥긴 도움 — 디아스→게히 긴 패스를 게히가 첫 터치 실수 · 맥긴 탈취 → 잭슨 앤더슨 제치고 니어 상단 · 1-0) · **52′ 홀란**(은디아예 도움 — 카마라 반칙 FK → 짧게 받은 은디아예 크로스 → 홀란 헤더 · 린델뢰프 공중 경합 패 · 1-1) · **60′ 잭슨**(음바예 도움 — 투입 1분 뒤 오른쪽 침투 컷백 → 잭슨 원터치 · 돈나룸마 발 정지 실패 · 2-1). 스코어 국면: lead 6–52′ · level 52–60′ · lead 60′~.
- **교체**: 맨시티 46′ 포든←셰르키 · 리코 루이스←게히(둘 다 경고 · 마레스카 「technical decision」(기술적 결정)) · 69′ 맥아이두←은디아예 / 빌라 **59′ 음바예←알리송** · **66′ 바클리←맥긴 · 부엔디아←만잠비** · **82′ 고레츠카←고메스 · 마조←잭슨**.
- **카드**: 맨시티 게히 32′ · 셰르키 38′ · 앤더슨 74′ · 맥아이두 76′ / 빌라 만잠비 54′(지연) · 캐시 55′ · 마조 83′(항의 — PL 데뷔) · 부엔디아 90+5′.
- **수집 엔드포인트**: SS `/api/v1/event/16363892/{lineups,heatmap,average-positions,statistics,incidents,shotmap,managers,graph}`(Playwright 기본 UA headless · `collect_event.py`) · FM `/api/data/matchDetails?matchId=5795486`(페이지 안 fetch · `load_fotmob_match.py`) · WS `matchCentreData`(**headful** Playwright — headless는 Cloudflare 「Attention Required」 · 앱 브라우저는 로컬 전송이 막혀 전사 대신 headful로 전체 저장).
- **유효 히트맵 기준(45분+ · hit_points 15+)**: 선발 11명 전원 통과(최저 만잠비 28 · 알리송 30 · 맥긴 35). 교체 5명(음바예 10 · 바클리 8 · 부엔디아 19 · 고레츠카 6 · 마조 13)은 45분 미만 — 리포트 근거로만 쓴다.

## 2. 전술 설명

### 점유 구조·빌드업
- **4백 + 더블 피벗 + 왼쪽 쏠림.** 명단 4-2-3-1 그대로 섰다. CB 린델뢰프 (25, 26)·토레스 (24, 66)가 넓게 갈라지고 캐시 (40, 17)·마트센 (45, 88)이 폭. 카마라 (38, 38)가 오른쪽·낮게, 고메스 (44, 68)가 왼쪽. 앞선은 맥긴 (61, 47) 중앙 · 만잠비 (58, 67) 왼쪽 안쪽 · 알리송 (63, 22) 오른쪽 · 잭슨 (61, 63)이 왼쪽 채널로 빠진다.
- **후방 순환 → 왼쪽 전진 또는 롱볼.** 연결 상위: 토레스→스즈키 20 · 린델뢰프→토레스 11 · 토레스→린델뢰프 10 · **마트센→고메스 10 · 마트센→토레스 10** · 스즈키→토레스 9 · 고메스→토레스 9 · 린델뢰프↔캐시 9/9. 롱볼 비중 **20%**(69/338 WS · SS 53/314) — 바이킹전 6.8%의 3배. 스즈키 패스 36/49 · 롱 19(성공 6) · GK 롱 비중 구간 0~100%(75′~ 70%).
- 중앙·상대 진영 볼 소유 레인 **왼쪽 44 · 중 26 · 오른 30%**. 상대 진영 볼 소유 상위: 잭슨 11 · **마트센 11** · 맥긴 7 · 알리송 7 · 마조 7.
- **잭슨은 박스에 머물지 않았다(다시).** 볼 소유 27 · 평균 (61, 63) 왼쪽 48% · 깊은 수신 7 · 운반 전진 3(69m · SS) · 스프린트 15회. 슈팅 2(둘 다 골 · xG 0.36).

### 비점유 구조·압박
- **0–6′ 높게 → 6′ 득점 뒤 중·저블록.** 빌라 def_x **55.6**(0–6′) → **31.8**(6–15′) · **32.2**(15–30′) · 41.8(30–45′) · 40.3(45–52′) · 34.8(52–59′) · **20.4**(60–66′) · 31.1(66–75′) · 35.8(75′~). PPDA 6.5 → 6.2 → 11.75 → 6.62 · 2H 9.53.
- **4-4-1-1.** 수비 액션 평균(0–52′): 캐시 (42, 11) · 알리송 (46, 22) · 맥긴 (39, 37) · 카마라 (33, 39) · 고메스 (33, 40) · 만잠비 (31, 62) · 잭슨 (52, 61) · 마트센 (51, 92). 맥긴이 카마라 옆으로 내려오고, 만잠비가 왼쪽 미드 라인을 지킨다. **마트센은 수비 액션도 높다(51, 92)** — 맨시티 오른쪽(쿠사노프 RB→은디아예)을 앞에서 끊는 쪽.
- 태클 31(맨시티 13) · 캐시 태클 **8**(양 팀 최다) — 도쿠 전담(BBC·UTV 「Cash shut Doku on the outside all game long」(경기 내내 바깥쪽으로 막았다)). 단 캐시 드리블 허용 5(SS dribbled past).
- 마레스카 「We struggled the first probably 10-15 minutes and we expected them in one way and they were in a different way」(처음 10~15분 고전했다 — 한 방식으로 나올 줄 알았는데 다르게 나왔다 · NBC) — 「다른 방식」의 내용은 미서술. 실측으로는 0–6′ def_x 55.6의 **높은 출발**이 그 후보다.

### 전환·rest-defense·세트피스
- **두 골 모두 전환.** 6′ 높은 위치 탈취(サッカーキング 「敵陣高い位置でボールを奪い切ると」(상대 진영 높은 위치에서 공을 완전히 빼앗자)) · 60′ 음바예 오른쪽 침투(ESPN 「one long ball over the top … has time to run into that space」(롱볼 하나로 공간에 뛰어들 시간)). 마레스카 「they play for that. They wait for that」(그걸 노리고 기다린다 · 회견 전사 auto-caption).
- **세트피스 실점.** 52′ 짧은 FK → 은디아예 (93, 22) 크로스 → 홀란. ESPN 히슬롭 「Villa … get very narrow … leave a striker out wide with a player like Ndiaye」(빌라가 아주 좁아져 은디아예 같은 선수를 측면에 남겼다 · auto-caption) — 은디아예 앞 만잠비 1대1. `match_set_pieces` 30행(우리 14).
- 빌라 세트 xG 0.13(코너 4).

## 3. 전술적 특성

- **강점**: ⑴ 첫 6분 높은 출발로 맨시티 빌드업 실책 유도(게히 · 마레스카도 인정) ⑵ 중·저블록에서 박스 수비 — 맨시티 박스 터치 53에 슈팅 xG 1.79 · 스즈키 선방 6(박스 안 5) · 마트센 골라인 클리어 ⑶ 교체 직후 속도(음바예)로 전환 한 방 ⑷ 캐시 도쿠 봉쇄(태클 8).
- **약점**: ⑴ 자기 창출 부족 — xG 0.61 · 빅찬스 1 · 크로스 0/5 · 박스 터치 12. 결과가 내용(xG 차 −1.18)을 크게 앞섰다 ⑵ 세트피스 측면 1대1(52′ 실점) ⑶ 롱볼 성공 19/53(36%) — 잭슨 공중 2/2 외에는 회수 근거 약함 ⑷ 60–66′ def_x 20.4까지 내려앉음.
- **상대 교란**: 맨시티는 1H 게히를 사실상 RB 위치에 두고(ESPN 「your center back playing almost as a right back」(센터백이 거의 라이트백처럼)) 쿠사노프를 높였다가, 하프타임 리코 루이스 투입으로 수비 시 3백(ESPN 「At times it was a three when they were defending」(수비할 때 가끔 3백))·그바르디올 전진. 2H 맨시티 PPDA **5.38**(빌라 자기 진영 패스 성공률 75′~ 63%).
- **기존 프로필·직전 경기 대비**: 강팀 원정/홈 저점유 경기의 에메리 계열(리드 후 블록 하강 — 뉴캐슬전 77′+·바이킹전 2H와 같은 방향)이다. 바이킹전의 고메스 RB→하프스페이스 3선은 **명단 복귀(캐시·마트센)와 함께 사라졌다** — 구조 선택이 아니라 가용 인원 강제였다는 obs#1129 판단을 실측이 지지한다.

## 4. 경기 중 변화

1. **0–6′ (0-0)**: 빌라 def_x 55.6 · PPDA 6.5 — 높은 압박. 6′ 게히 실책 → 맥긴 → 잭슨 1-0.
2. **6–52′ (리드)**: 중·저블록(def_x 31.8~41.8) · 맨시티 점유 59%. 13′·21′·24′ 은디아예·셰르키·쿠사노프 슈팅 선방(日刊スポーツ). 39′ 알리송 슈팅 디아스 블록. 1H xG 0.38–0.54.
3. **46′ 맨시티 2명 교체**: 포든·리코 루이스 — 측면(도쿠)으로 공 보내기(UTV) · 수비 3백 변형. 52′ FK → 홀란 1-1.
4. **59–60′ 음바예 투입 → 결승골**: 알리송 자리(오른쪽)에 음바예 — 1분 뒤 오른쪽 침투 컷백 → 잭슨 2-1.
5. **60–66′**: def_x **20.4** — 가장 낮게 내려앉음 · 맨시티 PPDA 5.5.
6. **66′ 바클리←맥긴 · 부엔디아←만잠비 / 82′ 고레츠카←고메스 · 마조←잭슨**: 부엔디아 왼쪽 (49, 75) · 바클리 오른쪽 중원 (49, 29) · 마조 최전방 (79, 60). 75′~ 빌라 GK 롱 비중 70% · PPDA 7.0. 2H 빌라 슈팅 2 · xG 0.22.

## 5. 선수별 분석 — 출전 선수 전원

평균 위치는 WS 볼 소유 이벤트 (x, y) · y 낮음=오른쪽 · 커널은 FC27 · 「1위(Δ)」는 해당 칸 1·2위 격차.

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치·히트맵 | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| 스즈키 | GK | 90 · SS **9.0** · FM 8.56 · 선방 6(박스 안 5) · 막은 실점 +1.74 · 패스 36/49 · 롱 19(성공 6) | (8.6, 51.3) | 경기 승부처 — 1H 유효 3 전부 선방 · 2H 56′·68′ 그바르디올 | gk_goalkeeper/Defend .939(Δ.034 무결정 · Balanced .905) |
| 캐시 | RB · 도쿠 전담 | 90 · SS 6.8 · FM 7.18 · **태클 8** · 드리블 허용 5 · 패스 19/22 | (40.1, 17.3) · 오른쪽 90% · 수비 (31, 15) | 바깥쪽 봉쇄 · 55′ 경고 · 막판 주장 완장 | fb_fullback/Balanced .929(Δ.023 무결정 · Versatile .906) |
| 린델뢰프 | RCB | 90 · SS 6.8 · 패스 35/41 · 클리어 4 · 공중 1-1 | (25.3, 26.4) | 52′ 홀란 공중 경합 패 · UTV 「crucial tackles」 | cb_bpd/Aggressive .921(Δ.005 무결정 · Build-Up .916) |
| 파우 토레스 | LCB | 90 · SS 6.5 · 패스 49/58 · 운반 23회 178m(SS · 전진 0) · 공중 0-2 | (23.9, 66.1) | 후방 순환 축(스즈키 연결 20) · BBC 「Calming presence」(안정감) | cb_bpd/Build-Up .975(Δ.058) |
| 마트센 | LB · 높은 폭 | 90 · SS 6.7 · FM 6.97 · 상대 진영 볼 소유 11 · 운반 전진 2(82m) · 태클 4 · 슈팅 1(블록) · 골라인 클리어 | (45.2, 88.2) · 왼쪽 93% | 왼쪽 쏠림의 출발점(→고메스 10·→토레스 10) · 평점 4~7로 갈림 | fb_wingback/Balanced .869(Δ.069) |
| 카마라 | RDM · 수비 중심 | 90 · SS 6.9 · FM 7.39 · 패스 27/30 · **태클 6**·수비 액션 27(팀 1위) · 클리어 4 · 52′ FK 내준 반칙 | (37.7, 38.3) · 수비 (33, 34) | BBC 「At the heart of everything good」(좋은 장면마다 중심) · 에메리 「today was match for them — like Kamara and Cash」(오늘은 카마라·캐시 같은 선수들의 경기였다) | dm_holding/Defend .779(Δ.013 무결정 · dm_centrehalf/Defend .765) · 보유 1위 dm_dlp/Defend .863 |
| 주앙 고메스 | **LDM**(RB 아님) | 82 · SS 6.7 · FM 7.05 · 패스 **27/28** · 가로채기 3 | (44.0, 67.9) · 왼쪽 58% | 볼 순환·왼쪽 연결 | dm_dlp/Build-Up .811(Δ.018 무결정 · dm_holding/Defend .792) |
| 맥긴 | CAM → 비보유 중원 셋째 | 66 · SS 7.3 · FM 7.98 · **도움 1** · 키패스 4 · 패스 8/15(WS) | (61.4, 47.2) · 수비 (34, 38) | 압박·탈취(6′) · 기회 창출 최다 | cam_playmaker/Build-Up .540(Δ.069) · 보유 1위 cam_halfwinger/Roaming .687 |
| 만잠비 | LM · 왼쪽 안쪽 | 66 · SS 6.8 · FM 6.77 · 태클 3 · 듀얼 6-3 · 54′ 경고 | (58.4, 66.9) · 왼쪽 71% · 수비 (31, 65) | 38′ 셰르키 탈취(경고 유도) · 52′ FK 측면 1대1(은디아예) | wm_widemid/Defend .538(Δ.007 무결정 · wm_wideplm/Build-Up .531) · 보유 1위 wm_insidefwd/Balanced .741 |
| 알리송 | RM · 오른쪽 윙어 | 59 · SS 6.4 · FM 6.66 · 슈팅 3(xG .10) · 스프린트 13 | (63.0, 22.2) · 오른쪽 75% | 39′ 박스 드리블→디아스 블록 · 수비 복귀 14 | wm_insidefwd/Attack .455(Δ.002 무결정 · wm_wideplm/Attack .454) |
| 잭슨 | ST → 왼쪽 채널 | 82 · SS **9.5** · FM 8.85 · **2골**(xG .36) · 드리블 2/2 · 공중 2/2 · 스프린트 15 | (60.8, 62.8) · 왼쪽 48% · 깊은 수신 7 | 결정력(xG .36 → 2골) · 에메리 「How he was defending, wow」(수비하는 모습이 와) | st_advanced/Support .375(Δ.035 무결정 · st_false9/Attack .340) — 전 ST 역할 .44 이하 |
| 음바예 (59′) | RM(알리송 자리 · **오른쪽**) | 31 · SS 6.6 · **도움 1**(60′) · 키패스 1 | (66.1, 26.4) | 투입 1분 뒤 결승골 공급 | 표본 미달 |
| 바클리 (66′) | 중원 오른쪽(맥긴 자리) | 24 · SS 6.6 · 패스 2/4 | (49.5, 28.7) | 리드 지키기 · 공중 1 | 표본 미달 |
| 부엔디아 (66′) | LM(만잠비 자리) | 24 · SS 6.5 · FM 5.88 · 태클 3 · 90+5′ 경고 | (48.9, 75.4) · 수비 (35, 92) | 왼쪽 수비 커버 · The National 「full of energy」(에너지가 넘쳤다) | 표본 미달 |
| 고레츠카 (82′) | LDM(고메스 자리) | 8 · SS 6.5 · 패스 2/3 | (43.9, 44.7) | — | 표본 미달 |
| 마조 (82′) | ST(잭슨 자리) · PL 데뷔 | 8 · SS 6.7 · 듀얼 4-4 · 83′ 경고 | (79.0, 59.8) | 높은 위치 기준점 | 표본 미달 |

## 6. 전술 변화 판정

- **유지**: 리드 후 블록 하강(뉴캐슬전·바이킹전과 같은 방향) · 잭슨의 박스 밖 이동(왼쪽 채널) · 세트피스 측면 수비 취약(쟁점 #29).
- **변화**: ⑴ 3백 빌드업·오른쪽 과부하 → **4백 + 왼쪽 쏠림**(가용 인원 복귀 + 37% 점유) ⑵ 고메스 RB → LDM ⑶ 맥긴 RDM/우측 → CAM(비보유 중원) ⑷ 음바예 왼쪽 → **오른쪽 교체 투입** ⑸ 롱볼 비중 6.8% → 20%.
- **직전 경기 대비**: 바이킹전(점유 54% · 3-2-5)과 이 경기(37% · 4-4-1-1 블록)는 경기 성격이 달라 「유지/변화」를 구조 선택으로 읽지 않는다 — 가용 인원(캐시·마트센·만잠비 복귀)과 상대 수준이 갈랐다(70-lessons 「선발은 가용성 질문」).
- **반영**: observations 4행(#1132~#1135 · 구조 변화·고메스 위치·결과-내용 괴리·가르나초) · `manager_profiles` situational 덧붙임(강팀 상대 저점유 블록 실측) · 이월 대조표 6행(`match_hypotheses`).

## 7. 게임 구현 판정

- 결론: **추가 관찰** — 단일 경기 · 여러 칸 Δ≤.05 · 결과가 내용(xG 0.61–1.79)과 어긋난 경기. 시즌 정본(slot_canon_roles · prescriptions · team_tactic_setups)은 바꾸지 않는다.
- **이 경기 전용 팀 설정**: FC27 · **4-2-3-1 Wide** · 빌드업 **Counter** · 수비 접근 **Balanced** · 라인 **48**. `core.team_settings.suggest(37, 314, 53, 8.55)` → Counter/Balanced/55~62(롱볼 16.9%) · 기록 Counter/Balanced/48 → **DIVERGE(라인)**: def_x 34.9(바이킹전 35.2와 같은 대역)·6–30′ 31.8~32.2·60–66′ 20.4로 실제 블록이 규칙 구간보다 낮다. PPDA 8.55는 0–6′ 높은 출발과 중원 태클(31)이 만든 값이라 라인 높이 근거로 약하다. ⚠️ FC27 라인 구간 자체가 미실측(HANDOFF P1 「라인 슬라이더 상하한」) — 48은 상대값.
- **보유/비보유 형태**: 보유 4-2-3-1(양 풀백 폭 · 왼쪽 쏠림) · 비보유 4-4-1-1(맥긴 하강).
- **이 경기 선발 11명(커널 단일 경기 fit)**:

| 슬롯 | 선수 | 역할/포커스 | fit | Δ(2위) | 선택 이유 |
|---|---|---|---|---|---|
| GK | 스즈키 | gk_goalkeeper/Defend | .939 | .034 무결정 (Balanced) | 커널 1위 |
| RB | 캐시 | fb_fullback/Balanced | .929 | .023 무결정 (Versatile) | 커널 1위 · 도쿠 전담 잔류형 |
| RCB | 린델뢰프 | cb_bpd/Aggressive | .921 | .005 무결정 (Build-Up) | 커널 1위 · 쟁점 #23 표본 |
| LCB | 파우 토레스 | cb_bpd/Build-Up | .975 | .058 (Defend) | 커널 1위 |
| LB | 마트센 | fb_wingback/Balanced | .869 | .069 (fb_fullback/Balanced) | 커널 1위 · 상대 진영 볼 소유 11 |
| RDM | 카마라 | dm_holding/Defend | .779 | .013 무결정 (dm_centrehalf/Defend) | 커널 1위 · 쟁점 #19·#51 표본(holding 쪽) |
| LDM | 주앙 고메스 | dm_dlp/Build-Up | .811 | .018 무결정 (dm_holding/Defend) | 커널 1위 + 패스 27/28 |
| CAM | 맥긴 | cam_playmaker/Build-Up | .540 | .069 (cam_halfwinger/Roaming) | 커널 1위 · ⚠️ 비보유 하강은 칸이 재현 못 함 |
| LM | 만잠비 | wm_widemid/Defend | .538 | .007 무결정 (wm_wideplm/Build-Up) | 커널 1위(수비 국면 우세) · 보유는 wm_insidefwd/Balanced .741 |
| RM | 알리송 | wm_insidefwd/Attack | .455 | .002 무결정 (wm_wideplm/Attack) | 실측 무결정 — 바이킹전 wm_winger/Attack .809와 갈림 · 쟁점 #14 |
| ST | 잭슨 | st_advanced/Support | .375 | .035 무결정 (st_false9/Attack) | 커널 1위 = 시즌 정본과 같음 · 전 역할 .44 이하 · 쟁점 #4 |

- **근거 등급(불변규칙 12)**: 역할 히트맵 = fut.gg 게임 역할 히트맵(B · FC27 역할표 FC26 전항 일치 승계 · 2026-10-22). 「Counter 빌드업은 롱볼·전환 우선」은 game_system_changes 기준 B(FC26 설명 승계 · FC27 변경 미확인). 「FC CAM은 비보유에 내려오지 않는다」는 **D(통설)** — 실측 미검증.
- **시즌 정본 대조**(slot_canon_roles FC27 · 4-2-3-1 Wide): ST 정본 `st_advanced/Support` — 이 경기 1위와 같다(.375 · 낮음). RDM 정본 `dm_holding/Defend` — 카마라 1위와 같다. LM 정본 `wm_insidefwd/Balanced` — 만잠비 **보유** 그리드 1위와 같다(.741 · 전체 그리드는 widemid/Defend). RB 정본 `fb_wingback/Balanced`(캐시) — 이 경기 1위 fb_fullback/Balanced(Δ.023 무결정).
- `prescriptions`·`slot_canon_roles`·`team_tactic_setups` 변경: **없음** · FC27 슬롯 정본 판단 5건(사용자 보류 · HANDOFF P1)은 「다음 AVL 공식전 2경기」 중 **1경기째** 표본이다 — 다음 경기(본머스 컵 또는 풀럼) 뒤 같은 표로 재제출.
- **판정 쟁점 `--due`(회차 마무리)**: AVL 「판정할 차례」 3건 — #7 음바예 윙어 vs IF · #14 알리송 수비 복귀형 vs 윙어 · #30 설정 축 없는 성향. 기한 초과 0(G39 통과)이라 이 회차에선 닫지 않았다. #14 근거(단일 경기 커널 RM · FC27): 뉴캐슬 wm_winger .857 vs wm_widemid .806(Δ.051) · 바이킹 .809 vs .410 · 맨시티 .447 vs .435(Δ.012 무결정) — 3경기 모두 winger 우위이나 결정적 격차는 1경기. 묶인 주장이 양쪽을 섞고 있어 사람 판정으로 넘긴다.
- **다음 경기 재검증**: ⑴ 알리송 RM 역할(쟁점 #14 · 이 경기 insidefwd 무결정 vs 바이킹전 winger) ⑵ 카마라 RDM holding vs dlp(#19·#51) ⑶ 마트센 LB 높이(fb_wingback 유지 여부) ⑷ 음바예 오른쪽 기용 반복 여부(#6·#48) ⑸ 가르나초 명단 복귀.

⚠️ 이 설정은 `match_game_setups`·`match_player_prescriptions`의 `MATCH ONLY` 프리셋이다. 전체 시즌 전술이나 대표 선수 역할에 자동 병합하지 않는다.

## 8. 영상·기사·감독 발언

- **영상**(AVL 필수 채널 4곳 + 검색 · 자막 포착은 전부 뮤트):
  - 전사·요약 4편(auto-caption · `match_videos` #380~#383 · 구현 주장 6행): **AVFC 공식** 「"Everything today was positive!" Unai Emery FULL post-match interview」(xN_Cosi8gC4 · 10-24) · **UTV** 「I'D RATHER BE A VILLAN THAN A CHEAT | ASTON VILLA 2-1 MANCHESTER CITY」(qcGR9TddiPo · 10-24) · **ESPN FC** 「Man City LOSE vs. Aston Villa! …」(NDhq-OUuzDo · 10-24 · 중립) · **BeanymanSports** 마레스카 경기 후 회견(tWsbxCU1SjE · 10-24 · 상대 감독).
  - **1874** 「Nicolas Jackson at the double as Villa beat Man City AGAIN」(1Xv_Y_4iecc) — 수집 시점 **라이브 진행 중**(자막 미생성) → 13:00 회차 재시도.
  - **The Villans · Jacob Horsfall** — 이 경기 영상 **0건**(최신은 경기 전 프리뷰 「Why Manchester City Face Biggest Challenge Yet At Villa Park」(9l_njxOTvEk) · Horsfall 「What Has Happened To Sunderland?」).
  - 미전사(검색 확보 · D+1~D+3 대상): More Lyes 「Emery Has Done It Again..」(v5XShfKHy-g) · tacticafoot 「Emery & Maresca React」(A07aC4fuVDc) · The Football Flex(aFXSkC3cwwY) · URKG(RpK7bMvg8_U) · Premier League Dad 라이브(s7go7bWC1no).
- **기사**: NBC(Nicholas Mendola · 양 감독 발언) · PA/Irish News(Sunny Badwal) · GOAL(Khaled Mahmoud · Adhe Makayasa) · Football365(Sam Cooper) · City Xtra(Nathan Allen) · SI · Sports Mole(Darren Plant) · TNT 라이브 · 평점(BBC/Yahoo · The National · AVN · EPL Index · dave.sport(AI 보조) · SportsDunia) · 다국어 아래.
- **감독 1차 발언**:
  - 에메리: 「We planned this match, trying to keep the same consistencies and demands.」(같은 일관성과 요구를 유지하도록 이 경기를 계획했다 · NBC) · 「today was match for them — like Kamara and Cash.」(오늘은 카마라·캐시 같은 선수들의 경기였다 — 바이킹전 휴식 선수 기용 · NBC) · 잭슨 「How he was working. How he was defending, wow.」(얼마나 일하고 수비했는지, 와 · NBC) · 공식 인터뷰 「we kept calm after their goal and … continue in our game plan」(실점 뒤 침착하게 게임 플랜을 이어갔다 · xN_Cosi8gC4 auto-caption). 알리송·고메스·맥긴·가르나초·밍스 개별 언급 **0건**.
  - 마레스카: 「We struggled the first probably 10-15 minutes and we expected them in one way and they were in a different way」(처음 10~15분 고전 — 다르게 나왔다 · NBC) · 「the second goal again came from transition」(두 번째 골은 또 전환에서 · 회견 전사 auto-caption) · 게히 교체 「It's just a technical decision … also because he had a yellow card」(기술적 결정이자 경고 때문 · PA).
- **다국어(불변규칙 10)**:
  - 스페인어(필수): EFE(Infobae) 「Emery acaba con el imparable City」(에메리가 멈추지 않던 시티를 끝냈다) — 에메리 직접 인용 없음 · Fútbol Centroamérica 「Hoy fue una prueba muy buena, estábamos muy motivados」(오늘은 아주 좋은 시험이었고 우리는 동기부여가 높았다) — **영어 발언의 번역(동일 원문)으로 판단**, 교차검증 아님 · La Nación(부엔디아 경고·마트센 클리어). Marca·AS·Relevo·MD·Cadena SER **차단** → **에메리 스페인어 원어 발언 미확보**.
  - 포르투갈어: hoop78(고메스 볼란치·알리송 윙어) · A Bola 라이브(만잠비 속도·셰르키 경고·알리송 39′·카마라 52′ 반칙) · Terra.
  - 프랑스어: wiwsport(음바예 첫 터치 도움) · Le Soleil · Foot Mercato(평점). 독일어/스위스: Blick(만잠비) · watson.ch(종아리 문제). 일본어: サッカーキング · 日刊スポーツ(스즈키 선방 시각) · FOOTBALL ZONE. 이탈리아어(마레스카): DerbyDerbyDerby 「si sono difesi con ordine e sono ripartiti con pericolosità」(질서 있게 수비하고 위협적으로 역습했다) · Tuttosport · Fanpage(403 — 검색요약 「Non credo che meritassimo di perdere」(질 만했다고 생각하지 않는다) 미검증).
- **미수행·미확인과 사유**:
  - **Jacob Tanswell X(@J_Tanswell)**: HTTP 402 · nitter 서비스 종료(10-10) · 검색은 9월 트윗만 → **미수행(접근 차단)** · 13:00 회차 재시도.
  - Birmingham Mail · Express & Star(403) · Shropshire Star(403) · Guardian · Sky · The Athletic · MEN · avillafan(AVR)·4th Official·MOMS: 검색 미노출 또는 차단 — D+1 13:00 회차.
  - 스코틀랜드(Daily Record·Herald·Scottish Sun·BBC Scotland) 차단 · 브라질 대형 매체(ge.globo·UOL·Lance!·GZH) 0건.
  - 전술 블로그(TFA·BTL·Spielverlagerung·Coaches' Voice): D+0 게시 전 — D+2·D+3 추적 대상.

## 9. 데이터 반영과 한계

- **DB 추가**: matches #127 · player_matches 16(국면 그리드 16 · phase 분 · pos_class · SS 확장(운반 실측) · FotMob 경기 스탯 +470키 · WS 운반 추정·수신) · team_match_stats 1(xG 4종 FotMob 동일 스냅샷 · PPDA·def_x) · match_events 19 · match_period_stats 2 · match_shots 23 · match_momentum 92점 · match_set_pieces 30 · match_reports #63 · match_player_reports 16 · match_game_setups 1 · match_player_prescriptions 16 · match_hypotheses 6(이월 C1~C6) · match_phase_metrics 74 · match_tactical_changes 6 · observations 4 · match_videos 4편 요약·구현 주장 6행 · manager_profiles situational 덧붙임.
- **한계**: ⑴ 결과-내용 괴리(xG 0.61–1.79 · 두 골 모두 상대 실책) — 「강팀 공략 성공」으로 일반화 금지 ⑵ 37% 점유라 보유 구조 표본이 짧다(WS 볼 소유 393) ⑶ SS missingPlayers가 만잠비를 「Physical Discomfort」로 남긴 채 출전 — 경기 전 표기 잔존 ⑷ 맥긴 패스 WS 8/15 vs FM 8/12(제공사 차이) ⑸ 영상은 D+0.5 시점이라 전술 분석 채널(The Villans·Horsfall·1874 사후판) 미게재 ⑹ 일부 평점 출처(dave.sport · OneFootball)는 AI 보조 작성 표기.
- `match_reports.status` = **draft**(D+1 13:00 보강 · D+2 · D+3 추적 남음). G12·G37 결과는 ship 로그.

## D+1 추적 (예약 `mw-avl-mancity-collect-1300` · 2026-10-25 13:00)

- 남은 것: 1874 사후판 전사 · Tanswell X 재시도 · Birmingham Mail(Townley·Preece)·Express & Star 원문 · avfc.co.uk 회견 전문 · The Athletic · 에메리 스페인어 원어 · 미전사 영상 5편.

## D+2 추적 (예약 `mw-avl-mancity-d2` · 2026-10-26 20:00)

- 전술 블로그·The Villans·Horsfall 분석 영상 · 이월 대조표 재판정.

## D+3 추적 (예약 `mw-avl-mancity-d3` · 2026-10-27 20:00)

- 다음 경기(본머스 컵 · 10-28 수) 명단으로 가르나초·밍스 재확인 · complete 판정.

## D+1 보강 (2026-10-25 13:00)

> 예약 `mw-avl-mancity-collect-1300` · 이 PC · 앞 회차(00:32) 이후 새 자료만. 실측(§2·§3) 재수집 없음. 기사 재검색 원 보고는 [2026-10-24-avl-mancity-d1-sources.md](2026-10-24-avl-mancity-d1-sources.md)(서브에이전트 · WebSearch/WebFetch **요약 경유**). 중점 4인 새 대목은 각 전용 절 「D+1 보강」 불릿.

### ⑴ 당일 판정 정정
- **가르나초 명단 제외 사유 「공식 0」 → 에메리 직접 발언 있음**(Hayters · obs#1136 · `match_hypotheses` C4 D1 정정 행 — 원래 D0 행 보존). 서열 판정은 계속 **판정 불가**(명단 밖). 원문·번역은 가르나초 절.
- 그 밖의 당일 판정 뒤집힘 **0**. 대조표 C1·C2·C3·C5·C6 그대로.

### ⑵ 감독 발언 새것 (에메리 · 회견/MOTD)
- 잭슨 역할 지시(obs#1137): 「Sometimes he can drop, because he's good at getting duels, but we need him more running in behind.」(경합에 강해 가끔 내려와도 되지만 우리는 뒷공간 침투를 더 원한다) · 「He is understanding as well where we need him.」(우리가 그를 어디에 필요로 하는지 이해한다) — Hayters · 요약 경유. 쟁점 #4·#5에 감독 진술 1건(이 경기 ST 1위 st_advanced/Support Δ.035 무결정 — 회견 1건으로 닫지 않음).
- 스즈키 빌드업 의도: 「he can play short, he can understand where is the superiority to break the opponent's press」(짧게 줄 수 있고 상대 압박을 깰 수적 우위가 어디인지 안다) · 「He has as well qualities to do long ball」(롱볼 자질도 있다) — WS 연결 1위 토레스→스즈키 20과 맞물림. 쟁점 #3.
- BBC MOTD(SoccerNews/Stats Perform 전재): 「We analysed the match against Arsenal at home. … We analysed the match against Forest at home. … We improved so many things against Brentford at home.」(홈 아스날전·포리스트전을 분석했고 … 홈 브렌트퍼드전에서 많은 걸 개선했다) — 강팀 홈전 준비 근거가 앞선 홈 3경기 분석이라는 진술(구체 전술 없음).
- PA: 「We have 11 points. It's not enough, but we have a much better feeling.」(승점 11은 부족하지만 느낌은 훨씬 좋다).
- 선수 개별(알리송·고메스·맥긴·밍스·음바예) 평가·교체 사유 발언: **0건**(이번 회차도).
- **에메리 스페인어 원어**: **0건** — GOAL 스페인어판 「Preparamos este encuentro intentando mantener la misma regularidad y exigencia.」(같은 일관성과 요구를 유지하려 이 경기를 준비했다)는 「Traducido por」 표기의 **영어 회견 번역 복제**(교차검증 아님). 시도: 「Unai Emery "City" "hemos" Aston Villa Jackson declaraciones」 · 「Emery … Marca AS Relevo」 · 「Movistar OR DAZN entrevista」 · 「Cadena SER OR El Desmarque OR COPE」.
- 선수 발언: 캐시 「He's always got a new plan for something.」(그는 늘 새 계획이 있다 · AVFC 공식) · 도쿠 대응 「I like to get tight early on」(일찍 바짝 붙는 걸 좋아한다 · TNT 경유 Sky).

### ⑶ Jacob Tanswell
- X 직접 조회 **402**(x.com) · nitter 종료 → 검색 색인 경유 경기 중 트윗 **1건**: 「Villa struggle to control games at the best of times, let alone against Man City. Villa leaning into transitional, pacey strengths.」(빌라는 평소에도 경기 통제가 어려운데 맨시티 상대로는 더하다. 전환·속도 강점에 기대고 있다) — 59′ 음바예 투입 시점. 우리 판정(4-4-1-1 중·저블록 + 역습)과 같은 방향.
- FT·회견 verbatim 트윗 · The Athletic 경기 기사: **0건**(시도 검색어 6종 — d1-sources §1). D+2에 브라우저 headful X 재시도.

### ⑷ 충돌 판정
| 서술 | 출처 | 실측 | 판정 |
|---|---|---|---|
| 도쿠를 「후반 대부분 마트센이 막았다」 | GOAL(맨시티 평점 · Adhe Makayasa) | WS 도쿠 이벤트 y̅ 1H **79.0**(36건 · y>66 32) · 2H **82.8**(42건 · y>66 40 · y<33 0) — 양 하프 모두 맨시티 **왼쪽** = 빌라 오른쪽(캐시) | **기각** — 캐시 담당(캐시 인터뷰·Bains·UTV 일치) |
| 맥긴 「오른쪽 유지」 | Sports Mole 경기 전 선발 기사 | 볼 소유 (61, 47) 중앙 | **기각**(명단 해석) |
| 「They want to keep the ball」(공을 지키려 한다) | 홀란 플래시 인터뷰(tacticafoot 재편집 · auto-caption) | 점유 37% · 롱볼 20% | 상대 선수 인상 — 채택 안 함 |
| 「press from the front」(전방 압박) | More Lyes(auto-caption) | 높았던 건 0–6′(def_x 55.6)뿐 · 전체 34.9 | 부분 — 초반 구간만 |
| 골킥 압박 7~8회 「한쪽 가두기」 | Bains Analysis(auto-caption) | 높은 압박 0–6′ 집중 · 골킥 국면 압박 횟수는 미조회 | 미검증(PENDING #17) |
| 교체 시각 음바예 55′/58′/60′ · 맥긴 65′ | FotMob 요약·BBC·라이브·AVFC | SS 59′·66′ | SS 정본 유지 |

### ⑸ 영상 (필수 채널 4곳 + 검색 · 전부 뮤트 pot 경로)
- **채널 최신 목록 조회(13:10)**: **1874** — 사후 라이브 「Nicolas Jackson at the double as Villa beat Man City AGAIN」(1Xv_Y_4iecc) 종료 → **전사**. **UTV** — 새 업로드 없음(최신 qcGR9TddiPo는 앞 회차 요약 완료). **The Villans** — 새 업로드 「PREMIER LEAGUE GAMEWEEK 8 PREDICTIONS」(2wNasTobcec · 경기 전 예측 → 건너뜀). **Jacob Horsfall** — 「What Has Happened To Sunderland?」(sh16rkzsmuw · 빌라 아님 → 건너뜀).
- **전사·요약·구현 주장 +6편**(`match_videos` #384~#389 · 전부 r63 귀속 · 주장 17행 · auto-caption):
  - 1874 사후 라이브(1Xv_Y_4iecc · 31:21): 보유 「4-2-4」(잭슨 왼쪽·맥긴/만잠비 가짜 공격수·알리송 오른쪽 폭) — WS 보유 위치와 일치. 주장 4(보유 형태 HELD #2 · 알리송 wm_winger/Attack PENDING #14 · 더블 피벗 압박 HELD #20 · 잭슨 채널 HELD #5).
  - Bains Analysis(e4hYc9wPpRo · 9:20 · 전술 분석): 캐시가 내려오는 도쿠에게 튀어나가 대인 · 카마라의 그바르디올 추적 · 골킥 압박 한쪽 가두기 · 피벗 벌린 빌드업. 주장 4(압박 트리거 PENDING #17 · 빌드업 형태 HELD #1 · 카마라 dm_holding/Defend PENDING #19(Δ.013 무결정 tie-break) · 잭슨 HELD #5).
  - NBC Sports 스튜디오(gsGnSC0JHfg): 「높게 시작 → 공을 내주고 촘촘히 하강 → 역습」 — 실측과 일치. 주장 2(HELD #59 · #1).
  - tacticafoot(A07aC4fuVDc): 에메리 대목은 §8 NBC 인용과 동일. 새것은 홀란 인터뷰 · 마레스카 플래시 「didn't deserve to lose」(질 만한 경기가 아니었다 · auto-caption) 영어 원문 확인(앞 회차 Fanpage 검색요약 미검증분). 주장 2(HELD #1 · #3).
  - More Lyes(v5XShfKHy-g): 재건 서사·맨시티 실책 위주 · 전술은 일반론. 주장 3(HELD #1 · #59 · #5).
  - LNobbins(7jer3zJlJR8 · 1:06:01 · 맨시티 팬 · **상대 관점**): 대부분 맨시티 내부 비판. 빌라 쪽은 스즈키 배급 출발점·캐시의 도쿠 봉쇄·카마라/고메스 중원 안정. 주장 2(HELD #1 · #3) — 「압박 끌어들여 통과」 서술은 롱볼 20%·점유 37%와 부분 불일치.
- 미전사(이번 회차 선별 제외): The Football Flex(aFXSkC3cwwY) · URKG(RpK7bMvg8_U) · Premier League Dad 라이브(s7go7bWC1no) · The 12th Man 팟캐스트(kSZxcE_QsFk) · The Football Brief(vafps5GtqKw) · 戦術と真実(Z8kmyUXeBJI · 일본어 · 경기 전 스즈키 프리뷰) — D+2 판단.

### ⑹ 다국어 결과 요약
- **포르투갈어**: 고메스 본인 발언 1건(somosfanaticos) · 알리송 0건. **스페인어**: 에메리 원어 0 · 가르나초 이 경기 0. **스코틀랜드**: 맥긴 0. **이탈리아어**: ANSA 사실 보도만 · Fanpage·Gazzetta 0. **영어 상대 관점**: Esteemed Kompany(맥긴 디아스 끌어내기)·GOAL 맨시티 평점(「disciplined low block」(규율 있는 로우 블록) · 「Emery's clinical counter-attacking setup」(에메리의 냉정한 역습 셋업)) · LNobbins 영상.
- 전술 블로그(TFA·BTL·Spielverlagerung·Coaches' Voice): **0건** — D+2.

### ⑺ DB 반영 (행 추가만)
- observations #1136(가르나초 사유 정정) · #1137(잭슨 역할 지시) · #1138(맥긴·만잠비 배치 서사 일치) · `match_hypotheses` C4 D1 정정 1행 · `match_videos` #384~#389 요약 · `video_impl_claims` 17행. 시즌 정본·경기 프리셋·처방 변경 없음(서사가 실측 판정을 바꾸지 않음).

### ⑻ 13:00 실제 실행 회차 델타 (2026-10-25 13:00 · 앞 블록은 07:16 커밋 52e623e에 선반영)

> 같은 예약의 정시 실행. 07:16 이후 새 자료만 훑었다. 실측 재수집 없음 · 당일 판정·대조표 변경 **0**.

- **필수 채널 4곳(yt-dlp 최신 목록 · 13:0x)**: UTV · The Villans · 1874 · Jacob Horsfall — **07:16 이후 새 업로드 0**(UTV 최신 qcGR9TddiPo · 1874 최신 라이브 1Xv_Y_4iecc 둘 다 전사 완료 · The Villans 2wNasTobcec 경기 전 · Horsfall sh16rkzsmuw 빌라 아님). 전사 추가 0.
- **알리송 ↔ 그바르디올(새 · obs#1139)**: Yardbarker(Alyssa Clang · 10-24 · 상대 관점 · 직접 fetch) 「He was tasked with neutralizing Villa's exciting Brazilian winger Alysson」(빌라의 브라질 윙어 알리송을 무력화하는 임무를 받았다) · 「Alysson was quick, but Gvardiol was quicker」(알리송은 빨랐지만 그바르디올이 더 빨랐다). **WS 대조**: 그바르디올 ȳ 76.2(1H)·78.0(2H) = 맨시티 왼쪽 → 알리송과 같은 측면 · 둘의 파울 경합 4회(13′·44′·56′ 알리송 반칙 — 빌라 x 84·90·61 높은 위치 · 24′ 알리송 피파울) · 알리송 드리블 1/2. ⇒ 「그 측면 돌파 실패」는 실측과 같은 방향, 「전담 임무」는 포지션상 자연 대면이라 지시 근거 아님. 쟁점 #14 표본 추가(단독으로 닫지 않음).
- **가르나초**: 새 1차 발언 0 — 기존 Hayters/BirminghamLive 인용의 재전재(Football365 · SportBible · LiveScore). 새 맥락 2건(모두 **LOW** · 판정 반영 없음): GOAL US 「Villa executed an identical manoeuvre with … Harvey Elliott last season」(지난 시즌 엘리엇에게도 같은 조치를 했다) — Football Insider 루머 재가공 · footballtransfers 「last ditch attempt … after Unai Emery showdown talks」(에메리와 담판 뒤 마지막 시도 · 제목만 · 원문 미확인).
- **맥긴**: RotoWire 「three crosses (zero accurate) and two corners」(크로스 3회(정확 0)·코너킥 2회) — 도움·기회 창출 4는 기존 실측과 같음. 스코틀랜드 매체 새 기사 0.
- **고메스**: 포르투갈어 새 기사 0(somosfanaticos 본인 발언은 07:16 반영분과 같은 것).
- **Tanswell**: 검색 색인상 경기 후 기사·트윗 **0**(색인된 최신은 경기 전 만잠비 출전 판단·「I am not celebrating」(축하하지 않는다) 회견 트윗) — D+2 headful X 재시도 유지.
- **0건 검색어 기록**: 스페인어 「Garnacho afuera de la convocatoria Aston Villa Emery City」·「Garnacho … Olé OR TyC OR Clarín」 · 포르투갈어 「Alysson Aston Villa Manchester City atuação」·「Alysson Gvardiol … brasileiro ponta」·「"João Gomes" Aston Villa City vitória volante」 · 스코틀랜드 「McGinn … Herald OR Scotsman OR "Scottish Sun"」 · 영어 「… player ratings Birmingham Live Townley」(검색 미노출) · 「Jacob Tanswell … October 2026」. 에메리 스페인어 원어 **여전히 0**.
- **DB(행 추가만)**: observations #1139 1행. 가설·대조표 정정 행 없음(새 근거로 닫히는 항목 없음). 시즌 정본·프리셋·처방 변경 없음.

## D+1 저녁 보강 (2026-10-25 20:50)

> 예약 `mw-avl-mancity-d1-evening` · 사용자 요청 추가 회차 · **13:00 회차 이후** 새 자료만. 실측(§2·§3) 재수집 없음. 기사 다국어 스윕은 서브에이전트(WebSearch/WebFetch · 읽기 전용), Tanswell X·UTV 자막은 메인이 브라우저로 직접(자막은 뮤트·정지 → 탭 닫기).

### ⑴ 당일 판정 정정
- **6′ 선제골 기전(obs#1140)**: §3 강점 ⑴ 「첫 6분 높은 출발로 맨시티 빌드업 실책 유도」 → **부분 일치로 정정**. dave.sport(James Chettle · 10-25 07:00 · Opta 2차 인용) 「Guéhi was not under pressure when he lost the ball」(게히는 공을 잃을 때 압박받지 않았다). WS 대조: 5′32″~47″ 맨시티 자기 진영 6패스 연속 동안 빌라 수비 이벤트 **0** → 5′47″ **엔소 페르난데스** 칩 롱패스 → 5′49″ 게히 첫 터치 실패(경합 이벤트 없음) → 맥긴 회수(게히에서 약 6m). 높은 위치(0–6′ def_x 55.6)는 맞지만 실책 순간 직접 압박은 없었다 — 빌라 기여는 **근접 위치 선점**이다. 원래 문구는 보존한다.
- **표기 정정**: §1 득점 줄의 「디아스→게히 긴 패스」는 WS상 **엔소 페르난데스**의 패스다(obs#1140).
- 이월 대조표 C1~C6·`match_hypotheses`: 변경 **0**(새 근거로 닫히는 가설 없음 · C4 가르나초는 아래 ⑹).

### ⑵ 감독 발언 새것
- **Tanswell X 직접 열람 성공**(13:00 회차는 402 — 이번엔 브라우저로 열림 · obs#1141). 회견에서 Tanswell이 직접 물은 잭슨 답 **전문**: 「But we need him more running in behind because we need the runners on the field, and one of the runners normally is the striker, and he has quality and power.」(필드에 러너가 필요하고 그 러너 중 하나는 보통 스트라이커라서 뒷공간으로 더 뛰길 원한다. 그는 질과 힘이 있다) · 「His speed is fantastic, and as well his capacity to get duels man to man. He's coachable.」(속도가 환상적이고 1대1 경합 능력도 있다. 지도를 잘 받아들인다). 13:00 회차의 Hayters 요약보다 「러너 = 보통 스트라이커」라는 이유가 붙었다 → 쟁점 #4(어드밴스드 vs 폴스9)에 배후 러너 쪽 감독 진술. 실측은 하강·경합도 함께 보여 단독으로 닫지 않는다.
- 같은 계정: 「This year we started so poor, we needed time to understand how we needed to improve or how to work in our structure.」(올해 출발이 너무 나빴고 어떻게 개선하고 우리 구조로 일할지 이해할 시간이 필요했다) · 스즈키 「We are very, very impressed with how he adapted so quick with us.」(그가 그렇게 빨리 적응한 데 매우 감명받았다).
- Telegraph(John Percy · Yahoo 전재 · 13:00 전 발행 · 미수집분): 잭슨에게 「How he was working, defending, getting duels… wow!」(일하고 수비하고 경합을 이기는 걸 보면… 와!).
- dave.sport(BBC MOTD·AOL 경유 2차): 「We needed the defence, keeper, sacrificing defensively a lot of the time.」(수비진과 골키퍼가 필요했고 많은 시간을 수비적으로 희생했다) — BBC 원문 미확인.
- **맨시티 쪽(상대 관점 · obs#1142)**: 디아스(mancity.com · Yahoo 전재) 「They changed the way they set up so we took time to adapt.」(그들이 셋업을 바꿔 적응에 시간이 걸렸다) · 「they ended up scoring two goals in two transitions - very efficient.」(전환 두 번에 두 골 — 매우 효율적) — 마레스카 「expected them in one way」(한 방식으로 예상했다)와 **독립 진술 2건째**(바이킹전 보유 3백 → 이 경기 4백 전환과 맞물림 · 구체 서술은 없음). 마레스카 「If you mention to come here and don't concede one or two transitions it's almost not the reality.」(여기 와서 전환 한두 번 안 내주는 건 거의 비현실적이다).
- **회견 전문**: avfc.co.uk 본문 잘림 · mancity.com 403 → **미확보**(VillaTV 영상만). **에메리 스페인어 원어 여전히 0** — zamin.uz 스페인어판은 출처 없는 영어판 번역 복제라 채택하지 않음(LOW).

### ⑶ Jacob Tanswell
- 경기 후 트윗 3건 전문 확보(위 ⑵). ⭐ **The Athletic 「Unai Emery, the Premier League's best coach」**(Tanswell · 2026-10-25 16:55 KST 공유 · 무료 링크) — **본문 미열람**: nytimes.com이 브라우저(안전 제한)·WebFetch 모두 차단. 제목만 기록 → D+2에서 다른 경로(전재·요약) 시도.

### ⑷ 기사·평점 (새것 · 상대 관점 포함)
| 서술 | 출처 | 실측 | 판정 |
|---|---|---|---|
| 「make his wingers drop back and form, sometimes, a line of six players」(윙어를 내려 때때로 6명 라인) | CityXtra(Enzo Krieger · 10-25 09:09 · 맨시티 관점) | 수비 액션 평균 알리송 (37.7, 27.2) 깊은 것 2/9 · 만잠비 (26.5, 60.0) 깊지만 **안쪽** · 측면 깊은 수비는 캐시·마트센·부엔디아·음바예 | **대체로 기각** — 선발 윙어 6백 아님(교체 뒤 음바예·부엔디아 구간만 가능 · 쟁점 #16 표본) |
| 「double man-marking on both flanks」(양 측면 이중 대인마크) | CityXtra | 오른쪽 캐시+카마라(ȳ 37.5) · Telegraph 「Doku sprints down the left but can't get past Kamara」(도쿠가 카마라를 넘지 못한다) / 왼쪽 마트센 태클 0/3 | 오른쪽만 일치 |
| 「pressed quickly in a man-to-man system」(맨투맨으로 빠르게 압박) | Squawka(Harry Edwards · 10-24 · 403 → 검색 요약 경유) | def_x 34.9 · 높은 압박은 0–6′뿐 | 부분 — 초반만 |
| 「Villa keep the pressure up for the opening minutes」(초반 몇 분 압박 유지) | Telegraph 라이브(Percy) | 0–6′ def_x 55.6 | 일치 |
| 만잠비 「on the left rather than as the No 10」(10번이 아니라 왼쪽) · 맥긴 「more centrally」(더 중앙) | Express & Star Verdict(George Bennett · 10-25 09:01 · 403 → 검색 요약 경유) | 만잠비 (58, 67) · 맥긴 (61, 47) | 일치(obs#1138 재확인) |
| 「release a runner, support him and arrive in the box」(침투자를 내보내고 지원하고 박스에 도착) | dave.sport | 역습 2골(잭슨) | 일반론 — 채택 안 함 |
| 고메스 82′ 교체 「might have taken that knock」(충돌로 다쳤을 수 있다) | Telegraph 라이브 | — | 추정 — 채택 안 함 |
- 평점: thefalse9(Arjun Rao) 잭슨 9 · 맥긴 8 · 카마라 7 · 고메스 6 · 알리송 6 · 만잠비 5 — 「31 tackles to City's 13」(태클 31 대 13)은 SS와 같음. Read Man City(10-25 09:42)는 마레스카 MOTD 「We adjusted then controlled the game.」(조정한 뒤 통제했다) 외 재전재.
- **0건**: Birmingham Mail/Live(Preece·Townley) 원문 · Express & Star Matt Maher 경기 Verdict · The Athletic(Sam Lee)·MEN 경기 기사.

### ⑸ 영상 (필수 채널 4곳 · 뮤트 경로)
- **최신 목록(20:5x)**: **UTV — 새 업로드 1편** 「WHY NICOLAS JACKSON SCARES EVERY DEFENCE!」(Id10w3mpHVI · 2026-10-25 17:00 KST · 36:36 · 전술 디브리프) → yt-dlp 봇 차단(「The page needs to be reloaded」) → 브라우저 pot 경로(mute·정지 확인 → 자막 포착 → 탭 닫기)로 **전사** → `match_videos` **#390**(r63 귀속) 요약 + 구현 주장 **7행**. **The Villans · 1874 · Jacob Horsfall — 13:00 이후 새 업로드 0**(최신 각각 2wNasTobcec 경기 전 · 1Xv_Y_4iecc 전사 완료 · sh16rkzsmuw 빌라 아님).
- #390 요지(auto-caption · obs#1143): ① **51′ 실점** 서술이 WS 이벤트 순서와 정확히 일치 — 잭슨 패스 차단 → 은디아예가 카마라 상대 파울 획득 → 빠른 FK → 은디아예 크로스 (93, 22) → 홀란 헤더(린델뢰프 패). ② **왼쪽 약점** 「we didn't really have that extra player at times that was really helping out with Ian Matson」(마트센을 돕는 추가 인원이 때때로 없었다) — WS 은디아예 터치 ȳ 16(빌라 왼쪽) · 빌라 왼쪽 수비 진영 태클 마트센 0/3·만잠비 1/3·부엔디아 0/3 → 같은 방향(쟁점 #47·#53). ③ 중원 박스(카마라·고메스·만잠비·맥긴 + 잭슨 하강 · #21). ④ 교체 역할(음바예 폭·캐시 지원 #48 · 부엔디아 마트센 보호 · 바클리·고레츠카 중원 · 마조 채널 홀드업). ⑤ 잭슨 홀드업 후 왼쪽 빈 공간으로 전개(#5). ⑥ 압박 「We know when to jump … We hunt in packs」(언제 튀어나갈지 안다 … 무리 지어 사냥한다 · #17 PENDING). ⑦ xG stat 수비 라인 ~30m 대 41m(#59).
- 13:00 회차 미전사 6편(The Football Flex · URKG · Premier League Dad · The 12th Man · The Football Brief · 戦術と真実): 이번 회차도 미전사 — D+2 판단 유지.

### ⑹ 중점 4인
- **알리송**(포르투갈어): 새 기사 **0**. 영어 Telegraph 「Gvardiol buys a foul from a naive Alysson on the left wing」(그바르디올이 순진한 알리송에게서 파울을 얻어냈다 — 맨시티 기준 왼쪽) — obs#1139 그바르디올 대면과 같은 방향.
- **주앙 고메스**(포르투갈어): 새 기사 **0**(ge·Lance·UOL 평점 미노출). 82′ 교체 「knock」(충돌)은 Telegraph 추정 — 채택 안 함.
- **맥긴**(스코틀랜드): 스코틀랜드 매체 **0**. Telegraph 「McGinn slides in Jackson on the inside left」(맥긴이 왼쪽 안쪽으로 잭슨에게 찔러준다) · UTV 「McIn four key passes」(키패스 4 — SS 4와 같음).
- **가르나초**(스페인어): 새 1차 근거 **0**. UTV 진행자 해석 「there's other players that are ahead of him」(그보다 앞선 선수들이 있다 — 교체 역할 서열)은 **등급 D 추론**으로 C4 판정 불변(판정 불가 유지).

### ⑺ 0건 검색어 (이번 회차 새로 시도 — 13:00 회차와 중복 없음)
- 스페인어·바스크어: 「Emery Aston Villa Manchester City Diario Vasco OR "Noticias de Gipuzkoa" OR "El Correo" OR "Mundo Deportivo"」 · 「Unai Emery entrevista Movistar Plus OR "El Larguero" OR "Onda Cero"」 · 「Emery Aston Villak Manchester City Jackson Berria … Hondarribia」 · 「Garnacho … no fue convocado … motivo Emery Olé TyC Marca」 · 「site:ole.com.ar Garnacho Aston Villa Manchester City」.
- 포르투갈어: 「Alysson Aston Villa ex-Grêmio … ponta」 · 「Alysson … Gvardiol … GZH OR "Correio do Povo" OR UOL」 · 「João Gomes … ex-Flamengo atuação Emery volante 25 outubro」 · 「"João Gomes" … nota ge globo OR Lance OR UOL」.
- 스코틀랜드: 「John McGinn … Steve Clarke Daily Record」 · 「McGinn … Scotland skipper Herald Scotsman October 25 2026」.
- 독일어: 「Aston Villa Manchester City Analyse Emery Maresca Konter Jackson Taktik」.
- 영어: 회견 전문 transcript · MEN Maresca verdict · Sam Lee · Matt Maher Verdict · BirminghamLive ratings · TFA/BTL/Coaches' Voice · 「five things/talking points」 — 상세는 서브에이전트 보고 기준 12종.
- 전술 블로그(TFA·BTL·Spielverlagerung·Coaches' Voice): **0** — D+2 유지.

### ⑻ DB 반영 (행 추가만)
- observations **#1140**(6′ 골 기전 정정) · **#1141**(Tanswell 잭슨 전문·회견 트윗) · **#1142**(맨시티 관점 셋업 변화·6백/이중마크 대조) · **#1143**(UTV #390 실점·왼쪽 약점) · `match_videos` #390 신규(색인) + 요약 · `video_impl_claims` 7행(HELD 6 · PENDING 1 — 전부 기존 쟁점 #47·#53·#21·#48·#5·#17·#59에 묶음). `match_hypotheses` 정정 행 없음 · 시즌 정본·경기 프리셋·처방 변경 없음(서사가 실측 판정을 바꾸지 않음).
- 마무리: `refresh_duty_applied.py` 신규 CONFLICT 0 · `claim_issues.py --due` 판정할 차례 15(AVL #7 음바예 역할 · #14 알리송 측면 기용 · #30 설정 축 없는 성향 + 보류 팀 12) — 이번 회차 새 근거로 닫히는 것이 없어 미판정(G39 7일 이내 · 게이트 통과). #14는 이 회차 obs#1139·#1142 표본 추가.

## D+2 추적 (2026-10-26)

> 예약 `mw-avl-mancity-d2` · 이 PC · D+1 저녁 회차(10-25 20:50) 이후 새 자료만. 실측(§2·§3) 재수집 없음 — 영상 주장 대조만 WS 원본 JSON에서 새로 셌다. 기사 다국어 스윕은 서브에이전트(WebSearch/WebFetch · 읽기 전용), 영상은 메인이 직접(yt-dlp 목록 → 자막은 브라우저 pot 경로 · **전부 뮤트·즉시 정지 → 탭 닫기**). 관전 메모(`notes/2026-10-24-avl-mancity*`) **없음**.

### ⑴ 당일 판정 정정
- **0건.** 새 자료가 뒤집은 당일 판정은 없다. 대신 아래 ⑷의 근거가 **C5 「4백 + 왼쪽 쏠림」**을 GK 배급 단계까지 재확인했다(obs#1144).
- 영상 쪽 오류는 출처 쪽 기각으로 기록했다(obs#1145) — 우리 판정 정정이 아니다.

### ⑵ 감독 발언 새것
- **에메리(2차 · Tanswell 전언)**: 1874 먼데이 리뷰에서 Tanswell이 경기 다음 날 에메리와 나눈 대화를 전했다. 「in certain games we wanted to come to feet, but in these type of games, all I wanted to do is just continue running behind, continue stretching the legs of Guéhi, Khusanov」(어떤 경기에서는 발밑으로 받길 원했지만, 이런 경기에서는 계속 뒷공간으로 뛰어 게히·쿠사노프의 다리를 늘리는 것만 원했다 · auto-caption). D+1 회견 트윗(obs#1141)과 같은 축이고, 「강팀전 한정」이라는 조건이 붙었다. → 쟁점 #4 PENDING 주장 1행.
- **마레스카(새 대목)**: 「Today we needed a technical midfielder, that's why Rayan was out and Phil was inside」(오늘은 기술적인 미드필더가 필요해서 라얀을 빼고 필을 안쪽에 넣었다 · GOAL Yosua Arya). HT 셰르키→포든 교체 사유다. 「Today Enzo and Elliot both had a very good game」(오늘 엔소와 엘리엇 둘 다 아주 좋은 경기를 했다 · PA/ESPN 10-25)라고도 했다 — 맨시티 팬 분석 LNobbins는 반대로 엔소 위치 오류를 실점 원인으로 지목한다(obs#1146).
- **회견 전문**: avfc.co.uk는 본문이 잘리고 mancity.com은 403 → **여전히 미확보**(D+1과 같음).
  - 에메리 스페인어 원어 **0건**. zamin.uz 스페인어판 「Tuvimos que sacrificar mucho para defender」(수비하려고 많은 걸 희생해야 했다)는 영어 MOTD 발언의 재번역으로 판단해 채택하지 않았다.
  - 마레스카 이탈리아어 calciomercato 「Oggi non meritavamo di perdere」(오늘 우리는 질 자격이 없었다)는 「Tradotto da」 표기의 **번역 복제**라 교차검증이 아니다.
- 에메리의 알리송·고메스·맥긴·밍스·음바예·만잠비 개별 평가: **0건**(3회차 연속).

### ⑶ Jacob Tanswell
- ⭐ **1874 「Jacob Tanswell on Unai Emery's Future & Villa's BRILLIANT Win Over Man City!」**(V4eYrxC3rws · 2026-10-26 · 41:56 · `match_videos` #392)를 전사·요약했다. 전술 대목은 앞 25분이다.
  - **선발 의도**: 「Villa picked a team that wasn't there to control a game」(빌라는 경기를 통제하려고 짠 선발이 아니었다). 알리송 선발은 「they wanted pace. They wanted one v one ability」(속도와 1대1 능력을 원했다)는 신호로 읽었다.
  - **맨시티 CB 좌우 교체**: 빠른 게히를 잭슨의 왼쪽 채널에 세웠다는 서술. → WS 일치(아래 ⑷).
  - **알리송 오프 더 볼**: 「it was actually a lot of mental pressure on him to remember what he's supposed to do」(해야 할 일을 기억하느라 정신적 부담이 컸다) · 「Lindelof was talking him through it」(린델뢰프가 말로 이끌었다) · 스프린트 반복이 늘었다.
  - **카마라**: 「he protects that back four excellently」(백4를 훌륭히 보호한다) · 「he can cover across」(좌우로 커버한다).
  - **캐시**: 도쿠 성향을 사전 분석했다(Alberto Carbo 분석 코치 언급).
- **Athletic 「Unai Emery, the Premier League's best coach」 본문**: 여전히 미열람. 전재·요약도 0건이다(서브에이전트 검색어 4종).
  - 영상에서 본인이 요지를 말했다: 「Emery is the best coach in the Premier League by a long way」(에메리가 PL 최고 감독이다, 큰 차이로). 근거는 경력(유로파 5회·18시즌 연속 유럽 진출)과 클럽 장악력이다 — 전술 서술은 없다.
- **비전술(기록만)**: 맨유의 에메리 관심설에 Tanswell은 「if there's news, I'll report on it」(뉴스가 있으면 보도하겠다)로 답을 피했다. 진행자 Bardell은 「he would never leave Villa mid-season」(시즌 중엔 절대 떠나지 않을 것)이라고 했다(의견 · 사실 근거 없음 명시). 계약은 2029년까지다. 10-28 본머스 컵전은 비조 선발 가능성 언급.

### ⑷ 영상·기사 주장 ↔ 실측 대조 (WS 1983617 원본)
| 서술 | 출처 | 실측 | 판정 |
|---|---|---|---|
| 맨시티가 CB 좌우를 바꿔 빠른 게히를 잭슨이 노는 빌라 왼쪽 채널에 세웠다 | Tanswell(1874 #392) · LNobbins(#394 · 맨시티 관점) | 1H 디아스 터치 ȳ **67.2**(맨시티 왼쪽) · 게히 ȳ **28.0**(오른쪽 · HT 교체) · 잭슨 볼 소유 왼쪽 48% | **일치** |
| 피벗 분할로 대인 중원을 끌어낸 뒤 내려온 맥긴에게 토레스가 세로 패스를 넣었고, 디아스가 따라 나와 파울했다 | LNobbins(#394) | 토레스→맥긴 연결 **4**(1′·23′·38′·41′ — 전부 전반) · 디아스의 맥긴 상대 파울 **2**(38′·41′) · 토레스 최다 연결은 스즈키 20 | **같은 방향 · 「매번」은 과장** |
| 스즈키가 왼쪽 깊숙이 잭슨을 겨냥해 롱볼을 찼다(내려온 왼쪽 2선을 상대 RB가 따라 나간 뒤 그 뒷공간) | TOTAL FOOTBALL(#393 · 일본어) | 스즈키 롱패스 19 중 왼쪽 레인(y>66) **14** · 성공 6 | **일치** — C5 왼쪽 쏠림을 GK 배급까지 재확인 |
| 첫 6분 점유 92% | Tanswell(#392) | 0–6′ 패스 47 대 13(**78%**) · 터치 54 대 25 | **과장**(방향만) |
| 「4-4-2 mid block」(4-4-2 미드블록) | LNobbins · AVillaFan(Wardhana Arya · 10-24) | 맥긴 수비 액션 (34, 38) · 카마라 (33, 34) 바로 옆 | 당일 4-4-1-1 **유지** — 쟁점 #15 누적 |
| 잭슨을 약간 왼쪽 중앙에 세워 상대 오른쪽 CB를 공략하게 했다 | talkSPORT(#396) | 위 게히 ȳ 28 · 잭슨 왼쪽 48% | **일치** |
| 동점골은 도쿠가 마트센을 제친 크로스, 결승골은 마트센 크로스에 잭슨 발리 | FußballFokus(#397) | 은디아예 FK 크로스(obs#1143) · 음바예 컷백 | **기각**(장면 오류) |
| 빌라 전반 태클이 두 시즌 PL 전반 최다 | FußballFokus(#397) | WS 전반 태클 빌라 13 · 맨시티 4 | 미검증(기록 대조 불가) |
| 6′ 골은 「one sharp press」(날카로운 압박 한 번) | TheFootballPlus(#398) | obs#1140 실책 순간 직접 압박 없음 | **기각** — 93:20 Cityzens(#395 · 맨시티 관점) 「no one pressing him」(아무도 압박하지 않았다)은 obs#1140과 같은 방향 |
| 맨시티 전반 빌라 박스 터치 29 = 이번 시즌 PL 전반 최다 | Opta Analyst(Harry Carr · 10-24) | 박스 터치 12 대 53(경기 전체) | 같은 방향(저블록) |

### ⑸ 영상 (필수 채널 4곳 + 검색 스윕 · 전부 뮤트 pot 경로)
- **필수 채널 최신 목록(yt-dlp · 20:0x)**
  - **1874 — 새 업로드 2편.** Tanswell 먼데이 리뷰(V4eYrxC3rws)는 **전사**했다. 「Watching the VILLANS Beat the VILLAINS | Matchday Experience」(xa7y91-yvFw · 직관 브이로그)는 건너뛰었다.
  - **UTV — 새것 0**(최신 Id10w3mpHVI는 D+1 저녁 회차에 요약 완료).
  - **The Villans — 새것 0**(최신 2wNasTobcec는 경기 전 예측).
  - **Jacob Horsfall — 새것 0**(최신 sh16rkzsmuw는 빌라 아님).
- **검색 스윕**(YouTube 결과 · 필터 「이번 주 업로드」 · 영·스페인어·포르투갈어·일본어 검색어 10종): DB에 없던 전술·분석 영상 **6편을 전사**했다.
  - **#393 TOTAL FOOTBALL**(0ZwcYQbYneg · 일본어): 스즈키 해설 — 선방 연동·왼쪽 롱볼·골킥 압박 회피.
  - **#394 LNobbins** 「Why City's Midfield Gamble Failed at Villa」(IkO2-skXk_8 · 맨시티 관점 전술 분석).
  - **#395 93:20 Cityzens**(NRx8B7L5x4A · 맨시티 관점).
  - **#396 talkSPORT**(OcRF3mY7VHI).
  - **#397 FußballFokus**(sK9YbFmOADo · 영어 내레이션).
  - **#398 TheFootballPlus**(w7oZ5SIVLdE).
- **#392 포함 7편 전 편**에 요약과 구현 주장 **13행**을 넣었다(HELD 10 · PENDING 2 · none 1 · 전부 auto-caption).
  - 쟁점별 묶음: #1×3 · #3 · #4 · #5×2 · #13 · #14 · #15 · #19 · #49.
- **건너뜀(사유)**
  - D+1 미전사 6편:
    - The Football Flex·URKG·The 12th Man — 일반 반응/팟캐스트.
    - Premier League Dad — 2시간대 라이브.
    - The Football Brief(bcX6qeWblGE) — 맨시티 반응 일반론.
    - 戦術と真実(Z8kmyUXeBJI) — 경기 전 프리뷰.
  - 검색 신규 중:
    - 축구조사실(Qw8YPqupG5o)·PastXI(zkJ02_V39x4)·Second Look FC(9IJOLYL6y6c) — 자동 생성 내레이션 의심. Second Look의 「56 touches in the box」(박스 터치 56)는 SS 53과 불일치.
    - 팬 반응·하이라이트 모음 다수 — 핵심 없음.
    - 일본 2ch 반응 모음 4편 — 반응 모음.

### ⑹ 다국어 결과
- **스페인어**: 에메리 원어 **0**. EFE 계열(Libertad Digital·Diez·La Prensa)은 사실 보도다. Mundiario(Yoknell León · 10-24) 「presionó desde los primeros pases … redujo los espacios interiores」(첫 패스부터 압박했고 안쪽 공간을 줄였다)는 기자 해석이다. 가르나초(Olé·TyC·Clarín) **0**. 스페인어 전술 분석(Ecos del Balón 등) **0**.
- **포르투갈어**: 고메스 GE 인용 「Todos sabem que jogo de volante, mas também estou à disposição para jogar de lateral, como foi no meio da semana contra o Viking」(다들 내가 볼란치인 걸 알지만 주중 바이킹전처럼 풀백으로 뛸 준비도 돼 있다 · Somos Fanáticos 경유 · ge 원문 미발견)는 D+1에 반영한 본인 발언 기사와 같은 출처다. **바이킹전 RB = 강제 1회성(C1)과 모순 없음.** 알리송 브라질 매체 평가는 **0**(바이킹전 MOM 기사만 있음).
- **스코틀랜드(맥긴)**: Daily Record·Herald·Scotsman·Scottish Sun **0**.
- **이탈리아어(마레스카)**: calciomercato는 번역 복제다. Gazzetta·Corriere dello Sport·Fanpage 원 기사 **0**.
- **일본어**: TOTAL FOOTBALL 1편을 전사했다(위). 반응 모음 채널은 제외했다.
- **프랑스어**: 경기 후 분석 **0**. **독일어**: FußballFokus(영어 내레이션)를 전사했고 독일어 기사 검색은 미수행이다(예산 우선순위).

### ⑺ 중점 4인
- **알리송**(포르투갈어): 브라질 새 기사 **0**. 영어로 새것 3건이다.
  - Tanswell: 선발 = 속도 신호 · 오프 더 볼 학습 중 · 린델뢰프가 말로 지도.
  - Independent(Jolly): 「dynamism and direct dribbling」(역동성과 직선 드리블).
  - The National 7/10: 「making important challenges tracking back」(수비 복귀 중 중요한 태클).
  - → 쟁점 #14(10-27 이후 선발 3경기) 주장 1행(HELD). 「수비 복귀형」 쪽 서술이 늘었지만 트리거 전이라 판정하지 않는다.
- **주앙 고메스**(포르투갈어): 새 1차 근거 **0** — 위 GE 인용은 재확인이다. Independent 「terrier-like」(테리어 같은) 중원 일원 · LNobbins 「피벗 분할로 앤더슨을 끌어냈다」(쟁점 #1 · #20 축).
- **맥긴**(스코틀랜드): 스코틀랜드 매체 **0**. LNobbins가 토레스 세로 패스의 수신자로 디아스를 끌어냈다고 썼다(WS 4회 · 파울 유도 2). 당일 「연결보다 압박·탈취」 판정은 그대로 두고, 「전반 라인 사이 수신」을 표본으로 추가한다.
- **가르나초**(스페인어): 새 1차 근거 **0**. C4 **판정 불가 유지**. 다음 확인은 D+3 본머스 컵전(10-28) 명단이다.

### ⑻ 이월 대조표·가설 재판정
| # | 당일 판정 | D+2 새 근거 | 재판정 |
|---|---|---|---|
| C1 고메스 RB 재기용 | 불일치(LDM) | 고메스 GE 인용 「볼란치지만 풀백도 가능」 — 바이킹전 RB를 예외로 언급 | **유지** |
| C2 만잠비 복귀 | 일치(왼쪽 안쪽) | Tanswell 「allowed to drift where he wants」(원하는 곳으로 흘러갈 수 있다) · WS 왼쪽 71% | **유지** |
| C3 마트센 복귀 | 일치(높은 LB) | 4th Official 리커버리 5·라인 브레이킹 4 · 뒷공간 보호 과제(obs#1143과 같은 축) | **유지** |
| C4 가르나초 서열 | 판정 불가 | 0 | **유지** — D+3 본머스 명단 |
| C5 4백 + 왼쪽 쏠림 | 불일치(변화) | 스즈키 롱패스 왼쪽 14/19 · 맨시티 CB 교체가 그 채널을 겨냥 | **유지 · 근거 강화**(obs#1144) |
| C6 맥긴·고메스 중원 축 | 불일치(이 경기 한정) | 토레스→맥긴 세로 4(맥긴–고메스 연결 아님) | **유지** |

### ⑼ 0건 검색어 (이번 회차 새로 시도 — 앞 회차와 중복 없음)
- **영어**:
  - `Tanswell "Unai Emery" Premier League's best coach Athletic`
  - `nytimes.com/athletic Unai Emery Aston Villa best coach Premier League`
  - `Unai Emery Premier League best manager Villa rebuild … October 26 2026`
  - `totalfootballanalysis Aston Villa Manchester City 2026`
  - `Bitter and Blue … Maresca tactics talking points`
  - `manchestereveningnews Man City Aston Villa Maresca verdict tactics`
  - `Sam Lee Maresca Villa City "Athletic"`
  - `"Aston Villa" "Man City" tactics Emery man-marking wings "double" Doku`
- **스페인어**:
  - `Unai Emery "Manchester City" Villa Park "hemos" OR "tuvimos" Marca OR AS OR Relevo`
  - `Unai Emery City Villa Park "cuatro años" Noticias de Gipuzkoa OR Diario Vasco OR Mundo Deportivo`
  - `Emery tumba al City … AS Marca Relevo crónica`
  - `"Emery" "City" Villa táctica análisis "bloque"`
  - `Garnacho Aston Villa Manchester City convocatoria ausencia motivo`
- **포르투갈어**:
  - `Alysson Edward Manchester City Gvardiol Aston Villa vitória brasileiro destaque`
  - `ge.globo João Gomes lateral Aston Villa Manchester City`
  - `Aston Villa x Manchester City João Gomes Alysson nota atuação ge globo`
- **스코틀랜드**: `McGinn Villa City captain Guehi press win Scotland Daily Record Clarke`
- **이탈리아어**: `Maresca "Aston Villa" "non meritavamo" OR "meritavamo di più"`
- **프랑스어**: `Emery Villa Manchester City analyse tactique bloc contre-attaque Jackson octobre 2026`
- **YouTube**(이번 주 필터):
  - `aston villa manchester city analisis tactico`
  - `aston villa manchester city alysson`
  - `joao gomes aston villa`
  - `garnacho aston villa`
  - → 스페인어·포르투갈어 **원어 분석 영상 0**(나온 것은 자동 번역 제목의 영어 영상).
- **전술 블로그**(TFA·BTL·Spielverlagerung·Coaches' Voice·Tifo·Statsbomb·Breaking the Lines): **0** — D+3 마지막 확인.

### ⑽ DB 반영 (행 추가만)
- **observations**:
  - **#1144** — 빌드업 경로 3원 수렴·C5 근거 강화.
  - **#1145** — 영상 주장 중 실측 불일치·기각.
  - **#1146** — 마레스카 새 대목·Opta·Independent·4th Official.
- **match_videos**: **#392~#398** 신규 7편(r63 귀속) — 요약 + `video_impl_claims` **13행**.
- 변경 없음: `match_hypotheses` 정정 행 · 시즌 정본 · 경기 프리셋 · 처방.
- 마무리 결과(`refresh_duty_applied.py` · `claim_issues.py --due`)는 아래 ⑾.

### ⑾ 마무리
- `refresh_duty_applied.py`: 신규 CONFLICT **0** · 억제 4건(기존).
- `claim_issues.py --due`: 열린 쟁점 72 · 판정할 차례 **12 — 전부 보류 팀(ATM·CHE·LIV)** · **AVL 0**. 이번 회차 주장은 모두 트리거 전 쟁점에 묶었다(#14 알리송은 트리거 10-27 이후 선발 3경기).
- `match_reports.status`는 **draft 유지** — D+3(10-27 20:00 · 본머스 컵전 명단 전날)에 complete 판정.

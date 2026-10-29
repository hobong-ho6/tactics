# 2026-10-28 AVL vs Bournemouth — 0-3 (원정 · 본머스 3-0 빌라)

> 수집일 2026-10-29(예약 `mw-avl-bournemouth-collect` 09:30 회차) · SofaScore event `17118370` · FotMob `6275374` · WhoScored `2035006` · **EFL컵(카라바오컵) 4라운드** · 원정(바이탈리티 스타디움) · 주심 Tony Harrington · 빌라 4-2-3-1 vs 본머스 4-1-4-1 · 본머스 감독 **Marco Rose** · 게임 버전 `core.game_version.live_on('2026-10-28')` = **FC27**
> DB: `matches` #128 · `match_reports` #64(draft) · 사용자 관전 메모 [notes/2026-10-28-avl-bournemouth-user-live.md](notes/2026-10-28-avl-bournemouth-user-live.md)(메모 1·2)

## 요약

- **0-3 탈락, 내용은 결과보다 덜 일방적이었다.** xG **1.65 대 2.71**(FotMob · 오픈플레이 1.29/1.64 · 세트 0.37/1.07 · PK 0), 슈팅 17–19, 유효 5–7, 점유 **51%**(전반 44 · 후반 54), 빅찬스 **4 전부 실패**(xGOT 0.99). 실점 3 중 2가 **빌라 에러에서**(SS `errorsLeadToGoal` 2 — 51′ 코너 직후 비조 · 69′ 보가르드 자기 진영 오른쪽), 1이 **빌라 오른쪽 배후 공략**(7′ 타버니어 칩 패스 → 솔레르 → 아들리)이었다.
- **로테이션 11명 중 9명 교체**(맨시티전 선발에서 고메스·마트센만 잔류). 에메리 본인 사유: 「it was a way to add some players our understanding, our idea, getting fit」(몇몇 선수에게 우리의 이해와 아이디어를 입히고 몸을 끌어올리는 길이었다 · E&S/PA).
- **형태는 맨시티전과 같은 4-2-3-1 — 보유 시 양 풀백 폭, 비보유 4-4-1-1.** 볼 소유 평균(WS): 하우드-벨리스 (33,36) · 밍스 (29,71) CB 2, 보가르드 (41,16) · 마트센 (45,85) 폭, 그 앞 **고메스 (52,45) · 고레츠카 (47,64)** 더블 피벗(고메스가 오른쪽·더 높게), 부엔디아 (64,39) 10번, 음바예 (62,16) 오른쪽 폭, 헤밍스 (60,79) 왼쪽 폭, 마조 (60,66). 빌드업은 **밍스 축 왼쪽**(밍스→마트센 24 · 비조→밍스 23 · 밍스↔하우드-벨리스 21/15).
- **압박은 빌라가 졌다.** PPDA 빌라 **14.25**(전반 9.75 · 후반 **21.0**) vs 본머스 **9.89** · def_x 35.0 vs 46.4. 에메리 「trying to break the high press, especially the first 10 minutes in each half. But we couldn't.」(각 하프 첫 10분 하이프레스를 깨려 했지만 못 했다 · Tanswell X).
- **사용자 관전 메모 판정**: 음바예는 **볼을 잡을 때 91%가 오른쪽 폭**(H1 「자주 중앙」은 볼 소유 기준 불일치 · 오프더볼 런은 이벤트로 측정 불가) · 본머스 볼 소유는 오히려 **빌라 왼쪽**에 쏠렸지만(전반 50%) **실점 2/3은 빌라 오른쪽에서 마무리**(H2 부분 일치) · 첫 실점 = 반대 전환 → 빌라 오른쪽(**H4 일치** · 단 전환 공백이 아니라 30초 정돈 공격) · 「공격→수비 전환 순간 오른쪽 공백」(H2′)은 이벤트 대조 **불일치**.
- **중점 5인**: 고레츠카 이적 후 첫 선발 = **더블 피벗(LDM)**(#25 표본 · 10번 아님 · FM 7.18 팀 1위) · 마조는 ST 칸이지만 **평균 위치 왼쪽 · 공중 경합 0 · 볼 터치 16**(#80 홀드업/침투 어느 쪽도 약한 표본) · 하우드-벨리스 RCB 90′ 지상 경합 5/5 · 패스 60/67 · 헤더 빅찬스 실패 · 음바예 폭 유지형 RM(#7·#48 표본) · 헤밍스 왼쪽 폭 LM(정본 인사이드 포워드와 갈림 · 새 쟁점 후보).
- **게임 구현: 추가 관찰.** 경기 전용 프리셋 4-2-3-1 Wide · Balanced/Balanced/48(규칙 48~58 · RULE). 시즌 정본 변경 없음. **슬롯 정본 보류 5건 재판정 표**는 끝 절 — 사용자 판단 대기.

## ⭐ 사용자 관전 메모 대조표 (메모 1 H1~H4 · 메모 2 H1′·H2′)

원료: WS matchCentreData 1,503건(scope=full). 좌표는 WS(각 팀 자기 공격 방향 x · y 0 = 그 팀 오른쪽). **빌라 오른쪽 = 본머스 왼쪽(본머스 y>63)**. 측정 한계: 이벤트는 **볼이 있는 순간**만 담는다 — 오프더볼 위치·런은 직접 측정이 안 된다(히트맵은 SofaScore 전체 위치).

| # | 사용자 가설 | 실측 | 판정 |
|---|---|---|---|
| H1 | 음바예가 오른쪽에서 중앙으로 자주 들어온다 | 볼 터치 26: **오른쪽 폭 18 · 오른쪽 하프스페이스 5 · 중앙 2 · 왼쪽 하프 1**(91% 오른쪽) · 중앙 볼 소유는 46′ 역습 슈팅·54′ 두 번 · SS 평균 위치 (58, y19) · 히트맵 오른쪽 열(col4) 최대 · 보유 그리드 하프스페이스(col3) 6/10 | **부분 일치** — 볼을 잡는 위치는 폭(불일치), 하프스페이스 진입은 보유 그리드에 있다. 오프더볼 중앙 런은 이벤트로 판정 불가 |
| H2 | 그 결과 빌라 오른쪽이 비고 오른쪽 라인이 자주 뚫린다 | 본머스 파이널서드 터치: **빌라 왼쪽 쪽 131 · 중앙 36 · 빌라 오른쪽 쪽 60** · 오픈플레이 크로스 출발 빌라 왼쪽 9 · 오른쪽 5 · 전반 본머스 볼 소유 레인 오른쪽(=빌라 왼쪽) **50%** · 그러나 **실점 1·3이 빌라 오른쪽에서 마무리**(7′ 솔레르 x98 y77 컷백 · 69′ 애덤스 y90 크로스) · 본머스 4-1-4-1은 비대칭 — 오른쪽 후안루 (51,14)·개넌-도크 (73,17)·타버니어 (70,29) 3명 vs 왼쪽은 솔레르 (54,88) 혼자 폭(아들리 (58,55) 안쪽) | **부분 일치** — 양으로는 빌라 왼쪽이 더 많이 공략됐다. 결정적 장면은 빌라 오른쪽(솔레르 1명의 폭 침투)에서 나왔다 |
| H3 | 본머스 공격 패턴 = 반대 전환으로 빌라 오른쪽 공략 | 긴 측면 전환(가로 Δy≥50): **빌라 오른쪽으로 4(성공 3 · 10초 안 슈팅/박스 2)** vs 빌라 왼쪽으로 9(성공 6 · 2) · 첫 실점 사슬에 전환 2회(아래) | **부분 일치** — 반대 전환은 있었고 효율은 빌라 오른쪽 쪽이 높았지만(2/3), 빈도는 반대쪽이 더 많았다 |
| H4 | 첫 실점도 반대 전환 → 빌라 오른쪽 경로 | 5′19 부엔디아 볼 상실 → 5′27 밍스 파울 → 프리킥 재개 뒤 **30초 정돈 공격**: 5′52 쿡 칩 패스 (31,42)→(67,3) **본머스 오른쪽(빌라 왼쪽)으로 전환** → 개넌-도크·타버니어·크리스티 중앙 회수 → 6′13 **타버니어 칩 패스 (65,58)→(97,77) 빌라 오른쪽 배후** → 솔레르 컷백 → 6′17 아들리(xG 0.32). 그 30초 동안 빌라 이벤트 **0**. BirminghamWorld 「found the run of Julio Soler, who had escaped the attentions of stand-in right-back Lamare Bogarde」(임시 RB 보가르드의 마크를 벗어난 솔레르의 침투를 찾았다) | **일치** — 끌어들인 뒤 반대쪽(빌라 오른쪽) 배후. 단 **전환 순간 공백이 아니라 정돈 공격**(H2′와 구분) |
| H1′ | 음바예 기본 위치는 오른쪽 넓게, 중앙 진입은 공격 국면에서만 | 보유 그리드(map25_poss) 오른쪽 폭 X(최대)·하프스페이스 6 · 비보유 그리드(map25_def) 오른쪽 열 5·5·5·5 · 수비 액션 평균 (42,35) | **부분 일치** — 기본 위치 폭 = 일치. 공격 국면 중앙 진입은 볼 소유로는 드물다(중앙 2/22) |
| H2′ | 오른쪽 공백은 공격→수비 전환 순간에 생긴다 | 빌라 볼 상실 후 10초 안 본머스의 빌라 수비 3분의 1 진입: **상대 진영 상실 34건 → 빌라 오른쪽 0 · 왼쪽 2** · 자기 진영 상실 46건 → 오른쪽 9 · 왼쪽 14 · 실점 3 중 전환 실점 0(정돈 공격·코너·자기 진영 에러) · 음바예는 69′ 실점 때 이미 교체(58′) | **불일치** — 이 경기 이벤트로는 전환 순간 오른쪽 공백이 실점·진입으로 이어지지 않았다 |

⇒ **게임 함의(판정 뒤 · 사용자 판단)**: 오른쪽 문제는 「음바예의 안쪽 진입」보다 **RB 보가르드의 배후 대응**(7′ 솔레르 · 68′ 에러)이 실측 원인에 가깝다. 음바예 RM은 wm_winger/Attack(정본)이 이 경기 1위 .685(무결정 Δ.019)로 정본과 일치 — 복귀를 원해 포커스를 낮출 근거는 이 경기에서 나오지 않았다(H2′ 불일치). 근거 등급: 실측(C 아님 — 실축 이벤트) · FC27 RM 역할 복귀 성향은 **D(통설)**.

## ⭐ 이월 확인 대조표 (맨시티전 D+3 → 이 경기)

| # | 이월 항목 | 실측 | 판정 |
|---|---|---|---|
| C1 | 가르나초 소집·교체 서열(obs#1135·#1136) | **소집 · 58′ 첫 교체 묶음**(알리송과 동시 · 헤밍스 자리 LM) · 32′ 볼 소유 22 (72,86) **왼쪽 100%** · 패스 14/16 · 78′ 스로인 세트 유효 슈팅(xG 0.17 · 1대1 디 그레고리오 선방) · 에메리 「Garnacho as well having 30 minutes to play, getting confidence and understanding our structure」(가르나초도 30분을 뛰며 자신감을 얻고 우리 구조를 이해했다 · avfc.co.uk) | **일치(명단 복귀 · 1순위 교체)** — 맨시티전 「준비된 선수들」 경쟁 사유(obs#1136)와 모순 없음. 컵·로테이션 경기라 리그 서열로 일반화하지 않는다 |
| C2 | 마첸·만잠비·카마라·캐시 로테이션 | **마첸 90′ 선발**(맨시티전에 이어 연속) · **카마라·캐시 벤치 미출전**(계획 휴식) · **만잠비 명단 밖**(avfc 프리뷰 「could again feature」(다시 나설 수 있다) · 사유 1차 소스 0) | **부분 일치** — 카마라·캐시는 휴식. 만잠비 제외 사유 미확인 → D+1 |
| C3 | 고메스 위치 | **RDM**(고레츠카 오른쪽) · 볼 소유 61 (52,45) · 패스 51/53 · 수비 액션 14 (42,41) · SS 7.0(빌라 최고) — 바이킹 RB(강제) → 맨시티 LDM → 본머스 RDM | **변화(피벗 좌우 교대)** — 6번 축은 유지, 짝에 따라 좌우가 바뀐다 |

## ⭐ 중점 5인 전용 절

### 마조 (#39 · 카메룬 · 전 메스)
- **실측**: 선발 **ST 칸**(라인업) 75′ · SS 6.7 · FM 6.41 · **평균 위치 (60, y67) = 왼쪽**(pos_class LAM · 히트포인트 18 얇음) · 볼 소유 16 (60,66) 중앙 50·왼쪽 50% · 왼쪽 터치라인 x33~37·x72 터치 다수 · **공중 경합 0** · 레이오프 1 · 헤딩 패스 1(실패) · 오프사이드 0 · 수신 9(x̄ 61.2 · ≥80 3) · 슈팅 2 **유효 2**(xG 0.34 · 29′ 부엔디아 슈팅 리바운드 · **72′ 빅찬스** — 고메스 탈취 → 맥긴 → 마조, 디 그레고리오 선방) · 키패스 1(41′) · 33′ 경고(다이빙) · 운반(SS) 4회 27m.
- **역할 커널**: ST 1위 st_advanced/Support **.351**(Δ.019 무결정 · 2위 st_advanced/Attack .332) · 보유 1위 같음 .348 · 정본과 같음. fit이 낮은 건 왼쪽으로 빠진 위치 + 표본 얇음.
- **에메리**: 긍정 사례로 이름을 들었다 — 「Playing Marco Bizot, playing Taylor, playing Leon Goretzka, playing as well Brian Madjo. I think it is positive to play some players and they play well. We need players.」(비조·테일러·고레츠카·마조까지 뛰었다. 몇몇이 뛰고 잘한 건 긍정적이다. 선수가 필요하다 · E&S 직접 열람 · Tanswell X 같은 문장).
- **평점**: AVR 3 「Never really had anything to go at.」(공략할 거리를 사실상 받지 못했다) · AVN 6 · E&S 5 「Showed his strength at times but would have wanted to do more」(때때로 힘을 보여줬지만 더 하고 싶었을 것 · 스니펫) · SportsDunia 6 · Rotowire 「Madjo took two shots (two on goal) in 75 minutes」(75분 동안 슈팅 2, 모두 유효).
- **모국어**: 프랑스어 경기 기사 **0건**(「Brian Madjo Aston Villa Bournemouth Coupe de la Ligue」 · 「Madjo titulaire Aston Villa éliminé Bournemouth Républicain Lorrain」 · 「Brian Madjo ancien Messin … carton jaune simulation」) · 카메룬(Camfoot) **미시도** → D+1.
- **쟁점 #80(홀드업 vs 침투)**: 홀드업 근거(공중 경합·레이오프·등지기 수신)도, 침투 근거(오프사이드·깊은 수신·배후 런)도 **약하다**. 공급 부족(AVR)과 왼쪽 이탈이 겹친 표본. 트리거 「마조 ST 선발 2경기」 진행도는 pos_class 기준이라 이 경기(실측 LAM)가 세지지 않을 수 있다 — 라인업 ST 선발 1경기로 리포트에 기록.

### 고레츠카 (#27 · 독일 · 전 바이에른)
- **실측**: **이적 후 첫 선발** · **LDM(더블 피벗 왼쪽 · 10번 아님 — 10번은 부엔디아)** 70′ · SS 6.7 · **FM 7.18(빌라 1위권)** · 볼 소유 39 (47,64) 중앙 46·왼쪽 49% · 상대 진영 10 · 패스 **34/35**(97%) · 키패스 3(FM 기회 창출 3) · 드리블 2/2 · 경합 5/3 · 공중 1/1 · 수비 액션 13 (34,60) · 운반(SS) 10회 97m(전진 2·33m) · 운반 추정 29 · 수신 29(x̄ 50.0) · 45+′ 코너 프리 헤더 빗나감(xG 0.03) · SS 「hit the woodwork」(골대 1 · Sofascore 리포트).
- **역할 커널**: LDM 1위 dm_holding/Roaming .639(Δ.056) · **비보유 1위 dm_centrehalf/Defend .800** · 정본 dm_dlp/Roaming .523. 비보유 때 수비 액션 (34,60)로 고메스 (42,41)보다 **8m 낮다** — 짝 중 아래 축.
- **에메리**: 긍정 사례 명단(위 마조 인용과 같은 문장) · 「Goretzka playing」(고레츠카가 뛰었다 · avfc.co.uk).
- **평점·서사**: AVR 5 「Protected the ball nicely and got stuck in out of possession.」(볼을 잘 지켰고 비보유 땐 적극적으로 부딪쳤다) · E&S 6 「lack of understanding with Gomes」(고메스와의 호흡 부족 · 스니펫) · AVN 7 · SportsDunia 7 · Sky Soccer Special Bothroyd 「I can't believe that; it's a free header.」(믿을 수 없다, 노마크 헤더였다) · afcb 「neatly squeezed between Villa pair Leon Goretzka and Ian Maatsen」(아들리가 고레츠카와 마트센 사이로 비집고 들어갔다 — 7′ 실점).
- **모국어(독일어)**: Sport1(10-28 23:32 · 직접) 「Die Startelfpremiere von Leon Goretzka endete in einer Enttäuschung.」(레온 고레츠카의 첫 선발은 실망으로 끝났다) · 「Abreibung für Goretzka bei Startelf-Debüt」(선발 데뷔전에서 혼쭐난 고레츠카) — 행동 서술 없음. 프리뷰 「Bis zum Mittwochabend stand Goretzka nur 53 Minuten auf dem Platz.」(수요일 밤까지 고레츠카는 53분만 뛰었다). kicker·Bild·tz·AZ·Sky DE 경기 기사·평점 **0건**.
- **쟁점 #25(더블 피벗 vs 10번)**: 이 경기 = **더블 피벗 확정**(라인업·평균 위치·서사 3원 일치). 트리거 「고레츠카 선발 2경기」가 이 경기로 **2/2 차서 판정할 차례** — 판정은 아래 「판정 쟁점」 절.

### 하우드-벨리스 (#4 · 잉글랜드 · 전 사우샘프턴)
- **실측**: 선발 **RCB** 90′ · SS 6.7 · FM 6.37 · 볼 소유 72 (33,36) · 패스 **60/67** · 후방 순환 축(밍스↔ 21/15 · →비조 21) · 태클 4 · **지상 경합 5/5** · 공중 0/1 · 클리어 4(헤딩 2) · 블록 1 · 수비 액션 14 (20,35) · 운반(SS) **28회 232m**(전진 1·24m) · 운반 추정 49(전진 10m+ 2) · 롱볼 2 · 68′ 세트피스 헤더 유효 슈팅(xG 0.12 · 빅찬스 실패) · 91′ 오프사이드 유도.
- **역할 커널**: RCB 1위 cb_bpd/Aggressive .869(Δ.015 무결정 · 2위 Build-Up) = 정본 · **비보유 1위 cb_defender/Defend .820**.
- **에메리**: 「playing Taylor」(테일러가 뛰었다 — avfc 원문은 「Tyler」, 문맥상 하우드-벨리스) 긍정 언급.
- **평점·서사**: AVR 4 「Showed a good nose for danger but ultimately unable to impose himself defensively in the key moments.」(위험을 잘 감지했지만 결정적 순간에 수비 존재감을 보이지 못했다) · 공을 몰고 전진하려는 의지가 커지고 있다(AVR 요약) · E&S 4 「Should have scored with a header」(헤더로 득점했어야 했다 · 스니펫) · AVN 5 · SportsDunia 6.
- **지역지**: Southern Daily Echo·MEN·Birmingham Mail **0건**.
- **쟁점 #24(슬롯별 포커스와 공중볼)·#58(PL 표본)**: #24 트리거 3/3 「판정할 차례」 — 이 경기는 컵이라 #58(PL) 진행도엔 안 세진다. 판정은 아래 절.

### 음바예 (#19 · 세네갈 · 전 PSG)
- **실측**: 선발 **RM** 58′ · SS 6.7 · FM 6.35 · 볼 소유 22 **(62,16) 오른쪽 91%** · 상대 진영 12 · 패스 17/19 · 크로스 1 · 드리블 1/1 · 운반(SS) 9회 129m(**전진 3·85m**) · 수신 17(x̄ 64.6 · 깊은 10 · ≥80 3) · 슈팅 1(47′ 역습 블록 — 헤밍스 맞고 빗나감) · 수비 액션 5 (42,35) · 12′ 자기 진영 클리어(x13 y13).
- **역할 커널**: RM 1위 **wm_winger/Attack .685**(Δ.019 무결정 · 2위 wm_wideplm/Attack .666) = 정본 · 보유 1위 wm_wideplm/Attack .754 · 비보유 1위 wm_winger/Attack .460.
- **관전 메모**: 위 대조표 H1·H1′·H2′(폭 유지형 · 전환 공백 불일치).
- **에메리**: 직접 언급 **0**(긍정 명단에 없음).
- **평점·서사**: AVR 5 「Never shy of putting in a shift.」(헌신적으로 뛰는 데 주저함이 없었다) · 보가르드를 도우려 수비 가담 · 전반 솔레르와의 대결 우위(AVR 요약) · E&S 5 「Comfortably his quietest performance in a Villa shirt」(빌라 유니폼을 입고 가장 조용한 경기 · 스니펫) · AVN 6 · beIN 「nearly levelling the scores through Ibrahim Mbaye」(음바예로 동점을 만들 뻔했다).
- **모국어**: 세네갈 Wiwsport(10-28 · 직접) 「les coéquipiers d'Ibrahim Mbaye – titulaire – n'ont pas su trouver la faille」(선발 출전한 이브라힘 음바예의 동료들은 틈을 찾지 못했다) — 행동 서술 없음. L'Équipe·Le Parisien·Foot Mercato·Senego·Seneweb·Record **0건** · Foot Africa 403.
- **쟁점 #6(RM 인선)·#7(윙어 vs 인사이드 포워드)·#48(폭·배후·수비)**: 이 경기 = **폭 유지 윙어 + 수비 가담**. #6·#7·#48 트리거가 이 경기로 찬다 — 판정은 아래 절.

### 헤밍스 (#53 · 잉글랜드 · 빌라 아카데미)
- **실측**: 선발 **LM**(부상 복귀 · Sports Mole) 58′ · SS 6.2 · FM 6.21 · 볼 소유 30 **(60,79) 왼쪽 80%** · 상대 진영 15 · 패스 16/19 · 슈팅 3(xG 0.19 · 9′ 역습 빗나감 · 29′ · 40′ 블록) · 드리블 2/5 · 경합 2/7 · 볼 상실 7 · 운반(SS) 12회 126m(**전진 6·89m** — 팀 최다 전진 운반) · 수신 25(깊은 11 · ≥80 6) · 수비 액션 5 (41,84).
- **역할 커널**: LM 1위 **wm_widemid/Support .723**(Δ.060) · 정본 **wm_insidefwd/Balanced .369** · wm_winger/Attack .563 — **안쪽 진입형 정본과 실측이 크게 갈린다**(폭 유지).
- **에메리**: 직접 언급 **0**.
- **평점·서사**: AVR 4 「Fired wide with Villa's first shot of the match.」(빌라의 첫 슈팅을 빗나가게 찼다) · 앞에 공간이 있을 때 가장 좋아 보였다(AVR 요약) · E&S 5 「No doubting his effort but … didn't always get the decisions right」(노력은 의심할 여지가 없지만 판단이 늘 옳지는 않았다 · 스니펫) · AVN 4 · SportsDunia 6.
- **모국어(영어 지역지)**: Birmingham Mail·아카데미 담당 기사 **0건**.
- **쟁점**: 맞는 쟁점 없음 → **새 쟁점 후보**「헤밍스 LM: 폭 유지(widemid/winger) vs 정본 인사이드 포워드」 — 트리거 후보: 헤밍스 LM 선발 2경기(사용자 판단 · 이번 회차에 쟁점 행은 열지 않았다 — 영상 주장이 생기면 그때 묶는다).

## 1. 경기 개요와 원천 수치

| 항목 | 빌라 | 본머스 |
|---|---|---|
| 점유(전반/후반) | **51**(44/54) | 49(56/46) |
| xG(FotMob · 오픈/세트) | **1.65**(1.29/0.37) | **2.71**(1.64/1.07) |
| xGOT | 0.99 | 2.56 |
| 슈팅(유효 · 블록) | 17(5 · 5) | 19(7 · 2) |
| 빅찬스(득점) | 4(0) | 3(1) |
| 패스(정확) | 486(431) | 456(406) |
| 롱볼 | 21/42 | 34/52 |
| 크로스 | 4/9 | 4/20 |
| 코너 | 2 | 6 |
| 경합 % | 50 | 50 |
| 공중 | 7/11 | 4/11 |
| 드리블 | 11/26 | 4/12 |
| 태클 · 가로채기 · 클리어 | 12 · 3 · 19 | 20 · 8 · 10 |
| 상대 박스 터치 | 24 | 37 |
| 오프사이드 | 1 | 4 |
| 에러→실점(SS) | **2** | 0 |
| PPDA(WS) | **14.25**(전반 9.75 · 후반 21.0) | **9.89**(12.18 · 7.95) |
| def_x(WS) | 35.0 | 46.4 |

- **득점 국면**: 0-0 0–7′(7분) · 0-1 7–51′ · 0-2 51–69′ · 0-3 69′– → `phase_level 7 · phase_trail 83`(분). 리드 국면 **0**.
- **교체**: 본머스 46′ 클라위버르트·라양(타버니어·아들리) · 63′ 애덤스·브룩스 · 80′ 크루피 / 빌라 58′ 알리송(↔음바예)·가르나초(↔헤밍스) · 70′ 맥긴(↔고레츠카)·바클리(↔부엔디아) · 75′ 아브라함(↔마조).
- **경고**: 빌라 부엔디아 12′ · 마조 33′ · 고메스 54′ / 본머스 후안루 16′ · 개넌-도크 25′ · 쿡 67′.
- **결장**: 완비사카(햄스트링) · 루게리(두어 달) · 오나나(부상 — avfc 프리뷰) · 만잠비 명단 밖(사유 미확인). 벤치 미출전: 스즈키 · 캐시 · 키바 시세(복귀 단계) · 카마라.
- **수집**: SS `/event/17118370/{lineups,statistics,incidents,shotmap,graph,managers}` + 선수 히트맵·평균 위치(collect_event.py headless — 403 없음) · FotMob 6275374(xG 4종 동시 스냅샷 · 슛맵 36 — **컵이라 SS 슛 xG 없음 → `match_shots` provider=FotMob**) · WS 2035006 headful 전체 JSON(1,503건) `data/2026-10-28-avl-ws-2035006.json`. 히트맵 기준(45분+ · hit_points 15+) 통과: 선발 11명 전원(마조 18 · 음바예 28 경계).

## 2. 전술 설명

### 점유 구조·빌드업
- 비조 → 밍스(23)·하우드-벨리스 후방 순환 → **밍스 → 마트센(24) 왼쪽 축**이 1번 경로. 전반 중앙·상대 진영 볼 소유 레인 **왼쪽 46 · 중앙 30 · 오른쪽 24%**(후반 34/43/23 — 중앙 증가).
- 비조 롱패스 16/51(31%). 고메스가 피벗 중 높은 쪽(볼 소유 x52)으로 전진 수신, 고레츠카는 왼쪽 하프스페이스 지원(x47).
- 부엔디아 10번은 **오른쪽 하프스페이스**로 기울었다(볼 소유 (64,39) · 상대 진영 21 팀 최다) — 음바예가 폭을 지키니 안쪽 칸을 부엔디아가 채웠다.
- 에메리 진단: 「trying to break the high press, especially the first 10 minutes in each half. But we couldn't.」(하이프레스를 깨려 했지만 못 했다) · Tanswell 「Villa pedestrian and struggled to play out.」(빌라는 굼떴고 빌드업 탈출에 애먹었다).

### 비점유 구조·압박
- 4-4-1-1 중·저블록: 수비 액션 높이 음바예 42 · 고메스 42 · 헤밍스 41 · 부엔디아 40 · 고레츠카 34 · 마조 64(혼자 높음).
- PPDA 14.25 — 맨시티전(8.55)보다 훨씬 수동적. 후반 21.0. def_x 0–7′ 46.4 → 7–15′ **21.4**(실점 직후 낮은 블록) · 45–51′ **15.6**(후반 시작 본머스 압도 · 51′ 실점).
- 본머스 4-1-4-1의 **오른쪽 3인 과부하**(후안루·개넌-도크·타버니어)를 빌라 왼쪽(마트센·헤밍스·고레츠카)이 받았고, 왼쪽은 솔레르 1명 폭 + 아들리 안쪽 — 빌라 오른쪽은 **보가르드가 솔레르 배후 침투를 감당**하는 구조.

### 전환·rest-defense·세트피스
- 빌라 상대 진영 볼 상실 34건 뒤 본머스가 10초 안에 빌라 수비 3분의 1에 들어간 것은 **2건**(모두 왼쪽) — rest-defense 자체는 버텼다.
- **세트피스가 결정적 약점**: 본머스 세트 xG **1.07** · 51′ 짧은 코너 → 쿡 터치라인 근처 슛이 비조 니어포스트로(에러) · 63′ 코너 로드리게스 xG **0.88** 빗나감. 빌라 세트 xG 0.37(하우드-벨리스 68′ 헤더 · 고레츠카 45+′ 프리 헤더 · 가르나초 78′ 스로인).

## 3. 전술적 특성

- **강점**: 점유 51%·패스 486으로 볼은 다뤘다(에메리 「we could progress, we could dominate」(전진했고 주도할 수 있었다)). 빅찬스 4 · xG 1.65 — 찬스 생산은 했다.
- **약점**: ⑴ 결정력(빅찬스 0/4 · xGOT 0.99) ⑵ 개인 에러 2(비조·보가르드) ⑶ 세트피스 수비 ⑷ **각 하프 첫 15분 강도**(def_x 7–15′ 21.4 · 45–51′ 15.6 · 모멘텀 2–22′ −30.1 · 47–56′ −41.2) ⑸ 임시 RB 보가르드의 배후 대응.
- **상대가 만든 교란**: Rose의 「early good starts」(초반 좋은 출발) 설계 — 「Now we changed the momentum, now we are a team that starts well」(이제 시작을 잘하는 팀이 됐다 · PA). 비대칭 4-1-4-1(오른쪽 과부하 + 왼쪽 솔레르 단독 폭)로 빌라를 왼쪽에 묶고 반대쪽으로 친 장면이 선제골.
- **직전 경기 대비**: 4-2-3-1·4-4-1-1 형태와 왼쪽 쏠림(맨시티전 C5)은 같다. 다른 점은 점유(37→51%)·압박 강도(PPDA 8.55→14.25)·인원(9명 교체).

## 4. 경기 중 변화

1. **0–7′ 0-0**: 본머스 강한 출발(def_x 본머스 46 · 빌라 46). 5′ 부엔디아 볼 상실 → 밍스 파울 → 30초 정돈 공격 → **7′ 0-1**.
2. **7–51′ 0-1**: 빌라 점유 회복(27–34′ 모멘텀 +25.8 · 30′ 부엔디아·마조 연속 슈팅 · 40′ 헤밍스). 전반 xG 0.61–0.97.
3. **46′ 본머스 클라위버르트·라양 투입 → 45–51′ 압도(빌라 def_x 15.6) → 51′ 코너·비조 에러 0-2.**
4. **58′ 알리송·가르나초 투입** → 57–61′ 모멘텀 **+43.8**(경기 최고) · 58′ 알리송 블록 · 59′ 고메스 유효 슈팅. 62–67′ 본머스 반격(−51.3 · 63′ 로드리게스 0.88 빗나감).
5. **69′ 보가르드 자기 진영 오른쪽 에러 → 애덤스 크로스 → 0-3.** 70′ 맥긴·바클리 · 75′ 아브라함 — 형태는 4-2-3-1 유지(인원 교체). 72′ 마조 빅찬스 · 78′ 가르나초 · 84′ 알리송 0.31 모두 무득점.

## 5. 선수별 분석 — 출전 선수 전원

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치·히트맵(WS 볼 소유 · 수비 액션) | 특성·수행 | FC 역할/포커스 함의(FC27 커널 · 단일 경기) |
|---|---|---|---|---|---|
| 비조 | GK · 후방 배급 시작 | 90′ SS 5.6 · FM 5.56 · 패스 38/51 · 롱 16 · 세이브 4 | (8,49) | ⚠️ 51′ 에러 → 실점 | gk_goalkeeper/Defend .943(Δ.034 무결정) · 정본 gk_ballplaying/Build-Up .667 |
| 보가르드 | RB(임시 · 코번트리전 이후 첫 선발) | 90′ SS 5.8 · FM 5.16 · 패스 37/41 · 수비 액션 7 | (41,16) 오른쪽 93% · 수비 (34,26) | ⚠️ 7′ 솔레르 배후 허용 · 68′ 에러 → 69′ 실점 | fb_wingback/Balanced .903(Δ.029) = 정본 |
| 하우드-벨리스 | RCB | 90′ SS 6.7 · 패스 60/67 · 지상 5/5 · 태클 4 · 운반 28회 232m | (33,36) · 수비 (20,35) | 후방 순환 축 · 68′ 헤더 빅찬스 실패 | cb_bpd/Aggressive .869(Δ.015) = 정본 · 비보유 cb_defender/Defend .820 |
| 밍스 | LCB · 빌드업 1번 | 90′ SS 6.9 · 패스 **83/88**(팀 최다) · 오프사이드 유도 3 | (29,71) · 수비 (30,60) | 왼쪽 축 시작점 | cb_bpd/Build-Up .909(Δ.014) = 정본 |
| 마첸 | LB(높은 폭) | 90′ SS 6.1 · 패스 48/57 · 상대 진영 13 | (45,85) 왼쪽 92% · 수비 (21,70) | 본머스 오른쪽 3인 과부하를 받음 | fb_fullback/Balanced .756(Δ.036) · 보유 fb_wingback/Balanced · 정본 fb_att_wb/Support .672 |
| 주앙 고메스 | **RDM**(피벗 중 높은 쪽) | 90′ **SS 7.0** · FM 7.13 · 패스 51/53 · 운반 29회 265m · 수비 액션 14 · 54′ 경고 | (52,45) · 수비 (42,41) | 72′ 마조 빅찬스 출발점(71′ 탈취) | **dm_dlp/Roaming .807(Δ.206 결정)** · 정본 dm_holding/Defend .437 |
| 고레츠카 | LDM | 70′ SS 6.7 · FM 7.18 · 패스 34/35 · 키패스 3 | (47,64) · 수비 (34,60) | 중점 절 | dm_holding/Roaming .639(Δ.056) · 정본 dm_dlp/Roaming .523 |
| 음바예 | RM(폭) | 58′ SS 6.7 · 운반 전진 3·85m | (62,16) 오른쪽 91% · 수비 (42,35) | 중점 절 | wm_winger/Attack .685(Δ.019) = 정본 |
| 부엔디아 | CAM(오른쪽 하프스페이스) | 70′ SS 6.5 · 패스 23/28 · 슈팅 4(블록 2) · 12′ 경고 | (64,39) 중앙 54·오른쪽 38% · 상대 진영 21 | 5′ 볼 상실이 7′ 실점의 출발 | cam_playmaker/Balanced .688(Δ.003 무결정 · 2위 Roaming = 정본) |
| 헤밍스 | LM(폭) | 58′ SS 6.2 · 슈팅 3 · 운반 전진 6 | (60,79) 왼쪽 80% | 중점 절 | wm_widemid/Support .723(Δ.060) · 정본 wm_insidefwd/Balanced .369 |
| 마조 | ST 칸 · 실측 왼쪽 | 75′ SS 6.7 · 슈팅 2(유효 2) · 공중 0 | (60,66) | 중점 절 | st_advanced/Support .351(Δ.019) = 정본 |
| 알리송 | RM(58′~) | 32′ SS 6.5 · 슈팅 3(84′ xG 0.31) · 수비 액션 7 | (60,24) · 수비 (36,23) | 짧은 표본 | 리포트용 — 1위 wm_widemid/Defend .518 |
| 가르나초 | LM(58′~) | 32′ SS 6.9 · 패스 14/16 · 78′ 유효 슈팅 | (72,86) 왼쪽 100% · 수비 액션 0 | C1 | 리포트용 — 1위 wm_winger/Attack .907 |
| 맥긴 | LDM 자리 → 실제 8번(x65) | 20′ SS 6.9 · 71′ 마조 빅찬스 패스 | (65,49) | 짧은 표본 | 리포트용 |
| 바클리 | CAM(70′~) | 20′ SS 6.5 · 패스 11/12 | (50,57) 중앙 81% | 짧은 표본 | 리포트용 |
| 아브라함 | ST(75′~) | 15′ SS 6.5 · 볼 소유 3 · 91′ 오프사이드 | — | 짧은 표본 | 리포트용 |

45분 미만 교체 5명은 리포트 근거로만 쓰고 대표 그리드·처방 집계에는 넣지 않는다.

## 6. 전술 변화 판정

- **유지**: 4-2-3-1(보유 양 풀백 폭) · 비보유 4-4-1-1 · 왼쪽 빌드업 축(맨시티전 C5와 같은 방향) · 6번 짝(고메스 + 1).
- **새로 나타난 것**: 고메스 RDM(좌우 교대) · 고레츠카 LDM 첫 선발 · 보가르드 RB · 음바예·헤밍스 양 폭 윙어(안쪽 진입형 아님).
- **직전 경기 대비 변화**: 압박 강도 하락(PPDA 8.55→14.25) — 로테이션 + 에메리가 밝힌 「강도에서 졌다」.
- **`manager_profiles` 반영**: rotation(컵 = 9명 교체 · 「add some players our understanding … getting fit」) → `situational` 축 덧붙임. pressing 축은 **갱신 불필요** — 컵 로테이션 경기의 PPDA를 감독 성향으로 일반화하지 않는다.

## 7. 게임 구현 판정

- 결론: **추가 관찰**.
- **이 경기 전용 팀 설정**(`match_game_setups` #64 · match_only): FC27 · 4-2-3-1 Wide · 빌드업 **Balanced** · 수비 접근 **Balanced** · 라인 **48** · `core.team_settings.suggest(51, 486, 42, 14.25)` → Balanced/Balanced/48~58 · rule_note **RULE** · 보유 4-2-3-1 / 비보유 4-4-1-1.
- **선발 11명**(`match_player_prescriptions` · FC27 커널 1위 · 무결정은 2위 병기):

| 칸 | 선수 | 역할/포커스 | fit | Δ | 2위 | 정본과 |
|---|---|---|---|---|---|---|
| GK | 비조 | gk_goalkeeper/Defend | .943 | .034 무결정 | Balanced | 다름(정본 BPK .667) |
| RB | 보가르드 | fb_wingback/Balanced | .903 | .029 무결정 | wingback/Support | 같음 |
| RCB | 하우드-벨리스 | cb_bpd/Aggressive | .869 | .015 무결정 | bpd/Build-Up | 같음 |
| LCB | 밍스 | cb_bpd/Build-Up | .909 | .014 무결정 | bpd/Aggressive | 같음 |
| LB | 마첸 | fb_fullback/Balanced | .756 | .036 무결정 | fullback/Versatile | 다름(정본 att_wb/Support .672) |
| RDM | 주앙 고메스 | **dm_dlp/Roaming** | .807 | **.206** | dlp/Build-Up | 다름(정본 holding/Defend .437) |
| LDM | 고레츠카 | dm_holding/Roaming | .639 | .056 | centrehalf/Defend | 다름(정본 dlp/Roaming .523) |
| RM | 음바예 | wm_winger/Attack | .685 | .019 무결정 | wideplm/Attack | 같음 |
| CAM | 부엔디아 | cam_playmaker/Balanced | .688 | .003 무결정 | playmaker/Roaming(정본) | 무결정 동률 |
| LM | 헤밍스 | wm_widemid/Support | .723 | .060 | widemid/Defend | 다름(정본 insidefwd/Balanced .369) |
| ST | 마조 | st_advanced/Support | .351 | .019 무결정 | advanced/Attack | 같음 |

- `prescriptions`·`slot_canon_roles`·`team_tactic_setups` 변경 **없음** — 로테이션 11명·컵·단일 경기. 등급: 커널 적합 = 실측(우리 계산) · 「Defend 포커스 = 덜 올라간다」류 해석은 **D**.
- 다음 경기 재검증: ⑴ 풀럼전(10-31) 주전 복귀 시 RDM·LM 칸 1위 ⑵ 가르나초 리그 명단 ⑶ 만잠비 제외 사유.

## 8. 영상·기사·감독 발언

### 감독·선수 1차 발언
- **에메리 — avfc.co.uk 「Emery on Bournemouth loss」(10-28 · 직접 열람)**: 「Since I arrived at Aston Villa we've played here four times, and we have won, we have drawn, and today we lost, but we played the same match like we played before.」(내가 온 뒤 여기서 네 번 경기했고 이기고 비기고 오늘은 졌지만 경기 자체는 이전과 같은 방식이었다) · 「Here, you must be compact, you must avoid the chances they were creating.」(여기서는 촘촘해야 하고 상대가 만드는 찬스를 막아야 한다) · 「because we were creating chances even more than other times we were playing here, and we weren't clinical today.」(여기서 치른 다른 경기보다 찬스를 더 많이 만들었는데 오늘은 마무리가 날카롭지 못했다) · 「We have Fulham on Saturday, and Premier League is the priority. Then we have the Champions League and FA Cup.」(토요일 풀럼전이 있고 프리미어리그가 우선이다. 그다음 챔피언스리그와 FA컵).
- **에메리 — E&S/PA(Matt Maher · 10-28 22:38 · 직접)**: 「We were motivated for this competition because it was a way to add some players our understanding, our idea, getting fit, but competing as well in a difficult place like this.」(이 대회에 의욕이 있었다. 몇몇 선수에게 우리의 이해·아이디어를 입히고 몸을 끌어올리면서 이런 어려운 원정에서 경쟁도 할 수 있는 길이었다) · 「the intensity they had in the first 15 minutes of the first and second half was the difference.」(전반과 후반 첫 15분 상대의 강도가 차이였다).
- **에메리 — Sky(10-28 23:25)**: 「the first 20 minutes we didn't start with the intensity needed, but we were progressing and getting better」(첫 20분은 필요한 강도로 시작하지 못했지만 점점 나아졌다) · 「We weren't clinical. The third goal finished the match.」(날카롭지 못했다. 세 번째 골로 경기가 끝났다).
- **Marco Rose — PA(Irish News · 10-28 23:19)**: 「We felt after Chelsea that we have to start better, especially if you talk about early good starts of the opponents」(첼시전 뒤 더 잘 시작해야 한다고 느꼈다) · 「We scored nice goals, we were relentless, won good balls」(좋은 골을 넣었고 끈질겼고 좋은 볼을 따냈다). 경기 전 afcb(10-27) 「They have quite a clear approach with the coach. I like the way they play.」(감독 아래 접근법이 뚜렷하다. 그들의 플레이 방식이 좋다). 빌라 구조를 직접 짚은 발언 0.

### Jacob Tanswell (X @J_Tanswell · 브라우저 직접 열람 · 로그아웃 상태 최근 4건)
- 21:34 FT 총평: 「First 15 minutes set the tone. Villa pedestrian and struggled to play out. Bournemouth pressed and showed the difference in intensity.」(첫 15분이 흐름을 정했다. 빌라는 굼떴고 빌드업 탈출에 애먹었다. 본머스가 압박하며 강도 차이를 보였다) · 「Defence poor, shape was all over the place, getting cut through too easily & players who hoped to stake a claim to Emery did not.」(수비는 형편없었고 대형은 엉망이었으며 너무 쉽게 뚫렸다. 에메리에게 어필하려던 선수들은 그러지 못했다).
- 22:20 에메리 verbatim: 「We knew before … and we planned to try and stop them with their intensity, trying and get duels, trying to break the high press, especially the first 10 minutes in each half. But we couldn't. But we could progress, we could dominate, but we weren't clinical.」(미리 알았고 그 강도를 막으려 계획했다. 경합에서 이기고 하이프레스를 깨려 했고 특히 각 하프 첫 10분이 그랬다. 하지만 못 했다. 그래도 전진했고 주도했지만 마무리가 날카롭지 못했다) — **탈압박 계획 실패 자기 진단**(PPDA·def_x 15′ 구간과 같은 방향).
- 21:23 「Antonio Silva is basically a right footed Pau Torres」(안토니우 실바는 사실상 오른발잡이 파우 토레스다).
- 미수행: 경기 전 트윗(명단 사유) — 로그아웃 상태에서 4건만 로드 · xcancel 451 · nitter 빈 응답.

### 기사·평점
- avfc 경기 리포트·팀뉴스·프리뷰(10-28) · E&S/BirminghamWorld 경기 리포트(Matt Maher · 직접) — 「The left-hand side was a problem area for Villa」(왼쪽이 빌라의 문제 구역이었다 — 어느 팀 기준 「왼쪽」인지 모호 · 실측은 양으로 빌라 왼쪽, 결정적 장면은 빌라 오른쪽) · afcb 매치 리포트(직접) · Sky 리포트(직접) · PA/Irish News(직접) · Aston Villa Review 평점(Chris Nee · 직접) · Aston Villa News 평점(직접 · 숫자만) · E&S 평점(**스니펫** · 403) · SportsDunia(숫자만) · beIN(직접) · Rotowire(마조).
- **스페인어**: 에메리 원어 **0**(Marca·AS·Relevo·El Desmarque·MD·Noticias de Gipuzkoa · EFE/Infobae 단신은 인용 없음). avfc ESPAÑOL 탭은 2025-05 이후 갱신 정지. 가르나초: Olé 전재(shango.media) 「entró al campo de juego durante los 13′ del segundo tiempo」(후반 13분에 투입됐다) — 플레이 서술 없음.

### 영상 (필수 채널 3곳 · Jacob Horsfall은 10-29 제외)
- UTV 「VILLA STINK OUT OF THE LEAGUE CUP | MATCH REACTION」(8Cj605t0jo8 · 10-28 · 28:16 · yt-dlp 자막 전사) → `match_videos` #457.
- 1874 「CarabOUT- Bournemouth dump Aston Villa out the League Cup...」(CsuD00ou-_o · 10-28 · 29:43 · 브라우저 pot 경로 · 뮤트) → #458.
- 1874 「AFC Bournemouth v Aston Villa | Madjo or Abraham to Lead the Line?」(_5yNVb6iyYk · 10-27 프리뷰 · 마조 중점이라 포함 · 뮤트 pot) → #459.
- 건너뜀: UTV 프리뷰(Y2u0lm29XjA) · UTV 워치얼롱 라이브(msPmoDVefnA) · The Villans 경기 후 업로드 **0**(프리뷰 #399는 기수집).
- 요약·구현 주장은 아래 「영상 요약」 절.

### 영상 요약 (전사 3편 · `match_videos` #457~#459 · 구현 주장 7행 · auto-caption)
- **#457 UTV 리액션**: 결과보다 「에메리식 구조 부재」를 문제 삼음 — 2선·ST가 더블 피벗 옆으로 내려오지 않아 백4 노출, 공격이 왼쪽에 쏠려 음바예 고립. [20:56] 「if you've got threat on the right surely you'd use it but we just chose totally to not pass to him」(오른쪽에 위협이 있으면 써야 하는데 아예 패스를 안 했다) · [23:01] 「Mbaye had 26 touches and he played 58 minutes. Not enough.」(58분 26터치, 부족하다) — 실측 볼 터치 26·왼쪽 빌드업 축과 같은 방향. [10:35] 「Gomez was CDM today and Geretska was the one playing in that more that number eight role. Geretska wasn't marauding forward」(오늘 고메스가 CDM, 고레츠카가 8번이었지만 치고 나가지 않았다) — ⚠️ 실측은 고메스가 피벗 중 **더 높은** 쪽(x52 vs 47) · 주장 PENDING #25. [15:11] 「Majo had no service whatsoever」(마조는 공급이 전혀 없었다). [13:39] 헤밍스 「he's not ready for Villa at this moment in time」(지금은 빌라 수준이 아니다).
- **#458 1874 사후 라이브**: 비조 51′ 에러가 최대 화제 · 보가르드는 RB가 아니다 · [17:08] 하우드-벨리스 「I don't think he did anything wrong tonight, but I felt he should have scored that … header」(잘못한 건 없지만 그 헤더는 넣었어야 했다 · 주장 PENDING #24) · [23:43] 마조 「a 17-y old center forward is always going to struggle」(17세 센터포워드는 늘 고전한다) · [05:19] 가르나초 「could have easily had a goal and an assist」(골·도움을 올릴 수도 있었다).
- **#459 1874 프리뷰**: 아브라함 선발·마조 교체 예상 → 실측 반대(진행자도 사후 「I was wrong」(내가 틀렸다) · 주장 NA) · [15:51] 「Unai Emery is … of the opinion with Brian Majer that he wants to ease him in」(에메리는 마조를 천천히 적응시키려 한다 · 진행자 해석 · 등급 D).
- 주장 7행: HELD 3(#54 피벗 보호 · #48 음바예 폭 고립 · #52 압박 하 중앙 턴오버) · PENDING 2(#25 · #24) · NA 2. 실측과 어긋난 영상 서술: UTV가 3실점째를 비조 탓으로 돌림(비조 에러는 51′ 2실점째) · 1874가 3실점 득점자를 「Ryan」으로(실측 로드리게스).

### 미수행·0건
- The Athletic 본문(유료벽) · BBC·Birmingham Mail 경기 기사(검색 0) · Bournemouth Daily Echo(Request blocked) · 카메룬 매체(마조) 미시도 · E&S 평점 원문(403 — 스니펫만).
- 전술 블로그(TFA·BTL·Spielverlagerung·Coaches' Voice): 경기 후 수 시간이라 **미게재** → D+1~D+3.

## 9. 데이터 반영과 한계

- DB(행 추가): `matches` #128 · `player_matches` 16(국면 그리드·phase 분·SS 운반·FotMob 경기 스탯·WS 운반 추정/수신 · pulled=2026-10-29 scope=full) · `team_match_stats` 1(xG 4종 FotMob 동일 스냅샷 · PPDA·def_x) · `match_events` 19 · `match_shots` 36(FotMob) · `match_period_stats` 2 · `match_momentum` 92 · `match_set_pieces` 20 · `match_reports` #64(draft) · `match_player_reports` 16 · `match_game_setups` 1 · `match_player_prescriptions` 16(선발 11 + 교체 5) · `phase_metrics` 78 · 가설 판정 9행 · `match_videos` 3.
- 집계(§4 · G18): measured 3행 재집계 — 헤밍스 LM #971 n=6→7 wm_winger/Balanced .7191(Δ.016 무결정 · 2위 widemid/Support) · 밍스 LCB #1004 n=6→7 cb_bpd/Aggressive .9366 · 하우드-벨리스 RCB #1005 n=3→4 cb_bpd/Aggressive .9275 — **argmax 전부 불변**(T2 아님 · 정본 불변). T1 `refresh_eval_samples --apply` 18행.
- 판정 쟁점: `claim_issues --due` AVL 판정할 차례 1건 — **#24 연장**(하우드-벨리스 LCB 선발 0이라 슬롯 비교 불성립 · 추가 선발 2경기). #6·#7·#25·#48·#80 진행도는 이 경기 반영 후 다음 회차에 다시 본다. 영상 주장 PENDING 2(#25·#24) · HELD 3(#54·#48·#52).
- 선수 상태(§0-1): `collect_fotmob_players.py --team AVL`만 실행(CHE·LIV·ATM 수집 보류).
- `manager_profiles` AVL `situational` 덧붙임(컵 로테이션) · pressing·buildup 등 나머지 축 갱신 불필요(로테이션 컵 경기 1개로 성향 일반화 금지).
- 한계: ⑴ 로테이션 11명·컵 — 시즌 정본 판단 표본으로 약하다 ⑵ 0-1이 7′부터라 83분이 열세 국면(스코어 효과) ⑶ 마조 히트포인트 18·음바예 28 경계 ⑷ 오프더볼 위치는 이벤트에 없다(H1·H2′의 측정 한계) ⑸ E&S 평점은 스니펫.
- `match_reports.status` = **draft** — D+1~D+3 추적 뒤 complete 판정.

## ⭐ 슬롯 정본 보류 5건 — 재판정 표 (맨시티 10-24 · 본머스 10-28 · 리서치 §1.2 형식)

조건(obs#1123) 「맨시티 포함 공식전 2경기」가 이 경기로 찬다. 실측 열은 두 경기 경기 프리셋(`match_player_prescriptions` #63·#64)의 FC27 커널 1위·Δ·보유 그리드. ⛔ **정본(`slot_canon_roles`·`team_tactic_setups` #46)과 인게임 코드 `7ZTFKBu$37p7`는 바꾸지 않았다 — 사용자 판단 대기.**

| # | 칸·쟁점 | 정본 FC27 | 맨시티(#63 · 37% · 리드 76분) | 본머스(#64 · 51% · 로테이션 · 열세 83분) | 2경기 판정(제안) | 비고·등급 |
|---|---|---|---|---|---|---|
| ⑴ | **RDM** dm_holding/Defend vs dm_dlp/Build-Up | dm_holding/Defend | 카마라 1위 **holding/Defend .779**(Δ.013 무결정 · 2위 centrehalf/Defend) · 보유 1위 dm_dlp/Defend .863 · dlp/Build-Up .673(보유 .762) | 고메스 1위 **dlp/Roaming .807**(Δ.206) · 보유 dlp/Roaming .855 · 정본 holding/Defend **.437** · dlp/Build-Up .601(보유 .685) | **갈림** — 카마라(37% 수비 경기)는 정본 쪽, 고메스(51%)는 DLP 쪽. 보유 그리드는 두 경기 모두 **DLP 계열 1위** | ⭐ 인게임 테스트 obs#1149 카마라 RDM DLP/Build-Up 「좋았다 — 유지」(사용자 · 10-29) — 보유 그리드 방향과 일치. 단 실측 1위 포커스는 Build-Up이 아니다(Defend/Roaming) · 실측 |
| ⑵ | **ST 포커스** Support vs Attack | st_advanced/Support | 잭슨 advanced/Support **.375** vs Attack .267 · 보유 1위 false9/Attack .436 | 마조 advanced/Support **.351** vs Attack .332(Δ.019) · 보유 Support .348 vs Attack .343 | **Support 2/2 — 단 둘 다 fit <.40 무결정 구간** | ST 커널 적합이 구조적으로 낮다(리서치 §1.2 「전부 .65 이하」와 같은 현상) · 실측은 Support 쪽 근소 · 인게임 Attack 유지 여부는 사용자 판단 · EA #11 Triggered Runs 거리 제한(A) |
| ⑶ | **LM 역할·포커스** | wm_insidefwd/Balanced | 만잠비 1위 widemid/Defend .538(Δ.007) · **보유 1위 insidefwd/Balanced .741** · 정본 .504 | 헤밍스 1위 **widemid/Support .723**(Δ.060) · 정본 insidefwd/Balanced **.369** · winger/Attack .563 | **선수 따라 갈림** — 만잠비(안쪽 프리롤)는 보유 기준 정본 일치, 헤밍스(폭)는 정본과 정반대 | 루게리 복귀 병기: **루게리 여전히 부상(두어 달 · AVR 프리뷰)** → LM 칸 대체 자원 표본만 쌓임 · 인게임 포커스 Attack(10-22)과 정본 Balanced 괴리는 그대로 · 실측 |
| ⑷ | **LB 저점유 프리셋 운용** | fb_att_wb/Support(인게임 Wingback/Balanced) | 마첸 1위 **fb_wingback/Balanced .869**(Δ.069) · 정본 .687 | 마첸 1위 fullback/Balanced .756(Δ.036 무결정) · **보유 1위 wingback/Balanced .799** · 정본 .672(보유 .786) | **wingback/Balanced 2/2(보유 기준)** — 정본 att_wb/Support는 두 경기 모두 2위 이하 | 점유 37%·51% 두 경기 모두 같은 방향 → 「저점유 전용」이 아니라 점유와 무관하게 wingback/Balanced(인게임 값) 쪽 · 실측 |
| ⑸ | **FC27 optimal:lead 신설** | 없음(#46 optimal만) | 리드 76분(6–52′ · 60–90′) · 리드 구간 def_x 31.8~32.2(6–30′) · **20.4(60–66′)** · PPDA 경기 8.55 | 리드 **0분**(7′부터 열세) — 표본 없음 | **판정 불가 — 리드 표본 1경기** | 맨시티 1경기는 「리드 시 블록을 20~32로 더 내린다」 방향 · 2경기 조건을 리드 국면 기준으로 다시 세면 아직 1/2 · 실측 |

⇒ **사용자 판단 요청 목록**(종료 보고에 올림): ⑴ RDM 정본을 dm_dlp 계열로 바꿀지(인게임 테스트 + 보유 그리드 2/2 · 포커스는 Build-Up vs Roaming 미정) ⑵ ST 인게임 Attack 유지 vs 정본 Support 맞춤 ⑶ LM은 선수별 갈림이라 정본 유지 + 헤밍스 쟁점 신설 여부 ⑷ LB 정본을 wingback/Balanced로 정렬할지 ⑸ lead 프리셋은 리드 경기 1개 더 필요.

## D+1 추적

- 예약 `mw-avl-bournemouth-collect-1330`(10-29 13:30 보강 · 이 PC) — 이 파일에 「D+1 보강」 절로 덧붙인다. 대상: The Villans 경기 후 영상 · Tanswell 기사/X(로그인 없이 보이는 범위) · BBC·Birmingham Mail · 만잠비 제외 사유 · 카메룬 매체(마조) · 전술 블로그.

## D+2 추적

- 예약 `mw-avl-bournemouth-d2`(10-30 20:00) — 지연 전술 분석(TFA·BTL·Spielverlagerung) · 상대 관점(본머스 팬 채널 · Daily Echo) · 1874 먼데이 리뷰류 · 당일 판정 정정 여부.

## D+3 추적

- 예약 `mw-avl-bournemouth-d3`(10-31 20:00) — 3일 추적 종결 · 풀럼전(10-31) 명단으로 가르나초·만잠비·고레츠카 서열 재확인 · complete 판정.

## D+1 보강 (2026-10-29 13:30)

> 예약 `mw-avl-bournemouth-collect-1330` · 분기 = **D+1 보강**(리포트·`match_reports` #64 존재 확인) · 경기 후 약 9시간 시점. 당일 절은 고치지 않고 정정은 아래 「당일 판정 정정」에 적는다.

### ⑴ 감독 회견 — 09:30 이후 새 전문 0 · 기존 인용 보충 1
- **에메리**: 새 회견 전사·영상 **0**. Tanswell X(22:2x) 긍정 명단 인용의 **뒷문장**을 직접 열람으로 보충 — 「We need players, we are playing a lot of matches and we need them.」(선수가 필요하다. 경기가 아주 많고 그들이 필요하다) → 컵 기용 사유가 「서열 시험」보다 **경기 수 대비 자원 확보**라는 당일 해석(§요약 E&S/PA 인용)과 같은 방향.
- **에메리 — Sky/E&S 검색 요약 경유(원문 미열람 · E&S·Shropshire Star 403)**: 「We played the idea we set out on so I can't tell nothing to the players, they tried so we move on.」(계획한 아이디어대로 했으니 선수들에게 할 말이 없다. 시도했으니 넘어간다) · 「We are out. I have to accept.」(탈락했다. 받아들여야 한다) — ⚠️ 검색 요약 경유라 confidence 중(1차 원문 재확인 D+2).
- **마르코 로제(본머스)**: Sky(검색 요약 경유 · 기사 미열람) 「We had eight changes today, and everyone played on a really good level. We are relentless, so it's the attitude and the effort.」(오늘 8명을 바꿨는데 모두 정말 좋은 수준으로 뛰었다. 우리는 끈질기다. 태도와 노력이다) · 「We are unpredictable in this stuff.」(이런 면에서 우리는 예측하기 어렵다 — 득점자 분산) — 빌라 구조를 짚은 대목 **여전히 0**. afcb.co.uk 회견 전문 검색 0.
- **스페인어(에메리 모국어 · 필수)**: EFE 전재(Infobae·Proceso·ABC Color·Unitel 10-28) 「Emery no da con la tecla en esta competición y otro año más se queda sin alcanzar los cuartos de final」(에메리는 이 대회에서 해법을 찾지 못하고 올해도 8강에 오르지 못했다) — 결과 기사, **에메리 스페인어 발언 0**. OKDiario 「el Aston Villa de Emery no fue rival para un Bournemouth」(에메리의 빌라는 본머스의 상대가 되지 못했다 · 스니펫 · 403). 검색어: 「Emery Bournemouth Copa de la Liga eliminado declaraciones」 · 「Emery "Copa de la Liga" Goretzka Madjo intensidad」.

### ⑵ Jacob Tanswell X — 추가분 0
- 브라우저 직접 열람(로그아웃 · 13:3x KST): 고정 1 + 경기 관련 4건(21:23 실바 · FT 총평 · 긍정 명단 · 탈압박 계획) — **09:30 회차와 같은 4건, 새 게시 0**. The Athletic 본문(유료벽) 검색 0.

### ⑶ 필수 채널 3곳 — 새 경기 영상 0 (G17 대상 없음)
| 채널 | 09:30 이후 새 업로드 | 판단 |
|---|---|---|
| UTV(@UTVFANCHANNEL) | videos·streams 탭 0 | 리액션 #457 기수집 |
| The Villans(@TheViIIans) | **경기 후 업로드 여전히 0**(최신 = 프리뷰 5xoiziTaf8o #399 기수집) | D+2에 재확인 |
| 1874(@The1874Podcast) | ZKAIfnEpyJ8 「Dan Bardell at talkSPORT…」(10-28 · 13:36) | **건너뜀** — 설명란 「discuss Aston Villa's win over Manchester City and Manchester United being linked with Unai Emery」(맨시티전 승리와 맨유-에메리 연결설을 다룬다) · 본머스전 아님(§2-1a 경기 한정) |
- 확인 방법: `yt-dlp --flat-playlist`(목록·설명란만 · 재생 없음 → 뮤트 해당 없음).

### ⑷ 다국어 기사 — 새 자료 3건
- **The False 9(Kabir Anand · 10-28 20:11 갱신 · 직접 열람) 「Rose's Press, Wide Overloads and a Fifth Straight Win」** — 전술 분석 형식이나 구체 수치는 경기 기본 지표뿐(등급 D 상당 · 지역지 아님):
  - 「Villa's midfielders received the ball facing their own goal」(빌라 미드필더들은 자기 골문을 향한 채 볼을 받았다) · 「loose passes in the middle third became Bournemouth attacks rather than clearances」(중앙 3분의 1 지역의 느슨한 패스가 걷어내기가 아니라 본머스 공격이 됐다) → 영상 주장 #52(압박 하 중앙 턴오버 · HELD)와 같은 방향.
  - 「Villa's right side had to defend the winger, the overlapping full-back and the late runner at the same time」(빌라 오른쪽은 윙어·오버래핑 풀백·늦게 들어오는 러너를 동시에 막아야 했다) → 사용자 메모 H2(실점 2/3 빌라 오른쪽 마무리 · 부분 일치)와 같은 방향 · 보가르드 RB 노출.
  - 부엔디아 「couldn't find space between Bournemouth's midfield and defence … because Christie and Cook rarely gave him a yard to turn in」(본머스 미드필드와 수비 사이에서 공간을 찾지 못했다 — 크리스티·쿡이 돌아설 틈을 거의 주지 않았다).
  - 마조 「his clearest chance, a run in behind in the first half, was smothered by Michele Di Gregorio」(가장 확실한 찬스였던 전반 배후 침투를 디 그레고리오가 몸으로 막았다) — ⚠️ **실측과 충돌**: 전반 마조 유효 슈팅은 29′ **부엔디아 슈팅 리바운드**(SS·E&S 「a mis-hit Emi Buendia shot almost became the perfect assist」(빗나간 부엔디아 슈팅이 완벽한 도움이 될 뻔했다 · E&S 검색 요약 경유))이고 빅찬스는 72′. 실측 채택(불변규칙 3) — #80 「침투」 근거로 세지 않는다.
- **Aston Villa News(Jacob Raw · 10-28 21:51 · 직접)** 보스로이드 비판 반박 기사 — 고레츠카와 고메스는 「were arguably two of Villa's better players against Bournemouth」(본머스전 빌라에서 가장 나은 두 선수였다고 할 만하다) · 「boasting an impressive 97 per cent passing accuracy」(패스 성공률 97%) · 「completing the joint-most dribbles in the match (2)」(경기 최다 타이 드리블 2회) · 「he needs to build his fitness up」(체력을 끌어올려야 한다) · 해당 헤더는 xG 0.03이라 빅찬스 실패가 아니라는 주장(실측 xG 0.03과 일치).
- **zamin.uz(프랑스어 · 10-28)** 「Nuit de sensations en Angleterre : Aston Villa balayé」(잉글랜드의 이변의 밤: 아스톤 빌라 완패) — 결과·라인업만. ⚠️ 음바예 교체 투입자를 가르나초로 적음 — SS incidents는 **58′ 알리송 ↔ 음바예 · 가르나초 ↔ 헤밍스**(실측 채택).
- 0건(검색어 기록): BBC·Birmingham Mail 경기 기사 재검색 0 · The Athletic(Tanswell) 0 · afcb.co.uk 로제 회견 전문 0.

### ⑸ 09:30 회차 결손 점검 — 결손 0
- `gates.py` 전항 통과(13:3x · G21 필수 3종·G23 국면 분·G37 가설/흐름/요약 포함) · `match_player_reports` #64 16행 전부 4열 채움 · `player_matches` 16행 국면 그리드·운반 적재 확인. 채울 빈칸 없음.

### ⭐ 중점 5인 — D+1 추가분
| 선수 | 새 언급(원문+번역) | 모국어·출신 리그 매체 | 쟁점 진행도(`claim_issues` 13:3x 실측) |
|---|---|---|---|
| **마조** | The False 9 「Brian Madjo, the 17-year-old striker leading the line, was booked for diving」(최전방을 맡은 17세 스트라이커 마조는 다이빙으로 경고를 받았다) · 배후 침투 서술은 실측과 충돌(위 ⑷) · E&S 「Madjo couldn't react in time」(마조는 제때 반응하지 못했다 · 29′ 리바운드 · 검색 요약) | ⚠️ **국적 정정**: 당일 절 「카메룬」은 오기 — DB `players.nationality` = **Luxembourg**(A대표 3경기 · 잉글랜드 U17 · 엔필드 출생 · 라싱 룩셈부르크 → 메스). 룩셈부르크 매체(L'essentiel·Luxemburger Wort·RTL) 검색 **0** · 카메룬(Camfoot) 검색 0 · 메스(Républicain Lorrain) 09:30 0 | **#80 0/2** — 이 경기 pos_class LAM이라 세지지 않음(당일 예상대로) |
| **고레츠카** | Aston Villa News 「two of Villa's better players」(빌라에서 가장 나은 두 선수 중 하나) · 「needs to build his fitness up」(체력을 끌어올려야 한다) · The False 9 「headed a free header wide in first-half stoppage time」(전반 추가시간 노마크 헤더를 빗나가게 했다) | 독일어 재검색(「Goretzka Aston Villa Bournemouth Pokal Aus Startelf Kritik」) — Sport1 기수집 외 **0**(headtopics 「Startelfdebüt für Leon Goretzka」(고레츠카 선발 데뷔)는 Sport1 재게시) | **#25 1/2** — ⚠️ 당일 「2/2 판정할 차례」는 **정정**(아래) |
| **하우드-벨리스** | 새 언급 0(The False 9·Villa News 모두 이름 없음) | 영어 지역지(Echo·MEN) 0 | **#24 0/2**(10-29 연장 후 재시작) · **#58 0/2**(PL 표본 — 컵이라 미산입) |
| **음바예** | 새 언급 0 · zamin.uz 교체 오기(위) | 프랑스어·세네갈 재검색(「Ibrahim Mbaye Aston Villa Bournemouth Coupe de la Ligue éliminé」) — Wiwsport 기수집 외 0 | **#6 2/3 · #7 1/2 · #48 1/2** — ⚠️ 당일 「이 경기로 찬다」는 **정정**(아래) |
| **헤밍스** | 새 언급 0 | 영어 지역지 0 | 대응 쟁점 없음 — 새 쟁점 후보(LM 폭 유지 vs 정본 인사이드 포워드) 그대로 · 사용자 판단 |

### 당일 판정 정정
- **쟁점 진행도**: 당일 절은 #25 「2/2 판정할 차례」, #6·#7·#48 「이 경기로 트리거가 찬다」고 적었으나 `claim_issues.py --due` 실측은 **#25 1/2 · #6 2/3 · #7 1/2 · #48 1/2 — AVL 판정할 차례 0**(목록 12건은 전부 보류 팀 CHE·LIV·ATM). 다음 음바예·고레츠카 선발 1경기(풀럼 10-31 또는 바르사 11-03)로 #25·#7·#48이 찬다. 당일 「판정은 아래 절」 표기는 무효.
- **마조 국적**: 카메룬 → 룩셈부르크(DB 정본 · 위 표). 예약 지시의 「카메룬」 모국어 매체 축은 **룩셈부르크(프랑스어·독일어·룩셈부르크어) + 메스(프랑스)**로 바꿔 훑었다.

### 보류 5건 재판정 표
- 리포트 끝에 이미 있음(09:30 회차 · obs#1123 형식) → 다시 붙이지 않았다. 정본·인게임 코드 변경 없음 — 사용자 판단 대기 그대로.

### D+2로 넘김
- The Villans 경기 후 영상 · E&S 에메리 회견 원문(403 → 다른 경로) · 전술 블로그(TFA·BTL·Spielverlagerung·Coaches' Voice) · 본머스 관점(Daily Echo·팬 채널) · 룩셈부르크 매체 재시도.

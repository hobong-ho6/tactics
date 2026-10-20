#!/usr/bin/env python3
"""영상 종류 판정 회귀 시험 (2026-10-20 · 「감독 회견 7편이 실제로는 팬 반응 영상」 사고).

    .venv/bin/python scripts/test_index_kind.py      # 실패하면 exit 1

index_transcripts.guess_kind의 「감독회견」 패턴을 넓히거나 좁힐 때 반드시 돌린다 —
실제로 오분류됐던 제목과, 그걸 고치다 거꾸로 깨졌던 제목(공식 채널 감독 Reaction)을 함께 고정한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from index_transcripts import guess_kind, resolve_kind  # noqa: E402

CASES = [  # (제목, 채널, 기대)
    ("Toothless Performance | Newcastle United 0-1 Aston Villa | Match Reaction", "GallowgateShots - NUFC", "경기반응"),
    ("Match Reaction | Newcastle 0 - 1 Aston Villa | Manzambi Dagger", "Penno | Aston Villa", "경기반응"),
    ("JOAO GOMES UPDATE | UNAI EMERY PRESS CONFERENCE REACTION", "UTV | Aston Villa Fan Channel", "경기반응"),
    ("POST-MATCH LIVE | With Alan McInally, Ian Taylor and Ross Barkley", "Aston Villa Football Club", "경기반응"),
    ("Alonso Press Conference | 16/10/26", "Chelsea Football Club", "감독회견"),
    ("SIMEONE rueda de prensa completa tras el ATLÉTICO", "Diario AS", "감독회견"),
    ("Pressekonferenz nach LASK - FC Liverpool", "LASKOfficial", "감독회견"),
    ("Oliver Glasner's Reaction", "NFFC 공식", "감독회견"),
    ("Iraola's Reaction: Anfield atmosphere, Barcola fitness", "Liverpool FC", "감독회견"),
    ("\"FANTASTIC NIGHT!\" | Unai Emery on 6-0 win against Fenerbahçe", "Aston Villa Football Club", "감독회견"),
    ("FENERBAHÇE 0 – 6 ASTON VILLA | MAÇ ANLATIMI VE TAKTİK ANALİZ", "Dr. Hikmet Taflan", "전술분석"),
]

# 채널 기본값·스코어 기본값까지 포함한 정본 판정(2026-10-20 「미분류 18편」 회귀)
CASES_R = [
    ("Newcastle United Are NOT Playing to Their Strengths!  Jaissle vs Aston Villa", "Two For Joy", "상대팀"),
    ("BOOS For Jaissle’s EXPOSED Mags! Newcastle 0-1 Aston Villa", "The Magpie Channel TV", "상대팀"),
    ("Why Jaissle Is Getting Newcastle’s Tactics WRONG", "A Game Of Two Halves", "전술분석"),
    ("How Unai Emery OUTSMARTED Newcastle", "Bains Analysis", "전술분석"),
    ("CANNOT be so EASY! | Matthias Jaissle | Newcastle United 0-1 Aston Villa", "HaytersTV", "감독회견"),
    ("THE WARM DOWN | MANZAMBI THE HERO! NEWCASTLE 0–1 ASTON VILLA", "Justin Talks Villa ", "경기반응"),
    ("Takeaways from Aston Villa's victory over Newcastle | Premier League", "NBC Sports", "경기반응"),
    ("🚨 \"HE NEARLY BROKE MY LEG!\" Nicolas Jackson SLAMS Botman Tackle! | Newcastle 0-1", "Show de Bola", "경기반응"),
    ("Toothless Performance | Newcastle United 0-1 Aston Villa | Match Reaction", "GallowgateShots - NUFC", "상대팀"),
    # UTV 분석 영상(2026-10-20 채널 스윕)
    ("UNAI EMERY FACES TACTICAL CONUNDRUM AGAINST BRENTFORD", "UTV | Aston Villa Fan Channel", "전술분석"),
    ("THE BEST ASTON VILLA XI WE HAVEN'T SEEN YET", "UTV | Aston Villa Fan Channel", "전술분석"),
    ("HOW DOES UNAI EMERY KEEP DOING THIS?", "UTV | Aston Villa Fan Channel", "전술분석"),
    ("HOW ZION SUZUKI IS TRANSFORMING ASTON VILLA", "UTV | Aston Villa Fan Channel", "선수스카우팅"),
    ("HOW ZION SUZUKI IS CHEAT CODE FOR ASTON VILLA", "UTV | Aston Villa Fan Channel", "선수스카우팅"),
    ("THE DATA SAYS ASTON VILLA MUST SIGN?", "UTV | Aston Villa Fan Channel", "선수스카우팅"),
    ("RATING ASTON VILLA'S NEW SIGNINGS ON PERFORMANCE", "UTV | Aston Villa Fan Channel", "선수스카우팅"),
    ("SOME OF THIS DOESN'T MAKE SENSE! | ASTON VILLA 2-2 BRENTFORD", "UTV | Aston Villa Fan Channel", "경기반응"),
]
bad = [(t, c, e, guess_kind(t, channel=c)) for t, c, e in CASES if guess_kind(t, channel=c) != e]
bad += [(t, c, e, resolve_kind(t, None, c)) for t, c, e in CASES_R if resolve_kind(t, None, c) != e]
CASES = CASES + CASES_R
for t, c, e, got in bad:
    print(f"❌ {t[:60]} ({c}) — 기대 {e} · 실제 {got}")
print(f"{'✅' if not bad else '⛔'} 영상 종류 판정 {len(CASES) - len(bad)}/{len(CASES)}")
sys.exit(1 if bad else 0)

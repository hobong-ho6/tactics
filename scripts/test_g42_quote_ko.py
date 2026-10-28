#!/usr/bin/env python3
"""G42(외국어 인용 한국어 병기)·G14 번역 삽입 허용 회귀 테스트 — 판정은 core/quote_ko.py 정본을 import한다.
사용: python3 scripts/test_g42_quote_ko.py   종료 코드 0=통과.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.quote_ko import missing, only_translation_inserts  # noqa: E402

FAIL = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAIL.append(name)


print("검출")
check("번역 없는 영어 인용 적발", len(missing("에메리 「It was my decision」 — 전술 판단이 아니다")) == 1)
check("일본어 인용 적발", len(missing("「鈴木彩艶がロングキックを蹴った」로 적었다")) == 1)
check("바로 뒤 괄호 번역은 통과", not missing("「It was my decision」(내 결정이었다)"))
check("— 「한국어」 번역은 통과", not missing("「Marco felt pain in his back」 — 「마르코가 등에 통증을 느꼈다」"))
check("한국어 인용은 대상 아님", not missing("「비보유 RB → 보유 중원」 구조"))
check("단어 하나(고유명)는 대상 아님", not missing("「Alysson」 표기"))
check("한글 없는 괄호(출처)는 번역 아님", len(missing("「we lost our shape」(obs#638)")) == 1)

print("G14 번역 삽입 허용")
old = "에메리 「It was my decision」 — 판단. 「so much cadeaus」 끝"
check("「」 뒤 한글 괄호 삽입만 → 허용",
      only_translation_inserts(old, old.replace("decision」", "decision」(내 결정이었다)")
                                       .replace("cadeaus」", "cadeaus」(선물을 너무 많이 줬다)")))
check("다른 곳 수정이 섞이면 → 불허",
      not only_translation_inserts(old, old.replace("decision」", "decision」(내 결정)").replace("끝", "끝!")))
check("한글 없는 괄호 삽입 → 불허", not only_translation_inserts(old, old.replace("decision」", "decision」(x)")))
check("「」 아닌 자리 삽입 → 불허", not only_translation_inserts(old, old.replace("판단.", "판단(가).")))

check("기존 번역 삭제 → 불허", not only_translation_inserts("「a b」(가나) 끝", "「a b」 끝"))
check("기존 괄호 앞에 새 번역 삽입 → 허용", only_translation_inserts("「a b」(obs#1) 끝", "「a b」(가 나)(obs#1) 끝"))
check("삽입 괄호와 같은 글자로 이어지는 본문 → 허용", only_translation_inserts("「a b」(번역 아님 x", "「a b」(번역)(번역 아님 x"))

print("✅ 전항 통과" if not FAIL else f"❌ 실패 {FAIL}")
sys.exit(1 if FAIL else 0)

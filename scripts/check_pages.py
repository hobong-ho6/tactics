#!/usr/bin/env python3
"""화면 회귀 검사 — 렌더·콘솔 오류·텍스트 덤프를 **한 번의 셸 호출**로 끝낸다.

왜 (2026-09-23 사용자 지시 「코드레벨이나 스크립트로 수행할 수 있는 것들은 전환해줘 —
더 이상 반복적인 실수가 일어나지 않고 토큰도 줄이도록」):
  화면을 고칠 때마다 세션이 **임시 Playwright 스크립트를 다시 짜고 있었다**(2026-09-23 한 세션에서만 4번).
  매번 같은 코드를 쓰는 데 컨텍스트가 들고, 그 컨텍스트는 이후 모든 툴 왕복에 다시 실려 나간다.
  ⇒ 저장소에 고정해 **한 줄로 부른다.** 출력은 사람이 읽을 요약뿐이라 대화 비용이 거의 없다.

⛔ 브라우저 MCP로 같은 일을 하지 말 것 — 화면 하나당 왕복이 3~5회다. 여기는 1회다.
⚠️ 서버는 `.claude/launch.json`의 `heatmap`(8123)이 떠 있어야 한다. 미러는 `scripts/export.py`가 갱신한다.

사용:
    python3 scripts/check_pages.py                      # 전 페이지 — 렌더 길이·콘솔 오류·HTTP 4xx
    python3 scripts/check_pages.py evolutions.html --tab paths          # 그 탭의 본문 텍스트
    python3 scripts/check_pages.py player.html --q 59 --click "게임 스탯"
    python3 scripts/check_pages.py evolutions.html --tab cat --grep "적용 가능"
    python3 scripts/check_pages.py --team CHE           # 팀을 바꿔서 전수
"""
import argparse
import asyncio
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "heatmap.html", "match-report.html", "squad.html", "compare.html",
         "transfer.html", "report.html", "player.html", "evolutions.html", "game.html", "manual.html"]
# FC25는 커널도 시스템 사실도 없어 파일을 만들지 않는다(core/export.py) — game.html이 catch로 넘긴다.
KNOWN_404 = ("kernels/FC25.json",)


async def visit(ctx, url, *, tab=None, click=None, wait=2500):
    pg = await ctx.new_page()
    errs, bad_http = [], []
    pg.on("pageerror", lambda e: errs.append(f"PAGEERROR {e}"[:300]))
    # ⚠️ 리소스 404는 콘솔에 **URL 없이** 찍힌다 — 그대로 모으면 알려진 404(FC25)를 거를 수 없다.
    #    그 줄은 버리고 아래 response 이벤트(URL이 있다)로만 판정한다.
    pg.on("console", lambda m: errs.append(f"[{m.type}] {m.text}"[:220])
          if m.type == "error" and "Failed to load resource" not in m.text else None)
    pg.on("response", lambda r: bad_http.append(f"{r.status} {r.url.split('?')[0]}")
          if r.status >= 400 and not any(k in r.url for k in KNOWN_404) else None)
    try:
        await pg.goto(url, wait_until="domcontentloaded", timeout=30000)
        await pg.wait_for_timeout(wait)
        if tab:
            await pg.click(f'[data-tab="{tab}"]', timeout=5000)
            await pg.wait_for_timeout(1500)
        if click:
            await pg.get_by_text(click, exact=True).first.click(timeout=5000)
            await pg.wait_for_timeout(1500)
    except Exception as e:
        errs.append(f"NAV {e}"[:200])
    text = await pg.evaluate("document.body.innerText")
    await pg.close()
    return text, list(dict.fromkeys(errs)), list(dict.fromkeys(bad_http))


async def main(a):
    from playwright.async_api import async_playwright
    base = f"http://127.0.0.1:{a.port}/site/"
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context()
        await ctx.add_init_script(f"localStorage.setItem('tactics_team','{a.team}')")
        bad = 0
        if a.page:
            url = base + a.page + (f"?id={a.q}" if a.q else "")
            text, errs, http = await visit(ctx, url, tab=a.tab, click=a.click)
            if a.grep:
                rx = re.compile(a.grep)
                text = "\n".join(l for l in text.split("\n") if rx.search(l))
            print(text[:a.max_chars])
            for e in errs:
                print("  ⛔", e); bad += 1
            for h in http:
                print("  ⛔ HTTP", h); bad += 1
        else:
            for name in PAGES:
                text, errs, http = await visit(ctx, base + name)
                # ⚠️ 렌더 길이는 **회귀 감지용 지표**다 — 갑자기 짧아지면 렌더가 죽은 것이다.
                flag = "⛔" if (errs or http or len(text) < 300) else "✅"
                print(f"{flag} {name:22} {len(text):>6}자")
                for e in errs:
                    print("     ", e); bad += 1
                for h in http:
                    print("      HTTP", h); bad += 1
                if len(text) < 300:
                    bad += 1
        await b.close()
    print(("⛔ 문제 %d건" % bad) if bad else "✅ 이상 없음")
    return 1 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", help="site/ 아래 파일명. 생략하면 전 페이지 렌더 검사")
    ap.add_argument("--tab", help='탭 전환: [data-tab="<값>"] 을 누른다 (evolutions.html: now/club/chem/cat/paths/tactic)')
    ap.add_argument("--click", help="정확히 일치하는 텍스트를 눌러 탭/토글을 연다 (player.html: 「게임 스탯」 등)")
    ap.add_argument("--q", help="쿼리스트링 id= 값 (player.html 선수 id)")
    ap.add_argument("--grep", help="본문에서 이 정규식에 걸리는 줄만 출력")
    ap.add_argument("--team", default="AVL", help="localStorage tactics_team (기본 AVL)")
    ap.add_argument("--port", default="8123")
    ap.add_argument("--max-chars", type=int, default=6000)
    a = ap.parse_args()
    venv = ROOT / ".venv" / "bin" / "python"
    try:
        import playwright  # noqa: F401
    except ImportError:
        if venv.exists() and Path(sys.executable).resolve() != venv.resolve():
            # ⭐ playwright는 .venv에만 있다 — 사용자가 `python3`로 불러도 알아서 넘긴다(런북 삽질 방지).
            sys.exit(subprocess.run([str(venv), __file__, *sys.argv[1:]]).returncode)
        sys.exit("⛔ playwright 없음 — .venv/bin/python 으로 실행할 것")
    sys.exit(asyncio.run(main(a)))

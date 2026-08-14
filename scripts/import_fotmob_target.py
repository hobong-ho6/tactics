#!/usr/bin/env python3
"""FotMob 원천 JSON을 영입 후보의 선수 마스터와 상세 스탯 표에 적재한다.

transfer_targets는 이적 확정 전에도 실측·평가를 가질 수 있다. 상세 FotMob 표는
players FK를 쓰므로, 후보를 squad_entries로 승격하지 않고 players에만 연결한다.
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import ROOT


SEASON_LABELS = {
    "goals": ("Goals", "골"),
    "assists": ("Assists", "어시스트"),
    "matches_uppercase": ("Matches", "경기"),
    "player_started_matches": ("Started", "선발"),
    "minutes_played": ("Minutes played", "출전 시간"),
    "rating": ("Rating", "평점"),
    "yellow_cards": ("Yellow cards", "경고"),
    "red_cards": ("Red cards", "퇴장"),
}

TRAIT_KR = {
    "chances_created": "기회 창출",
    "aerials_won": "공중 볼 경합",
    "defensive_actions": "수비적 행동",
    "goals": "득점",
    "shot_attempts": "슛 시도",
    "touches": "터치",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target_id", type=int)
    ap.add_argument("--player-data", type=Path, required=True)
    ap.add_argument("--player-stats", type=Path, required=True)
    ap.add_argument("--season", required=True)
    ap.add_argument("--league", required=True)
    ap.add_argument("--pulled", required=True)
    a = ap.parse_args()

    profile = json.loads(a.player_data.read_text(encoding="utf-8"))
    stats = json.loads(a.player_stats.read_text(encoding="utf-8"))
    source_profile = f"fotmob.com/api/data/playerData (player {profile['id']}, {a.pulled} 수집)"
    source_stats = (
        f"fotmob.com/api/data/playerStats (player {profile['id']}, "
        f"{a.season} {a.league}, {a.pulled} 수집)"
    )

    con = sqlite3.connect(ROOT / "db/tactics.db")
    con.row_factory = sqlite3.Row
    try:
        target = con.execute(
            "SELECT * FROM transfer_targets WHERE id=?", (a.target_id,)
        ).fetchone()
        if not target:
            raise SystemExit(f"transfer_targets id={a.target_id} 없음")
        if profile.get("name") != target["name"]:
            raise SystemExit(
                f"선수명 불일치: target={target['name']} FotMob={profile.get('name')}"
            )

        player = con.execute(
            "SELECT id FROM players WHERE name=?", (target["name"],)
        ).fetchone()
        if player:
            player_id = player["id"]
            con.execute(
                """UPDATE players SET name_kr=COALESCE(name_kr,?),
                       sofascore_id=COALESCE(sofascore_id,?),
                       fotmob_id=?, birth_year=COALESCE(birth_year,?),
                       primary_position=COALESCE(primary_position,?) WHERE id=?""",
                (target["name_kr"], target["sofascore_id"], profile["id"],
                 int(profile["birthDate"]["utcTime"][:4]), target["position"], player_id),
            )
        else:
            cur = con.execute(
                """INSERT INTO players(name,name_kr,sofascore_id,birth_year,
                       primary_position,notes,fotmob_id) VALUES(?,?,?,?,?,?,?)""",
                (target["name"], target["name_kr"], target["sofascore_id"],
                 int(profile["birthDate"]["utcTime"][:4]), target["position"],
                 f"transfer_targets 2026-summer {target['team_code']} 후보 — "
                 f"{a.pulled} FotMob 상세 스탯 수집용 등재", profile["id"]),
            )
            player_id = cur.lastrowid
        con.execute(
            "UPDATE transfer_targets SET player_id=? WHERE id=?", (player_id, a.target_id)
        )

        metric_kr = {
            r["metric_key"]: r["metric_kr"]
            for r in con.execute(
                """SELECT metric_key, MAX(metric_kr) metric_kr
                   FROM fotmob_detail_stats GROUP BY metric_key"""
            )
        }
        detail_items = [
            item
            for section in stats["statsSection"]["items"]
            for item in section["items"]
        ]
        for item in detail_items:
            key = item["localizedTitleId"]
            con.execute(
                """INSERT INTO fotmob_detail_stats(
                       player_id,pulled,season,league,metric_key,metric,metric_kr,
                       stat_value,per90,percentile,percentile_per90,source)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(player_id,season,league,metric_key) DO UPDATE SET
                     pulled=excluded.pulled,metric=excluded.metric,metric_kr=excluded.metric_kr,
                     stat_value=excluded.stat_value,per90=excluded.per90,
                     percentile=excluded.percentile,
                     percentile_per90=excluded.percentile_per90,source=excluded.source""",
                (player_id, a.pulled, a.season, a.league, key, item["title"],
                 metric_kr.get(key), item.get("statValue"), item.get("per90"),
                 round(item["percentileRank"]) if item.get("percentileRank") is not None else None,
                 round(item["percentileRankPer90"]) if item.get("percentileRankPer90") is not None else None,
                 source_stats),
            )

        traits = profile.get("traits") or {}
        for item in traits.get("items", []):
            con.execute(
                """INSERT INTO fotmob_traits(
                       player_id,pulled,pos_group,metric,metric_kr,percentile,source)
                   VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(player_id,metric) DO UPDATE SET
                     pulled=excluded.pulled,pos_group=excluded.pos_group,
                     metric_kr=excluded.metric_kr,percentile=excluded.percentile,
                     source=excluded.source""",
                (player_id, a.pulled, traits.get("title"), item["title"],
                 TRAIT_KR.get(item["key"]), round(item["value"] * 100), source_profile),
            )

        season_items = {item["localizedTitleId"]: item for item in stats["topStatCard"]["items"]}
        for section in stats["statsSection"]["items"]:
            for item in section["items"]:
                if item["localizedTitleId"] in ("yellow_cards", "red_cards"):
                    season_items[item["localizedTitleId"]] = item
        for key, (metric, korean) in SEASON_LABELS.items():
            item = season_items.get(key)
            if not item:
                continue
            con.execute(
                """INSERT INTO fotmob_season_stats(
                       player_id,pulled,league,season,metric,metric_kr,value,source)
                   VALUES(?,?,?,?,?,?,?,?)
                   ON CONFLICT(player_id,league,season,metric) DO UPDATE SET
                     pulled=excluded.pulled,metric_kr=excluded.metric_kr,
                     value=excluded.value,source=excluded.source""",
                (player_id, a.pulled, a.league, a.season, metric, korean,
                 item.get("statValue"), source_stats),
            )

        con.commit()
        print(
            f"player_id={player_id} · 상세 {len(detail_items)}지표 · "
            f"traits {len(traits.get('items', []))}축 · 시즌요약 {len(SEASON_LABELS)}항"
        )
    finally:
        con.close()


if __name__ == "__main__":
    main()

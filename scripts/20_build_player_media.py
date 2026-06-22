"""
Build player_media.json for the web app.

Resolves ESPN headshot URLs and school names from prospect_master.csv.
Run from repo root:
  PYTHONPATH=. python scripts/20_build_player_media.py

Output: web/public/data/player_media.json
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
PROSPECTS = ROOT / "data/processed/prospect_master.csv"
OUT = ROOT / "web/public/data/player_media.json"

SCHOOL_SLUGS = {
    "Alabama": "alabama",
    "Alba Berlin": "alba-berlin",
    "Arizona": "arizona",
    "Arkansas": "arkansas",
    "Auburn": "auburn",
    "BC Oostende": "bc-oostende",
    "BYU": "byu",
    "Baylor": "baylor",
    "Butler": "butler",
    "Cincinnati": "cincinnati",
    "Duke": "duke",
    "Florida": "florida",
    "George Washington": "george-washington",
    "Houston": "houston",
    "Illinois": "illinois",
    "Indiana": "indiana",
    "Iowa": "iowa",
    "Iowa State": "iowa-state",
    "KK Mega Basket": "kk-mega-basket",
    "Kansas": "kansas",
    "Kentucky": "kentucky",
    "Louisville": "louisville",
    "Miami": "miami",
    "Miami (Ohio)": "miami-ohio",
    "Michigan": "michigan",
    "Missouri": "missouri",
    "NC State": "nc-state",
    "New Zealand": "new-zealand",
    "North Carolina": "north-carolina",
    "Northwestern": "northwestern",
    "Ohio State": "ohio-state",
    "Oregon": "oregon",
    "Purdue": "purdue",
    "Santa Clara": "santa-clara",
    "South Florida": "south-florida",
    "Stanford": "stanford",
    "Tennessee": "tennessee",
    "Tennessee State": "tennessee-state",
    "Texas": "texas",
    "Texas Tech": "texas-tech",
    "UCLA": "ucla",
    "UConn": "uconn",
    "Valencia": "valencia",
    "Vanderbilt": "vanderbilt",
    "Virginia": "virginia",
    "Virginia Tech": "virginia-tech",
    "Washington": "washington",
    "Wisconsin": "wisconsin",
}

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "nba-draft-intelligence/1.0 (portfolio project)"})


def slugify(name: str) -> str:
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", name.lower()))


def extract_school(raw_text: str | None) -> str | None:
    if not raw_text or not isinstance(raw_text, str):
        return None
    match = re.search(r"\|\s*([^0-9']+?)\s+\d", raw_text)
    return match.group(1).strip() if match else None


def espn_search(player: str) -> dict | None:
    url = (
        "https://site.web.api.espn.com/apis/common/v3/search"
        f"?query={quote(player)}&limit=5&type=player"
    )
    resp = SESSION.get(url, timeout=20)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    for item in items:
        if item.get("league") != "mens-college-basketball":
            continue
        if item.get("displayName", "").lower() != player.lower():
            # allow close match for suffixes like Jr.
            if player.split()[0].lower() not in item.get("displayName", "").lower():
                continue
        athlete_id = item.get("id")
        if not athlete_id:
            continue
        detail = SESSION.get(
            "https://site.api.espn.com/apis/common/v3/sports/basketball/"
            f"mens-college-basketball/athletes/{athlete_id}",
            timeout=20,
        )
        if detail.status_code != 200:
            continue
        athlete = detail.json().get("athlete", {})
        headshot = (athlete.get("headshot") or {}).get("href")
        team = (athlete.get("team") or {}).get("displayName")
        return {
            "espn_id": str(athlete_id),
            "headshot_url": headshot,
            "espn_team": team,
        }
    return None


def main() -> None:
    df = pd.read_csv(PROSPECTS)
    players = (
        df.loc[df["player"].notna() & (df["player"].astype(str).str.len() > 0), "player"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    rows = []
    for i, player in enumerate(players, start=1):
        subset = df[df["player"] == player]
        school = None
        for raw in subset["raw_text"].dropna():
            school = extract_school(str(raw))
            if school:
                break

        media = {"player": player, "slug": slugify(player), "school": school}
        if school:
            media["school_slug"] = SCHOOL_SLUGS.get(school, slugify(school))

        try:
            espn = espn_search(player)
            if espn:
                media.update(espn)
        except Exception as exc:  # noqa: BLE001
            media["espn_error"] = str(exc)

        rows.append(media)
        print(f"[{i}/{len(players)}] {player} -> {media.get('headshot_url', 'no photo')}")
        time.sleep(0.35)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(rows)} players)")


if __name__ == "__main__":
    main()

"""
NBA.com Draft Combine Scraper via NBA Stats API.

Outputs:
data/raw/nba_combine/combine_anthro.csv
data/raw/nba_combine/combine_strength_agility.csv
data/raw/nba_combine/combine_stats.csv

Run:
PYTHONPATH=src python src/scrapers/nba_combine_scraper.py
"""

from pathlib import Path
import time
import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "nba_combine"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com",
    "Accept": "application/json, text/plain, */*",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}

ENDPOINTS = {
    "combine_stats": "https://stats.nba.com/stats/draftcombinestats",
    "combine_anthro": "https://stats.nba.com/stats/draftcombineplayeranthro",
    "combine_strength_agility": "https://stats.nba.com/stats/draftcombineplayeranthro",  # fallback first
}

PARAMS = {
    "LeagueID": "00",
    "SeasonYear": "2025-26",
}


def nba_stats_get(endpoint: str, params: dict) -> pd.DataFrame:
    r = requests.get(endpoint, headers=HEADERS, params=params, timeout=30)
    print("URL:", r.url)
    print("Status:", r.status_code)
    r.raise_for_status()

    data = r.json()
    result_set = data["resultSets"][0]
    headers = result_set["headers"]
    rows = result_set["rowSet"]

    return pd.DataFrame(rows, columns=headers)


def save_df(df: pd.DataFrame, name: str):
    raw_path = RAW_DIR / f"{name}.csv"
    processed_path = PROCESSED_DIR / f"{name}.csv"

    df.to_csv(raw_path, index=False)
    df.to_csv(processed_path, index=False)

    print(f"Saved {name}: {len(df)} rows")
    print(raw_path)
    print(df.head(10).to_string(index=False))


def main():
    # 1. Combine stats
    try:
        print("\n=== NBA Combine Stats ===")
        df_stats = nba_stats_get(
            "https://stats.nba.com/stats/draftcombinestats",
            PARAMS,
        )
        save_df(df_stats, "combine_stats_2026")
        time.sleep(2)
    except Exception as e:
        print("[ERROR] combine stats failed:", e)

    # 2. Anthro
    try:
        print("\n=== NBA Combine Anthro ===")
        df_anthro = nba_stats_get(
            "https://stats.nba.com/stats/draftcombineplayeranthro",
            PARAMS,
        )
        save_df(df_anthro, "combine_anthro_2026")
        time.sleep(2)
    except Exception as e:
        print("[ERROR] combine anthro failed:", e)

    # 3. Historical years fallback: 2024-25, 2023-24, etc.
    # Useful because 2026 combine data may not exist yet before the event.
    historical_seasons = ["2024-25", "2023-24", "2022-23", "2021-22", "2020-21"]

    all_stats = []
    all_anthro = []

    for season in historical_seasons:
        params = {"LeagueID": "00", "SeasonYear": season}

        try:
            print(f"\n=== Historical Combine Stats {season} ===")
            df = nba_stats_get(
                "https://stats.nba.com/stats/draftcombinestats",
                params,
            )
            df["SEASON_YEAR"] = season
            all_stats.append(df)
            time.sleep(2)
        except Exception as e:
            print(f"[WARN] stats failed {season}: {e}")

        try:
            print(f"\n=== Historical Combine Anthro {season} ===")
            df = nba_stats_get(
                "https://stats.nba.com/stats/draftcombineplayeranthro",
                params,
            )
            df["SEASON_YEAR"] = season
            all_anthro.append(df)
            time.sleep(2)
        except Exception as e:
            print(f"[WARN] anthro failed {season}: {e}")

    if all_stats:
        save_df(pd.concat(all_stats, ignore_index=True), "combine_stats_historical")

    if all_anthro:
        save_df(pd.concat(all_anthro, ignore_index=True), "combine_anthro_historical")


if __name__ == "__main__":
    main()
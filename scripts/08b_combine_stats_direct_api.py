from pathlib import Path
import time
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data/raw/nba_combine"
PROCESSED_DIR = PROJECT_ROOT / "data/processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://stats.nba.com/stats/draftcombinestats"

SEASONS = ["2025-26", "2024-25", "2023-24", "2022-23", "2021-22", "2020-21"]

HEADERS = {
    "Host": "stats.nba.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "x-nba-stats-token": "true",
    "x-nba-stats-origin": "stats",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/stats/draft/combine",
    "Accept-Language": "en-US,en;q=0.9",
}

def session_with_retry():
    s = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.headers.update(HEADERS)
    return s

def fetch_combine_stats(season):
    params = {
        "LeagueID": "00",
        "SeasonYear": season,
    }

    s = session_with_retry()
    print(f"\nFetching combine stats {season}...")
    r = s.get(URL, params=params, timeout=120)
    print("Status:", r.status_code)
    print("URL:", r.url)
    r.raise_for_status()

    data = r.json()
    result = data["resultSets"][0]
    df = pd.DataFrame(result["rowSet"], columns=result["headers"])
    df["SEASON_YEAR"] = season
    return df

def save(df, name):
    raw = RAW_DIR / f"{name}.csv"
    processed = PROCESSED_DIR / f"{name}.csv"
    df.to_csv(raw, index=False)
    df.to_csv(processed, index=False)
    print(f"[OK] {name}: rows={len(df)}")
    print(processed)

def main():
    frames = []

    for season in SEASONS:
        try:
            df = fetch_combine_stats(season)
            print("Rows:", len(df))
            if len(df) > 0:
                frames.append(df)
                if season == "2025-26":
                    save(df, "combine_stats_2026")
            time.sleep(3)
        except Exception as e:
            print(f"[WARN] failed {season}: {e}")

    if frames:
        all_df = pd.concat(frames, ignore_index=True, sort=False)
        save(all_df, "combine_stats_all")
    else:
        raise RuntimeError("No combine stats fetched.")

if __name__ == "__main__":
    main()
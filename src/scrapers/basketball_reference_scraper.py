"""
Basketball Reference NBA Draft Scraper

Goal:
Scrape NBA Draft data from Basketball Reference for 2000-2025.

Source pattern:
https://www.basketball-reference.com/draft/NBA_2025.html

Output:
data/raw/historical_drafts/basketball_reference/draft_2000.csv
...
data/processed/historical_drafts_master.csv

Run:
PYTHONPATH=src python src/scrapers/basketball_reference_scraper.py
"""

from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://www.basketball-reference.com/draft/NBA_{year}.html"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "historical_drafts" / "basketball_reference"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

START_YEAR = 2000
END_YEAR = 2025

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def clean_column_name(col: str) -> str:
    """
    Normalize Basketball Reference column names.
    """
    col = str(col).strip().lower()
    col = col.replace("%", "pct")
    col = col.replace("/", "_")
    col = col.replace("-", "_")
    col = col.replace(" ", "_")
    col = col.replace(".", "")
    return col


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basketball Reference tables sometimes have MultiIndex columns.
    This flattens them into simple names.
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(x) for x in tup if str(x) != "nan"]).strip()
            for tup in df.columns
        ]

    df.columns = [clean_column_name(c) for c in df.columns]
    return df


def build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)
    return session


def fetch_html(year: int) -> str:
    url = BASE_URL.format(year=year)
    session = build_session()

    try:
        response = session.get(url, timeout=45)
        response.raise_for_status()
        return response.text
    except requests.exceptions.SSLError:
        print(f"[WARN] SSL error for {year}, retrying with verify=False...")
        response = session.get(url, timeout=45, verify=False)
        response.raise_for_status()
        return response.text


def parse_draft_table(html: str, year: int) -> pd.DataFrame:
    """
    Parse draft table from Basketball Reference HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "stats"})

    if table is None:
        raise RuntimeError(f"No draft table found for year {year}")

    df = pd.read_html(str(table))[0]
    df = flatten_columns(df)

    # Remove repeated header rows inside the table
    if "rk" in df.columns:
        df = df[df["rk"] != "Rk"]

    df.insert(0, "year", year)

    return df.reset_index(drop=True)


def standardize_draft_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize common Basketball Reference draft columns.

    Basketball Reference column names may change slightly,
    so we keep all original fields but create normalized core columns.
    """
    rename_map = {
        "pk": "pick",
        "tm": "team",
        "player": "player",
        "college": "college",
        "years": "career_years",
        "g": "career_games",
        "mp": "career_minutes",
        "pts": "career_points",
        "trb": "career_rebounds",
        "ast": "career_assists",
        "fgpct": "fg_pct",
        "3ppct": "three_pt_pct",
        "ftpct": "ft_pct",
        "mpg": "mpg",
        "ppg": "ppg",
        "trbpg": "rpg",
        "astpg": "apg",
        "ws": "win_shares",
        "ws_48": "ws_per_48",
        "bpm": "bpm",
        "vorp": "vorp",
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    numeric_cols = [
        "year",
        "pick",
        "career_years",
        "career_games",
        "career_minutes",
        "career_points",
        "career_rebounds",
        "career_assists",
        "fg_pct",
        "three_pt_pct",
        "ft_pct",
        "mpg",
        "ppg",
        "rpg",
        "apg",
        "win_shares",
        "ws_per_48",
        "bpm",
        "vorp",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "pick" in df.columns:
        df = df.dropna(subset=["pick"])
        df["pick"] = df["pick"].astype(int)

    if "team" in df.columns:
        df["team"] = df["team"].astype(str).str.strip()

    if "player" in df.columns:
        df["player"] = df["player"].astype(str).str.strip()

    if "college" in df.columns:
        df["college"] = df["college"].astype(str).str.strip()

    return df


def scrape_one_year(
    year: int, sleep_seconds: float = 2.5, force: bool = False
) -> pd.DataFrame:
    """
    Scrape and save one draft year. Skips fetch if raw CSV already exists unless force=True.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / f"draft_{year}.csv"

    if output_path.exists() and not force:
        print(f"Skipping {year} (already exists: {output_path})")
        return pd.read_csv(output_path)

    print(f"Scraping NBA Draft {year}...")

    html = fetch_html(year)
    df = parse_draft_table(html, year)
    df = standardize_draft_df(df)
    df.to_csv(output_path, index=False)

    print(f"Saved {output_path} | rows={len(df)}")

    time.sleep(sleep_seconds)
    return df


def build_master_from_raw() -> pd.DataFrame:
    """
    Combine all per-year raw CSVs into one master dataframe.
    """
    files = sorted(RAW_DIR.glob("draft_*.csv"))
    if not files:
        raise RuntimeError(f"No draft CSVs found in {RAW_DIR}")

    dfs = [pd.read_csv(f) for f in files]
    master = pd.concat(dfs, ignore_index=True, sort=False)
    return standardize_draft_df(master)


def scrape_year_range(
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
    force: bool = False,
) -> pd.DataFrame:
    """
    Scrape a year range and rebuild master from all available raw CSVs.
    """
    for year in range(start_year, end_year + 1):
        try:
            scrape_one_year(year, force=force)
        except Exception as e:
            print(f"[ERROR] {year}: {e}")

    master = build_master_from_raw()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    master_path = PROCESSED_DIR / "historical_drafts_master.csv"
    master.to_csv(master_path, index=False)

    print("\nDone.")
    print(f"Master file saved to: {master_path}")
    print(f"Total rows: {len(master)}")

    return master


if __name__ == "__main__":
    scrape_year_range(2000, 2025)
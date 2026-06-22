"""
Tankathon NBA Draft Scraper

Targets:
1. Big Board:
   https://www.tankathon.com/big_board

2. Mock Draft:
   https://www.tankathon.com/mock_draft

Outputs:
data/raw/tankathon/big_board_raw.csv
data/raw/tankathon/mock_draft_raw.csv

data/processed/prospects_2026_tankathon.csv
data/processed/mock_draft_2026_tankathon.csv

Run:
PYTHONPATH=src python src/scrapers/tankathon_scraper.py
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "tankathon"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

BIG_BOARD_URL = "https://www.tankathon.com/big_board"
MOCK_DRAFT_URL = "https://www.tankathon.com/mock_draft"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_html(url: str, sleep_seconds: float = 2.0) -> str:
    print(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    time.sleep(sleep_seconds)
    return response.text


def clean_text(x: Optional[str]) -> Optional[str]:
    if x is None:
        return None
    x = re.sub(r"\s+", " ", str(x)).strip()
    return x if x else None


def height_to_inches(height: Optional[str]) -> Optional[float]:
    """
    Convert height like 6'8" or 6-8 into inches.
    """
    if not height:
        return None

    text = str(height).strip()

    match = re.search(r"(\d+)\s*['-]\s*(\d+)", text)
    if not match:
        return None

    feet = int(match.group(1))
    inches = int(match.group(2))
    return feet * 12 + inches


def parse_weight(weight: Optional[str]) -> Optional[float]:
    if not weight:
        return None

    match = re.search(r"(\d+)", str(weight))
    if not match:
        return None

    return float(match.group(1))


def parse_big_board(html: str) -> pd.DataFrame:
    """
    Tankathon pages are not always traditional tables.
    This parser uses broad CSS/text extraction and then normalizes.
    """
    soup = BeautifulSoup(html, "html.parser")

    rows = []

    # Tankathon often uses div-based cards/rows.
    possible_rows = soup.select(
        ".big-board-row, .mock-row, .player-row, .draft-row, "
        ".board-row, .player, tr"
    )

    for row in possible_rows:
        text = clean_text(row.get_text(" ", strip=True))
        if not text:
            continue

        # Candidate row usually starts with rank number.
        rank_match = re.match(r"^(\d+)\s+", text)
        if not rank_match:
            continue

        rank = int(rank_match.group(1))

        # Keep raw row first; we will refine after inspecting output.
        rows.append(
            {
                "rank": rank,
                "raw_text": text,
            }
        )

    df = pd.DataFrame(rows).drop_duplicates()

    if df.empty:
        raise RuntimeError("No rows parsed from Tankathon Big Board.")

    return df


def parse_mock_draft(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")

    rows = []

    possible_rows = soup.select(
        ".mock-row, .draft-row, .pick-row, .player-row, "
        ".mock-draft-row, tr"
    )

    for row in possible_rows:
        text = clean_text(row.get_text(" ", strip=True))
        if not text:
            continue

        pick_match = re.match(r"^(\d+)\s+", text)
        if not pick_match:
            continue

        pick = int(pick_match.group(1))

        rows.append(
            {
                "pick": pick,
                "raw_text": text,
            }
        )

    df = pd.DataFrame(rows).drop_duplicates()

    if df.empty:
        raise RuntimeError("No rows parsed from Tankathon Mock Draft.")

    return df


def extract_basic_big_board_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Best-effort extraction from raw_text.

    This is intentionally conservative.
    We preserve raw_text so we can improve parsing after seeing real output.
    """
    out = df.copy()

    players = []
    positions = []
    schools = []
    heights = []
    weights = []

    position_tokens = {"PG", "SG", "SF", "PF", "C", "G", "F", "W"}

    for text in out["raw_text"].astype(str):
        parts = text.split(" ")

        # Remove leading rank
        parts_no_rank = parts[1:]

        # Find first likely position token
        pos_idx = None
        for i, token in enumerate(parts_no_rank):
            clean_token = token.replace(",", "").strip()
            if clean_token in position_tokens:
                pos_idx = i
                break

        if pos_idx is not None and pos_idx > 0:
            player = " ".join(parts_no_rank[:pos_idx])
            position = parts_no_rank[pos_idx]
            remainder = parts_no_rank[pos_idx + 1 :]
        else:
            player = None
            position = None
            remainder = parts_no_rank

        # Try height and weight
        height = None
        weight = None

        for token in remainder:
            if re.search(r"\d+['-]\d+", token):
                height = token
                break

        for token in remainder:
            if re.fullmatch(r"\d{3}", token):
                weight = token
                break

        # School is fuzzy; keep best effort as text before height
        school = None
        if height and height in remainder:
            idx = remainder.index(height)
            school_tokens = remainder[:idx]
            school = " ".join(school_tokens) if school_tokens else None

        players.append(clean_text(player))
        positions.append(clean_text(position))
        schools.append(clean_text(school))
        heights.append(clean_text(height))
        weights.append(clean_text(weight))

    out["player"] = players
    out["position"] = positions
    out["school_or_league"] = schools
    out["height"] = heights
    out["height_inches"] = out["height"].apply(height_to_inches)
    out["weight"] = weights
    out["weight_lbs"] = out["weight"].apply(parse_weight)

    return out


def extract_basic_mock_fields(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    players = []
    teams = []
    positions = []

    position_tokens = {"PG", "SG", "SF", "PF", "C", "G", "F", "W"}

    for text in out["raw_text"].astype(str):
        parts = text.split(" ")
        parts_no_pick = parts[1:]

        # Very conservative.
        # We keep raw_text for manual parser improvement.
        pos_idx = None
        for i, token in enumerate(parts_no_pick):
            clean_token = token.replace(",", "").strip()
            if clean_token in position_tokens:
                pos_idx = i
                break

        if pos_idx is not None and pos_idx > 0:
            before_pos = parts_no_pick[:pos_idx]
            position = parts_no_pick[pos_idx]

            # Heuristic: player name usually two words before position.
            player = " ".join(before_pos[-2:]) if len(before_pos) >= 2 else " ".join(before_pos)

            # Anything before player may include team.
            team = " ".join(before_pos[:-2]) if len(before_pos) > 2 else None
        else:
            player = None
            team = None
            position = None

        players.append(clean_text(player))
        teams.append(clean_text(team))
        positions.append(clean_text(position))

    out["team"] = teams
    out["player"] = players
    out["position"] = positions

    return out


def scrape_tankathon_big_board() -> pd.DataFrame:
    html = fetch_html(BIG_BOARD_URL)
    raw_df = parse_big_board(html)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "big_board_raw.csv"
    raw_df.to_csv(raw_path, index=False)

    processed_df = extract_basic_big_board_fields(raw_df)

    processed_path = PROCESSED_DIR / "prospects_2026_tankathon.csv"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(processed_path, index=False)

    print(f"Saved raw big board: {raw_path}")
    print(f"Saved processed big board: {processed_path}")
    print(processed_df.head(20).to_string(index=False))

    return processed_df


def scrape_tankathon_mock_draft() -> pd.DataFrame:
    html = fetch_html(MOCK_DRAFT_URL)
    raw_df = parse_mock_draft(html)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "mock_draft_raw.csv"
    raw_df.to_csv(raw_path, index=False)

    processed_df = extract_basic_mock_fields(raw_df)

    processed_path = PROCESSED_DIR / "mock_draft_2026_tankathon.csv"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(processed_path, index=False)

    print(f"Saved raw mock draft: {raw_path}")
    print(f"Saved processed mock draft: {processed_path}")
    print(processed_df.head(30).to_string(index=False))

    return processed_df


def main() -> None:
    print("=== Tankathon Big Board ===")
    try:
        scrape_tankathon_big_board()
    except Exception as e:
        print(f"[ERROR] Big Board failed: {e}")

    print("\n=== Tankathon Mock Draft ===")
    try:
        scrape_tankathon_mock_draft()
    except Exception as e:
        print(f"[ERROR] Mock Draft failed: {e}")


if __name__ == "__main__":
    main()
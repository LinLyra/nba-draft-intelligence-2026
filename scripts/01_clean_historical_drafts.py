"""
Clean Basketball Reference historical NBA Draft data.

Input:
data/processed/historical_drafts_master.csv

Output:
data/processed/historical_drafts_clean.csv

Run:
PYTHONPATH=src python scripts/01_clean_historical_drafts.py
"""

from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "historical_drafts_master.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "historical_drafts_clean.csv"


COLUMN_MAP = {
    "year": "year",
    "unnamed:_0_level_0_rk": "rank",
    "unnamed:_1_level_0_pk": "pick",
    "unnamed:_2_level_0_tm": "team",
    "round_1_player": "player",
    "round_1_college": "college",
    "unnamed:_5_level_0_yrs": "career_years",
    "totals_g": "career_games",
    "totals_mp": "career_minutes",
    "totals_pts": "career_points",
    "totals_trb": "career_rebounds",
    "totals_ast": "career_assists",
    "shooting_fgpct": "fg_pct",
    "shooting_3ppct": "three_pt_pct",
    "shooting_ftpct": "ft_pct",
    "per_game_mp": "mpg",
    "per_game_pts": "ppg",
    "per_game_trb": "rpg",
    "per_game_ast": "apg",
    "advanced_ws": "win_shares",
    "advanced_ws_48": "ws_per_48",
    "advanced_bpm": "bpm",
    "advanced_vorp": "vorp",
}


NUMERIC_COLUMNS = [
    "year",
    "rank",
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


def clean_historical_drafts() -> pd.DataFrame:
    df = pd.read_csv(INPUT_PATH)

    missing = [c for c in COLUMN_MAP if c not in df.columns]
    if missing:
        print("[WARN] Missing expected columns:")
        for col in missing:
            print(f"  - {col}")

    df = df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns})

    keep_cols = [v for k, v in COLUMN_MAP.items() if v in df.columns]
    df = df[keep_cols].copy()

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["team", "player", "college"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .replace({"nan": None, "": None})
            )

    df = df.dropna(subset=["year", "pick", "player"])
    df["year"] = df["year"].astype(int)
    df["pick"] = df["pick"].astype(int)

    # Core derived fields
    df["round"] = df["pick"].apply(lambda x: 1 if x <= 30 else 2)
    df["is_first_round"] = df["pick"] <= 30
    df["is_lottery"] = df["pick"] <= 14
    df["is_top_5"] = df["pick"] <= 5
    df["is_top_10"] = df["pick"] <= 10

    # Career outcome labels for future evaluation
    df["played_nba"] = df["career_games"].fillna(0) > 0
    df["rotation_player_proxy"] = df["career_games"].fillna(0) >= 200
    df["starter_level_proxy"] = df["career_minutes"].fillna(0) >= 10000
    df["high_value_proxy"] = df["win_shares"].fillna(0) >= 30

    # Pick bucket
    def pick_tier(pick: int) -> str:
        if pick <= 5:
            return "top_5"
        if pick <= 10:
            return "top_10"
        if pick <= 14:
            return "lottery"
        if pick <= 30:
            return "late_first"
        return "second_round"

    df["pick_tier"] = df["pick"].apply(pick_tier)

    df = df.sort_values(["year", "pick"]).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Clean historical draft data saved.")
    print(f"Path: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Years: {df['year'].min()}-{df['year'].max()}")
    print(f"First-round rows: {df['is_first_round'].sum()}")
    print(f"Lottery rows: {df['is_lottery'].sum()}")

    print("\nColumns:")
    for col in df.columns:
        print(f"  - {col}")

    print("\nSample:")
    print(df.head(10).to_string(index=False))

    return df


if __name__ == "__main__":
    clean_historical_drafts()
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import trim_mean

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data/processed/mock_sources_normalized.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/mock_consensus_robust_2026.csv"

EXCLUDE_SOURCES = {"athletic", "espn", "yahoo"}

SOURCE_WEIGHTS = {
    "tankathon": 1.5,
    "cbs_final": 1.5,
    "bleacher": 1.5,
    "nbadraftnet": 1.5,
    "hoopshq": 1.0,
    "netscouts": 1.0,
    "sb_nation": 1.0,
    "usa_today_ftw": 1.0,
}

TRIM_FRACTION = 0.15


def weighted_mean_pick(picks: pd.Series, weights: pd.Series) -> float:
    return np.average(picks, weights=weights)


def trimmed_mean_pick(picks: np.ndarray) -> float:
    if len(picks) == 0:
        return np.nan
    if len(picks) == 1:
        return float(picks[0])
    return float(trim_mean(picks, proportiontocut=TRIM_FRACTION))


def build_robust_consensus(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["weight"] = df["source"].map(SOURCE_WEIGHTS)

    unknown = sorted(df.loc[df["weight"].isna(), "source"].unique())
    if unknown:
        raise ValueError(f"Missing source weights for: {unknown}")

    rows = []
    for player, group in df.groupby("player"):
        picks = group["pick"].to_numpy(dtype=float)
        weights = group["weight"].to_numpy(dtype=float)

        rows.append(
            {
                "player": player,
                "weighted_mean_pick": weighted_mean_pick(group["pick"], group["weight"]),
                "median_pick": float(np.median(picks)),
                "std_pick": float(np.std(picks, ddof=0)) if len(picks) > 1 else 0.0,
                "min_pick": float(np.min(picks)),
                "max_pick": float(np.max(picks)),
                "source_count": int(group["source"].nunique()),
                "trimmed_mean_pick": trimmed_mean_pick(picks),
            }
        )

    consensus = pd.DataFrame(rows)
    return consensus.sort_values("trimmed_mean_pick").reset_index(drop=True)


if __name__ == "__main__":
    raw_df = pd.read_csv(INPUT_PATH)
    filtered_df = raw_df[~raw_df["source"].isin(EXCLUDE_SOURCES)].copy()

    print(f"Loaded {len(raw_df)} rows from {len(raw_df['source'].unique())} sources")
    print(f"Excluded {EXCLUDE_SOURCES}")
    print(f"Using {len(filtered_df)} rows from {len(filtered_df['source'].unique())} sources")

    consensus_df = build_robust_consensus(filtered_df)
    consensus_df.to_csv(OUTPUT_PATH, index=False)

    print()
    print(consensus_df.head(30).to_string(index=False))
    print()
    print("saved to")
    print(OUTPUT_PATH)

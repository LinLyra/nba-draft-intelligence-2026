from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import trim_mean

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data/processed/mock_sources_normalized.csv"
SOURCE_WEIGHTS_PATH = PROJECT_ROOT / "data/manual/source_weights.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/mock_consensus_weighted_2026.csv"

EXCLUDE_SOURCES = {"athletic", "espn", "yahoo"}
TRIM_FRACTION = 0.15


def load_source_weights(path: Path) -> dict[str, float]:
    weights_df = pd.read_csv(path)
    return dict(zip(weights_df["source"], weights_df["weight"].astype(float)))


def weighted_mean_pick(picks: pd.Series, weights: pd.Series) -> float:
    return float(np.average(picks, weights=weights))


def weighted_median_pick(picks: np.ndarray, weights: np.ndarray) -> float:
    if len(picks) == 0:
        return np.nan
    if len(picks) == 1:
        return float(picks[0])

    order = np.argsort(picks)
    sorted_picks = picks[order]
    sorted_weights = weights[order]
    cumulative = np.cumsum(sorted_weights)
    midpoint = cumulative[-1] / 2.0
    idx = int(np.searchsorted(cumulative, midpoint))
    return float(sorted_picks[min(idx, len(sorted_picks) - 1)])


def trimmed_mean_pick(picks: np.ndarray) -> float:
    if len(picks) == 0:
        return np.nan
    if len(picks) == 1:
        return float(picks[0])
    return float(trim_mean(picks, proportiontocut=TRIM_FRACTION))


def build_weighted_consensus(df: pd.DataFrame, source_weights: dict[str, float]) -> pd.DataFrame:
    df = df.copy()
    df["weight"] = df["source"].map(source_weights)

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
                "weighted_median_pick": weighted_median_pick(picks, weights),
                "trimmed_mean_pick": trimmed_mean_pick(picks),
                "std_pick": float(np.std(picks, ddof=0)) if len(picks) > 1 else 0.0,
                "min_pick": float(np.min(picks)),
                "max_pick": float(np.max(picks)),
                "source_count": int(group["source"].nunique()),
                "weighted_source_count": float(
                    group.drop_duplicates("source")["weight"].sum()
                ),
            }
        )

    consensus = pd.DataFrame(rows)
    return consensus.sort_values("trimmed_mean_pick").reset_index(drop=True)


if __name__ == "__main__":
    source_weights = load_source_weights(SOURCE_WEIGHTS_PATH)
    raw_df = pd.read_csv(INPUT_PATH)
    filtered_df = raw_df[~raw_df["source"].isin(EXCLUDE_SOURCES)].copy()

    print(f"Loaded {len(raw_df)} rows from {len(raw_df['source'].unique())} sources")
    print(f"Excluded {EXCLUDE_SOURCES}")
    print(f"Using {len(filtered_df)} rows from {len(filtered_df['source'].unique())} sources")
    print(f"Source weights from {SOURCE_WEIGHTS_PATH}")

    consensus_df = build_weighted_consensus(filtered_df, source_weights)
    consensus_df.to_csv(OUTPUT_PATH, index=False)

    print()
    print(consensus_df.head(30).to_string(index=False))
    print()
    print("saved to")
    print(OUTPUT_PATH)

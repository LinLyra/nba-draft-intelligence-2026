from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "historical_drafts_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports" / "pick_value"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

first_round = df[df["is_first_round"]].copy()

# 防止极端老将/超级明星让曲线过度波动，做 winsorize
for col in ["win_shares", "vorp", "career_minutes"]:
    first_round[f"{col}_capped"] = first_round[col].clip(
        lower=first_round[col].quantile(0.02),
        upper=first_round[col].quantile(0.98),
    )

pick_curve = (
    first_round.groupby("pick")
    .agg(
        sample_size=("player", "count"),
        avg_ws=("win_shares", "mean"),
        median_ws=("win_shares", "median"),
        avg_ws_capped=("win_shares_capped", "mean"),
        avg_vorp=("vorp", "mean"),
        median_vorp=("vorp", "median"),
        avg_vorp_capped=("vorp_capped", "mean"),
        avg_minutes=("career_minutes", "mean"),
        avg_minutes_capped=("career_minutes_capped", "mean"),
        rotation_rate=("rotation_player_proxy", "mean"),
        starter_rate=("starter_level_proxy", "mean"),
        high_value_rate=("high_value_proxy", "mean"),
    )
    .reset_index()
)

# 平滑顺位价值：rolling average
pick_curve["smoothed_ws_value"] = (
    pick_curve["avg_ws_capped"]
    .rolling(window=5, center=True, min_periods=1)
    .mean()
)

pick_curve["smoothed_vorp_value"] = (
    pick_curve["avg_vorp_capped"]
    .rolling(window=5, center=True, min_periods=1)
    .mean()
)

# 归一化为 0-100 的 pick value score
def normalize_0_100(series: pd.Series) -> pd.Series:
    min_v = series.min()
    max_v = series.max()
    if max_v == min_v:
        return pd.Series([50] * len(series), index=series.index)
    return 100 * (series - min_v) / (max_v - min_v)

pick_curve["pick_value_score"] = normalize_0_100(
    0.6 * pick_curve["smoothed_ws_value"] + 0.4 * pick_curve["smoothed_vorp_value"]
)

pick_curve["pick_value_score"] = pick_curve["pick_value_score"].round(2)

output_path = OUTPUT_DIR / "pick_value_curve.csv"
pick_curve.to_csv(output_path, index=False)

report_path = REPORT_DIR / "pick_value_curve_summary.csv"
pick_curve.to_csv(report_path, index=False)

print("Pick value curve saved:")
print(output_path)
print("\nTop 10 pick value curve:")
print(
    pick_curve[
        [
            "pick",
            "sample_size",
            "avg_ws",
            "avg_vorp",
            "rotation_rate",
            "starter_rate",
            "high_value_rate",
            "pick_value_score",
        ]
    ]
    .head(10)
    .to_string(index=False)
)
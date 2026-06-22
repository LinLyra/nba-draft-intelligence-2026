from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "historical_drafts_clean.csv"
REPORT_DIR = PROJECT_ROOT / "reports" / "eda"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

summary = {
    "rows": len(df),
    "years": f"{df['year'].min()}-{df['year'].max()}",
    "first_round_rows": int(df["is_first_round"].sum()),
    "lottery_rows": int(df["is_lottery"].sum()),
    "top_5_rows": int(df["is_top_5"].sum()),
    "avg_win_shares": round(df["win_shares"].mean(), 2),
    "median_win_shares": round(df["win_shares"].median(), 2),
    "avg_vorp": round(df["vorp"].mean(), 2),
    "median_vorp": round(df["vorp"].median(), 2),
}

pd.DataFrame([summary]).to_csv(REPORT_DIR / "historical_summary.csv", index=False)

tier_summary = (
    df.groupby("pick_tier")
    .agg(
        players=("player", "count"),
        avg_ws=("win_shares", "mean"),
        median_ws=("win_shares", "median"),
        avg_vorp=("vorp", "mean"),
        median_vorp=("vorp", "median"),
        rotation_rate=("rotation_player_proxy", "mean"),
        starter_rate=("starter_level_proxy", "mean"),
        high_value_rate=("high_value_proxy", "mean"),
    )
    .reset_index()
)

tier_summary.to_csv(REPORT_DIR / "pick_tier_outcomes.csv", index=False)

year_summary = (
    df.groupby("year")
    .agg(
        players=("player", "count"),
        first_round_players=("is_first_round", "sum"),
        avg_ws=("win_shares", "mean"),
        avg_vorp=("vorp", "mean"),
        high_value_players=("high_value_proxy", "sum"),
    )
    .reset_index()
)

year_summary.to_csv(REPORT_DIR / "yearly_draft_quality.csv", index=False)

first_round = df[df["is_first_round"]].copy()

first_round_summary = (
    first_round.groupby("pick")
    .agg(
        players=("player", "count"),
        avg_ws=("win_shares", "mean"),
        median_ws=("win_shares", "median"),
        avg_vorp=("vorp", "mean"),
        median_vorp=("vorp", "median"),
        rotation_rate=("rotation_player_proxy", "mean"),
        starter_rate=("starter_level_proxy", "mean"),
        high_value_rate=("high_value_proxy", "mean"),
    )
    .reset_index()
)

first_round_summary.to_csv(REPORT_DIR / "first_round_pick_outcomes.csv", index=False)

print("EDA reports saved to:", REPORT_DIR)
print("\nPick tier outcomes:")
print(tier_summary.to_string(index=False))
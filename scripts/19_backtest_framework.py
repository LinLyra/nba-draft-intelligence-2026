from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_PATH = PROJECT_ROOT / "data/processed/historical_drafts_clean.csv"
PICK_VALUE_PATH = PROJECT_ROOT / "data/processed/pick_value_curve.csv"
BOARD_2026_PATH = PROJECT_ROOT / "data/processed/final_calibrated_monte_carlo_board_2026.csv"
PROB_2026_PATH = PROJECT_ROOT / "data/processed/calibrated_monte_carlo_pick_probabilities.csv"
BACKTEST_ROOT = PROJECT_ROOT / "data/backtest"
REPORTS_DIR = PROJECT_ROOT / "reports"

LOTTERY_PICKS = 14
FIRST_ROUND_PICKS = 30
HISTORICAL_YEARS = list(range(2019, 2026))

PREDICTED_BOARD_COLS = ["pick", "team", "predicted_player", "probability", "alternatives"]
ACTUAL_DRAFT_COLS = ["pick", "team", "player"]
EVAL_TEMPLATE_COLS = [
    "pick",
    "team_pred",
    "predicted_player",
    "probability",
    "alternatives",
    "team_actual",
    "actual_player",
    "exact_match",
    "pick_error",
    "in_predicted_top30",
]

METRIC_NAMES = [
    "exact_pick_accuracy",
    "top_3_pick_accuracy",
    "top_5_pick_accuracy",
    "mean_absolute_pick_error",
    "lottery_accuracy",
    "first_round_player_coverage",
]


def normalize_player_name(name: object) -> str:
    if pd.isna(name):
        return ""
    return str(name).strip().lower()


def backtest_paths(year: int) -> dict[str, Path]:
    year_dir = BACKTEST_ROOT / str(year)
    return {
        "mock_sources": year_dir / "mock_sources_normalized.csv",
        "actual_draft": year_dir / "actual_draft.csv",
        "final_board": year_dir / "final_board.csv",
    }


def load_actual_draft(year: int) -> pd.DataFrame:
    paths = backtest_paths(year)
    actual_path = paths["actual_draft"]

    if actual_path.exists():
        df = pd.read_csv(actual_path)
        return _standardize_actual_draft(df, year)

    if year == 2026:
        return _empty_actual_draft(year)

    if HISTORICAL_PATH.exists():
        historical = pd.read_csv(HISTORICAL_PATH)
        year_rows = historical[(historical["year"] == year) & (historical["is_first_round"] == True)]
        if len(year_rows) > 0:
            return pd.DataFrame(
                {
                    "year": year,
                    "pick": year_rows["pick"].astype(int),
                    "team": year_rows["team"],
                    "player": year_rows["player"],
                }
            ).sort_values("pick")

    raise FileNotFoundError(
        f"No actual draft data for {year}. "
        f"Expected {actual_path} or rows in {HISTORICAL_PATH.name}."
    )


def _standardize_actual_draft(df: pd.DataFrame, year: int) -> pd.DataFrame:
    rename_map = {}
    if "actual_player" in df.columns and "player" not in df.columns:
        rename_map["actual_player"] = "player"
    if "predicted_player" in df.columns and "player" not in df.columns:
        rename_map["predicted_player"] = "player"

    df = df.rename(columns=rename_map)
    required = {"pick", "player"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Actual draft for {year} missing columns: {sorted(missing)}")

    out = df.copy()
    out["pick"] = pd.to_numeric(out["pick"], errors="coerce").astype("Int64")
    out["year"] = year
    if "team" not in out.columns:
        out["team"] = pd.NA

    return out[["year", "pick", "team", "player"]].dropna(subset=["pick"]).astype({"pick": int})


def _empty_actual_draft(year: int) -> pd.DataFrame:
    return pd.DataFrame(columns=["year", "pick", "team", "player"])


def load_predicted_board(year: int) -> pd.DataFrame:
    if year == 2026 and BOARD_2026_PATH.exists():
        return pd.read_csv(BOARD_2026_PATH)

    board_path = backtest_paths(year)["final_board"]
    if board_path.exists():
        return pd.read_csv(board_path)

    raise FileNotFoundError(
        f"No predicted board for {year}. "
        f"Expected {BOARD_2026_PATH} or {board_path}."
    )


def load_pick_probabilities(year: int) -> pd.DataFrame | None:
    if year == 2026 and PROB_2026_PATH.exists():
        return pd.read_csv(PROB_2026_PATH)

    prob_path = backtest_paths(year)["final_board"].parent / "pick_probabilities.csv"
    if prob_path.exists():
        return pd.read_csv(prob_path)
    return None


def _player_predicted_pick_map(pred: pd.DataFrame) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for _, row in pred.iterrows():
        mapping[normalize_player_name(row["predicted_player"])] = int(row["pick"])
    return mapping


def _top_n_players_at_pick(prob: pd.DataFrame | None, pick: int, n: int) -> set[str]:
    if prob is None or prob.empty:
        return set()
    pick_rows = prob[prob["pick"] == pick].sort_values("probability", ascending=False).head(n)
    return {normalize_player_name(name) for name in pick_rows["player"]}


def evaluate_board(
    pred: pd.DataFrame,
    actual: pd.DataFrame,
    prob: pd.DataFrame | None = None,
) -> dict[str, float | int | None]:
    if actual.empty:
        return {metric: None for metric in METRIC_NAMES}

    pred_by_pick = pred.copy()
    pred_by_pick["pick"] = pred_by_pick["pick"].astype(int)
    actual_eval = actual.copy()
    actual_eval["pick"] = actual_eval["pick"].astype(int)

    merged = pred_by_pick.merge(
        actual_eval[["pick", "team", "player"]],
        on="pick",
        how="inner",
        suffixes=("_pred", "_actual"),
    )

    if merged.empty:
        return {metric: None for metric in METRIC_NAMES}

    merged["exact_match"] = merged.apply(
        lambda row: normalize_player_name(row["predicted_player"])
        == normalize_player_name(row["player"]),
        axis=1,
    )

    exact_pick_accuracy = float(merged["exact_match"].mean())

    top_3_hits = []
    top_5_hits = []
    for _, row in merged.iterrows():
        actual_name = normalize_player_name(row["player"])
        pick = int(row["pick"])
        top_3_hits.append(actual_name in _top_n_players_at_pick(prob, pick, 3))
        top_5_hits.append(actual_name in _top_n_players_at_pick(prob, pick, 5))

    top_3_pick_accuracy = float(pd.Series(top_3_hits).mean()) if top_3_hits else None
    top_5_pick_accuracy = float(pd.Series(top_5_hits).mean()) if top_5_hits else None

    lottery = merged[merged["pick"] <= LOTTERY_PICKS]
    lottery_accuracy = float(lottery["exact_match"].mean()) if len(lottery) else None

    predicted_pick_map = _player_predicted_pick_map(pred_by_pick)
    pick_errors = []
    for _, row in actual_eval.iterrows():
        player_key = normalize_player_name(row["player"])
        if player_key in predicted_pick_map:
            pick_errors.append(abs(int(row["pick"]) - predicted_pick_map[player_key]))

    mean_absolute_pick_error = float(pd.Series(pick_errors).mean()) if pick_errors else None

    predicted_players = {
        normalize_player_name(name) for name in pred_by_pick["predicted_player"] if pd.notna(name)
    }
    actual_players = {
        normalize_player_name(row["player"])
        for _, row in actual_eval.iterrows()
        if pd.notna(row["player"]) and int(row["pick"]) <= FIRST_ROUND_PICKS
    }
    if actual_players:
        first_round_player_coverage = len(actual_players & predicted_players) / len(actual_players)
    else:
        first_round_player_coverage = None

    return {
        "exact_pick_accuracy": exact_pick_accuracy,
        "top_3_pick_accuracy": top_3_pick_accuracy,
        "top_5_pick_accuracy": top_5_pick_accuracy,
        "mean_absolute_pick_error": mean_absolute_pick_error,
        "lottery_accuracy": lottery_accuracy,
        "first_round_player_coverage": first_round_player_coverage,
        "evaluated_picks": int(len(merged)),
    }


def build_2026_evaluation_template(pred: pd.DataFrame) -> pd.DataFrame:
    template = pred.copy()
    template = template.rename(columns={"team": "team_pred"})
    template["team_actual"] = pd.NA
    template["actual_player"] = pd.NA
    template["exact_match"] = pd.NA
    template["pick_error"] = pd.NA
    template["in_predicted_top30"] = True
    return template[EVAL_TEMPLATE_COLS]


def build_metrics_template(year: int) -> pd.DataFrame:
    rows = [{"year": year, "metric": metric, "value": pd.NA} for metric in METRIC_NAMES]
    rows.append({"year": year, "metric": "evaluated_picks", "value": pd.NA})
    rows.append({"year": year, "metric": "status", "value": "pending_actual_draft"})
    return pd.DataFrame(rows)


def summarize_historical_placeholder(years: list[int]) -> pd.DataFrame:
    rows = []
    for year in years:
        paths = backtest_paths(year)
        rows.append(
            {
                "year": year,
                "mode": "historical_placeholder",
                "mock_sources_ready": paths["mock_sources"].exists(),
                "actual_draft_ready": paths["actual_draft"].exists(),
                "final_board_ready": paths["final_board"].exists(),
                "status": "awaiting_archived_mock_sources_and_actual_outcomes",
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    BACKTEST_ROOT.mkdir(parents=True, exist_ok=True)

    pred_2026 = load_predicted_board(2026)
    actual_2026 = load_actual_draft(2026)
    prob_2026 = load_pick_probabilities(2026)

    template_2026 = build_2026_evaluation_template(pred_2026)
    template_2026_path = REPORTS_DIR / "backtest_template_2026.csv"
    template_2026.to_csv(template_2026_path, index=False)

    metrics_template = build_metrics_template(2026)
    metrics_template_path = REPORTS_DIR / "backtest_metrics_template.csv"
    metrics_template.to_csv(metrics_template_path, index=False)

    placeholder_summary = summarize_historical_placeholder(HISTORICAL_YEARS)
    placeholder_path = REPORTS_DIR / "backtest_historical_placeholder.csv"
    placeholder_summary.to_csv(placeholder_path, index=False)

    print("NBA Draft Intelligence — Backtest Framework")
    print()
    print("Mode A (2026 post-draft evaluation)")
    print(f"  Predicted board: {BOARD_2026_PATH}")
    print(f"  Actual draft file (future): {backtest_paths(2026)['actual_draft']}")
    print(f"  Evaluation template: {template_2026_path}")
    print(f"  Metrics template: {metrics_template_path}")
    print()
    print("Mode B (2019-2025 historical placeholders)")
    print(placeholder_summary.to_string(index=False))
    print(f"  Saved: {placeholder_path}")
    print()
    print("Expected actual draft schema:")
    print(f"  {ACTUAL_DRAFT_COLS}")
    print()
    print("Predicted board schema:")
    print(f"  {PREDICTED_BOARD_COLS}")
    print()
    if actual_2026.empty:
        print("2026 actual draft not available yet — metrics not computed.")
    else:
        metrics = evaluate_board(pred_2026, actual_2026, prob_2026)
        print("2026 backtest metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")

    if PICK_VALUE_PATH.exists():
        pick_value = pd.read_csv(PICK_VALUE_PATH)
        print()
        print(f"Pick value curve loaded for context: {len(pick_value)} picks")

    print()
    print(
        "Backtest framework ready. Historical backtest requires archived mock sources "
        "and actual draft outcomes."
    )

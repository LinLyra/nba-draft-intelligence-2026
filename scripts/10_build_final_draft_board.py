from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data/processed"
OUT = PROCESSED / "final_draft_board_2026.csv"

consensus = pd.read_csv(PROCESSED / "mock_consensus_2026.csv")
odds_path = PROCESSED / "betting_consensus_2026.csv"

odds = pd.read_csv(odds_path) if odds_path.exists() else pd.DataFrame()

board = consensus.copy()

# Consensus probability proxy: lower avg_pick + more sources + lower std = higher confidence
board["std_pick"] = board["std_pick"].fillna(5.0)
board["source_count"] = board["source_count"].fillna(1)

board["mock_strength"] = (
    (1 / board["avg_pick"].clip(lower=1))
    * np.log1p(board["source_count"])
    * (1 / (1 + board["std_pick"].clip(lower=0)))
)

board["mock_strength"] = board["mock_strength"] / board["mock_strength"].max()

# Add betting odds adjustment for #1 and #2 only
board["odds_boost"] = 0.0
if not odds.empty:
    number1 = odds[odds["market"] == "number_1_overall"][["player", "avg_fair_prob"]]
    number2 = odds[odds["market"] == "number_2_overall"][["player", "avg_fair_prob"]]

    if len(number1):
        board = board.merge(number1.rename(columns={"avg_fair_prob": "odds_no1"}), on="player", how="left")
    else:
        board["odds_no1"] = np.nan

    if len(number2):
        board = board.merge(number2.rename(columns={"avg_fair_prob": "odds_no2"}), on="player", how="left")
    else:
        board["odds_no2"] = np.nan

    board["odds_boost"] = board[["odds_no1", "odds_no2"]].fillna(0).max(axis=1)
else:
    board["odds_no1"] = np.nan
    board["odds_no2"] = np.nan

board["final_score"] = (
    0.75 * board["mock_strength"]
    + 0.25 * board["odds_boost"].fillna(0)
)

board = board.sort_values(["avg_pick", "final_score"], ascending=[True, False]).reset_index(drop=True)

# Use consensus ranking as final board
board["final_pick"] = range(1, len(board) + 1)
board["predicted_team"] = board["most_common_team"].replace({None: np.nan, "None": np.nan}).fillna("TBD")

final_cols = [
    "final_pick",
    "predicted_team",
    "player",
    "avg_pick",
    "median_pick",
    "std_pick",
    "source_count",
    "consensus_score",
    "odds_no1",
    "odds_no2",
    "final_score",
]

board[final_cols].head(30).to_csv(OUT, index=False)

print("Saved:", OUT)
print(board[final_cols].head(30).to_string(index=False))
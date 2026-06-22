from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSENSUS_PATH = PROJECT_ROOT / "data/processed/mock_consensus_weighted_2026.csv"
BETTING_PATH = PROJECT_ROOT / "data/processed/betting_consensus_2026.csv"
TEAM_FIT_PATH = PROJECT_ROOT / "data/processed/team_fit_scores.csv"
MOCK_SOURCES_PATH = PROJECT_ROOT / "data/processed/mock_sources_normalized.csv"
OLD_BOARD_PATH = PROJECT_ROOT / "data/processed/final_monte_carlo_board_2026.csv"
PICK_PROB_PATH = PROJECT_ROOT / "data/processed/calibrated_monte_carlo_pick_probabilities.csv"
FINAL_BOARD_OUT_PATH = PROJECT_ROOT / "data/processed/final_calibrated_monte_carlo_board_2026.csv"

N_SIMULATIONS = 20_000
RANDOM_SEED = 42
N_PICKS = 30
CANDIDATE_WINDOW = 12
MIN_CANDIDATES = 6

WEIGHTS = {
    "consensus": 0.60,
    "reliability": 0.12,
    "betting": 0.18,
    "team_fit": 0.10,
}

DRAFT_ORDER = [
    "Wizards",
    "Jazz",
    "Grizzlies",
    "Bulls",
    "Clippers",
    "Nets",
    "Kings",
    "Hawks",
    "Mavericks",
    "Bucks",
    "Warriors",
    "Thunder",
    "Heat",
    "Hornets",
    "Bulls",
    "Grizzlies",
    "Thunder",
    "Hornets",
    "Raptors",
    "Spurs",
    "Pistons",
    "76ers",
    "Hawks",
    "Knicks",
    "Lakers",
    "Nuggets",
    "Celtics",
    "Timberwolves",
    "Cavaliers",
    "Mavericks",
]


def pick_temperature(pick: int) -> float:
    if pick <= 4:
        return 0.055
    if pick <= 14:
        return 0.12
    return 0.18


def load_betting_probs() -> tuple[dict[str, float], dict[str, float]]:
    betting = pd.read_csv(BETTING_PATH)
    pick1 = (
        betting[betting["market"] == "number_1_overall"]
        .set_index("player")["avg_fair_prob"]
        .to_dict()
    )
    pick2 = (
        betting[betting["market"] == "number_2_overall"]
        .set_index("player")["avg_fair_prob"]
        .to_dict()
    )
    return pick1, pick2


def load_team_fit_lookup() -> dict[tuple[str, str], float]:
    team_fit = pd.read_csv(TEAM_FIT_PATH)
    return {
        (row["team"], row["player"]): float(row["team_fit_score"])
        for _, row in team_fit.iterrows()
    }


def build_exact_pick_source_counts(
    mock_sources: pd.DataFrame,
    valid_players: set[str],
) -> dict[tuple[str, int], int]:
    filtered = mock_sources[mock_sources["player"].isin(valid_players)].copy()
    filtered["pick"] = pd.to_numeric(filtered["pick"], errors="coerce")
    filtered = filtered.dropna(subset=["pick", "player"])

    counts = (
        filtered.groupby(["player", "pick"])["source"]
        .nunique()
        .reset_index(name="exact_pick_source_count")
    )
    return {
        (row["player"], int(row["pick"])): int(row["exact_pick_source_count"])
        for _, row in counts.iterrows()
    }


def softmax(scores: np.ndarray, temperature: float) -> np.ndarray:
    scaled = scores / temperature
    shifted = scaled - scaled.max()
    exp_scores = np.exp(shifted)
    total = exp_scores.sum()
    if total <= 0:
        return np.full(len(scores), 1.0 / len(scores))
    return exp_scores / total


def select_candidate_pool(
    available_idx: np.ndarray,
    pick: int,
    trimmed: np.ndarray,
    betting_pick1: np.ndarray,
    betting_pick2: np.ndarray,
) -> np.ndarray:
    window_mask = trimmed[available_idx] <= pick + CANDIDATE_WINDOW
    pool = available_idx[window_mask]

    if pick == 1:
        odds_idx = available_idx[betting_pick1[available_idx] > 0]
        pool = np.unique(np.concatenate([pool, odds_idx]))
    elif pick == 2:
        odds_idx = available_idx[betting_pick2[available_idx] > 0]
        pool = np.unique(np.concatenate([pool, odds_idx]))

    if len(pool) < MIN_CANDIDATES:
        distances = np.abs(trimmed[available_idx] - pick)
        closest = available_idx[np.argsort(distances)]
        pool = closest[: min(len(closest), max(MIN_CANDIDATES, 12))]

    return pool


def spike_multiplier(
    player: str,
    pick: int,
    std_value: float,
    exact_pick_counts: dict[tuple[str, int], int],
) -> float:
    exact_count = exact_pick_counts.get((player, pick), 0)
    if exact_count <= 1 and std_value > 1.5:
        return 0.55
    if exact_count <= 2 and std_value > 2.5:
        return 0.70
    return 1.0


def compute_candidate_scores(
    candidate_idx: np.ndarray,
    pick: int,
    players: list[str],
    trimmed: np.ndarray,
    std_pick: np.ndarray,
    reliability_count: np.ndarray,
    betting_pick1: np.ndarray,
    betting_pick2: np.ndarray,
    team_fit: np.ndarray,
    exact_pick_counts: dict[tuple[str, int], int],
) -> np.ndarray:
    consensus_component = np.exp(
        -np.abs(trimmed[candidate_idx] - pick) / (1.0 + std_pick[candidate_idx])
    )

    reliability_component = np.log1p(reliability_count[candidate_idx])
    reliability_max = reliability_component.max()
    if reliability_max > 0:
        reliability_component = reliability_component / reliability_max

    if pick == 1:
        betting_component = betting_pick1[candidate_idx]
    elif pick == 2:
        betting_component = betting_pick2[candidate_idx]
    else:
        betting_component = np.zeros(len(candidate_idx))

    team_fit_component = team_fit[candidate_idx]

    scores = (
        WEIGHTS["consensus"] * consensus_component
        + WEIGHTS["reliability"] * reliability_component
        + WEIGHTS["betting"] * betting_component
        + WEIGHTS["team_fit"] * team_fit_component
    )

    if pick > 2:
        # Picks 1-2 already encode uncertainty via betting odds; avoid double-penalizing.
        scores = scores / (1.0 + 0.15 * std_pick[candidate_idx])

    for i, player_idx in enumerate(candidate_idx):
        scores[i] *= spike_multiplier(
            players[player_idx],
            pick,
            float(std_pick[player_idx]),
            exact_pick_counts,
        )

    return scores


def run_simulations(
    players: list[str],
    trimmed: np.ndarray,
    std_pick: np.ndarray,
    reliability_count: np.ndarray,
    betting_pick1: np.ndarray,
    betting_pick2: np.ndarray,
    team_fit_matrix: np.ndarray,
    exact_pick_counts: dict[tuple[str, int], int],
    n_simulations: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n_players = len(players)
    pick_counts = np.zeros((N_PICKS, n_players), dtype=np.int32)
    player_pick_sums = np.zeros(n_players, dtype=np.float64)
    player_selection_counts = np.zeros(n_players, dtype=np.int32)

    for _ in range(n_simulations):
        available = np.ones(n_players, dtype=bool)

        for pick in range(1, N_PICKS + 1):
            available_idx = np.where(available)[0]
            candidate_idx = select_candidate_pool(
                available_idx,
                pick,
                trimmed,
                betting_pick1,
                betting_pick2,
            )
            team_idx = pick - 1
            scores = compute_candidate_scores(
                candidate_idx,
                pick,
                players,
                trimmed,
                std_pick,
                reliability_count,
                betting_pick1,
                betting_pick2,
                team_fit_matrix[team_idx],
                exact_pick_counts,
            )
            probs = softmax(scores, pick_temperature(pick))
            chosen_local = rng.choice(len(candidate_idx), p=probs)
            chosen = candidate_idx[chosen_local]

            pick_counts[pick - 1, chosen] += 1
            player_pick_sums[chosen] += pick
            player_selection_counts[chosen] += 1
            available[chosen] = False

    return pick_counts, player_pick_sums, player_selection_counts


def build_team_fit_matrix(
    players: list[str],
    team_fit_lookup: dict[tuple[str, str], float],
) -> np.ndarray:
    matrix = np.full((N_PICKS, len(players)), 0.5, dtype=float)
    for pick_idx, team in enumerate(DRAFT_ORDER):
        for player_idx, player in enumerate(players):
            matrix[pick_idx, player_idx] = team_fit_lookup.get((team, player), 0.5)
    return matrix


def format_alternatives(
    pick_probs: pd.Series,
    predicted_player: str,
    top_n: int = 3,
) -> str:
    alternatives = (
        pick_probs.drop(labels=[predicted_player], errors="ignore")
        .sort_values(ascending=False)
        .head(top_n)
    )
    parts = [f"{player} ({prob * 100:.1f}%)" for player, prob in alternatives.items()]
    return "; ".join(parts)


def build_outputs(
    players: list[str],
    consensus: pd.DataFrame,
    pick_counts: np.ndarray,
    player_pick_sums: np.ndarray,
    player_selection_counts: np.ndarray,
    n_simulations: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    consensus_lookup = consensus.set_index("player")
    avg_selected_pick = np.divide(
        player_pick_sums,
        player_selection_counts,
        out=np.full(len(players), np.nan),
        where=player_selection_counts > 0,
    )

    probability_rows = []
    board_rows = []

    for pick in range(1, N_PICKS + 1):
        team = DRAFT_ORDER[pick - 1]
        pick_probs = pick_counts[pick - 1] / n_simulations
        active_players = np.where(pick_probs > 0)[0]

        for player_idx in active_players:
            player = players[player_idx]
            consensus_row = consensus_lookup.loc[player]
            probability_rows.append(
                {
                    "pick": pick,
                    "team": team,
                    "player": player,
                    "probability": round(float(pick_probs[player_idx]), 6),
                    "avg_selected_pick": round(float(avg_selected_pick[player_idx]), 3)
                    if not np.isnan(avg_selected_pick[player_idx])
                    else np.nan,
                    "source_count": int(consensus_row["source_count"]),
                    "weighted_source_count": float(consensus_row["weighted_source_count"])
                    if "weighted_source_count" in consensus_row.index
                    else np.nan,
                    "trimmed_mean_pick": float(consensus_row["trimmed_mean_pick"]),
                    "weighted_mean_pick": float(consensus_row["weighted_mean_pick"])
                    if "weighted_mean_pick" in consensus_row.index
                    else np.nan,
                    "std_pick": float(consensus_row["std_pick"]),
                    "min_pick": float(consensus_row["min_pick"])
                    if "min_pick" in consensus_row.index
                    else np.nan,
                    "max_pick": float(consensus_row["max_pick"])
                    if "max_pick" in consensus_row.index
                    else np.nan,
                }
            )

        pick_prob_series = pd.Series(
            {players[idx]: pick_probs[idx] for idx in active_players}
        )
        predicted_player = pick_prob_series.idxmax()
        board_rows.append(
            {
                "pick": pick,
                "team": team,
                "predicted_player": predicted_player,
                "probability": round(float(pick_prob_series.max()), 6),
                "alternatives": format_alternatives(pick_prob_series, predicted_player),
            }
        )

    return pd.DataFrame(probability_rows), pd.DataFrame(board_rows)


def print_pick5_comparison(
    old_board: pd.DataFrame,
    new_board: pd.DataFrame,
    new_probs: pd.DataFrame,
) -> None:
    print()
    print("=== Pick 5 comparison: previous vs current calibrated board ===")
    old_row = old_board[old_board["pick"] == 5]
    new_row = new_board[new_board["pick"] == 5]

    if not old_row.empty:
        old = old_row.iloc[0]
        print(
            f"Previous: {old['team']} | {old['predicted_player']} "
            f"({old['probability'] * 100:.1f}%) | {old['alternatives']}"
        )
    else:
        print("Previous: (missing)")

    if not new_row.empty:
        new = new_row.iloc[0]
        print(
            f"Current:  {new['team']} | {new['predicted_player']} "
            f"({new['probability'] * 100:.1f}%) | {new['alternatives']}"
        )

    pick5_probs = (
        new_probs[new_probs["pick"] == 5]
        .sort_values("probability", ascending=False)
        .head(8)[["player", "probability", "trimmed_mean_pick", "std_pick"]]
    )
    print()
    print("Calibrated pick 5 probability distribution (top 8):")
    print(pick5_probs.to_string(index=False))


if __name__ == "__main__":
    previous_board_df = (
        pd.read_csv(FINAL_BOARD_OUT_PATH) if FINAL_BOARD_OUT_PATH.exists() else pd.DataFrame()
    )

    consensus_df = pd.read_csv(CONSENSUS_PATH)
    mock_sources_df = pd.read_csv(MOCK_SOURCES_PATH)
    players = consensus_df["player"].tolist()
    valid_players = set(players)

    trimmed = consensus_df["trimmed_mean_pick"].to_numpy(dtype=float)
    std_pick = consensus_df["std_pick"].fillna(0).to_numpy(dtype=float)
    if "weighted_source_count" in consensus_df.columns:
        reliability_count = consensus_df["weighted_source_count"].to_numpy(dtype=float)
    else:
        reliability_count = consensus_df["source_count"].to_numpy(dtype=float)

    betting_pick1_map, betting_pick2_map = load_betting_probs()
    betting_pick1 = np.array([betting_pick1_map.get(player, 0.0) for player in players])
    betting_pick2 = np.array([betting_pick2_map.get(player, 0.0) for player in players])

    team_fit_lookup = load_team_fit_lookup()
    team_fit_matrix = build_team_fit_matrix(players, team_fit_lookup)
    exact_pick_counts = build_exact_pick_source_counts(mock_sources_df, valid_players)

    pick_counts, player_pick_sums, player_selection_counts = run_simulations(
        players=players,
        trimmed=trimmed,
        std_pick=std_pick,
        reliability_count=reliability_count,
        betting_pick1=betting_pick1,
        betting_pick2=betting_pick2,
        team_fit_matrix=team_fit_matrix,
        exact_pick_counts=exact_pick_counts,
        n_simulations=N_SIMULATIONS,
        seed=RANDOM_SEED,
    )

    probability_df, board_df = build_outputs(
        players=players,
        consensus=consensus_df,
        pick_counts=pick_counts,
        player_pick_sums=player_pick_sums,
        player_selection_counts=player_selection_counts,
        n_simulations=N_SIMULATIONS,
    )

    probability_df.to_csv(PICK_PROB_PATH, index=False)
    board_df.to_csv(FINAL_BOARD_OUT_PATH, index=False)

    old_board_df = previous_board_df

    print(f"Ran {N_SIMULATIONS:,} calibrated Monte Carlo simulations")
    print(f"Player pool: {len(players)} prospects from weighted consensus")
    print(f"Consensus input: {CONSENSUS_PATH.name}")
    print()
    print(board_df.to_string(index=False))

    print_pick5_comparison(old_board_df, board_df, probability_df)

    print()
    print("saved to")
    print(PICK_PROB_PATH)
    print(FINAL_BOARD_OUT_PATH)

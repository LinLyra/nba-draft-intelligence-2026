from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSENSUS_PATH = PROJECT_ROOT / "data/processed/mock_consensus_robust_2026.csv"
BETTING_PATH = PROJECT_ROOT / "data/processed/betting_consensus_2026.csv"
TEAM_FIT_PATH = PROJECT_ROOT / "data/processed/team_fit_scores.csv"
FINAL_BOARD_PATH = PROJECT_ROOT / "data/processed/final_draft_board_2026.csv"
PICK_PROB_PATH = PROJECT_ROOT / "data/processed/monte_carlo_pick_probabilities.csv"
FINAL_BOARD_OUT_PATH = PROJECT_ROOT / "data/processed/final_monte_carlo_board_2026.csv"

N_SIMULATIONS = 10_000
RANDOM_SEED = 42
N_PICKS = 30
SOFTMAX_TEMPERATURE = 0.07
CANDIDATE_WINDOW = 10
MIN_CANDIDATES = 6

WEIGHTS = {
    "consensus": 0.55,
    "reliability": 0.15,
    "betting": 0.20,
    "team_fit": 0.10,
}

FALLBACK_DRAFT_ORDER = [
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

TEAM_ALIASES = {
    "Washington Wizards": "Wizards",
    "Utah Jazz": "Jazz",
    "Memphis Grizzlies": "Grizzlies",
    "Chicago Bulls": "Bulls",
    "LA Clippers": "Clippers",
    "Brooklyn Nets": "Nets",
    "Sacramento Kings": "Kings",
    "Atlanta Hawks": "Hawks",
    "Dallas Mavericks": "Mavericks",
    "Milwaukee Bucks": "Bucks",
    "Golden State Warriors": "Warriors",
    "Oklahoma City Thunder": "Thunder",
    "Miami Heat": "Heat",
    "Charlotte Hornets": "Hornets",
    "Toronto Raptors": "Raptors",
    "San Antonio Spurs": "Spurs",
    "Detroit Pistons": "Pistons",
    "Philadelphia 76ers": "76ers",
    "New York Knicks": "Knicks",
    "Los Angeles Lakers": "Lakers",
    "Denver Nuggets": "Nuggets",
    "Boston Celtics": "Celtics",
    "Minnesota Timberwolves": "Timberwolves",
    "Cleveland Cavaliers": "Cavaliers",
}


def normalize_team_name(team: object) -> str | None:
    if pd.isna(team):
        return None
    name = str(team).strip()
    if name in FALLBACK_DRAFT_ORDER or name in set(FALLBACK_DRAFT_ORDER):
        return name
    if name in TEAM_ALIASES:
        return TEAM_ALIASES[name]
    return None


def load_draft_order() -> list[str]:
    order = {pick: team for pick, team in enumerate(FALLBACK_DRAFT_ORDER, start=1)}

    if FINAL_BOARD_PATH.exists():
        board = pd.read_csv(FINAL_BOARD_PATH).sort_values("final_pick")
        for _, row in board.iterrows():
            pick = int(row["final_pick"])
            team = normalize_team_name(row["predicted_team"])
            if team and pick not in order:
                order[pick] = team

    return [order[pick] for pick in range(1, N_PICKS + 1)]


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


def softmax(scores: np.ndarray, temperature: float = SOFTMAX_TEMPERATURE) -> np.ndarray:
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


def compute_candidate_scores(
    available_idx: np.ndarray,
    pick: int,
    team: str,
    trimmed: np.ndarray,
    std_pick: np.ndarray,
    source_count: np.ndarray,
    betting_pick1: np.ndarray,
    betting_pick2: np.ndarray,
    team_fit: np.ndarray,
) -> np.ndarray:
    consensus_component = np.exp(
        -np.abs(trimmed[available_idx] - pick) / (1.0 + std_pick[available_idx])
    )

    reliability_component = np.log1p(source_count[available_idx])
    reliability_max = reliability_component.max()
    if reliability_max > 0:
        reliability_component = reliability_component / reliability_max

    if pick == 1:
        betting_component = betting_pick1[available_idx]
    elif pick == 2:
        betting_component = betting_pick2[available_idx]
    else:
        betting_component = np.zeros(len(available_idx))

    team_fit_component = team_fit[available_idx]

    return (
        WEIGHTS["consensus"] * consensus_component
        + WEIGHTS["reliability"] * reliability_component
        + WEIGHTS["betting"] * betting_component
        + WEIGHTS["team_fit"] * team_fit_component
    )


def run_simulations(
    players: list[str],
    trimmed: np.ndarray,
    std_pick: np.ndarray,
    source_count: np.ndarray,
    betting_pick1: np.ndarray,
    betting_pick2: np.ndarray,
    team_fit_matrix: np.ndarray,
    draft_order: list[str],
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
                draft_order[team_idx],
                trimmed,
                std_pick,
                source_count,
                betting_pick1,
                betting_pick2,
                team_fit_matrix[team_idx],
            )
            probs = softmax(scores)
            chosen_local = rng.choice(len(candidate_idx), p=probs)
            chosen = candidate_idx[chosen_local]

            pick_counts[pick - 1, chosen] += 1
            player_pick_sums[chosen] += pick
            player_selection_counts[chosen] += 1
            available[chosen] = False

    return pick_counts, player_pick_sums, player_selection_counts


def build_team_fit_matrix(
    players: list[str],
    draft_order: list[str],
    team_fit_lookup: dict[tuple[str, str], float],
) -> np.ndarray:
    matrix = np.full((N_PICKS, len(players)), 0.5, dtype=float)
    for pick_idx, team in enumerate(draft_order):
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
    draft_order: list[str],
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
        team = draft_order[pick - 1]
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
                    "trimmed_mean_pick": float(consensus_row["trimmed_mean_pick"]),
                    "std_pick": float(consensus_row["std_pick"]),
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


if __name__ == "__main__":
    consensus_df = pd.read_csv(CONSENSUS_PATH)
    players = consensus_df["player"].tolist()

    trimmed = consensus_df["trimmed_mean_pick"].to_numpy(dtype=float)
    std_pick = consensus_df["std_pick"].fillna(0).to_numpy(dtype=float)
    source_count = consensus_df["source_count"].to_numpy(dtype=float)

    betting_pick1_map, betting_pick2_map = load_betting_probs()
    betting_pick1 = np.array([betting_pick1_map.get(player, 0.0) for player in players])
    betting_pick2 = np.array([betting_pick2_map.get(player, 0.0) for player in players])

    team_fit_lookup = load_team_fit_lookup()
    draft_order = load_draft_order()
    team_fit_matrix = build_team_fit_matrix(players, draft_order, team_fit_lookup)

    pick_counts, player_pick_sums, player_selection_counts = run_simulations(
        players=players,
        trimmed=trimmed,
        std_pick=std_pick,
        source_count=source_count,
        betting_pick1=betting_pick1,
        betting_pick2=betting_pick2,
        team_fit_matrix=team_fit_matrix,
        draft_order=draft_order,
        n_simulations=N_SIMULATIONS,
        seed=RANDOM_SEED,
    )

    probability_df, board_df = build_outputs(
        players=players,
        consensus=consensus_df,
        draft_order=draft_order,
        pick_counts=pick_counts,
        player_pick_sums=player_pick_sums,
        player_selection_counts=player_selection_counts,
        n_simulations=N_SIMULATIONS,
    )

    probability_df.to_csv(PICK_PROB_PATH, index=False)
    board_df.to_csv(FINAL_BOARD_OUT_PATH, index=False)

    print(f"Ran {N_SIMULATIONS:,} Monte Carlo simulations")
    print(f"Player pool: {len(players)} prospects from robust consensus")
    print()
    print(board_df.to_string(index=False))
    print()
    print("saved to")
    print(PICK_PROB_PATH)
    print(FINAL_BOARD_OUT_PATH)

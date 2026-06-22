from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSENSUS_PATH = PROJECT_ROOT / "data/processed/mock_consensus_robust_2026.csv"
PROSPECT_PATH = PROJECT_ROOT / "data/processed/prospect_master.csv"
FINAL_BOARD_PATH = PROJECT_ROOT / "data/processed/final_draft_board_2026.csv"
DRAFT_ORDER_PATH = PROJECT_ROOT / "data/processed/draft_order_2026_sample.csv"
MOCK_SOURCES_PATH = PROJECT_ROOT / "data/processed/mock_sources_normalized.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/team_fit_scores.csv"

STAT_COLS = [
    "height_inches",
    "weight_lbs",
    "ppg",
    "rpg",
    "apg",
    "spg",
    "bpg",
    "ts_pct",
    "usg_pct",
    "obpm",
    "dbpm",
    "age",
]

ARCHETYPE_COLS = [
    "creation_score",
    "shooting_score",
    "size_score",
    "defense_score",
    "upside_score",
    "nba_ready_score",
]

WEIGHT_KEYS = [
    "creation",
    "shooting",
    "size",
    "defense",
    "upside",
    "nba_ready",
]

VALID_TEAMS = [
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
    "Raptors",
    "Spurs",
    "Pistons",
    "76ers",
    "Knicks",
    "Lakers",
    "Nuggets",
    "Celtics",
    "Timberwolves",
    "Cavaliers",
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

BASE_PROFILES = {
    "rebuilding": {
        "creation": 0.28,
        "shooting": 0.12,
        "size": 0.15,
        "defense": 0.10,
        "upside": 0.28,
        "nba_ready": 0.07,
    },
    "contender": {
        "creation": 0.12,
        "shooting": 0.25,
        "size": 0.15,
        "defense": 0.22,
        "upside": 0.10,
        "nba_ready": 0.16,
    },
    "balanced": {
        "creation": 0.18,
        "shooting": 0.18,
        "size": 0.18,
        "defense": 0.18,
        "upside": 0.15,
        "nba_ready": 0.13,
    },
}

NEED_ADJUSTMENTS = {
    "guard": {"creation": 0.08, "shooting": 0.06},
    "frontcourt": {"size": 0.08, "defense": 0.06},
    "balanced": {},
}

TEAM_CONFIG: dict[str, dict[str, str]] = {
    "Wizards": {"base": "rebuilding", "need": "guard"},
    "Jazz": {"base": "rebuilding", "need": "guard"},
    "Hornets": {"base": "rebuilding", "need": "frontcourt"},
    "Pistons": {"base": "rebuilding", "need": "balanced"},
    "Spurs": {"base": "rebuilding", "need": "frontcourt"},
    "Nets": {"base": "rebuilding", "need": "guard"},
    "Celtics": {"base": "contender", "need": "balanced"},
    "Thunder": {"base": "contender", "need": "balanced"},
    "Bucks": {"base": "contender", "need": "balanced"},
    "Nuggets": {"base": "contender", "need": "balanced"},
    "Cavaliers": {"base": "contender", "need": "balanced"},
    "Knicks": {"base": "contender", "need": "balanced"},
    "Lakers": {"base": "contender", "need": "balanced"},
    "Warriors": {"base": "contender", "need": "shooting"},
    "Heat": {"base": "contender", "need": "frontcourt"},
    "Grizzlies": {"base": "balanced", "need": "frontcourt"},
    "Bulls": {"base": "balanced", "need": "frontcourt"},
    "Clippers": {"base": "balanced", "need": "balanced"},
    "Kings": {"base": "balanced", "need": "guard"},
    "Hawks": {"base": "balanced", "need": "guard"},
    "Mavericks": {"base": "balanced", "need": "guard"},
    "Raptors": {"base": "balanced", "need": "frontcourt"},
    "Timberwolves": {"base": "balanced", "need": "balanced"},
    "76ers": {"base": "balanced", "need": "balanced"},
}


def normalize_team_name(team: object) -> str | None:
    if pd.isna(team):
        return None
    name = str(team).strip()
    if name in VALID_TEAMS:
        return name
    if name in TEAM_ALIASES:
        return TEAM_ALIASES[name]
    return None


def extract_player_from_raw(raw: object) -> str | None:
    if pd.isna(raw):
        return None
    match = re.match(r"^\d+\s+(.+?)\s+(?:PG/SG|SG/PG|SF/PF|PF/C|SG/SF|PG|SG|SF|PF|C)\b", str(raw))
    if match:
        return match.group(1).strip()
    return None


def minmax_normalize(series: pd.Series, invert: bool = False) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").astype(float)
    minimum = values.min()
    maximum = values.max()
    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series(0.5, index=series.index, dtype=float)
    normalized = (values - minimum) / (maximum - minimum)
    if invert:
        normalized = 1.0 - normalized
    return normalized.fillna(0.5)


def load_prospects() -> pd.DataFrame:
    df = pd.read_csv(PROSPECT_PATH)
    df["player"] = df["player"].replace("", np.nan)
    df["player"] = df.groupby("rank")["player"].transform(
        lambda group: group.dropna().iloc[0] if group.notna().any() else np.nan
    )
    missing_player = df["player"].isna()
    df.loc[missing_player, "player"] = df.loc[missing_player, "raw_text"].map(extract_player_from_raw)

    df = df.sort_values(["has_core_profile", "has_box_score"], ascending=False)
    df = df.dropna(subset=["player"]).drop_duplicates(subset=["player"], keep="first").copy()

    for col in STAT_COLS:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    return df.reset_index(drop=True)


def build_archetype_scores(prospects: pd.DataFrame, consensus: pd.DataFrame) -> pd.DataFrame:
    df = prospects.merge(
        consensus[["player", "trimmed_mean_pick"]],
        on="player",
        how="inner",
    ).copy()

    norm = {
        "ppg": minmax_normalize(df["ppg"]),
        "apg": minmax_normalize(df["apg"]),
        "usg_pct": minmax_normalize(df["usg_pct"]),
        "ts_pct": minmax_normalize(df["ts_pct"]),
        "height_inches": minmax_normalize(df["height_inches"]),
        "weight_lbs": minmax_normalize(df["weight_lbs"]),
        "spg": minmax_normalize(df["spg"]),
        "bpg": minmax_normalize(df["bpg"]),
        "dbpm": minmax_normalize(df["dbpm"]),
        "obpm": minmax_normalize(df["obpm"]),
        "age_young": minmax_normalize(df["age"], invert=True),
        "consensus_strength": minmax_normalize(-df["trimmed_mean_pick"]),
    }

    df["creation_score"] = (norm["apg"] + norm["usg_pct"] + norm["ppg"]) / 3.0
    df["shooting_score"] = norm["ts_pct"]
    df["size_score"] = (norm["height_inches"] + norm["weight_lbs"]) / 2.0
    df["defense_score"] = (norm["spg"] + norm["bpg"] + norm["dbpm"]) / 3.0
    df["upside_score"] = (norm["age_young"] + norm["consensus_strength"]) / 2.0
    df["nba_ready_score"] = (norm["obpm"] + norm["dbpm"] + norm["ppg"]) / 3.0

    return df


def build_team_weights(team: str) -> dict[str, float]:
    config = TEAM_CONFIG.get(team, {"base": "balanced", "need": "balanced"})
    weights = BASE_PROFILES[config["base"]].copy()

    need = config["need"]
    if need == "shooting":
        weights["shooting"] += 0.10
        weights["nba_ready"] += 0.04
        weights["upside"] -= 0.07
        weights["creation"] -= 0.07
    else:
        for key, boost in NEED_ADJUSTMENTS.get(need, {}).items():
            weights[key] += boost

    total = sum(weights.values())
    return {key: value / total for key, value in weights.items()}


def build_team_fit_scores(prospects: pd.DataFrame) -> pd.DataFrame:
    rows = []
    team_weights = {team: build_team_weights(team) for team in VALID_TEAMS}

    for team in VALID_TEAMS:
        weights = team_weights[team]
        for _, player in prospects.iterrows():
            team_fit_score = sum(
                weights[key] * float(player[f"{key}_score"])
                for key in WEIGHT_KEYS
            )
            rows.append(
                {
                    "team": team,
                    "player": player["player"],
                    "team_fit_score": round(team_fit_score, 6),
                    "creation_score": round(float(player["creation_score"]), 6),
                    "shooting_score": round(float(player["shooting_score"]), 6),
                    "size_score": round(float(player["size_score"]), 6),
                    "defense_score": round(float(player["defense_score"]), 6),
                    "upside_score": round(float(player["upside_score"]), 6),
                    "nba_ready_score": round(float(player["nba_ready_score"]), 6),
                }
            )

    return pd.DataFrame(rows)


def load_top_teams(n: int = 10) -> list[str]:
    teams_by_pick: dict[int, str] = {}

    if DRAFT_ORDER_PATH.exists():
        draft_order = pd.read_csv(DRAFT_ORDER_PATH)
        for _, row in draft_order.iterrows():
            pick = int(row["pick_number"])
            team = normalize_team_name(row["current_owner"])
            if team:
                teams_by_pick[pick] = team

    if FINAL_BOARD_PATH.exists():
        board = pd.read_csv(FINAL_BOARD_PATH).sort_values("final_pick")
        for _, row in board.iterrows():
            pick = int(row["final_pick"])
            team = normalize_team_name(row["predicted_team"])
            if team:
                teams_by_pick[pick] = team

    if MOCK_SOURCES_PATH.exists() and len(teams_by_pick) < n:
        mocks = pd.read_csv(MOCK_SOURCES_PATH)
        mocks = mocks[mocks["team"].notna() & (mocks["team"] != "")]
        for pick, group in mocks.groupby("pick"):
            if int(pick) in teams_by_pick:
                continue
            mode_team = group["team"].mode()
            if len(mode_team) == 0:
                continue
            team = normalize_team_name(mode_team.iloc[0])
            if team:
                teams_by_pick[int(pick)] = team

    ordered: list[str] = []
    for pick in range(1, n + 1):
        team = teams_by_pick.get(pick)
        if team and team not in ordered:
            ordered.append(team)

    for team in VALID_TEAMS:
        if len(ordered) >= n:
            break
        if team not in ordered:
            ordered.append(team)

    return ordered[:n]


def print_top_fits(fit_scores: pd.DataFrame, top_teams: list[str], top_n: int = 5) -> None:
    print()
    for team in top_teams:
        print(f"=== {team} ===")
        team_rows = (
            fit_scores[fit_scores["team"] == team]
            .sort_values("team_fit_score", ascending=False)
            .head(top_n)
        )
        print(team_rows[["player", "team_fit_score"]].to_string(index=False))
        print()


if __name__ == "__main__":
    consensus_df = pd.read_csv(CONSENSUS_PATH)
    prospects_df = load_prospects()
    scored_prospects = build_archetype_scores(prospects_df, consensus_df)

    missing_players = sorted(set(consensus_df["player"]) - set(scored_prospects["player"]))
    if missing_players:
        print(f"Warning: {len(missing_players)} consensus players missing from prospect_master:")
        print(", ".join(missing_players[:10]))

    fit_scores_df = build_team_fit_scores(scored_prospects)
    fit_scores_df.to_csv(OUTPUT_PATH, index=False)

    top_teams = load_top_teams(10)
    print(f"Loaded {len(consensus_df)} consensus players")
    print(f"Matched {len(scored_prospects)} prospects with archetype scores")
    print(f"Built {len(fit_scores_df)} team-player fit rows")
    print(f"Top 10 draft teams: {', '.join(top_teams)}")
    print_top_fits(fit_scores_df, top_teams)

    print("saved to")
    print(OUTPUT_PATH)

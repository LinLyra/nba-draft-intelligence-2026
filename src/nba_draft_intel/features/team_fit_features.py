import pandas as pd

FIT_DIMENSIONS = [
    ("creation_score", "need_creation"),
    ("shooting_score", "need_shooting"),
    ("defense_score", "need_defense"),
    ("size_score", "need_size"),
    ("rim_score", "need_rim_protection"),
    ("ready_now_score", "need_ready_now"),
    ("upside_score", "need_upside"),
]


def compute_team_fit_matrix(prospects: pd.DataFrame, team_needs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, p in prospects.iterrows():
        for _, t in team_needs.iterrows():
            score_parts = []
            for player_col, team_col in FIT_DIMENSIONS:
                if player_col in prospects.columns and team_col in team_needs.columns:
                    score_parts.append(float(p[player_col]) * float(t[team_col]))
            team_fit_score = sum(score_parts) / max(len(score_parts), 1)
            rows.append({
                "player_id": p["player_id"],
                "player_name": p["player_name"],
                "team": t["team"],
                "team_fit_score": team_fit_score,
                "fit_reason": _fit_reason(p, t),
            })
    return pd.DataFrame(rows)


def _fit_reason(player: pd.Series, team: pd.Series) -> str:
    needs = {
        "creation": team.get("need_creation", 0),
        "shooting": team.get("need_shooting", 0),
        "defense": team.get("need_defense", 0),
        "size": team.get("need_size", 0),
        "rim protection": team.get("need_rim_protection", 0),
        "upside": team.get("need_upside", 0),
    }
    top_needs = sorted(needs, key=needs.get, reverse=True)[:2]
    return f"Best aligned with {team['team']} needs in {top_needs[0]} and {top_needs[1]}."

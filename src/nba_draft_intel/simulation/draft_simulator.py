from dataclasses import dataclass
import pandas as pd
from nba_draft_intel.models.consensus_model import add_mock_consensus_score


@dataclass
class DraftWeights:
    prospect_value: float = 0.35
    team_fit: float = 0.25
    mock_consensus: float = 0.30
    availability: float = 0.10
    trade_risk_penalty: float = 0.10


def run_draft_board(
    prospects: pd.DataFrame,
    draft_order: pd.DataFrame,
    team_fit: pd.DataFrame,
    weights: DraftWeights | None = None,
) -> pd.DataFrame:
    weights = weights or DraftWeights()
    remaining = prospects.copy()
    rows = []

    for _, pick in draft_order.sort_values("pick_number").iterrows():
        pick_number = int(pick["pick_number"])
        team = pick["current_owner"]
        scored = add_mock_consensus_score(remaining, pick_number)
        scored = scored.merge(
            team_fit[team_fit["team"] == team][["player_id", "team_fit_score", "fit_reason"]],
            on="player_id",
            how="left",
        )
        scored["team_fit_score"] = scored["team_fit_score"].fillna(0.5)
        scored["availability_score"] = 1.0
        trade_risk = float(pick.get("trade_risk_score", pick.get("trade_risk_prior", 0.15)))
        scored["final_selection_score"] = (
            weights.prospect_value * scored["prospect_value_score"]
            + weights.team_fit * scored["team_fit_score"]
            + weights.mock_consensus * scored["mock_consensus_score"]
            + weights.availability * scored["availability_score"]
            - weights.trade_risk_penalty * trade_risk
        )
        best = scored.sort_values("final_selection_score", ascending=False).iloc[0]
        alternatives = scored.sort_values("final_selection_score", ascending=False).head(4).iloc[1:]
        rows.append({
            "pick_number": pick_number,
            "team": team,
            "predicted_player": best["player_name"],
            "player_id": best["player_id"],
            "position": best.get("position", None),
            "confidence_proxy": round(float(best["final_selection_score"]), 4),
            "prospect_value_score": round(float(best["prospect_value_score"]), 4),
            "team_fit_score": round(float(best["team_fit_score"]), 4),
            "mock_consensus_score": round(float(best["mock_consensus_score"]), 4),
            "trade_risk_score": round(trade_risk, 4),
            "trade_risk_label": pick.get("trade_risk_label", None),
            "alternatives": ", ".join(alternatives["player_name"].tolist()),
            "reason": best.get("fit_reason", "Highest combined value across prospect, fit, consensus, and availability."),
        })
        remaining = remaining[remaining["player_id"] != best["player_id"]]
        if remaining.empty:
            break

    return pd.DataFrame(rows)

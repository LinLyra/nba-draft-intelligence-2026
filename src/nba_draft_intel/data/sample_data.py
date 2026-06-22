import pandas as pd
from nba_draft_intel.config.paths import PROCESSED_DIR
from nba_draft_intel.utils.io import write_csv


def create_sample_processed_data() -> None:
    prospects = pd.DataFrame([
        {"player_id": "p001", "player_name": "AJ Dybantsa", "position": "Wing", "age": 19.0, "height_in": 80, "wingspan_in": 84, "prospect_value_manual": 96, "creation_score": 0.90, "shooting_score": 0.78, "defense_score": 0.72, "size_score": 0.88, "rim_score": 0.40, "ready_now_score": 0.70, "upside_score": 0.98, "avg_mock_pick": 1.4, "mock_std": 0.8},
        {"player_id": "p002", "player_name": "Darryn Peterson", "position": "Guard", "age": 19.0, "height_in": 77, "wingspan_in": 80, "prospect_value_manual": 94, "creation_score": 0.95, "shooting_score": 0.82, "defense_score": 0.62, "size_score": 0.70, "rim_score": 0.20, "ready_now_score": 0.76, "upside_score": 0.94, "avg_mock_pick": 2.1, "mock_std": 1.1},
        {"player_id": "p003", "player_name": "Cameron Boozer", "position": "Forward", "age": 19.0, "height_in": 81, "wingspan_in": 83, "prospect_value_manual": 93, "creation_score": 0.70, "shooting_score": 0.74, "defense_score": 0.78, "size_score": 0.86, "rim_score": 0.68, "ready_now_score": 0.88, "upside_score": 0.90, "avg_mock_pick": 3.0, "mock_std": 1.0},
        {"player_id": "p004", "player_name": "Caleb Wilson", "position": "Forward", "age": 19.0, "height_in": 82, "wingspan_in": 86, "prospect_value_manual": 89, "creation_score": 0.62, "shooting_score": 0.70, "defense_score": 0.82, "size_score": 0.92, "rim_score": 0.75, "ready_now_score": 0.72, "upside_score": 0.91, "avg_mock_pick": 4.5, "mock_std": 1.8},
        {"player_id": "p005", "player_name": "Nate Ament", "position": "Forward", "age": 19.0, "height_in": 81, "wingspan_in": 85, "prospect_value_manual": 88, "creation_score": 0.65, "shooting_score": 0.84, "defense_score": 0.72, "size_score": 0.86, "rim_score": 0.50, "ready_now_score": 0.68, "upside_score": 0.92, "avg_mock_pick": 5.2, "mock_std": 2.0},
    ])

    draft_order = pd.DataFrame([
        {"pick_number": 1, "current_owner": "Washington Wizards", "original_team": "Washington Wizards", "via_trade": False, "trade_risk_prior": 0.08},
        {"pick_number": 2, "current_owner": "Utah Jazz", "original_team": "Utah Jazz", "via_trade": False, "trade_risk_prior": 0.12},
        {"pick_number": 3, "current_owner": "Memphis Grizzlies", "original_team": "Memphis Grizzlies", "via_trade": False, "trade_risk_prior": 0.15},
        {"pick_number": 4, "current_owner": "Chicago Bulls", "original_team": "Chicago Bulls", "via_trade": False, "trade_risk_prior": 0.20},
        {"pick_number": 5, "current_owner": "LA Clippers", "original_team": "Indiana Pacers", "via_trade": True, "trade_risk_prior": 0.38},
    ])

    team_needs = pd.DataFrame([
        {"team": "Washington Wizards", "rebuild_stage": "deep_rebuild", "need_creation": 0.95, "need_shooting": 0.75, "need_defense": 0.70, "need_size": 0.80, "need_rim_protection": 0.40, "need_ready_now": 0.35, "need_upside": 0.98},
        {"team": "Utah Jazz", "rebuild_stage": "rebuild", "need_creation": 0.90, "need_shooting": 0.80, "need_defense": 0.65, "need_size": 0.65, "need_rim_protection": 0.40, "need_ready_now": 0.45, "need_upside": 0.90},
        {"team": "Memphis Grizzlies", "rebuild_stage": "retool", "need_creation": 0.60, "need_shooting": 0.75, "need_defense": 0.80, "need_size": 0.85, "need_rim_protection": 0.65, "need_ready_now": 0.75, "need_upside": 0.70},
        {"team": "Chicago Bulls", "rebuild_stage": "rebuild", "need_creation": 0.80, "need_shooting": 0.78, "need_defense": 0.70, "need_size": 0.75, "need_rim_protection": 0.60, "need_ready_now": 0.55, "need_upside": 0.85},
        {"team": "LA Clippers", "rebuild_stage": "transition", "need_creation": 0.70, "need_shooting": 0.88, "need_defense": 0.75, "need_size": 0.80, "need_rim_protection": 0.55, "need_ready_now": 0.85, "need_upside": 0.55},
    ])

    write_csv(prospects, PROCESSED_DIR / "prospects_2026_sample.csv")
    write_csv(draft_order, PROCESSED_DIR / "draft_order_2026_sample.csv")
    write_csv(team_needs, PROCESSED_DIR / "team_needs_2026_sample.csv")


if __name__ == "__main__":
    create_sample_processed_data()

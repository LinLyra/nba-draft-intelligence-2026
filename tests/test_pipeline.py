from nba_draft_intel.data.sample_data import create_sample_processed_data
from nba_draft_intel.config.paths import PROCESSED_DIR
from nba_draft_intel.data.loaders import load_prospects, load_draft_order, load_team_needs
from nba_draft_intel.models.prospect_value_model import score_prospects
from nba_draft_intel.models.trade_risk_model import score_trade_risk
from nba_draft_intel.features.team_fit_features import compute_team_fit_matrix
from nba_draft_intel.simulation.draft_simulator import run_draft_board


def test_sample_pipeline_runs():
    create_sample_processed_data()
    prospects = score_prospects(load_prospects(PROCESSED_DIR / "prospects_2026_sample.csv"))
    draft_order = score_trade_risk(load_draft_order(PROCESSED_DIR / "draft_order_2026_sample.csv"))
    team_needs = load_team_needs(PROCESSED_DIR / "team_needs_2026_sample.csv")
    team_fit = compute_team_fit_matrix(prospects, team_needs)
    board = run_draft_board(prospects, draft_order, team_fit)
    assert len(board) > 0
    assert "predicted_player" in board.columns

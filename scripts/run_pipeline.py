from nba_draft_intel.config.paths import PROCESSED_DIR, REPORTS_DIR
from nba_draft_intel.data.sample_data import create_sample_processed_data
from nba_draft_intel.data.loaders import load_prospects, load_draft_order, load_team_needs
from nba_draft_intel.models.prospect_value_model import score_prospects
from nba_draft_intel.models.trade_risk_model import score_trade_risk
from nba_draft_intel.features.team_fit_features import compute_team_fit_matrix
from nba_draft_intel.simulation.draft_simulator import run_draft_board
from nba_draft_intel.reports.report_builder import build_markdown_report
from nba_draft_intel.utils.io import write_csv


def main() -> None:
    create_sample_processed_data()

    prospects = load_prospects(PROCESSED_DIR / "prospects_2026_sample.csv")
    draft_order = load_draft_order(PROCESSED_DIR / "draft_order_2026_sample.csv")
    team_needs = load_team_needs(PROCESSED_DIR / "team_needs_2026_sample.csv")

    prospects_scored = score_prospects(prospects)
    draft_order_scored = score_trade_risk(draft_order)
    team_fit = compute_team_fit_matrix(prospects_scored, team_needs)
    board = run_draft_board(prospects_scored, draft_order_scored, team_fit)

    write_csv(board, REPORTS_DIR / "draft_board_2026_sample.csv")
    build_markdown_report(board, REPORTS_DIR / "final_report.md")
    print(board.to_string(index=False))
    print(f"\nSaved outputs to {REPORTS_DIR}")


if __name__ == "__main__":
    main()

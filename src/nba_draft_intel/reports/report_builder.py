from pathlib import Path
import pandas as pd


def build_markdown_report(draft_board: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# NBA Draft Intelligence 2026 — Analyst Report",
        "",
        "## Executive Summary",
        "This report presents an explainable first-round NBA Draft projection using prospect quality, team fit, mock-draft consensus, availability, and trade-risk scoring.",
        "",
        "## Projected Board",
        "",
        draft_board.to_markdown(index=False),
        "",
        "## Limitations",
        "- Sample data is placeholder until real 2026 prospect, combine, team, and mock-draft data is loaded.",
        "- Draft-night trades are modeled as risk, not exact transaction forecasts.",
        "- Confidence is currently a calibrated score proxy, not a bookmaker-grade probability.",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")

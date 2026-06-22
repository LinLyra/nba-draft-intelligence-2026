from pathlib import Path
import pandas as pd

from src.parsers.realgm_local_parser import parse_realgm_local_html


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS = PROJECT_ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)


SOURCES = {
    "historical_drafts_clean": PROCESSED / "historical_drafts_clean.csv",
    "pick_value_curve": PROCESSED / "pick_value_curve.csv",
    "prospect_master": PROCESSED / "prospect_master.csv",
    "tankathon_mock": PROCESSED / "mock_draft_2026_tankathon.csv",
    "realgm_pick_assets": PROCESSED / "pick_assets_realgm_local.csv",
    "combine_stats": PROCESSED / "combine_stats_2026.csv",
    "combine_anthro": PROCESSED / "combine_anthro_2026.csv",
}


def check_csv(name: str, path: Path) -> dict:
    if not path.exists():
        return {
            "source": name,
            "status": "missing",
            "path": str(path),
            "rows": 0,
            "columns": "",
        }

    try:
        df = pd.read_csv(path)
        return {
            "source": name,
            "status": "available",
            "path": str(path),
            "rows": len(df),
            "columns": ", ".join(df.columns[:12]),
        }
    except Exception as e:
        return {
            "source": name,
            "status": f"error: {e}",
            "path": str(path),
            "rows": 0,
            "columns": "",
        }


def main():
    print("=== Data Acquisition Pipeline ===")

    # RealGM fallback: parse local HTML if provided.
    parse_realgm_local_html()

    rows = []
    for name, path in SOURCES.items():
        rows.append(check_csv(name, path))

    status_df = pd.DataFrame(rows)
    out = REPORTS / "data_acquisition_status.csv"
    status_df.to_csv(out, index=False)

    print("\nData source status:")
    print(status_df.to_string(index=False))
    print("\nSaved:", out)

    critical = ["historical_drafts_clean", "prospect_master", "tankathon_mock"]
    missing_critical = status_df[
        (status_df["source"].isin(critical)) & (status_df["status"] != "available")
    ]

    if len(missing_critical) > 0:
        raise RuntimeError(
            "Critical data missing:\n"
            + missing_critical[["source", "status", "path"]].to_string(index=False)
        )

    print("\n[OK] Critical pipeline ready.")


if __name__ == "__main__":
    main()
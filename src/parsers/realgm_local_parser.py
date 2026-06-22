from pathlib import Path
from io import StringIO
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANUAL_HTML = PROJECT_ROOT / "data" / "manual" / "realgm_future_picks.html"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "pick_assets_realgm_local.csv"


def parse_realgm_local_html() -> pd.DataFrame | None:
    if not MANUAL_HTML.exists():
        print(f"[WARN] RealGM local HTML not found: {MANUAL_HTML}")
        return None

    html = MANUAL_HTML.read_text(encoding="utf-8", errors="ignore")
    tables = pd.read_html(StringIO(html))

    if not tables:
        print("[WARN] No tables found in RealGM local HTML.")
        return None

    frames = []
    for i, table in enumerate(tables):
        table = table.copy()
        table["source_table_id"] = i
        frames.append(table)

    df = pd.concat(frames, ignore_index=True, sort=False)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"[OK] RealGM local parsed: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    return df


if __name__ == "__main__":
    parse_realgm_local_html()
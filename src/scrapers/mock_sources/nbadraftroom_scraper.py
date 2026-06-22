from pathlib import Path
from io import StringIO
import re
import requests
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "data/raw/mock_sources"
OUTPUT_PATH = OUTPUT_DIR / "nba_draft_room.csv"
URL = "https://nbadraftroom.com/2026-nba-mock-draft/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
}

BAD = {"player", "player comp", "his", "comp", "team", "position", "school"}

def clean(x):
    return re.sub(r"\s+", " ", str(x)).strip()

def looks_like_player(x):
    x = clean(x)
    if not x or x.lower() in BAD:
        return False
    if any(bad in x.lower() for bad in ["player comp", "read more", "comments"]):
        return False
    return bool(re.match(r"^[A-Z][A-Za-z'\.-]+(?:\s+[A-Z][A-Za-z'\.-]+){1,3}$", x))

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    r = requests.get(URL, headers=HEADERS, timeout=30)
    print("Status:", r.status_code)
    r.raise_for_status()

    html = r.text
    (OUTPUT_DIR / "nba_draft_room_raw.html").write_text(html, encoding="utf-8")

    tables = pd.read_html(StringIO(html))
    print("Tables:", len(tables))

    records = []

    for ti, t in enumerate(tables):
        print(f"\n--- table {ti} columns ---")
        print(list(t.columns))

        t = t.copy()
        t.columns = [clean(c).lower() for c in t.columns]

        pick_col = None
        for c in t.columns:
            if c in ["pick", "#", "rk", "no."] or "pick" in c:
                pick_col = c
                break

        if pick_col is None:
            continue

        for _, row in t.iterrows():
            pick = pd.to_numeric(row.get(pick_col), errors="coerce")
            if pd.isna(pick) or not (1 <= int(pick) <= 60):
                continue

            candidates = []
            for c in t.columns:
                val = clean(row.get(c, ""))
                if looks_like_player(val):
                    candidates.append(val)

            if not candidates:
                continue

     
            player = candidates[0]

            records.append({
                "source": "nba_draft_room",
                "pick": int(pick),
                "team": None,
                "player": player
            })

    df = pd.DataFrame(records)

    if df.empty:
        print("[ERROR] No valid rows parsed.")
        return

    df = df.drop_duplicates(subset=["pick"], keep="first")
    df = df.sort_values("pick")
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved:", OUTPUT_PATH)
    print("Rows:", len(df))
    print(df.head(60).to_string(index=False))

if __name__ == "__main__":
    main()
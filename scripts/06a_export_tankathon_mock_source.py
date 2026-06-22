from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT = PROJECT_ROOT / "data/processed/mock_draft_2026_tankathon.csv"
OUTPUT_DIR = PROJECT_ROOT / "data/raw/mock_sources"
OUTPUT = OUTPUT_DIR / "tankathon.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

cols = ["pick", "team", "player"]
df = df[[c for c in cols if c in df.columns]].copy()

df["source"] = "tankathon"
df = df[["source", "pick", "team", "player"]]

df = df.dropna(subset=["pick", "player"])
df["pick"] = df["pick"].astype(int)

df.to_csv(OUTPUT, index=False)

print(f"Saved: {OUTPUT}")
print(df.head(30).to_string(index=False))
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data/processed/mock_sources_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/mock_sources_normalized.csv"

NORMALIZE_DICT = {
    "Acuff Jr.": "Darius Acuff Jr.",
    "Brown Jr.": "Mikel Brown Jr.",
    "Philon Jr.": "Labaron Philon Jr.",
    "Johnson Jr.": "Morez Johnson Jr.",
    "Reed Jr.": "Tarris Reed Jr.",
    "Karim Lopez": "Karim López",
}


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    original_player = df["player"].astype(str).str.strip()

    df["player"] = original_player.replace(NORMALIZE_DICT)

    changed_rows = int((original_player != df["player"]).sum())

    dup_counts = (
        df.groupby("player")
        .size()
        .sort_values(ascending=False)
        .head(15)
        .reset_index(name="row_count")
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"changed rows: {changed_rows}")
    print()
    print("top duplicated players after normalization:")
    print(dup_counts.to_string(index=False))
    print()
    print(df.head(20).to_string(index=False))
    print()
    print("saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()

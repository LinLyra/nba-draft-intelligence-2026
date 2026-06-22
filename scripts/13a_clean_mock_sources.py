from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data/raw/mock_sources"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/mock_sources_clean.csv"

KEEP_SOURCES = {
    "tankathon",
    "cbs_final",
    "bleacher",
    "espn",
    "athletic",
    "nbadraftnet",
    "hoopshq",
    "netscouts",
    "sb_nation",
    "usa_today_ftw",
}

EXCLUDE_SOURCES = {
    "cbs",
    "bleacher_report",
    "nba_com_consensus",
    "yahoo",
}

OUTPUT_COLS = ["source", "pick", "team", "player"]


def load_source(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    source_name = path.stem

    if source_name in EXCLUDE_SOURCES:
        return pd.DataFrame(columns=OUTPUT_COLS)

    if source_name not in KEEP_SOURCES:
        return pd.DataFrame(columns=OUTPUT_COLS)

    if "source" not in df.columns:
        df["source"] = source_name
    else:
        df["source"] = df["source"].fillna(source_name).astype(str).str.strip()
        df.loc[df["source"].eq("") | df["source"].eq("nan"), "source"] = source_name

    for col in OUTPUT_COLS:
        if col not in df.columns:
            df[col] = pd.NA

    df = df[OUTPUT_COLS].copy()
    df["pick"] = pd.to_numeric(df["pick"], errors="coerce")
    df["team"] = df["team"].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA})
    df["player"] = df["player"].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA})

    df = df.dropna(subset=["pick", "player"])
    df = df[(df["pick"] >= 1) & (df["pick"] <= 60)]
    df["pick"] = df["pick"].astype(int)
    df = df.drop_duplicates(subset=["source", "pick"], keep="first")

    return df.reset_index(drop=True)


def main() -> None:
    frames = []

    for path in sorted(RAW_DIR.glob("*.csv")):
        df = load_source(path)
        if df.empty:
            print(f"[SKIP] {path.name}")
            continue
        frames.append(df)
        print(f"[KEEP] {path.name} rows={len(df)}")

    if not frames:
        raise RuntimeError("No mock source files kept after cleaning.")

    clean = pd.concat(frames, ignore_index=True)
    clean = clean.sort_values(["source", "pick"]).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUTPUT_PATH, index=False)

    source_count = clean["source"].nunique()
    row_count = len(clean)

    print()
    print(f"source count: {source_count}")
    print(f"row count: {row_count}")
    print()
    print(clean.head(20).to_string(index=False))
    print()
    print("saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()

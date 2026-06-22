from pathlib import Path
import time
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data/raw/nba_combine"
PROCESSED_DIR = PROJECT_ROOT / "data/processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

SEASONS = ["2025-26", "2024-25", "2023-24", "2022-23", "2021-22", "2020-21"]


def save(df, name):
    raw = RAW_DIR / f"{name}.csv"
    processed = PROCESSED_DIR / f"{name}.csv"
    df.to_csv(raw, index=False)
    df.to_csv(processed, index=False)
    print(f"[OK] {name}: rows={len(df)}")
    print(processed)


def fetch_with_nba_api():
    from nba_api.stats.endpoints import (
        draftcombinestats,
        draftcombineplayeranthro,
        draftcombinedrillresults,
        draftcombinespotshooting,
        draftcombinenonstationaryshooting,
    )

    all_stats = []
    all_anthro = []
    all_drills = []
    all_spot = []
    all_motion = []

    for season in SEASONS:
        print(f"\n=== Season {season} ===")

        try:
            df = draftcombinestats.DraftCombineStats(
                league_id="00",
                season_year=season,
                timeout=90,
            ).get_data_frames()[0]
            df["SEASON_YEAR"] = season
            all_stats.append(df)
            print("stats", len(df))
            time.sleep(2)
        except Exception as e:
            print("[WARN] stats failed:", e)

        try:
            df = draftcombineplayeranthro.DraftCombinePlayerAnthro(
                league_id="00",
                season_year=season,
                timeout=90,
            ).get_data_frames()[0]
            df["SEASON_YEAR"] = season
            all_anthro.append(df)
            print("anthro", len(df))
            time.sleep(2)
        except Exception as e:
            print("[WARN] anthro failed:", e)

        try:
            df = draftcombinedrillresults.DraftCombineDrillResults(
                league_id="00",
                season_year=season,
                timeout=90,
            ).get_data_frames()[0]
            df["SEASON_YEAR"] = season
            all_drills.append(df)
            print("drills", len(df))
            time.sleep(2)
        except Exception as e:
            print("[WARN] drills failed:", e)

        try:
            df = draftcombinespotshooting.DraftCombineSpotShooting(
                league_id="00",
                season_year=season,
                timeout=90,
            ).get_data_frames()[0]
            df["SEASON_YEAR"] = season
            all_spot.append(df)
            print("spot shooting", len(df))
            time.sleep(2)
        except Exception as e:
            print("[WARN] spot shooting failed:", e)

        try:
            df = draftcombinenonstationaryshooting.DraftCombineNonStationaryShooting(
                league_id="00",
                season_year=season,
                timeout=90,
            ).get_data_frames()[0]
            df["SEASON_YEAR"] = season
            all_motion.append(df)
            print("motion shooting", len(df))
            time.sleep(2)
        except Exception as e:
            print("[WARN] motion shooting failed:", e)

    if all_stats:
        save(pd.concat(all_stats, ignore_index=True), "combine_stats_all")
        save(all_stats[0], "combine_stats_2026")

    if all_anthro:
        save(pd.concat(all_anthro, ignore_index=True), "combine_anthro_all")
        save(all_anthro[0], "combine_anthro_2026")

    if all_drills:
        save(pd.concat(all_drills, ignore_index=True), "combine_drills_all")

    if all_spot:
        save(pd.concat(all_spot, ignore_index=True), "combine_spot_shooting_all")

    if all_motion:
        save(pd.concat(all_motion, ignore_index=True), "combine_motion_shooting_all")


if __name__ == "__main__":
    fetch_with_nba_api()
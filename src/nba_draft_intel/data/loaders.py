from pathlib import Path
import pandas as pd


def load_table(path: str | Path, required_columns: list[str] | None = None) -> pd.DataFrame:
    df = pd.read_csv(path)
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")
    return df


def load_prospects(path: str | Path) -> pd.DataFrame:
    return load_table(path, ["player_id", "player_name", "position"])


def load_draft_order(path: str | Path) -> pd.DataFrame:
    return load_table(path, ["pick_number", "current_owner"])


def load_team_needs(path: str | Path) -> pd.DataFrame:
    return load_table(path, ["team", "need_creation", "need_shooting", "need_defense"])

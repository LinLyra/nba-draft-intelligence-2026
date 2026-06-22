import numpy as np
import pandas as pd


def add_mock_consensus_score(prospects: pd.DataFrame, pick_number: int) -> pd.DataFrame:
    df = prospects.copy()
    if "avg_mock_pick" not in df.columns:
        df["mock_consensus_score"] = 0.5
        return df
    distance = (df["avg_mock_pick"] - pick_number).abs()
    uncertainty = df.get("mock_std", pd.Series(1.0, index=df.index)).clip(lower=0.5)
    df["mock_consensus_score"] = np.exp(-(distance / (2.0 * uncertainty + 1e-6)))
    return df

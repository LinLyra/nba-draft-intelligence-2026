import pandas as pd


def minmax(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    if s.max() == s.min():
        return pd.Series(0.5, index=s.index)
    scaled = (s - s.min()) / (s.max() - s.min())
    return scaled if higher_is_better else 1 - scaled


def build_prospect_features(prospects: pd.DataFrame) -> pd.DataFrame:
    df = prospects.copy()
    if "prospect_value_manual" in df.columns:
        df["prospect_value_score"] = df["prospect_value_manual"] / 100
    else:
        components = []
        for col in ["height_in", "wingspan_in", "ts_pct", "ast_pct", "stl_pct", "blk_pct"]:
            if col in df.columns:
                components.append(minmax(df[col]))
        if "age" in df.columns:
            components.append(minmax(df["age"], higher_is_better=False))
        df["prospect_value_score"] = sum(components) / max(len(components), 1)
    return df

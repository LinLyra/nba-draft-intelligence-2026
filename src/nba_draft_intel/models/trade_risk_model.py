import pandas as pd


def score_trade_risk(draft_order: pd.DataFrame) -> pd.DataFrame:
    df = draft_order.copy()
    base = df.get("trade_risk_prior", pd.Series(0.15, index=df.index)).astype(float)
    if "via_trade" in df.columns:
        base = base + df["via_trade"].astype(int) * 0.08
    df["trade_risk_score"] = base.clip(0, 1)
    df["trade_risk_label"] = pd.cut(
        df["trade_risk_score"],
        bins=[-0.01, 0.20, 0.40, 1.0],
        labels=["Low", "Medium", "High"],
    )
    return df

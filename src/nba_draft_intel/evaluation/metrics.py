import pandas as pd


def evaluate_draft_predictions(predictions: pd.DataFrame, actuals: pd.DataFrame) -> dict:
    merged = predictions.merge(actuals, on="predicted_player", how="left", suffixes=("_pred", "_actual"))
    if "pick_number_actual" not in merged.columns:
        return {"note": "Actual pick numbers unavailable."}
    error = (merged["pick_number_pred"] - merged["pick_number_actual"]).abs()
    return {
        "mean_absolute_pick_error": float(error.mean()),
        "top_3_range_accuracy": float((error <= 3).mean()),
        "top_5_range_accuracy": float((error <= 5).mean()),
    }

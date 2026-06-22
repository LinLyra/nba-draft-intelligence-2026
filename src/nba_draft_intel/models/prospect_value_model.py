import pandas as pd
from nba_draft_intel.features.prospect_features import build_prospect_features


def score_prospects(prospects: pd.DataFrame) -> pd.DataFrame:
    return build_prospect_features(prospects)

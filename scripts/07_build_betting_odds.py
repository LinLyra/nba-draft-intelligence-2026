from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "data/processed/betting_odds_2026.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

# True public odds snapshots from sportsbook/search-visible pages.
# Sources:
# FanDuel: Dybantsa -425, Peterson +330, Boozer +3500
# Sportsbet: Dybantsa 1.17, Peterson 4.20, Boozer 34.00
rows = [
    {"source": "fanduel", "market": "number_1_overall", "player": "AJ Dybantsa", "american_odds": -425, "decimal_odds": None},
    {"source": "fanduel", "market": "number_1_overall", "player": "Darryn Peterson", "american_odds": 330, "decimal_odds": None},
    {"source": "fanduel", "market": "number_1_overall", "player": "Cameron Boozer", "american_odds": 3500, "decimal_odds": None},

    {"source": "sportsbet", "market": "number_1_overall", "player": "AJ Dybantsa", "american_odds": None, "decimal_odds": 1.17},
    {"source": "sportsbet", "market": "number_1_overall", "player": "Darryn Peterson", "american_odds": None, "decimal_odds": 4.20},
    {"source": "sportsbet", "market": "number_1_overall", "player": "Cameron Boozer", "american_odds": None, "decimal_odds": 34.00},
    {"source": "sportsbet", "market": "number_1_overall", "player": "Caleb Wilson", "american_odds": None, "decimal_odds": 101.00},
    {"source": "sportsbet", "market": "number_1_overall", "player": "Darius Acuff Jr.", "american_odds": None, "decimal_odds": 201.00},

    {"source": "sportsbet", "market": "number_2_overall", "player": "Darryn Peterson", "american_odds": None, "decimal_odds": 1.67},
    {"source": "sportsbet", "market": "number_2_overall", "player": "Cameron Boozer", "american_odds": None, "decimal_odds": 3.10},
    {"source": "sportsbet", "market": "number_2_overall", "player": "AJ Dybantsa", "american_odds": None, "decimal_odds": 5.00},
    {"source": "sportsbet", "market": "number_2_overall", "player": "Caleb Wilson", "american_odds": None, "decimal_odds": 51.00},
    {"source": "sportsbet", "market": "number_2_overall", "player": "Darius Acuff Jr.", "american_odds": None, "decimal_odds": 176.00},
]

df = pd.DataFrame(rows)

def american_to_implied_prob(odds):
    if pd.isna(odds):
        return None
    odds = float(odds)
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    return 100 / (odds + 100)

def decimal_to_implied_prob(odds):
    if pd.isna(odds):
        return None
    return 1 / float(odds)

df["implied_prob"] = df.apply(
    lambda r: american_to_implied_prob(r["american_odds"])
    if pd.notna(r["american_odds"])
    else decimal_to_implied_prob(r["decimal_odds"]),
    axis=1
)

# Remove bookmaker overround within each source-market
df["fair_prob"] = df.groupby(["source", "market"])["implied_prob"].transform(
    lambda s: s / s.sum()
)

consensus = (
    df.groupby(["market", "player"])
    .agg(
        avg_fair_prob=("fair_prob", "mean"),
        max_fair_prob=("fair_prob", "max"),
        source_count=("source", "nunique"),
    )
    .reset_index()
    .sort_values(["market", "avg_fair_prob"], ascending=[True, False])
)

df.to_csv(OUT, index=False)
consensus.to_csv(PROJECT_ROOT / "data/processed/betting_consensus_2026.csv", index=False)

print("Saved:", OUT)
print(consensus.to_string(index=False))
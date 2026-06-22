from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(PROJECT_ROOT / "data/processed/mock_consensus_2026.csv")

cols = ["player", "avg_pick", "median_pick", "std_pick", "min_pick", "max_pick", "source_count"]
report = df[cols].sort_values("std_pick", ascending=False)

out = PROJECT_ROOT / "reports/mock_uncertainty_report.csv"
out.parent.mkdir(parents=True, exist_ok=True)
report.to_csv(out, index=False)

print("Most uncertain prospects:")
print(report.head(15).to_string(index=False))
print("\nMost stable prospects:")
print(df[cols].sort_values("std_pick").head(10).to_string(index=False))
print("\nSaved:", out)
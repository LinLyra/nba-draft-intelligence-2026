from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "data/raw/mock_sources/cbs_final.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

rows = [
    (1, "Wizards", "AJ Dybantsa"),
    (2, "Jazz", "Darryn Peterson"),
    (3, "Grizzlies", "Cameron Boozer"),
    (4, "Bulls", "Caleb Wilson"),
    (5, "Clippers", "Keaton Wagler"),
    (6, "Nets", "Darius Acuff Jr."),
    (7, "Kings", "Mikel Brown Jr."),
    (8, "Hawks", "Kingston Flemings"),
    (9, "Mavericks", "Brayden Burries"),
    (10, "Bucks", "Nate Ament"),
    (11, "Warriors", "Yaxel Lendeborg"),
    (12, "Thunder", "Aday Mara"),
    (13, "Heat", "Labaron Philon Jr."),
    (14, "Hornets", "Morez Johnson Jr."),
    (15, "Bulls", "Hannes Steinbach"),
    (16, "Grizzlies", "Dailyn Swain"),
    (17, "Thunder", "Christian Anderson"),
    (18, "Hornets", "Cameron Carr"),
    (19, "Raptors", "Jayden Quaintance"),
    (20, "Spurs", "Karim Lopez"),
    (21, "Pistons", "Bennett Stirtz"),
    (22, "76ers", "Chris Cenac Jr."),
    (23, "Hawks", "Tarris Reed Jr."),
    (24, "Knicks", "Maleek Thomas"),
    (25, "Lakers", "Allen Graves"),
    (26, "Nuggets", "Ebuka Okorie"),
    (27, "Celtics", "Henri Veesaar"),
    (28, "Timberwolves", "Koa Peat"),
    (29, "Cavaliers", "Joshua Jefferson"),
    (30, "Mavericks", "Isaiah Evans"),
]

df = pd.DataFrame(rows, columns=["pick", "team", "player"])
df.insert(0, "source", "cbs_final")
df.to_csv(OUT, index=False)

print("Saved:", OUT)
print(df.to_string(index=False))
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT = PROJECT_ROOT / "data/raw/mock_sources"
OUT.mkdir(parents=True, exist_ok=True)

sources = {
    "nba_com_consensus": [
        "AJ Dybantsa","Cameron Boozer","Darryn Peterson","Caleb Wilson","Darius Acuff Jr.",
        "Keaton Wagler","Mikel Brown Jr.","Brayden Burries","Karim López","Kingston Flemings",
        "Aday Mara","Yaxel Lendeborg","Hannes Steinbach","Morez Johnson Jr."
    ],
    "bleacher_report": [
        "AJ Dybantsa","Darryn Peterson","Cameron Boozer","Caleb Wilson","Keaton Wagler",
        "Darius Acuff Jr.","Kingston Flemings","Mikel Brown Jr.","Brayden Burries","Nate Ament",
        "Karim López","Aday Mara","Cameron Carr","Yaxel Lendeborg"
    ],
    "cbs": [
        "AJ Dybantsa","Darryn Peterson","Cameron Boozer","Caleb Wilson","Keaton Wagler",
        "Mikel Brown Jr.","Darius Acuff Jr.","Kingston Flemings","Brayden Burries","Nate Ament",
        "Yaxel Lendeborg","Aday Mara","Hannes Steinbach","Morez Johnson Jr."
    ],
    "netscouts": [
        "AJ Dybantsa","Darryn Peterson","Cameron Boozer","Caleb Wilson","Keaton Wagler",
        "Darius Acuff Jr.","Mikel Brown Jr.","Aday Mara","Kingston Flemings","Brayden Burries",
        "Yaxel Lendeborg","Nate Ament","Labaron Philon Jr.","Morez Johnson Jr."
    ],
    "hoopshq": [
        "AJ Dybantsa","Darryn Peterson","Cameron Boozer","Caleb Wilson","Mikel Brown Jr.",
        "Darius Acuff Jr.","Kingston Flemings","Aday Mara","Keaton Wagler","Brayden Burries",
        "Nate Ament","Yaxel Lendeborg","Labaron Philon Jr.","Morez Johnson Jr."
    ],
    "sb_nation": [
        "AJ Dybantsa","Darryn Peterson","Cameron Boozer","Caleb Wilson","Keaton Wagler",
        "Nate Ament","Darius Acuff Jr.","Mikel Brown Jr.","Brayden Burries","Labaron Philon Jr.",
        "Yaxel Lendeborg","Aday Mara","Karim López","Morez Johnson Jr."
    ],
    "usa_today_ftw": [
        "AJ Dybantsa","Cameron Boozer","Darryn Peterson","Caleb Wilson","Keaton Wagler",
        "Mikel Brown Jr.","Darius Acuff Jr.","Brayden Burries","Kingston Flemings","Yaxel Lendeborg",
        "Karim López","Nate Ament","Hannes Steinbach","Morez Johnson Jr."
    ],
}

for source, players in sources.items():
    df = pd.DataFrame({
        "source": source,
        "pick": range(1, len(players) + 1),
        "team": None,
        "player": players,
    })
    path = OUT / f"{source}.csv"
    df.to_csv(path, index=False)
    print(f"saved {path} rows={len(df)}")
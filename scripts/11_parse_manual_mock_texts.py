from pathlib import Path
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = PROJECT_ROOT / "data/manual/mock_texts"
OUT_DIR = PROJECT_ROOT / "data/raw/mock_sources"
OUT_DIR.mkdir(parents=True, exist_ok=True)

KNOWN_PLAYERS = [
    "AJ Dybantsa", "Darryn Peterson", "Cameron Boozer", "Caleb Wilson",
    "Keaton Wagler", "Darius Acuff Jr.", "Mikel Brown Jr.", "Kingston Flemings",
    "Brayden Burries", "Nate Ament", "Aday Mara", "Yaxel Lendeborg",
    "Karim López", "Karim Lopez", "Labaron Philon Jr.", "Morez Johnson Jr.",
    "Hannes Steinbach", "Cameron Carr", "Jayden Quaintance", "Bennett Stirtz",
    "Chris Cenac Jr.", "Tarris Reed Jr.", "Maleek Thomas", "Allen Graves",
    "Ebuka Okorie", "Henri Veesaar", "Koa Peat", "Isaiah Evans",
    "Joshua Jefferson", "Christian Anderson", "Dailyn Swain"
]

TEAMS = [
    "Wizards","Jazz","Grizzlies","Bulls","Clippers","Nets","Kings","Hawks",
    "Mavericks","Bucks","Warriors","Thunder","Heat","Hornets","Raptors",
    "Spurs","Pistons","76ers","Knicks","Lakers","Nuggets","Celtics",
    "Timberwolves","Cavaliers"
]

def clean(x):
    return re.sub(r"\s+", " ", str(x)).strip()

def parse_file(path: Path):
    source = path.stem
    text = clean(path.read_text(encoding="utf-8", errors="ignore"))
    rows = []

    for player in KNOWN_PLAYERS:
        if player not in text:
            continue

        idx = text.find(player)
        window = text[max(0, idx-120):idx+120]

        pick = None
        team = None

        pick_match = re.search(r"(?:Pick|No\.|#)?\s*(\d{1,2})", window)
        if pick_match:
            p = int(pick_match.group(1))
            if 1 <= p <= 60:
                pick = p

        for t in TEAMS:
            if t in window:
                team = t
                break

        if pick:
            rows.append({
                "source": source,
                "pick": pick,
                "team": team,
                "player": player.replace("Karim Lopez", "Karim López")
            })

    df = pd.DataFrame(rows)

    if df.empty:
        print(f"[WARN] no rows parsed: {path.name}")
        return

    df = df.sort_values("pick").drop_duplicates(subset=["pick"], keep="first")
    out = OUT_DIR / f"{source}.csv"
    df.to_csv(out, index=False)

    print(f"[OK] {path.name} -> {out} rows={len(df)}")
    print(df.head(30).to_string(index=False))

def main():
    for path in TEXT_DIR.glob("*.txt"):
        parse_file(path)

if __name__ == "__main__":
    main()
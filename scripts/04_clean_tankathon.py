from pathlib import Path
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "prospects_2026_tankathon.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "prospect_master.csv"

df = pd.read_csv(INPUT_PATH)
df["raw_text"] = df["raw_text"].astype(str)

POSITION_PATTERN = r"(PG/SG|SG/PG|SF/PF|PF/C|SG/SF|PG|SG|SF|PF|C)"
HEIGHT_PATTERN = r"(\d+'\d+(?:\.\d+)?)"
WEIGHT_PATTERN = r"(\d{3})\s*lbs"

def clean_text(x):
    return re.sub(r"\s+", " ", str(x)).strip()

def parse_row(raw):
    raw = clean_text(raw)

    rank_match = re.match(r"^(\d+)\s+", raw)
    rank = int(rank_match.group(1)) if rank_match else None

    no_rank = re.sub(r"^\d+\s+", "", raw)

    # name + position + school before height
    main_match = re.search(
        rf"^(.*?)\s+{POSITION_PATTERN}\s+\|\s+(.*?)\s+{HEIGHT_PATTERN}\s+{WEIGHT_PATTERN}",
        no_rank,
    )

    player = position = school = height = weight_lbs = None

    if main_match:
        player = main_match.group(1).strip()
        position = main_match.group(2).strip()
        school = main_match.group(3).strip()
        height = main_match.group(4).strip()
        weight_lbs = float(main_match.group(5))
    else:
        # fallback: sometimes missing clean school split
        pos_match = re.search(POSITION_PATTERN, no_rank)
        if pos_match:
            position = pos_match.group(1)
            player = no_rank[:pos_match.start()].strip()

        height_match = re.search(HEIGHT_PATTERN, no_rank)
        if height_match:
            height = height_match.group(1)

        weight_match = re.search(WEIGHT_PATTERN, no_rank)
        if weight_match:
            weight_lbs = float(weight_match.group(1))

    def extract_float(pattern):
        m = re.search(pattern, raw)
        return float(m.group(1)) if m else None

    age = extract_float(r"(\d+\.\d+)\s*yrs")
    ppg = extract_float(r"(\d+\.\d+)\s*pts")
    rpg = extract_float(r"pts\s+(\d+\.\d+)\s*reb")
    apg = extract_float(r"reb\s+(\d+\.\d+)\s*ast")
    bpg = extract_float(r"ast\s+(\d+\.\d+)\s*blk")
    spg = extract_float(r"blk\s+(\d+\.\d+)\s*stl")
    ts_pct = extract_float(r"(\d+\.\d+)\s*TS%")
    usg_pct = extract_float(r"(\d+\.\d+)\s*USG")
    obpm = extract_float(r"(-?\d+\.\d+)\s*OBPM")
    dbpm = extract_float(r"(-?\d+\.\d+)\s*DBPM")

    return {
        "rank": rank,
        "player": player,
        "position": position,
        "school_or_league": school,
        "height": height,
        "weight_lbs": weight_lbs,
        "age": age,
        "ppg": ppg,
        "rpg": rpg,
        "apg": apg,
        "spg": spg,
        "bpg": bpg,
        "ts_pct": ts_pct,
        "usg_pct": usg_pct,
        "obpm": obpm,
        "dbpm": dbpm,
        "raw_text": raw,
    }

parsed = pd.DataFrame([parse_row(x) for x in df["raw_text"]])

# height inches
def height_to_inches(h):
    if pd.isna(h) or h is None:
        return None
    m = re.search(r"(\d+)'(\d+(?:\.\d+)?)", str(h))
    if not m:
        return None
    return int(m.group(1)) * 12 + float(m.group(2))

parsed["height_inches"] = parsed["height"].apply(height_to_inches)

# broad position group
def position_group(pos):
    if pd.isna(pos) or pos is None:
        return "Unknown"
    pos = str(pos)
    if "PG" in pos or "SG" in pos:
        return "Guard"
    if "SF" in pos:
        return "Wing"
    if "PF" in pos or pos == "C":
        return "Big"
    return "Unknown"

parsed["position_group"] = parsed["position"].apply(position_group)

# basic data quality flags
parsed["has_core_profile"] = (
    parsed["player"].notna()
    & parsed["position"].notna()
    & parsed["height"].notna()
    & parsed["weight_lbs"].notna()
)

parsed["has_box_score"] = (
    parsed["ppg"].notna()
    & parsed["rpg"].notna()
    & parsed["apg"].notna()
)

parsed = parsed.sort_values("rank").reset_index(drop=True)
parsed.to_csv(OUTPUT_PATH, index=False)

print("Saved to:", OUTPUT_PATH)
print("Rows:", len(parsed))
print("Core profile parsed:", parsed["has_core_profile"].sum())
print("Box score parsed:", parsed["has_box_score"].sum())
print(parsed.head(30).to_string(index=False))
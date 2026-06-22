from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MOCK_DIR = PROJECT_ROOT / "data/raw/mock_sources"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/mock_consensus_2026.csv"


def load_all_mock_sources():

    dfs=[]

    csv_files=list(MOCK_DIR.glob("*.csv"))

    print(f"Found {len(csv_files)} sources")

    for file in csv_files:

        try:

            df=pd.read_csv(file)

            df["source_file"]=file.stem

            dfs.append(df)

            print(f"Loaded {file.name} rows={len(df)}")

        except Exception as e:

            print(file,e)

    if len(dfs)==0:
        raise RuntimeError("No mock source csv found")

    return pd.concat(dfs,ignore_index=True)


def build_consensus(df):

    consensus=(

        df.groupby("player")

        .agg(

            avg_pick=("pick","mean"),

            median_pick=("pick","median"),

            std_pick=("pick","std"),

            min_pick=("pick","min"),

            max_pick=("pick","max"),

            source_count=("source_file","nunique")

        )

        .reset_index()

    )

    team_mode=(

        df.groupby("player")["team"]

        .agg(lambda x:x.mode().iloc[0] if len(x.mode())>0 else None)

        .reset_index()

        .rename(columns={"team":"most_common_team"})

    )

    consensus=consensus.merge(team_mode,on="player")

    consensus["consensus_score"]=(

        100

        -consensus["avg_pick"]

        +2*consensus["source_count"]

    )

    consensus=consensus.sort_values(

        "avg_pick"

    ).reset_index(drop=True)

    return consensus


if __name__=="__main__":

    raw_df=load_all_mock_sources()

    consensus_df=build_consensus(raw_df)

    consensus_df.to_csv(

        OUTPUT_PATH,

        index=False

    )

    print()

    print(consensus_df.head(30))

    print()

    print("saved to")

    print(OUTPUT_PATH)
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from nba_draft_intel.config.paths import REPORTS_DIR  # noqa: E402

st.set_page_config(page_title="NBA Draft Intelligence 2026", layout="wide")
st.title("NBA Draft Intelligence 2026")
st.caption("Explainable draft-board projection: prospect value × team fit × consensus × trade risk")

board_path = REPORTS_DIR / "draft_board_2026_sample.csv"
if not board_path.exists():
    st.warning("Run `python scripts/run_pipeline.py` first.")
    st.stop()

board = pd.read_csv(board_path)
st.dataframe(board, use_container_width=True)

team = st.selectbox("Select team", board["team"].unique())
row = board[board["team"] == team].iloc[0]

st.subheader(f"Pick #{row['pick_number']} — {team}")
st.metric("Predicted Player", row["predicted_player"])
st.metric("Confidence Proxy", row["confidence_proxy"])
st.write("**Alternatives:**", row["alternatives"])
st.write("**Reason:**", row["reason"])

# NBA Draft Intelligence System

Probabilistic NBA Draft forecasting for the 2026 class — multi-source consensus, betting markets, team-fit modeling, and Monte Carlo simulation, with a Next.js analytics frontend.

## What it is

An end-to-end **Draft Intelligence System** that estimates where prospects land, how confident we are, and what alternatives exist at each pick. Built for sports analytics research and interactive exploration, not a single deterministic ranking.

## Stack

- **Python** — scrapers, consensus, team fit, calibrated Monte Carlo
- **Next.js** — board, player scout reports, team fits, draft simulator

## Quick start

```bash
pip install -r requirements.txt
node web/scripts/build-data.mjs
PYTHONPATH=. python scripts/20_build_player_media.py
cd web && npm install && npm run dev
```

## Deploy

Vercel → import repo → **Root Directory:** `web`

## Author

**LLyra** · [GitHub](https://github.com/LinLyra/nba-draft-intelligence-2026)

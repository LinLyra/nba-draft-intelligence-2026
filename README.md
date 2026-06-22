# NBA Draft Intelligence System (DIS)

**AI-powered probabilistic NBA Draft forecasting platform** — integrating multi-source consensus, betting markets, player archetypes, team-fit optimization, and Monte Carlo simulation to estimate draft outcomes **and uncertainty**.

> Portfolio / research project · 2026 NBA Draft · [Live demo on Vercel](#deploy) (after you connect the repo)

---

## Why this project

This is not a single CSV or a black-box pick list. It is an end-to-end **Draft Intelligence System**:

| Layer | What it does |
|-------|----------------|
| Data engineering | Scrapers, normalization, prospect DB, mock sources, betting odds |
| Information fusion | Source-weighted robust consensus (trimmed mean) |
| Sports analytics | Archetype scores, team needs, fit engine |
| Probabilistic modeling | Calibrated Monte Carlo (20,000 sims) |
| Product | Next.js web app — board, player scout reports, simulator |

**Keywords:** uncertainty · probability · information aggregation · simulation · market efficiency

---

## Architecture

```text
15 Mock Sources
        ↓
Name Normalization
        ↓
Source-Weighted Robust Consensus (trimmed mean)
        ↓
Betting Odds Layer (#1 / #2)
        ↓
Team Fit Engine (archetype × needs)
        ↓
Calibrated Monte Carlo (20,000 simulations)
        ↓
Probability Board + Volatility + Alternatives
        ↓
Next.js Web App (Vercel)
```

### Model weights (script 17)

- 60% consensus (trimmed mean location prior)
- 12% source reliability
- 18% betting odds (picks 1–2 only)
- 10% team fit

Calibration: uncertainty penalty, single-source spike control, pick-dependent softmax temperature, candidate pool window.

---

## Features

- Multi-source mock aggregation (8 weighted sources)
- Source-weighted robust consensus + volatility report
- Betting market integration
- Team fit engine (creation / shooting / size / defense / upside / NBA-ready)
- Calibrated Monte Carlo draft simulator
- Backtest framework (2019–2025 placeholders + 2026 eval template)
- **Web UI:** Top-30 board, player scout pages, team fits, simulator, methodology

---

## Example outputs

| Player | Pick | Probability | Volatility |
|--------|------|-------------|------------|
| AJ Dybantsa | #1 | 99.9% | Low |
| Darryn Peterson | #2 | 99.5% | Low |
| Cameron Boozer | #3 | 98.9% | Low |
| Keaton Wagler | #5 | ~69% | Medium |

Wagler at #5 is intentional — multiple credible mocks cluster him there; Monte Carlo reflects alternatives (Acuff, Brown, Flemings).

---

## Repository layout

```text
nba-draft-intelligence-2026/
├── src/
│   ├── scrapers/          # Tankathon, RealGM, NBA Combine, Basketball Reference, mock sources
│   └── nba_draft_intel/   # Core package (loaders, features, simulation, evaluation)
├── scripts/               # 01–20 pipeline scripts (fully open)
├── web/                   # Next.js frontend → Vercel
│   ├── app/               # Board, players, teams, simulator, methodology
│   └── public/data/       # JSON exports for static deploy
├── config/                # Example configs (e.g. source_weights.example.csv)
├── tests/
└── docs/
```

### What is **open** (~80%)

- All `scripts/` (01–20)
- All `src/` scrapers and core package
- Full `web/` frontend
- `web/public/data/*.json` (model outputs for demo deploy)
- README, tests, example configs

### What stays **private** (gitignored)

- `data/raw/` — scraped HTML/CSV
- `data/manual/` — mock text files, manual weights, RealGM HTML
- `data/processed/*.csv` — large tables (rebuild locally)
- `.env` / API keys
- `reports/*.csv` generated locally

Clone the repo → run scrapers + pipeline → reproduce the system. Raw third-party dumps are not redistributed.

---

## Quick start (Python pipeline)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1) Scrape / acquire data (writes to data/raw — local only)
PYTHONPATH=src python src/scrapers/tankathon_scraper.py

# 2) Copy example source weights to manual folder
mkdir -p data/manual
cp config/source_weights.example.csv data/manual/source_weights.csv

# 3) Run core modeling scripts (after you have processed inputs)
PYTHONPATH=. python scripts/13b_normalize_player_names.py
PYTHONPATH=. python scripts/18_source_weighted_consensus.py
PYTHONPATH=. python scripts/15_team_fit_engine.py
PYTHONPATH=. python scripts/17_calibrated_monte_carlo.py

# 4) Export JSON for web
node web/scripts/build-data.mjs
PYTHONPATH=. python scripts/20_build_player_media.py   # ESPN headshots + school logos
```

Official 2026 board: `data/processed/final_calibrated_monte_carlo_board_2026.csv` (local).

---

## Quick start (Web app)

```bash
node web/scripts/build-data.mjs
cd web && npm install && npm run dev
```

Open http://localhost:3000

Pages: `/` · `/players/aj-dybantsa` · `/teams/clippers` · `/simulator` · `/methodology`

Logos: NBA (`cdn.nba.com`), schools (Tankathon NCAA CDN), player headshots (ESPN CDN via `player_media.json`).

---

## Deploy {#deploy}

### Vercel

1. Push this repo to GitHub
2. Vercel → New Project → import repo
3. **Root Directory:** `web`
4. Deploy

Ensure `web/public/data/*.json` is committed (generated by `build-data.mjs` + `20_build_player_media.py`).

---

## Script index

| Script | Purpose |
|--------|---------|
| 01–05 | Historical drafts, Tankathon, data acquisition |
| 06–13 | Mock consensus, betting, combine, normalization |
| 14–18 | Robust / weighted consensus, volatility |
| 15 | Team fit engine |
| 16–17 | Monte Carlo + calibrated Monte Carlo |
| 19 | Backtest framework |
| 20 | Player media (ESPN headshots) for web |

---

## Resume / pitch line

> Built an NBA Draft Intelligence System integrating multi-source consensus, betting markets, archetype modeling, team-fit optimization, and Monte Carlo simulation — with a production Next.js analytics frontend.

---

## License

MIT (add `LICENSE` if you choose). Data from third-party sources belongs to respective owners; this project is for research and portfolio use.

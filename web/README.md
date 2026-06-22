# NBA Draft Intelligence System — Web

Next.js frontend for the DIS probabilistic draft forecasting pipeline.

## Local dev

```bash
# From repo root — refresh JSON from latest CSV outputs
node web/scripts/build-data.mjs

cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Deploy to Vercel

1. Push this repo to GitHub.
2. In Vercel: **New Project** → import the repo.
3. Set **Root Directory** to `web`.
4. Framework preset: **Next.js** (auto-detected).
5. Deploy.

Before each deploy (or in CI), run `node web/scripts/build-data.mjs` from the repo root so `web/public/data/*.json` reflects the latest model outputs.

## Pages

| Route | Description |
|-------|-------------|
| `/` | Top 30 board with probabilities, volatility, team logos |
| `/players/[slug]` | Scout report, archetype radar, Monte Carlo, mock sources, team fits |
| `/teams/[slug]` | Top fits, needs radar, roster weakness signals |
| `/simulator` | Pick distributions + stochastic scenario |
| `/volatility` | Boom-or-bust prospects |
| `/sources` | Source reliability weights |
| `/methodology` | Pipeline + calibration |
| `/about` | Project framing |

## Data

Static JSON in `public/data/` is generated from:

- `data/processed/final_calibrated_monte_carlo_board_2026.csv`
- `data/processed/calibrated_monte_carlo_pick_probabilities.csv`
- `data/processed/mock_consensus_weighted_2026.csv`
- `data/processed/team_fit_scores.csv`
- `data/manual/source_weights.csv`
- `data/processed/mock_sources_normalized.csv`
- `data/processed/prospect_master.csv`

Team logos load from NBA CDN (`cdn.nba.com`).

# GitHub Push Checklist

Repo: https://github.com/LinLyra/nba-draft-intelligence-2026

You push yourself — this file tells you **exactly what goes up** and what stays local.

---

## 1. Before first push (one-time)

```bash
cd /Users/lynnlong/Downloads/nba-draft-intelligence-2026

# Export web data + player photos (needs network for ESPN)
node web/scripts/build-data.mjs
PYTHONPATH=. python scripts/20_build_player_media.py

# Verify web builds
cd web && npm install && npm run build && cd ..
```

---

## 2. Initialize git (if not done)

```bash
git init
git remote add origin https://github.com/LinLyra/nba-draft-intelligence-2026.git
```

---

## 3. PUSH these (public ~80%)

```text
✅ README.md
✅ requirements.txt
✅ pyproject.toml
✅ .gitignore

✅ scripts/                    # all 01–20 + run_pipeline.py
✅ src/                        # scrapers + nba_draft_intel
✅ tests/
✅ config/source_weights.example.csv

✅ web/                        # entire Next.js app EXCEPT node_modules / .next
   ├── app/
   ├── components/
   ├── lib/
   ├── public/data/*.json      # IMPORTANT for Vercel demo
   ├── scripts/build-data.mjs
   ├── package.json
   ├── vercel.json
   └── README.md

✅ docs/                       # if present
✅ app/streamlit_app.py        # optional legacy dashboard
✅ .github/                    # CI if you add it later
```

### `web/public/data/` — commit these JSON files

```text
board.json
probabilities.json
consensus.json
team_fit.json
source_weights.json
volatility.json
mock_sources.json
prospects.json
player_index.json
player_media.json             # after script 20
```

These are **small derived outputs**, not raw scrapes. Vercel needs them for static deploy without running Python in production.

---

## 4. DO NOT push (gitignored)

```text
❌ data/raw/                   # scraped HTML, CSV dumps
❌ data/manual/                # mock texts, your source_weights.csv, RealGM HTML
❌ data/processed/*.csv        # large tables — rebuild locally
❌ data/interim/*              # except .gitkeep
❌ reports/*.csv / *.html
❌ .env
❌ web/node_modules/
❌ web/.next/
❌ .venv/
```

---

## 5. Push commands

```bash
git add README.md requirements.txt pyproject.toml .gitignore
git add scripts/ src/ tests/ config/ docs/ app/
git add web/app web/components web/lib web/public web/scripts
git add web/package.json web/package-lock.json web/tsconfig.json
git add web/next.config.mjs web/tailwind.config.ts web/postcss.config.mjs
git add web/vercel.json web/README.md web/next-env.d.ts

git status   # double-check: NO data/raw, NO data/manual, NO data/processed csv

git commit -m "$(cat <<'EOF'
Add NBA Draft Intelligence System: open pipeline + Next.js web app

Publish scripts, scrapers, and frontend for portfolio use. Model outputs
ship as web/public/data JSON for Vercel; raw scrapes and manual inputs
stay local via .gitignore.
EOF
)"

git branch -M main
git push -u origin main
```

---

## 6. Connect Vercel

1. https://vercel.com → Import `LinLyra/nba-draft-intelligence-2026`
2. **Root Directory:** `web`
3. Framework: Next.js (auto)
4. Deploy

No env vars required for static JSON deploy.

---

## 7. After model updates (later)

```bash
# Local only
PYTHONPATH=. python scripts/17_calibrated_monte_carlo.py
node web/scripts/build-data.mjs
PYTHONPATH=. python scripts/20_build_player_media.py

# Commit only changed JSON
git add web/public/data/
git commit -m "Refresh 2026 board outputs"
git push
```

Vercel redeploys automatically on push.

---

## 8. Logos on the site

| Asset | Source |
|-------|--------|
| NBA team logos | `cdn.nba.com` |
| School logos | Tankathon NCAA CDN (`d2uki2uvp6v3wr.cloudfront.net/ncaa/{slug}.svg`) |
| Player headshots | ESPN CDN (resolved by `scripts/20_build_player_media.py` → `player_media.json`) |

If a headshot is missing, UI falls back to initials avatar.

---

## 9. Optional additions (nice for portfolio)

- `LICENSE` (MIT)
- `docs/screenshots/` — homepage + AJ Dybantsa player page
- GitHub About: link to Vercel demo URL
- Topics: `nba` `sports-analytics` `monte-carlo` `nextjs` `data-engineering`

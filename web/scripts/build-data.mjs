/**
 * Export processed CSVs to web/public/data/*.json
 * Run from repo root: node web/scripts/build-data.mjs
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "../..");
const OUT = path.join(__dirname, "../public/data");

function readCsv(filePath) {
  const text = fs.readFileSync(filePath, "utf-8").trim();
  const lines = text.split("\n");
  const headers = lines[0].split(",");
  return lines.slice(1).map((line) => {
    const cols = line.split(",");
    const row = {};
    headers.forEach((h, i) => {
      const v = cols[i] ?? "";
      const n = Number(v);
      row[h] = v !== "" && !Number.isNaN(n) && h !== "player" && h !== "team" && h !== "source" && h !== "predicted_player" && h !== "alternatives" && h !== "position" && h !== "school_or_league" && h !== "height" && h !== "position_group" && h !== "name" && h !== "slug"
        ? n
        : v;
    });
    return row;
  });
}

function write(name, data) {
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, name), JSON.stringify(data, null, 2));
}

function slugify(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

const board = readCsv(path.join(ROOT, "data/processed/final_calibrated_monte_carlo_board_2026.csv"));
const probs = readCsv(path.join(ROOT, "data/processed/calibrated_monte_carlo_pick_probabilities.csv"));
const consensus = readCsv(path.join(ROOT, "data/processed/mock_consensus_weighted_2026.csv"));
const teamFit = readCsv(path.join(ROOT, "data/processed/team_fit_scores.csv"));
const sourceWeights = readCsv(path.join(ROOT, "data/manual/source_weights.csv"));
const mockSources = readCsv(path.join(ROOT, "data/processed/mock_sources_normalized.csv"));
const prospects = readCsv(path.join(ROOT, "data/processed/prospect_master.csv"));

const volatility = [...consensus]
  .sort((a, b) => b.std_pick - a.std_pick)
  .map((r) => ({
    player: r.player,
    std_pick: r.std_pick,
    min_pick: Math.max(1, Math.round(r.trimmed_mean_pick - r.std_pick)),
    max_pick: Math.round(r.trimmed_mean_pick + r.std_pick),
    source_count: r.source_count,
  }));

const playerIndex = board.map((b) => ({
  name: b.predicted_player,
  slug: slugify(b.predicted_player),
  pick: b.pick,
  team: b.team,
  probability: b.probability,
}));

write("board.json", board);
write("probabilities.json", probs);
write("consensus.json", consensus);
write("team_fit.json", teamFit);
write("source_weights.json", sourceWeights.map((r) => ({ source: r.source, weight: r.weight })));
write("mock_sources.json", mockSources);
write("prospects.json", prospects);
write("volatility.json", volatility);
write("player_index.json", playerIndex);

console.log(`Wrote ${OUT}`);

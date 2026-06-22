import fs from "fs";
import path from "path";

export { slugify } from "./slug";
export { volatilityLabel } from "./volatility";

const DATA_DIR = path.join(process.cwd(), "public", "data");

function readJson<T>(filename: string): T {
  const filePath = path.join(DATA_DIR, filename);
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw) as T;
}

export interface BoardRow {
  pick: number;
  team: string;
  predicted_player: string;
  probability: number;
  alternatives: string;
}

export interface ConsensusRow {
  player: string;
  weighted_mean_pick: number;
  trimmed_mean_pick: number;
  std_pick: number;
  source_count: number;
  weighted_source_count: number;
  consensus_score: number;
}

export interface ProspectRow {
  player: string;
  position: string | null;
  school_or_league: string | null;
  height: string | null;
  weight_lbs: number | null;
  age: number | null;
  height_inches: number | null;
  position_group: string | null;
  rank: number | null;
}

export interface ProbRow {
  pick: number;
  team: string;
  player: string;
  probability: number;
  trimmed_mean_pick: number;
  std_pick: number;
  source_count: number;
}

export interface TeamFitRow {
  team: string;
  player: string;
  team_fit_score: number;
  creation_score: number;
  shooting_score: number;
  size_score: number;
  defense_score: number;
  upside_score: number;
  nba_ready_score: number;
}

export interface MockSourceRow {
  source: string;
  pick: number;
  team: string;
  player: string;
}

export interface VolatilityRow {
  player: string;
  std_pick: number;
  min_pick: number;
  max_pick: number;
  source_count: number;
}

export interface SourceWeightRow {
  source: string;
  weight: number;
}

export interface PlayerIndexRow {
  name: string;
  slug: string;
  pick: number | null;
  team: string | null;
  probability: number | null;
}

export function getBoard() {
  return readJson<BoardRow[]>("board.json");
}

export function getConsensus() {
  return readJson<ConsensusRow[]>("consensus.json");
}

export function getProspects() {
  return readJson<ProspectRow[]>("prospects.json");
}

export function getProbabilities() {
  return readJson<ProbRow[]>("probabilities.json");
}

export function getTeamFit() {
  return readJson<TeamFitRow[]>("team_fit.json");
}

export function getMockSources() {
  return readJson<MockSourceRow[]>("mock_sources.json");
}

export function getVolatility() {
  return readJson<VolatilityRow[]>("volatility.json");
}

export function getSourceWeights() {
  return readJson<SourceWeightRow[]>("source_weights.json");
}

export function getPlayerIndex() {
  return readJson<PlayerIndexRow[]>("player_index.json");
}

export function pct(n: number): string {
  return `${(n * 100).toFixed(1)}%`;
}

export function getPlayerBySlug(slug: string) {
  const index = getPlayerIndex();
  return index.find((p) => p.slug === slug);
}

export function getProspect(name: string) {
  return getProspects().find((p) => p.player === name);
}

export function getConsensusPlayer(name: string) {
  return getConsensus().find((p) => p.player === name);
}

export function getPlayerProbabilities(name: string) {
  return getProbabilities()
    .filter((p) => p.player === name && p.probability > 0.001)
    .sort((a, b) => a.pick - b.pick);
}

export function getPlayerMockSources(name: string) {
  return getMockSources().filter((m) => m.player === name);
}

export function getTeamFitsForPlayer(name: string) {
  return getTeamFit()
    .filter((t) => t.player === name)
    .sort((a, b) => b.team_fit_score - a.team_fit_score)
    .slice(0, 8);
}

export function getTeamFitsForTeam(team: string) {
  return getTeamFit()
    .filter((t) => t.team === team)
    .sort((a, b) => b.team_fit_score - a.team_fit_score)
    .slice(0, 10);
}

export function getPickProbabilities(pick: number) {
  return getProbabilities()
    .filter((p) => p.pick === pick)
    .sort((a, b) => b.probability - a.probability)
    .slice(0, 8);
}

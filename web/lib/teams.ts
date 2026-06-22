export type TeamSlug =
  | "wizards"
  | "jazz"
  | "grizzlies"
  | "bulls"
  | "clippers"
  | "nets"
  | "kings"
  | "hawks"
  | "mavericks"
  | "bucks"
  | "warriors"
  | "thunder"
  | "heat"
  | "hornets"
  | "raptors"
  | "spurs"
  | "pistons"
  | "76ers"
  | "knicks"
  | "lakers"
  | "nuggets"
  | "celtics"
  | "timberwolves"
  | "cavaliers";

export interface TeamInfo {
  name: string;
  slug: TeamSlug;
  abbr: string;
  nbaId: number;
  color: string;
  needs: string[];
  profile: Record<string, number>;
}

export const TEAMS: Record<string, TeamInfo> = {
  Wizards: {
    name: "Wizards",
    slug: "wizards",
    abbr: "WAS",
    nbaId: 1610612764,
    color: "#002B5C",
    needs: ["Secondary creator", "Perimeter shooting", "Young upside"],
    profile: { creation: 0.28, shooting: 0.15, defense: 0.1, size: 0.15, upside: 0.28, nba_ready: 0.07 },
  },
  Jazz: {
    name: "Jazz",
    slug: "jazz",
    abbr: "UTA",
    nbaId: 1610612762,
    color: "#002B5C",
    needs: ["Lead guard", "Shot creation", "Defensive wing"],
    profile: { creation: 0.28, shooting: 0.12, defense: 0.1, size: 0.15, upside: 0.28, nba_ready: 0.07 },
  },
  Grizzlies: {
    name: "Grizzlies",
    slug: "grizzlies",
    abbr: "MEM",
    nbaId: 1610612763,
    color: "#5D76A9",
    needs: ["Frontcourt depth", "Rim protection", "Two-way wing"],
    profile: { creation: 0.18, shooting: 0.18, defense: 0.22, size: 0.22, upside: 0.15, nba_ready: 0.13 },
  },
  Bulls: {
    name: "Bulls",
    slug: "bulls",
    abbr: "CHI",
    nbaId: 1610612741,
    color: "#CE1141",
    needs: ["Frontcourt size", "Interior defense", "Playmaking"],
    profile: { creation: 0.18, shooting: 0.18, defense: 0.22, size: 0.22, upside: 0.15, nba_ready: 0.13 },
  },
  Clippers: {
    name: "Clippers",
    slug: "clippers",
    abbr: "LAC",
    nbaId: 1610612746,
    color: "#C8102E",
    needs: ["Secondary creator", "Wing depth", "Youth pipeline"],
    profile: { creation: 0.18, shooting: 0.18, defense: 0.18, size: 0.18, upside: 0.15, nba_ready: 0.13 },
  },
  Nets: {
    name: "Nets",
    slug: "nets",
    abbr: "BKN",
    nbaId: 1610612751,
    color: "#000000",
    needs: ["Franchise guard", "Upside bets", "Spacing"],
    profile: { creation: 0.28, shooting: 0.12, defense: 0.1, size: 0.15, upside: 0.28, nba_ready: 0.07 },
  },
  Kings: {
    name: "Kings",
    slug: "kings",
    abbr: "SAC",
    nbaId: 1610612758,
    color: "#5A2D81",
    needs: ["Perimeter defense", "Wing shooting", "Backup guard"],
    profile: { creation: 0.22, shooting: 0.22, defense: 0.14, size: 0.14, upside: 0.15, nba_ready: 0.13 },
  },
  Hawks: {
    name: "Hawks",
    slug: "hawks",
    abbr: "ATL",
    nbaId: 1610612737,
    color: "#E03A3E",
    needs: ["Creator guard", "Two-way wing", "Rim protection"],
    profile: { creation: 0.22, shooting: 0.22, defense: 0.14, size: 0.14, upside: 0.15, nba_ready: 0.13 },
  },
  Mavericks: {
    name: "Mavericks",
    slug: "mavericks",
    abbr: "DAL",
    nbaId: 1610612742,
    color: "#00538C",
    needs: ["Guard depth", "Perimeter defense", "Shooting"],
    profile: { creation: 0.22, shooting: 0.22, defense: 0.14, size: 0.14, upside: 0.15, nba_ready: 0.13 },
  },
  Bucks: {
    name: "Bucks",
    slug: "bucks",
    abbr: "MIL",
    nbaId: 1610612749,
    color: "#00471B",
    needs: ["Wing defense", "NBA-ready role player", "Shooting"],
    profile: { creation: 0.12, shooting: 0.25, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
  Warriors: {
    name: "Warriors",
    slug: "warriors",
    abbr: "GSW",
    nbaId: 1610612744,
    color: "#1D428A",
    needs: ["Spacing big", "Wing shooting", "Defensive versatility"],
    profile: { creation: 0.12, shooting: 0.28, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
  Thunder: {
    name: "Thunder",
    slug: "thunder",
    abbr: "OKC",
    nbaId: 1610612760,
    color: "#007AC1",
    needs: ["Roster balance", "Shooting", "Defensive depth"],
    profile: { creation: 0.12, shooting: 0.25, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
  Heat: {
    name: "Heat",
    slug: "heat",
    abbr: "MIA",
    nbaId: 1610612748,
    color: "#98002E",
    needs: ["Frontcourt defense", "Size", "Shot creation"],
    profile: { creation: 0.12, shooting: 0.22, defense: 0.26, size: 0.2, upside: 0.1, nba_ready: 0.16 },
  },
  Hornets: {
    name: "Hornets",
    slug: "hornets",
    abbr: "CHA",
    nbaId: 1610612766,
    color: "#1D1160",
    needs: ["Franchise upside", "Creator", "Frontcourt"],
    profile: { creation: 0.28, shooting: 0.12, defense: 0.1, size: 0.2, upside: 0.28, nba_ready: 0.07 },
  },
  Raptors: {
    name: "Raptors",
    slug: "raptors",
    abbr: "TOR",
    nbaId: 1610612761,
    color: "#CE1141",
    needs: ["Frontcourt", "Defense", "Playmaking"],
    profile: { creation: 0.18, shooting: 0.18, defense: 0.22, size: 0.22, upside: 0.15, nba_ready: 0.13 },
  },
  Spurs: {
    name: "Spurs",
    slug: "spurs",
    abbr: "SAS",
    nbaId: 1610612759,
    color: "#C4CED4",
    needs: ["Young core support", "Wing upside", "Big man"],
    profile: { creation: 0.28, shooting: 0.12, defense: 0.1, size: 0.2, upside: 0.28, nba_ready: 0.07 },
  },
  Pistons: {
    name: "Pistons",
    slug: "pistons",
    abbr: "DET",
    nbaId: 1610612765,
    color: "#C8102E",
    needs: ["Shooting", "Wing depth", "Creator"],
    profile: { creation: 0.28, shooting: 0.12, defense: 0.1, size: 0.15, upside: 0.28, nba_ready: 0.07 },
  },
  "76ers": {
    name: "76ers",
    slug: "76ers",
    abbr: "PHI",
    nbaId: 1610612755,
    color: "#006BB6",
    needs: ["Wing shooting", "Defense", "Youth"],
    profile: { creation: 0.18, shooting: 0.18, defense: 0.18, size: 0.18, upside: 0.15, nba_ready: 0.13 },
  },
  Knicks: {
    name: "Knicks",
    slug: "knicks",
    abbr: "NYK",
    nbaId: 1610612752,
    color: "#F58426",
    needs: ["Wing depth", "Shooting", "Defense"],
    profile: { creation: 0.12, shooting: 0.25, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
  Lakers: {
    name: "Lakers",
    slug: "lakers",
    abbr: "LAL",
    nbaId: 1610612747,
    color: "#552583",
    needs: ["Wing defense", "Shooting", "Depth"],
    profile: { creation: 0.12, shooting: 0.25, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
  Nuggets: {
    name: "Nuggets",
    slug: "nuggets",
    abbr: "DEN",
    nbaId: 1610612743,
    color: "#0E2240",
    needs: ["Wing depth", "Defense", "Shooting"],
    profile: { creation: 0.12, shooting: 0.25, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
  Celtics: {
    name: "Celtics",
    slug: "celtics",
    abbr: "BOS",
    nbaId: 1610612738,
    color: "#007A33",
    needs: ["Roster balance", "Wing depth", "NBA-ready"],
    profile: { creation: 0.12, shooting: 0.25, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
  Timberwolves: {
    name: "Timberwolves",
    slug: "timberwolves",
    abbr: "MIN",
    nbaId: 1610612750,
    color: "#0C2340",
    needs: ["Creator", "Wing shooting", "Depth"],
    profile: { creation: 0.18, shooting: 0.18, defense: 0.18, size: 0.18, upside: 0.15, nba_ready: 0.13 },
  },
  Cavaliers: {
    name: "Cavaliers",
    slug: "cavaliers",
    abbr: "CLE",
    nbaId: 1610612739,
    color: "#860038",
    needs: ["Wing shooting", "Defense", "Playmaking"],
    profile: { creation: 0.12, shooting: 0.25, defense: 0.22, size: 0.15, upside: 0.1, nba_ready: 0.16 },
  },
};

export function teamLogoUrl(teamName: string): string {
  const team = TEAMS[teamName];
  if (!team) return "";
  return `https://cdn.nba.com/logos/nba/${team.nbaId}/global/L/logo.svg`;
}

export function getTeam(name: string): TeamInfo | undefined {
  return TEAMS[name];
}

export function teamSlug(name: string): string {
  return TEAMS[name]?.slug ?? name.toLowerCase().replace(/\s+/g, "-");
}

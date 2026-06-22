import fs from "fs";
import path from "path";
import { slugify } from "./data";

export interface PlayerMediaRow {
  player: string;
  slug: string;
  school: string | null;
  school_slug?: string;
  espn_id?: string;
  headshot_url?: string;
  espn_team?: string;
}

const MEDIA_PATH = path.join(process.cwd(), "public", "data", "player_media.json");

let cache: PlayerMediaRow[] | null = null;

export function getPlayerMedia(): PlayerMediaRow[] {
  if (cache) return cache;
  if (!fs.existsSync(MEDIA_PATH)) {
    cache = [];
    return cache;
  }
  cache = JSON.parse(fs.readFileSync(MEDIA_PATH, "utf-8")) as PlayerMediaRow[];
  return cache;
}

export function getPlayerMediaBySlug(slug: string): PlayerMediaRow | undefined {
  return getPlayerMedia().find((p) => p.slug === slug);
}

export function getPlayerMediaByName(name: string): PlayerMediaRow | undefined {
  return getPlayerMedia().find((p) => p.player === name);
}

export function playerHeadshotUrl(nameOrSlug: string): string | null {
  const row =
    getPlayerMediaBySlug(nameOrSlug) ??
    getPlayerMediaByName(nameOrSlug) ??
    getPlayerMedia().find((p) => p.slug === slugify(nameOrSlug));
  return row?.headshot_url ?? null;
}

export function playerSchool(nameOrSlug: string): string | null {
  const row = getPlayerMediaByName(nameOrSlug) ?? getPlayerMediaBySlug(nameOrSlug);
  return row?.school ?? null;
}

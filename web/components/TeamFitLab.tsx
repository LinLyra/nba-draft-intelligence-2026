"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { DualRadar } from "@/components/DualRadar";
import { PlayerAvatar } from "@/components/PlayerAvatar";
import { TeamLogo } from "@/components/TeamLogo";
import { slugify } from "@/lib/slug";

type TeamProfile = {
  name: string;
  slug: string;
  profile: Record<string, number>;
  needs: string[];
};

type FitRow = {
  team: string;
  player: string;
  team_fit_score: number;
  creation_score: number;
  shooting_score: number;
  size_score: number;
  defense_score: number;
  upside_score: number;
  nba_ready_score: number;
};

type MediaRow = { player: string; headshot_url?: string };

const TRAITS = [
  ["creation", "Creation"],
  ["shooting", "Shooting"],
  ["size", "Size"],
  ["defense", "Defense"],
  ["upside", "Upside"],
  ["nba_ready", "NBA Ready"],
] as const;

export function TeamFitLab({
  teams,
  fits,
  media,
}: {
  teams: TeamProfile[];
  fits: FitRow[];
  media: MediaRow[];
}) {
  const mediaMap = Object.fromEntries(media.map((m) => [m.player, m]));
  const [teamName, setTeamName] = useState(teams[0]?.name ?? "Wizards");

  const teamFits = useMemo(
    () => fits.filter((f) => f.team === teamName).sort((a, b) => b.team_fit_score - a.team_fit_score).slice(0, 12),
    [fits, teamName]
  );

  const [playerName, setPlayerName] = useState(teamFits[0]?.player ?? "");

  const activePlayer = teamFits.find((f) => f.player === playerName) ?? teamFits[0];
  const teamInfo = teams.find((t) => t.name === teamName);

  const radarData = useMemo(() => {
    if (!teamInfo || !activePlayer) return [];
    return TRAITS.map(([key, label]) => ({
      trait: label,
      team: teamInfo.profile[key] ?? 0,
      player: activePlayer[`${key}_score` as keyof FitRow] as number,
    }));
  }, [teamInfo, activePlayer]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-4">
        <label className="text-sm text-gray-400">
          Select team
          <select
            className="ml-2 rounded-lg border border-line bg-panel px-3 py-2 text-white"
            value={teamName}
            onChange={(e) => {
              setTeamName(e.target.value);
              const next = fits
                .filter((f) => f.team === e.target.value)
                .sort((a, b) => b.team_fit_score - a.team_fit_score)[0];
              if (next) setPlayerName(next.player);
            }}
          >
            {teams.map((t) => (
              <option key={t.name} value={t.name}>
                {t.name}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="panel p-5">
          <div className="mb-4 flex items-center gap-3">
            <TeamLogo team={teamName} size={40} />
            <h2 className="text-lg font-semibold text-white">Top Fits · {teamName}</h2>
          </div>
          <div className="space-y-2">
            {teamFits.map((f, i) => (
              <button
                key={f.player}
                type="button"
                onClick={() => setPlayerName(f.player)}
                className={`flex w-full items-center justify-between rounded-lg border px-3 py-2 text-left text-sm transition ${
                  f.player === activePlayer?.player
                    ? "border-amber-500/50 bg-amber-500/10"
                    : "border-line hover:bg-white/5"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="w-5 font-bold text-amber-300">{i + 1}</span>
                  <PlayerAvatar
                    name={f.player}
                    src={mediaMap[f.player]?.headshot_url}
                    size={32}
                    className="rounded-lg"
                  />
                  <Link
                    href={`/players/${slugify(f.player)}`}
                    className="hover:text-amber-300"
                    onClick={(e) => e.stopPropagation()}
                  >
                    {f.player}
                  </Link>
                </div>
                <span className="font-mono text-amber-300">{f.team_fit_score.toFixed(3)}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="panel p-5">
          <h2 className="mb-2 text-lg font-semibold text-white">Need Profile Overlap</h2>
          {activePlayer && (
            <p className="mb-3 text-sm text-gray-400">
              {activePlayer.player} vs {teamName} roster needs
            </p>
          )}
          {radarData.length ? (
            <DualRadar
              data={radarData}
              teamLabel={`${teamName} needs`}
              playerLabel={activePlayer?.player ?? "Player"}
            />
          ) : (
            <p className="text-gray-500">Select a player to compare profiles.</p>
          )}
        </section>

        {teamInfo && (
          <section className="panel p-5 lg:col-span-2">
            <h2 className="mb-3 text-lg font-semibold text-white">Roster Weakness Signals</h2>
            <ul className="list-inside list-disc text-sm text-gray-300">
              {teamInfo.needs.map((n) => (
                <li key={n}>{n}</li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </div>
  );
}

import Link from "next/link";
import { notFound } from "next/navigation";
import { ArchetypeRadar } from "@/components/ArchetypeRadar";
import { PlayerAvatar } from "@/components/PlayerAvatar";
import { ProbBarChart } from "@/components/ProbBarChart";
import { SchoolLogo } from "@/components/SchoolLogo";
import { TeamLogo } from "@/components/TeamLogo";
import {
  getConsensusPlayer,
  getPlayerBySlug,
  getPlayerMockSources,
  getPlayerProbabilities,
  getProspect,
  getTeamFitsForPlayer,
  pct,
  volatilityLabel,
} from "@/lib/data";
import { getPlayerIndex } from "@/lib/data";
import { getPlayerMediaBySlug } from "@/lib/media";
import { teamSlug } from "@/lib/teams";

export function generateStaticParams() {
  return getPlayerIndex().map((p) => ({ slug: p.slug }));
}

export default function PlayerPage({ params }: { params: { slug: string } }) {
  const player = getPlayerBySlug(params.slug);
  if (!player) notFound();

  const name = player.name;
  const prospect = getProspect(name);
  const consensus = getConsensusPlayer(name);
  const probs = getPlayerProbabilities(name);
  const mocks = getPlayerMockSources(name);
  const fits = getTeamFitsForPlayer(name);
  const fitRow = fits[0];
  const media = getPlayerMediaBySlug(params.slug);
  const school = media?.school ?? prospect?.school_or_league ?? null;

  const radar = fitRow
    ? [
        { trait: "Creation", value: fitRow.creation_score },
        { trait: "Shooting", value: fitRow.shooting_score },
        { trait: "Size", value: fitRow.size_score },
        { trait: "Defense", value: fitRow.defense_score },
        { trait: "Upside", value: fitRow.upside_score },
        { trait: "NBA Ready", value: fitRow.nba_ready_score },
      ]
    : [];

  const probChart = probs.slice(0, 8).map((p) => ({
    label: `#${p.pick}`,
    value: p.probability,
  }));

  const mockBySource = mocks.map((m) => ({
    source: m.source,
    pick: m.pick,
    team: m.team || "—",
  }));


  return (
    <div className="space-y-8">
      <section className="panel flex flex-col gap-6 p-6 md:flex-row md:items-center">
        <PlayerAvatar name={name} src={media?.headshot_url} size={96} />
        <div className="flex-1 space-y-2">
          <p className="text-sm uppercase tracking-widest text-amber-400">Prospect Report</p>
          <h1 className="text-4xl font-semibold text-white">{name}</h1>
          <p className="flex items-center gap-2 text-gray-300">
            <span>{prospect?.position || "—"}</span>
            {school && (
              <>
                <span>·</span>
                <SchoolLogo school={school} size={22} />
                <span>{school}</span>
              </>
            )}
          </p>
          <p className="text-gray-400">
            {prospect?.height || "—"} · {prospect?.weight_lbs ? `${prospect.weight_lbs} lbs` : "—"}
            {prospect?.age ? ` · Age ${prospect.age}` : ""}
          </p>
        </div>
        {player.team && (
          <div className="flex items-center gap-3">
            <TeamLogo team={player.team} size={56} />
            <div>
              <div className="text-sm text-gray-400">Projected to</div>
              <div className="text-xl font-semibold">{player.team}</div>
              {player.probability && (
                <div className="text-amber-300">{pct(player.probability)} at #{player.pick}</div>
              )}
            </div>
          </div>
        )}
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Draft Projection</h2>
          {consensus ? (
            <dl className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <dt className="stat-label">Trimmed Mean</dt>
                <dd className="stat-value">{consensus.trimmed_mean_pick.toFixed(1)}</dd>
              </div>
              <div>
                <dt className="stat-label">Range</dt>
                <dd className="stat-value">
                  {Math.round(consensus.trimmed_mean_pick - consensus.std_pick)}–
                  {Math.round(consensus.trimmed_mean_pick + consensus.std_pick)}
                </dd>
              </div>
              <div>
                <dt className="stat-label">Sources</dt>
                <dd className="stat-value">{consensus.source_count}</dd>
              </div>
              <div>
                <dt className="stat-label">Volatility</dt>
                <dd className="stat-value">{volatilityLabel(consensus.std_pick)}</dd>
              </div>
            </dl>
          ) : (
            <p className="text-gray-400">No consensus data.</p>
          )}
        </section>

        <section className="panel p-5">
          <h2 className="mb-2 text-lg font-semibold">Archetype Radar</h2>
          {radar.length ? <ArchetypeRadar data={radar} /> : <p className="text-gray-400">No fit scores.</p>}
        </section>

        <section className="panel p-5 lg:col-span-2">
          <h2 className="mb-4 text-lg font-semibold">Monte Carlo Probability</h2>
          {probChart.length ? <ProbBarChart data={probChart} /> : <p className="text-gray-400">No simulation data.</p>}
        </section>

        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Mock Source Distribution</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-gray-500">
                <tr>
                  <th className="pb-2">Source</th>
                  <th className="pb-2">Pick</th>
                  <th className="pb-2">Team</th>
                </tr>
              </thead>
              <tbody>
                {mockBySource.map((m) => (
                  <tr key={`${m.source}-${m.pick}`} className="border-t border-line">
                    <td className="py-2 capitalize">{m.source.replace(/_/g, " ")}</td>
                    <td className="py-2">#{m.pick}</td>
                    <td className="py-2">{m.team}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Top Team Fits</h2>
          <div className="space-y-3">
            {fits.map((f) => (
              <Link
                key={f.team}
                href={`/teams/${teamSlug(f.team)}`}
                className="flex items-center justify-between rounded-lg border border-line px-3 py-2 hover:bg-white/5"
              >
                <div className="flex items-center gap-3">
                  <TeamLogo team={f.team} size={28} />
                  <span>{f.team}</span>
                </div>
                <span className="font-mono text-amber-300">{f.team_fit_score.toFixed(3)}</span>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

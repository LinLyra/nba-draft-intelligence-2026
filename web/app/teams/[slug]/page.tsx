import Link from "next/link";
import { notFound } from "next/navigation";
import { ArchetypeRadar } from "@/components/ArchetypeRadar";
import { TeamLogo } from "@/components/TeamLogo";
import { getBoard, getTeamFitsForTeam, slugify } from "@/lib/data";
import { TEAMS, type TeamInfo } from "@/lib/teams";

function findTeamBySlug(slug: string): TeamInfo | undefined {
  return Object.values(TEAMS).find((t) => t.slug === slug);
}

export function generateStaticParams() {
  return Object.values(TEAMS).map((t) => ({ slug: t.slug }));
}

export default function TeamPage({ params }: { params: { slug: string } }) {
  const team = findTeamBySlug(params.slug);
  if (!team) notFound();

  const fits = getTeamFitsForTeam(team.name);
  const boardPick = getBoard().find((b) => b.team === team.name);

  const needsRadar = [
    { trait: "Creation", value: team.profile.creation },
    { trait: "Shooting", value: team.profile.shooting },
    { trait: "Defense", value: team.profile.defense },
    { trait: "Size", value: team.profile.size },
    { trait: "Upside", value: team.profile.upside },
    { trait: "NBA Ready", value: team.profile.nba_ready },
  ];

  return (
    <div className="space-y-8">
      <section className="panel flex items-center gap-6 p-6">
        <TeamLogo team={team.name} size={72} />
        <div>
          <p className="text-sm uppercase tracking-widest text-amber-400">Team Page</p>
          <h1 className="text-4xl font-semibold text-white">{team.name}</h1>
          {boardPick && (
            <p className="mt-2 text-gray-300">
              Pick #{boardPick.pick}: {boardPick.predicted_player} (
              {(boardPick.probability * 100).toFixed(1)}%)
            </p>
          )}
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Top Fits</h2>
          <table className="w-full text-sm">
            <thead className="text-left text-gray-500">
              <tr>
                <th className="pb-2">Player</th>
                <th className="pb-2 text-right">Fit Score</th>
              </tr>
            </thead>
            <tbody>
              {fits.map((f) => (
                <tr key={f.player} className="border-t border-line">
                  <td className="py-2">
                    <Link
                      href={`/players/${slugify(f.player)}`}
                      className="hover:text-amber-300"
                    >
                      {f.player}
                    </Link>
                  </td>
                  <td className="py-2 text-right font-mono text-amber-300">
                    {f.team_fit_score.toFixed(3)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="panel p-5">
          <h2 className="mb-2 text-lg font-semibold">Team Needs Radar</h2>
          <ArchetypeRadar data={needsRadar} color="#60a5fa" />
        </section>

        <section className="panel p-5 lg:col-span-2">
          <h2 className="mb-3 text-lg font-semibold">Roster Weakness Signals</h2>
          <ul className="list-inside list-disc space-y-1 text-gray-300">
            {team.needs.map((n) => (
              <li key={n}>{n}</li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}

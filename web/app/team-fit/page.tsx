import { TeamFitLab } from "@/components/TeamFitLab";
import { getTeamFit } from "@/lib/data";
import { getPlayerMedia } from "@/lib/media";
import { TEAMS } from "@/lib/teams";

export default function TeamFitPage() {
  const teams = Object.values(TEAMS).map((t) => ({
    name: t.name,
    slug: t.slug,
    profile: t.profile,
    needs: t.needs,
  }));

  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Team Fit Lab</h1>
        <p className="mt-2 max-w-3xl text-gray-400">
          Match prospect archetypes to franchise need profiles. Overlap between team
          radar and player radar highlights where a pick solves real roster gaps.
        </p>
      </section>
      <TeamFitLab teams={teams} fits={getTeamFit()} media={getPlayerMedia()} />
    </div>
  );
}

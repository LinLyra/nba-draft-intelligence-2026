import { ProbabilityCurves } from "@/components/ProbabilityCurves";
import { getBoard, getProbabilities } from "@/lib/data";
import { getPlayerMedia } from "@/lib/media";
import { slugify } from "@/lib/slug";

export default function ProbabilityPage() {
  const board = getBoard();
  const probs = getProbabilities();
  const media = Object.fromEntries(getPlayerMedia().map((m) => [m.player, m]));

  const featured = board.slice(0, 12).map((row) => ({
    name: row.predicted_player,
    slug: slugify(row.predicted_player),
    headshot: media[row.predicted_player]?.headshot_url,
  }));

  const byPlayer: Record<string, { pick: number; probability: number }[]> = {};
  for (const row of probs) {
    if (!byPlayer[row.player]) byPlayer[row.player] = [];
    byPlayer[row.player].push({ pick: row.pick, probability: row.probability });
  }
  for (const name of Object.keys(byPlayer)) {
    byPlayer[name].sort((a, b) => a.pick - b.pick);
  }

  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Probability Curves</h1>
        <p className="mt-2 max-w-3xl text-gray-400">
          Floor-to-ceiling pick distributions from 20,000 calibrated simulations. A sharp
          peak means consensus; a wide spread means boom-or-bust volatility.
        </p>
      </section>
      <ProbabilityCurves players={featured} probabilities={byPlayer} />
    </div>
  );
}

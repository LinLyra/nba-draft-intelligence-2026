import Link from "next/link";
import { VolatilityBubbleChart } from "@/components/VolatilityBubbleChart";
import { getConsensus, getVolatility, slugify, volatilityLabel } from "@/lib/data";

export default function VolatilityPage() {
  const consensusMap = Object.fromEntries(getConsensus().map((c) => [c.player, c]));
  const rows = getVolatility()
    .map((v) => {
      const c = consensusMap[v.player];
      return {
        player: v.player,
        mean_pick: c?.trimmed_mean_pick ?? (v.min_pick + v.max_pick) / 2,
        std_pick: v.std_pick,
        source_count: v.source_count,
        min_pick: v.min_pick,
        max_pick: v.max_pick,
      };
    })
    .filter((r) => r.mean_pick <= 35)
    .slice(0, 40);

  const topBoom = rows.slice(0, 8);

  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Boom-or-Bust Chart</h1>
        <p className="mt-2 max-w-2xl text-gray-400">
          Mean pick vs mock-draft dispersion. Upper-right bubbles are high-upside,
          high-uncertainty prospects — the picks front offices stress-test hardest.
        </p>
      </section>

      <section className="panel p-5">
        <VolatilityBubbleChart data={rows} />
      </section>

      <section className="panel p-5">
        <h2 className="mb-4 text-lg font-semibold text-white">Highest Uncertainty</h2>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
          {topBoom.map((r) => (
            <Link
              key={r.player}
              href={`/players/${slugify(r.player)}`}
              className="rounded-lg border border-line px-3 py-3 transition hover:border-amber-500/40 hover:bg-white/5"
            >
              <p className="font-medium text-white">{r.player}</p>
              <p className="mt-1 text-xs text-gray-500">
                μ #{r.mean_pick.toFixed(1)} · σ {r.std_pick.toFixed(1)}
              </p>
              <span
                className={
                  volatilityLabel(r.std_pick) === "High"
                    ? "badge-high mt-2 inline-block"
                    : volatilityLabel(r.std_pick) === "Medium"
                      ? "badge-medium mt-2 inline-block"
                      : "badge-low mt-2 inline-block"
                }
              >
                {volatilityLabel(r.std_pick)}
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}

import Link from "next/link";
import { getVolatility, slugify, volatilityLabel } from "@/lib/data";

export default function VolatilityPage() {
  const rows = getVolatility().slice(0, 20);

  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-4xl font-semibold text-white">Boom-or-Bust Prospects</h1>
        <p className="mt-2 max-w-2xl text-gray-400">
          Highest mock-draft volatility — where single-source spikes and source disagreement
          create the widest pick ranges.
        </p>
      </section>

      <div className="panel overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-white/5 text-left text-gray-400">
            <tr>
              <th className="px-4 py-3">Player</th>
              <th className="px-4 py-3">Std Pick</th>
              <th className="px-4 py-3">Range</th>
              <th className="px-4 py-3">Sources</th>
              <th className="px-4 py-3">Label</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.player} className="border-t border-line hover:bg-white/5">
                <td className="px-4 py-3">
                  <Link href={`/players/${slugify(r.player)}`} className="font-medium text-white hover:text-amber-300">
                    {r.player}
                  </Link>
                </td>
                <td className="px-4 py-3 font-mono">{r.std_pick.toFixed(2)}</td>
                <td className="px-4 py-3">
                  #{r.min_pick} – #{r.max_pick}
                </td>
                <td className="px-4 py-3">{r.source_count}</td>
                <td className="px-4 py-3">
                  <span
                    className={
                      volatilityLabel(r.std_pick) === "High"
                        ? "badge-high"
                        : volatilityLabel(r.std_pick) === "Medium"
                          ? "badge-medium"
                          : "badge-low"
                    }
                  >
                    {volatilityLabel(r.std_pick)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

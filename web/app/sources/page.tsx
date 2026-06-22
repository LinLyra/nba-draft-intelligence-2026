import { getSourceWeights } from "@/lib/data";

export default function SourcesPage() {
  const sources = getSourceWeights().sort((a, b) => b.weight - a.weight);

  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-4xl font-semibold text-white">Source Explorer</h1>
        <p className="mt-2 max-w-2xl text-gray-400">
          Not a simple average. Each mock source carries a reliability weight tuned for
          historical signal quality and single-source volatility control.
        </p>
      </section>

      <div className="panel overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-white/5 text-left text-gray-400">
            <tr>
              <th className="px-4 py-3">Source</th>
              <th className="px-4 py-3">Weight</th>
              <th className="px-4 py-3">Tier</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((s) => (
              <tr key={s.source} className="border-t border-line">
                <td className="px-4 py-3 capitalize">{s.source.replace(/_/g, " ")}</td>
                <td className="px-4 py-3 font-mono text-amber-300">{s.weight.toFixed(1)}</td>
                <td className="px-4 py-3 text-gray-400">
                  {s.weight >= 1.3 ? "High" : s.weight >= 1.0 ? "Standard" : "Discounted"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <section className="panel p-5 text-sm text-gray-400">
        Excluded from consensus: Athletic, ESPN, Yahoo (low reliability / noise).
        Edit weights in <code className="text-amber-300">data/manual/source_weights.csv</code>{" "}
        and re-run script 18.
      </section>
    </div>
  );
}

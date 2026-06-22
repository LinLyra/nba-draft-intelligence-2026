import {
  getMockSources,
  getPlayerMockSources,
  getSourceWeights,
} from "@/lib/data";

const LAYERS = [
  {
    layer: "Data Layer",
    detail: "8 weighted mock sources · prospect database · betting markets",
    sources: ["CBS Final", "Bleacher Report", "Tankathon", "NBA Draft Net", "Hoopshq", "Netscouts", "SB Nation", "USA Today FTW"],
  },
  { layer: "Consensus Layer", detail: "Source-weighted robust trimmed-mean aggregation" },
  { layer: "Market Layer", detail: "Betting odds integration at picks #1–#2" },
  { layer: "Archetype Layer", detail: "Creation · shooting · size · defense · upside · NBA-ready" },
  { layer: "Team Fit Layer", detail: "Prospect archetype × franchise need profile" },
  { layer: "Monte Carlo Layer", detail: "20,000 calibrated stochastic simulations" },
  { layer: "Probability Outputs", detail: "Board · volatility · confidence · scenarios" },
];

const WEIGHTS = [
  { label: "Consensus", pct: 60 },
  { label: "Betting", pct: 18 },
  { label: "Reliability", pct: 12 },
  { label: "Team Fit", pct: 10 },
];

function getSourceStats() {
  const mocks = getMockSources();
  return getSourceWeights()
    .sort((a, b) => b.weight - a.weight)
    .map((w) => ({
      source: w.source,
      weight: w.weight,
      coverage: new Set(mocks.filter((m) => m.source === w.source).map((m) => m.player)).size,
    }));
}

export default function MethodologyPage() {
  const sourceStats = getSourceStats();
  const ajMocks = getPlayerMockSources("AJ Dybantsa").sort((a, b) => a.pick - b.pick);

  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Methodology</h1>
        <p className="mt-2 max-w-3xl text-gray-400">
          A layered probabilistic framework — from information aggregation to calibrated
          simulation — designed for explainability, not black-box rankings.
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <section className="panel p-6">
          <h2 className="mb-6 text-lg font-semibold text-white">System Layers</h2>
          <div className="space-y-0">
            {LAYERS.map((item, i) => (
              <div key={item.layer} className="relative pl-8">
                {i < LAYERS.length - 1 && (
                  <div className="absolute left-3 top-8 h-full w-px bg-amber-500/30" />
                )}
                <div className="absolute left-0 top-1 flex h-6 w-6 items-center justify-center rounded-full bg-amber-500/20 text-xs font-bold text-amber-300">
                  {i + 1}
                </div>
                <div className="pb-6">
                  <h3 className="font-semibold text-white">{item.layer}</h3>
                  <p className="text-sm text-gray-400">{item.detail}</p>
                  {item.sources && (
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {item.sources.map((s) => (
                        <span
                          key={s}
                          className="rounded-full border border-line px-2 py-0.5 text-xs text-gray-500"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="panel p-6">
          <h2 className="mb-4 text-lg font-semibold text-white">Weight Matrix</h2>
          <div className="space-y-4">
            {WEIGHTS.map((w) => (
              <div key={w.label}>
                <div className="mb-1 flex justify-between text-sm">
                  <span className="text-gray-300">{w.label}</span>
                  <span className="font-mono text-amber-300">{w.pct}%</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-white/5">
                  <div
                    className="h-full rounded-full bg-amber-500"
                    style={{ width: `${w.pct}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
          <dl className="mt-6 grid grid-cols-2 gap-3 text-sm">
            <div>
              <dt className="stat-label">Simulations</dt>
              <dd className="stat-value">20,000</dd>
            </div>
            <div>
              <dt className="stat-label">#1 Overall</dt>
              <dd className="stat-value">AJ · 99.9%</dd>
            </div>
          </dl>
        </section>
      </div>

      <section className="panel overflow-hidden">
        <h2 className="border-b border-line px-5 py-4 text-lg font-semibold text-white">
          Source Reliability
        </h2>
        <table className="w-full text-sm">
          <thead className="bg-white/5 text-left text-gray-500">
            <tr>
              <th className="px-5 py-3">Source</th>
              <th className="px-5 py-3">Weight</th>
              <th className="px-5 py-3">Coverage</th>
            </tr>
          </thead>
          <tbody>
            {sourceStats.map((s) => (
              <tr key={s.source} className="border-t border-line">
                <td className="px-5 py-3 capitalize">{s.source.replace(/_/g, " ")}</td>
                <td className="px-5 py-3 font-mono text-amber-300">{s.weight.toFixed(1)}</td>
                <td className="px-5 py-3">{s.coverage} players</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {ajMocks.length > 0 && (
        <section className="panel p-6">
          <h2 className="mb-2 text-lg font-semibold text-white">Information Conflict · AJ Dybantsa</h2>
          <p className="mb-4 text-sm text-gray-500">
            When sources disagree, volatility rises — even for consensus #1 picks.
          </p>
          <div className="flex flex-wrap gap-2">
            {ajMocks.map((m) => (
              <div
                key={`${m.source}-${m.pick}`}
                className={`rounded-lg border px-3 py-2 text-sm ${
                  m.pick <= 3
                    ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-200"
                    : "border-rose-500/30 bg-rose-500/10 text-rose-200"
                }`}
              >
                <span className="capitalize text-gray-400">{m.source.replace(/_/g, " ")}</span>
                <span className="ml-2 font-mono font-bold">#{m.pick}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

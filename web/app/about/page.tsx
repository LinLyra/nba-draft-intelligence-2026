const TRADITIONAL = [
  "Static single ranking",
  "One media outlet",
  "No team context",
  "No probability or alternatives",
];

const DIS = [
  "8 weighted mock sources",
  "Betting market signals",
  "Team fit engine",
  "20,000 Monte Carlo simulations",
  "Volatility & confidence scoring",
  "Explainable methodology",
];

const OUTPUTS = [
  "Probability board",
  "Volatility report",
  "Team fit scores",
  "Scenario simulation",
  "Probability curves",
];

export default function AboutPage() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Why Draft Intelligence?</h1>
        <p className="mt-2 max-w-3xl text-gray-400">
          Traditional mock drafts are deterministic. Draft Intelligence treats the NBA
          draft as a probabilistic decision problem.
        </p>
      </section>

      <div className="grid gap-6 md:grid-cols-2">
        <section className="panel p-6">
          <h2 className="mb-4 text-lg font-semibold text-rose-300">Traditional Mocks</h2>
          <ul className="space-y-2 text-sm text-gray-400">
            {TRADITIONAL.map((item) => (
              <li key={item} className="flex gap-2">
                <span className="text-rose-400">✕</span>
                {item}
              </li>
            ))}
          </ul>
          <p className="mt-4 text-sm text-gray-500">
            Tankathon, ESPN, CBS and most public boards provide one ordered list. They do
            not quantify disagreement, uncertainty, or franchise fit.
          </p>
        </section>

        <section className="panel p-6">
          <h2 className="mb-4 text-lg font-semibold text-emerald-300">Draft Intelligence</h2>
          <ul className="space-y-2 text-sm text-gray-300">
            {DIS.map((item) => (
              <li key={item} className="flex gap-2">
                <span className="text-emerald-400">✓</span>
                {item}
              </li>
            ))}
          </ul>
          <p className="mt-4 text-sm text-gray-500">
            We estimate not only who goes where, but how confident we are — and what
            alternatives exist at each pick.
          </p>
        </section>
      </div>

      <section className="panel p-6">
        <h2 className="mb-4 text-lg font-semibold text-white">Outputs</h2>
        <div className="flex flex-wrap gap-2">
          {OUTPUTS.map((o) => (
            <span
              key={o}
              className="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-sm text-amber-200"
            >
              {o}
            </span>
          ))}
        </div>
      </section>

      <section className="panel p-6">
        <h2 className="mb-4 text-lg font-semibold text-white">Architecture</h2>
        <pre className="overflow-x-auto rounded-xl bg-black/30 p-4 text-sm leading-relaxed text-gray-300">
{`Data Layer          → 8 weighted mock sources + prospects + betting
Consensus Layer     → robust trimmed-mean aggregation
Market Layer        → odds at #1 / #2
Archetype Layer     → creation · shooting · size · defense · upside
Team Fit Layer      → prospect × franchise need matching
Monte Carlo Layer   → 20,000 calibrated simulations
Probability Outputs → board · volatility · confidence · scenarios`}
        </pre>
      </section>

      <section className="text-center">
        <p className="font-signature text-3xl text-amber-400/90">LLyra</p>
        <p className="mt-1 text-sm text-gray-500">NBA Draft Intelligence System · 2026</p>
      </section>
    </div>
  );
}

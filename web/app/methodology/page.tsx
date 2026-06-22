const FRAMEWORK = [
  {
    title: "Multi-Source Consensus",
    body: "Aggregates weighted mock-draft signals into a robust pick estimate with explicit volatility.",
  },
  {
    title: "Market Layer",
    body: "Blends betting-market information at the top of the board where price discovery is strongest.",
  },
  {
    title: "Team Fit Engine",
    body: "Scores prospect archetypes against team needs — creation, shooting, defense, size, upside, NBA readiness.",
  },
  {
    title: "Calibrated Monte Carlo",
    body: "20,000 stochastic draft simulations produce pick probabilities, alternatives, and uncertainty bands.",
  },
];

export default function MethodologyPage() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Methodology</h1>
        <p className="mt-2 max-w-3xl text-gray-400">
          A probabilistic draft forecasting framework — information aggregation, sports
          analytics, and simulation — to estimate outcomes and uncertainty.
        </p>
      </section>

      <section className="panel p-6">
        <h2 className="mb-4 text-lg font-semibold text-white">Framework</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {FRAMEWORK.map((item, i) => (
            <div key={item.title} className="rounded-xl border border-line p-4">
              <div className="mb-2 flex items-center gap-3">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-amber-500/20 text-sm font-bold text-amber-300">
                  {i + 1}
                </span>
                <h3 className="font-semibold text-white">{item.title}</h3>
              </div>
              <p className="text-sm text-gray-400">{item.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="panel p-6">
        <h2 className="mb-4 text-lg font-semibold text-white">Model Snapshot</h2>
        <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <dt className="stat-label">Simulations</dt>
            <dd className="stat-value">20,000</dd>
          </div>
          <div>
            <dt className="stat-label">Mock Sources</dt>
            <dd className="stat-value">8 weighted</dd>
          </div>
          <div>
            <dt className="stat-label">#1 Overall</dt>
            <dd className="stat-value">AJ Dybantsa · 99.9%</dd>
          </div>
          <div>
            <dt className="stat-label">Most Volatile (Top 30)</dt>
            <dd className="stat-value">Isaiah Evans</dd>
          </div>
        </dl>
      </section>

      <section className="panel p-6 text-sm text-gray-400">
        <p>
          Final outputs emphasize <span className="text-amber-300">probability</span>,{" "}
          <span className="text-amber-300">volatility</span>, and{" "}
          <span className="text-amber-300">alternatives</span> — the same lens NBA front
          offices and analytics groups use when stress-testing a draft board.
        </p>
      </section>
    </div>
  );
}

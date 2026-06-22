const STEPS = [
  "Raw mock sources + prospect database",
  "Name normalization",
  "Source-weighted robust consensus (trimmed mean)",
  "Betting odds layer (#1 / #2 markets)",
  "Team fit engine (archetype × team needs)",
  "Calibrated Monte Carlo (20,000 simulations)",
  "Probability board + uncertainty outputs",
];

export default function MethodologyPage() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-4xl font-semibold text-white">Methodology</h1>
        <p className="mt-2 max-w-3xl text-gray-400">
          A probabilistic draft forecasting framework integrating multi-source consensus,
          market information, player archetypes, team-fit optimization, and Monte Carlo
          simulation to estimate outcomes and uncertainty.
        </p>
      </section>

      <section className="panel p-8">
        <div className="space-y-4">
          {STEPS.map((step, i) => (
            <div key={step} className="flex items-start gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-500/20 font-bold text-amber-300">
                {i + 1}
              </div>
              <div className="pt-2 text-lg text-white">{step}</div>
              {i < STEPS.length - 1 && (
                <div className="ml-5 hidden flex-1 border-b border-dashed border-line md:block" />
              )}
            </div>
          ))}
        </div>
      </section>

      <div className="grid gap-6 md:grid-cols-2">
        <section className="panel p-5 text-sm text-gray-300">
          <h2 className="mb-3 text-lg font-semibold text-white">Scoring Weights</h2>
          <ul className="list-inside list-disc space-y-1">
            <li>60% consensus (trimmed mean location prior)</li>
            <li>12% source reliability (weighted source count)</li>
            <li>18% betting odds (picks 1–2 only)</li>
            <li>10% team fit score</li>
          </ul>
        </section>
        <section className="panel p-5 text-sm text-gray-300">
          <h2 className="mb-3 text-lg font-semibold text-white">Calibration</h2>
          <ul className="list-inside list-disc space-y-1">
            <li>Uncertainty penalty for high std_pick (pick 3+)</li>
            <li>Single-source spike control via exact-pick counts</li>
            <li>Pick-dependent softmax temperature</li>
            <li>Candidate pool window (trimmed_mean ± 12)</li>
          </ul>
        </section>
      </div>
    </div>
  );
}

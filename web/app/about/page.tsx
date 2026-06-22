export default function AboutPage() {
  return (
    <div className="max-w-3xl space-y-6">
      <h1 className="text-4xl font-semibold text-white">About</h1>
      <p className="text-lg text-gray-300">
        NBA Draft Intelligence System (DIS) is a probabilistic draft forecasting framework
        inspired by NBA front offices and sports analytics departments.
      </p>
      <p className="text-gray-400">
        It integrates multi-source mock consensus, betting market information, player
        archetype modeling, team-fit optimization, and Monte Carlo simulation to estimate
        draft outcomes — with explicit uncertainty, alternatives, and source reliability.
      </p>
      <div className="panel p-5 text-sm text-gray-400">
        <p className="mb-2 font-semibold text-white">Keywords</p>
        <p>Uncertainty · Probability · Information aggregation · Simulation · Market efficiency</p>
      </div>
      <p className="text-sm text-gray-500">
        Backtest framework ready. Formal accuracy metrics will be computed after the 2026
        draft via exact pick, top-k accuracy, and MAE.
      </p>
    </div>
  );
}

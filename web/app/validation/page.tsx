const METRICS = [
  { name: "Exact Pick Accuracy", key: "exact_pick_accuracy", status: "Pending" },
  { name: "Top-3 Pick Accuracy", key: "top_3_pick_accuracy", status: "Pending" },
  { name: "Top-5 Pick Accuracy", key: "top_5_pick_accuracy", status: "Pending" },
  { name: "Mean Absolute Pick Error", key: "mean_absolute_pick_error", status: "Pending" },
  { name: "Lottery Accuracy (Picks 1–14)", key: "lottery_accuracy", status: "Pending" },
  { name: "First-Round Player Coverage", key: "first_round_player_coverage", status: "Pending" },
];

const CALIBRATION = [
  "20,000 Monte Carlo simulations per release",
  "Source-weighted robust consensus (trimmed mean)",
  "Temperature-adjusted softmax by pick band",
  "Single-source spike suppression",
  "Uncertainty penalty for high mock-draft dispersion",
  "Betting market layer at picks #1–#2",
];

export default function ValidationPage() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Validation</h1>
        <p className="mt-2 max-w-3xl text-gray-400">
          A serious forecasting system publishes its evaluation plan before outcomes are known.
          Post-draft metrics for 2026 will be computed automatically via the backtest framework.
        </p>
      </section>

      <section className="panel p-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">2026 Pre-Draft Model</h2>
          <span className="rounded-full bg-amber-500/15 px-3 py-1 text-xs font-medium text-amber-300">
            Awaiting draft night
          </span>
        </div>
        <table className="w-full text-sm">
          <thead className="text-left text-gray-500">
            <tr>
              <th className="pb-3">Metric</th>
              <th className="pb-3 text-right">Status</th>
            </tr>
          </thead>
          <tbody>
            {METRICS.map((m) => (
              <tr key={m.key} className="border-t border-line">
                <td className="py-3 text-gray-200">{m.name}</td>
                <td className="py-3 text-right text-gray-500">{m.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <div className="grid gap-6 md:grid-cols-2">
        <section className="panel p-6">
          <h2 className="mb-3 text-lg font-semibold text-white">Historical Backtest Framework</h2>
          <p className="text-sm text-gray-400">
            Implemented for 2019–2025 with placeholder pipelines. Each season expects mock
            sources, a predicted board, and actual draft results under{" "}
            <code className="text-amber-300">data/backtest/{"{year}"}/</code>.
          </p>
          <p className="mt-3 text-sm text-gray-400">
            Current public release ships the <strong className="text-gray-200">2026 pre-draft</strong>{" "}
            model. Formal accuracy will be reported after the draft via{" "}
            <code className="text-amber-300">scripts/19_backtest_framework.py</code>.
          </p>
        </section>

        <section className="panel p-6">
          <h2 className="mb-3 text-lg font-semibold text-white">Calibration</h2>
          <ul className="list-inside list-disc space-y-2 text-sm text-gray-400">
            {CALIBRATION.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>
      </div>

      <section className="panel p-6 text-sm text-gray-400">
        <p>
          Validation is intentionally <span className="text-amber-300">pending</span> — not
          hidden. The framework is ready; only the 2026 ground truth is missing. That is
          how research-grade forecasting systems document uncertainty about their own
          performance.
        </p>
      </section>
    </div>
  );
}

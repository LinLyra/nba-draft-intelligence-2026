import { BoardCard } from "@/components/BoardCard";
import { getBoard, getConsensus, getProspects } from "@/lib/data";

export default function HomePage() {
  const board = getBoard();
  const consensus = getConsensus();
  const prospectMap = Object.fromEntries(getProspects().map((p) => [p.player, p]));
  const stdMap = Object.fromEntries(consensus.map((c) => [c.player, c.std_pick]));

  return (
    <div className="space-y-10">
      <section className="space-y-4">
        <p className="text-sm uppercase tracking-[0.3em] text-amber-400">
          AI-Powered NBA Draft Intelligence Platform
        </p>
        <h1 className="max-w-3xl font-display text-4xl font-semibold leading-tight text-white md:text-5xl">
          Probabilistic 2026 Mock Draft Board
        </h1>
        <p className="max-w-2xl text-gray-400">
          Source-weighted consensus, betting market signals, team-fit optimization,
          and 20,000 Monte Carlo simulations — not a single deterministic ranking.
        </p>
      </section>

      <section className="grid gap-8 lg:grid-cols-[2fr_1fr]">
        <div className="space-y-3">
          <h2 className="text-xl font-semibold text-white">Final Mock Board · Top 30</h2>
          {board.map((row) => (
            <BoardCard
              key={row.pick}
              row={row}
              stdPick={stdMap[row.predicted_player]}
              prospect={prospectMap[row.predicted_player]}
            />
          ))}
        </div>

        <aside className="space-y-4">
          <div className="panel p-5">
            <h3 className="mb-3 text-lg font-semibold">Model Snapshot</h3>
            <dl className="space-y-3 text-sm">
              <div>
                <dt className="stat-label">Simulations</dt>
                <dd className="stat-value">20,000</dd>
              </div>
              <div>
                <dt className="stat-label">Sources</dt>
                <dd className="stat-value">8 weighted mocks</dd>
              </div>
              <div>
                <dt className="stat-label">#1 Overall</dt>
                <dd className="stat-value">AJ Dybantsa · 99.9%</dd>
              </div>
              <div>
                <dt className="stat-label">Most volatile top-30</dt>
                <dd className="stat-value">Isaiah Evans</dd>
              </div>
            </dl>
          </div>
          <div className="panel p-5 text-sm text-gray-400">
            Click any prospect for scout report, probability curve, mock-source
            distribution, and team-fit matches.
          </div>
        </aside>
      </section>
    </div>
  );
}

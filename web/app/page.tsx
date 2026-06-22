import { BoardCard } from "@/components/BoardCard";
import { getBoard, getConsensus, getProspects } from "@/lib/data";

export default function HomePage() {
  const board = getBoard();
  const consensus = getConsensus();
  const prospectMap = Object.fromEntries(getProspects().map((p) => [p.player, p]));
  const stdMap = Object.fromEntries(consensus.map((c) => [c.player, c.std_pick]));
  const srcMap = Object.fromEntries(consensus.map((c) => [c.player, c.source_count]));

  return (
    <div className="space-y-10">
      <section className="space-y-4">
          <p className="text-sm uppercase tracking-[0.3em] text-amber-400">
            AI-Powered NBA Draft Intelligence Platform
          </p>
          <h1 className="max-w-3xl font-display text-4xl font-bold leading-tight tracking-tight text-white md:text-5xl">
            Probabilistic 2026 Mock Draft Board
          </h1>
          <p className="max-w-2xl text-gray-400">
            Source-weighted consensus, betting market signals, team-fit optimization,
            and 20,000 Monte Carlo simulations — not a single deterministic ranking.
          </p>
      </section>

      <section>
        <h2 className="mb-4 text-xl font-semibold text-white">Final Mock Board · Top 30</h2>
        <div className="grid gap-3 md:grid-cols-2">
          {board.map((row) => (
            <BoardCard
              key={row.pick}
              row={row}
              stdPick={stdMap[row.predicted_player]}
              sourceCount={srcMap[row.predicted_player]}
              prospect={prospectMap[row.predicted_player]}
            />
          ))}
        </div>
        <p className="mt-4 text-sm text-gray-500">
          Click any prospect for scout report, probability curve, and team-fit matches.
        </p>
      </section>
    </div>
  );
}

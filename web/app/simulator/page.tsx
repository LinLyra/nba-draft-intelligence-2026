import { DraftSimulator } from "@/components/DraftSimulator";
import { getBoard, getProbabilities } from "@/lib/data";
import { getPlayerMedia } from "@/lib/media";

export default function SimulatorPage() {
  const board = getBoard();
  const probabilities = getProbabilities();
  const media = getPlayerMedia().map((m) => ({
    player: m.player,
    headshot_url: m.headshot_url,
  }));

  return (
    <div className="space-y-6">
      <section>
        <h1 className="font-display text-4xl font-bold text-white">Draft Simulator</h1>
        <p className="mt-2 max-w-2xl text-gray-400">
          Draft Night mode reveals picks one-by-one from 20,000 calibrated simulations.
          Explore distributions pick-by-pick or watch a full stochastic first round unfold.
        </p>
      </section>
      <DraftSimulator board={board} probabilities={probabilities} media={media} />
    </div>
  );
}

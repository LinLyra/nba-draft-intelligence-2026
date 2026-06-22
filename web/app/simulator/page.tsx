import { DraftSimulator } from "@/components/DraftSimulator";
import { getBoard, getProbabilities } from "@/lib/data";

export default function SimulatorPage() {
  const board = getBoard();
  const probabilities = getProbabilities();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-4xl font-semibold text-white">Draft Simulator</h1>
        <p className="mt-2 max-w-2xl text-gray-400">
          Explore calibrated Monte Carlo outputs. Pick distributions come from 20,000
          simulations; scenario button samples one stochastic first-round path.
        </p>
      </section>
      <DraftSimulator board={board} probabilities={probabilities} />
    </div>
  );
}

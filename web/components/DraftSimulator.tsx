"use client";

import { useMemo, useState } from "react";
import { ProbBarChart } from "@/components/ProbBarChart";
import { TeamLogo } from "@/components/TeamLogo";

type BoardRow = {
  pick: number;
  team: string;
  predicted_player: string;
  probability: number;
};

type ProbRow = {
  pick: number;
  team: string;
  player: string;
  probability: number;
};

export function DraftSimulator({
  board,
  probabilities,
}: {
  board: BoardRow[];
  probabilities: ProbRow[];
}) {
  const [pick, setPick] = useState(5);
  const [seed, setSeed] = useState(0);

  const pickDist = useMemo(() => {
    return probabilities
      .filter((p) => p.pick === pick)
      .sort((a, b) => b.probability - a.probability)
      .slice(0, 6)
      .map((p) => ({ label: p.player, value: p.probability }));
  }, [pick, probabilities]);

  const scenario = useMemo(() => {
    const rng = mulberry32(42 + seed);
    const byPick: Record<number, ProbRow[]> = {};
    for (const p of probabilities) {
      if (!byPick[p.pick]) byPick[p.pick] = [];
      byPick[p.pick].push(p);
    }

    const used = new Set<string>();
    const result: { pick: number; team: string; player: string }[] = [];

    for (let i = 1; i <= 30; i++) {
      const candidates = (byPick[i] || []).filter((c) => !used.has(c.player));
      if (!candidates.length) {
        const fallback = board.find((b) => b.pick === i);
        if (fallback) {
          result.push({ pick: i, team: fallback.team, player: fallback.predicted_player });
        }
        continue;
      }
      const total = candidates.reduce((s, c) => s + c.probability, 0);
      let roll = rng() * total;
      let chosen = candidates[0];
      for (const c of candidates) {
        roll -= c.probability;
        if (roll <= 0) {
          chosen = c;
          break;
        }
      }
      used.add(chosen.player);
      result.push({ pick: i, team: chosen.team, player: chosen.player });
    }
    return result;
  }, [board, probabilities, seed]);

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center gap-4">
        <button
          type="button"
          onClick={() => setSeed((s) => s + 1)}
          className="rounded-xl bg-amber-500 px-5 py-3 font-semibold text-black transition hover:bg-amber-400"
        >
          Run Simulation Scenario
        </button>
        <label className="text-sm text-gray-400">
          Inspect pick
          <select
            className="ml-2 rounded-lg border border-line bg-panel px-3 py-2 text-white"
            value={pick}
            onChange={(e) => setPick(Number(e.target.value))}
          >
            {Array.from({ length: 30 }, (_, i) => i + 1).map((n) => (
              <option key={n} value={n}>
                #{n}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Pick {pick} Distribution</h2>
          <ProbBarChart data={pickDist} />
        </section>

        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Sample Scenario (30 picks)</h2>
          <div className="max-h-80 space-y-2 overflow-y-auto text-sm">
            {scenario.map((s) => (
              <div
                key={s.pick}
                className="flex items-center justify-between rounded-lg border border-line px-3 py-2"
              >
                <div className="flex items-center gap-2">
                  <span className="w-6 font-bold text-amber-300">#{s.pick}</span>
                  <TeamLogo team={s.team} size={24} />
                  <span className="text-gray-400">{s.team}</span>
                </div>
                <span className="font-medium">{s.player}</span>
              </div>
            ))}
          </div>
        </section>
      </div>

      <section className="panel p-5">
        <h2 className="mb-4 text-lg font-semibold">Most Likely Board (Model Mean)</h2>
        <div className="grid gap-2 md:grid-cols-2">
          {board.map((b) => (
            <div
              key={b.pick}
              className="flex items-center justify-between rounded-lg border border-line px-3 py-2 text-sm"
            >
              <div className="flex items-center gap-2">
                <span className="font-bold text-amber-300">#{b.pick}</span>
                <TeamLogo team={b.team} size={22} />
                <span>{b.team}</span>
              </div>
              <span>
                {b.predicted_player}{" "}
                <span className="text-gray-500">({(b.probability * 100).toFixed(1)}%)</span>
              </span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function mulberry32(a: number) {
  return function () {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

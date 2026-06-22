"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { PlayerAvatar } from "@/components/PlayerAvatar";
import { ProbBarChart } from "@/components/ProbBarChart";
import { TeamLogo } from "@/components/TeamLogo";
import { slugify } from "@/lib/slug";

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

type MediaRow = { player: string; headshot_url?: string };

type ScenarioPick = { pick: number; team: string; player: string };

const REVEAL_MS = 520;

export function DraftSimulator({
  board,
  probabilities,
  media = [],
}: {
  board: BoardRow[];
  probabilities: ProbRow[];
  media?: MediaRow[];
}) {
  const [pick, setPick] = useState(5);
  const [seed, setSeed] = useState(0);
  const [revealed, setRevealed] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);
  const activeRef = useRef<HTMLDivElement>(null);

  const mediaMap = Object.fromEntries(media.map((m) => [m.player, m]));

  const scenario = useMemo(() => buildScenario(board, probabilities, seed), [board, probabilities, seed]);

  const pickDist = useMemo(() => {
    return probabilities
      .filter((p) => p.pick === pick)
      .sort((a, b) => b.probability - a.probability)
      .slice(0, 6)
      .map((p) => ({ label: p.player, value: p.probability }));
  }, [pick, probabilities]);

  const onClock = revealed > 0 ? scenario[revealed - 1] : null;
  const nextPick = revealed < 30 ? scenario[revealed] : null;

  const runDraftNight = useCallback(() => {
    setSeed((s) => s + 1);
    setRevealed(0);
    setIsRunning(true);
  }, []);

  useEffect(() => {
    if (!isRunning) return;
    if (revealed >= 30) {
      setIsRunning(false);
      return;
    }
    const timer = window.setTimeout(() => setRevealed((n) => n + 1), REVEAL_MS);
    return () => window.clearTimeout(timer);
  }, [isRunning, revealed]);

  useEffect(() => {
    activeRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [revealed]);

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center gap-4">
        <button
          type="button"
          onClick={runDraftNight}
          disabled={isRunning}
          className="rounded-xl bg-amber-500 px-5 py-3 font-semibold text-black transition hover:bg-amber-400 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isRunning ? "Draft in progress…" : "Run Draft Night"}
        </button>
        {!isRunning && revealed === 30 && (
          <button
            type="button"
            onClick={() => {
              setSeed((s) => s + 1);
              setRevealed(30);
            }}
            className="rounded-xl border border-line px-4 py-3 text-sm text-gray-300 hover:bg-white/5"
          >
            New Scenario (instant)
          </button>
        )}
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

      <section className="panel overflow-hidden border-amber-500/20">
        <div className="border-b border-line bg-gradient-to-r from-amber-500/10 to-transparent px-5 py-4">
          <p className="text-xs uppercase tracking-[0.25em] text-amber-400">
            {isRunning ? "On the clock" : revealed === 30 ? "Draft complete" : "Draft Night Simulator"}
          </p>
          {onClock && (
            <div className="mt-2 flex flex-wrap items-center gap-4">
              <span className="text-3xl font-bold text-amber-300">#{onClock.pick}</span>
              <TeamLogo team={onClock.team} size={36} />
              <div>
                <p className="text-sm text-gray-400">{onClock.team}</p>
                <p className="text-xl font-semibold text-white">{onClock.player}</p>
              </div>
              {isRunning && nextPick && (
                <p className="ml-auto text-sm text-gray-500">Next: #{nextPick.pick} {nextPick.team}</p>
              )}
            </div>
          )}
          {!onClock && !isRunning && (
            <p className="mt-1 text-gray-400">Run a stochastic first-round path — one pick at a time.</p>
          )}
        </div>

        <div ref={listRef} className="max-h-[28rem] space-y-1 overflow-y-auto p-4">
          {scenario.map((s, i) => {
            const visible = i < revealed;
            const isActive = i === revealed - 1 && isRunning;
            return (
              <div
                key={s.pick}
                ref={isActive ? activeRef : undefined}
                className={`flex items-center justify-between rounded-lg border px-3 py-2.5 text-sm transition-all duration-300 ${
                  visible
                    ? isActive
                      ? "border-amber-500/60 bg-amber-500/15 shadow-lg shadow-amber-500/10"
                      : "border-line bg-white/[0.03] opacity-100"
                    : "border-transparent opacity-25"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="w-7 font-bold text-amber-300">#{s.pick}</span>
                  <TeamLogo team={s.team} size={26} />
                  <span className="text-gray-400">{s.team}</span>
                </div>
                <div className="flex items-center gap-2">
                  {visible && (
                    <PlayerAvatar
                      name={s.player}
                      src={mediaMap[s.player]?.headshot_url}
                      size={28}
                      className="rounded-lg"
                    />
                  )}
                  {visible ? (
                    <Link href={`/players/${slugify(s.player)}`} className="font-medium hover:text-amber-300">
                      {s.player}
                    </Link>
                  ) : (
                    <span className="text-gray-600">—</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
        <div className="border-t border-line px-5 py-2">
          <div className="h-1 overflow-hidden rounded-full bg-white/5">
            <div
              className="h-full rounded-full bg-amber-500 transition-all duration-300"
              style={{ width: `${(revealed / 30) * 100}%` }}
            />
          </div>
          <p className="mt-1 text-center text-xs text-gray-500">{revealed} / 30 picks</p>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Pick {pick} Distribution</h2>
          <ProbBarChart data={pickDist} />
        </section>

        <section className="panel p-5">
          <h2 className="mb-4 text-lg font-semibold">Most Likely Board (Model Mean)</h2>
          <div className="max-h-72 space-y-2 overflow-y-auto text-sm">
            {board.slice(0, 15).map((b) => (
              <div
                key={b.pick}
                className="flex items-center justify-between rounded-lg border border-line px-3 py-2"
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
    </div>
  );
}

function buildScenario(board: BoardRow[], probabilities: ProbRow[], seed: number): ScenarioPick[] {
  const rng = mulberry32(42 + seed);
  const byPick: Record<number, ProbRow[]> = {};
  for (const p of probabilities) {
    if (!byPick[p.pick]) byPick[p.pick] = [];
    byPick[p.pick].push(p);
  }

  const used = new Set<string>();
  const result: ScenarioPick[] = [];

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
}

function mulberry32(a: number) {
  return function () {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

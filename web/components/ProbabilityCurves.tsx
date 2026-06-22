"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { PlayerAvatar } from "@/components/PlayerAvatar";
import { slugify } from "@/lib/slug";

type ProbPoint = { pick: number; probability: number };
type PlayerOption = { name: string; slug: string; headshot?: string };

export function ProbabilityCurves({
  players,
  probabilities,
}: {
  players: PlayerOption[];
  probabilities: Record<string, ProbPoint[]>;
}) {
  const [selected, setSelected] = useState(players[0]?.name ?? "");

  const chartData = useMemo(() => {
    const pts = probabilities[selected] ?? [];
    return pts.map((p) => ({
      pick: p.pick,
      probability: p.probability,
      pct: `${(p.probability * 100).toFixed(1)}%`,
    }));
  }, [selected, probabilities]);

  const peak = chartData.reduce(
    (best, row) => (row.probability > best.probability ? row : best),
    chartData[0] ?? { pick: 0, probability: 0, pct: "0%" }
  );

  const media = players.find((p) => p.name === selected);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-2">
        {players.map((p) => (
          <button
            key={p.name}
            type="button"
            onClick={() => setSelected(p.name)}
            className={`flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm transition ${
              selected === p.name
                ? "border-amber-500/50 bg-amber-500/10 text-amber-200"
                : "border-line text-gray-400 hover:bg-white/5"
            }`}
          >
            <PlayerAvatar name={p.name} src={p.headshot} size={24} className="rounded-full" />
            {p.name}
          </button>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <section className="panel p-5">
          <h2 className="mb-1 text-lg font-semibold text-white">{selected}</h2>
          <p className="mb-4 text-sm text-gray-500">Pick probability distribution · Monte Carlo</p>
          <div className="h-72 w-full">
            <ResponsiveContainer>
              <AreaChart data={chartData} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="probFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#f59e0b" stopOpacity={0.45} />
                    <stop offset="100%" stopColor="#f59e0b" stopOpacity={0.02} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#1f2937" vertical={false} />
                <XAxis
                  dataKey="pick"
                  tick={{ fill: "#9ca3af", fontSize: 12 }}
                  label={{ value: "Pick", position: "insideBottom", offset: -2, fill: "#6b7280" }}
                />
                <YAxis
                  tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                  tick={{ fill: "#9ca3af", fontSize: 12 }}
                  domain={[0, "auto"]}
                />
                <Tooltip
                  formatter={(v: number) => [`${(v * 100).toFixed(1)}%`, "Probability"]}
                  labelFormatter={(l) => `Pick #${l}`}
                  contentStyle={{ background: "#111827", border: "1px solid #374151" }}
                />
                <Area
                  type="monotone"
                  dataKey="probability"
                  stroke="#f59e0b"
                  strokeWidth={2}
                  fill="url(#probFill)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel flex flex-col gap-4 p-5">
          <div className="flex items-center gap-4">
            <PlayerAvatar name={selected} src={media?.headshot} size={64} />
            <div>
              <Link
                href={`/players/${media?.slug ?? slugify(selected)}`}
                className="text-lg font-semibold text-white hover:text-amber-300"
              >
                {selected}
              </Link>
              <p className="text-sm text-gray-500">Floor · ceiling from simulation mass</p>
            </div>
          </div>
          {peak && (
            <dl className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <dt className="stat-label">Peak Pick</dt>
                <dd className="stat-value">#{peak.pick}</dd>
              </div>
              <div>
                <dt className="stat-label">Peak Probability</dt>
                <dd className="stat-value">{peak.pct}</dd>
              </div>
            </dl>
          )}
          <div className="max-h-48 space-y-1 overflow-y-auto text-sm">
            {chartData
              .filter((r) => r.probability >= 0.01)
              .sort((a, b) => b.probability - a.probability)
              .map((r) => (
                <div key={r.pick} className="flex items-center justify-between rounded border border-line px-2 py-1">
                  <span className="text-gray-400">#{r.pick}</span>
                  <div className="mx-2 h-1.5 flex-1 overflow-hidden rounded-full bg-white/5">
                    <div
                      className="h-full rounded-full bg-amber-500"
                      style={{ width: `${Math.min(r.probability * 100, 100)}%` }}
                    />
                  </div>
                  <span className="w-12 text-right font-mono text-amber-300">{r.pct}</span>
                </div>
              ))}
          </div>
        </section>
      </div>
    </div>
  );
}

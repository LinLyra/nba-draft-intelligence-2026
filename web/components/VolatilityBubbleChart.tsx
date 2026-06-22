"use client";

import Link from "next/link";
import { useMemo } from "react";
import {
  CartesianGrid,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";
import { volatilityLabel } from "@/lib/volatility";
import { slugify } from "@/lib/slug";

export type VolatilityPoint = {
  player: string;
  mean_pick: number;
  std_pick: number;
  source_count: number;
  min_pick: number;
  max_pick: number;
};

const COLORS = {
  High: "#fb7185",
  Medium: "#fbbf24",
  Low: "#34d399",
};

function BubbleShape(props: {
  cx?: number;
  cy?: number;
  payload?: VolatilityPoint & { fill: string };
}) {
  const { cx = 0, cy = 0, payload } = props;
  if (!payload) return null;
  const r = 6 + payload.source_count * 2.2;
  return (
    <circle
      cx={cx}
      cy={cy}
      r={r}
      fill={payload.fill}
      fillOpacity={0.55}
      stroke={payload.fill}
      strokeWidth={1.5}
      strokeOpacity={0.9}
    />
  );
}

export function VolatilityBubbleChart({ data }: { data: VolatilityPoint[] }) {
  const chartData = useMemo(
    () =>
      data.map((d) => ({
        ...d,
        label: volatilityLabel(d.std_pick),
        fill: COLORS[volatilityLabel(d.std_pick)],
      })),
    [data]
  );

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-4 text-xs text-gray-400">
        <span className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-rose-400" /> High volatility
        </span>
        <span className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-amber-400" /> Medium
        </span>
        <span className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-emerald-400" /> Low
        </span>
        <span className="text-gray-500">Bubble size = source count</span>
      </div>

      <div className="h-[28rem] w-full">
        <ResponsiveContainer>
          <ScatterChart margin={{ top: 16, right: 24, bottom: 24, left: 8 }}>
            <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />
            <XAxis
              type="number"
              dataKey="mean_pick"
              name="Mean pick"
              domain={[0, 35]}
              tick={{ fill: "#9ca3af", fontSize: 12 }}
              label={{ value: "Mean pick", position: "insideBottom", offset: -8, fill: "#6b7280" }}
            />
            <YAxis
              type="number"
              dataKey="std_pick"
              name="Std pick"
              tick={{ fill: "#9ca3af", fontSize: 12 }}
              label={{
                value: "Volatility (std)",
                angle: -90,
                position: "insideLeft",
                fill: "#6b7280",
              }}
            />
            <ZAxis type="number" dataKey="source_count" range={[80, 400]} />
            <Tooltip
              cursor={{ strokeDasharray: "3 3", stroke: "#4b5563" }}
              content={({ active, payload }) => {
                if (!active || !payload?.length) return null;
                const p = payload[0].payload as VolatilityPoint & { label: string };
                return (
                  <div className="rounded-lg border border-line bg-panel p-3 text-sm shadow-xl">
                    <Link href={`/players/${slugify(p.player)}`} className="font-semibold text-amber-300">
                      {p.player}
                    </Link>
                    <p className="mt-1 text-gray-400">Mean #{p.mean_pick.toFixed(1)}</p>
                    <p className="text-gray-400">Std {p.std_pick.toFixed(2)} · {p.label}</p>
                    <p className="text-gray-500">
                      Range #{p.min_pick}–#{p.max_pick} · {p.source_count} sources
                    </p>
                  </div>
                );
              }}
            />
            <Scatter data={chartData} shape={<BubbleShape />} />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

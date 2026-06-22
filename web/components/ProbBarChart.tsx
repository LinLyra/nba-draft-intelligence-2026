"use client";

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface Props {
  data: { label: string; value: number }[];
}

export function ProbBarChart({ data }: Props) {
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer>
        <BarChart data={data} layout="vertical" margin={{ left: 8, right: 16 }}>
          <XAxis type="number" domain={[0, 1]} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} stroke="#6b7280" />
          <YAxis type="category" dataKey="label" width={120} tick={{ fill: "#d1d5db", fontSize: 12 }} />
          <Tooltip
            formatter={(v: number) => [`${(v * 100).toFixed(1)}%`, "Probability"]}
            contentStyle={{ background: "#111827", border: "1px solid #374151" }}
          />
          <Bar dataKey="value" fill="#f59e0b" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

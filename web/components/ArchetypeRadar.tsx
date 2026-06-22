"use client";

import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

interface Props {
  data: { trait: string; value: number }[];
  color?: string;
}

export function ArchetypeRadar({ data, color = "#f59e0b" }: Props) {
  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="75%">
          <PolarGrid stroke="#374151" />
          <PolarAngleAxis dataKey="trait" tick={{ fill: "#9ca3af", fontSize: 11 }} />
          <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
          <Radar
            dataKey="value"
            stroke={color}
            fill={color}
            fillOpacity={0.25}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

"use client";

import {
  Legend,
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";

interface TraitRow {
  trait: string;
  team: number;
  player: number;
}

interface Props {
  data: TraitRow[];
  teamLabel?: string;
  playerLabel?: string;
}

export function DualRadar({
  data,
  teamLabel = "Team Needs",
  playerLabel = "Player Profile",
}: Props) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer>
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="72%">
          <PolarGrid stroke="#374151" />
          <PolarAngleAxis dataKey="trait" tick={{ fill: "#9ca3af", fontSize: 11 }} />
          <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
          <Radar
            name={teamLabel}
            dataKey="team"
            stroke="#60a5fa"
            fill="#60a5fa"
            fillOpacity={0.2}
            strokeWidth={2}
          />
          <Radar
            name={playerLabel}
            dataKey="player"
            stroke="#f59e0b"
            fill="#f59e0b"
            fillOpacity={0.25}
            strokeWidth={2}
          />
          <Legend wrapperStyle={{ color: "#d1d5db", fontSize: 12 }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

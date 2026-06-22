import Image from "next/image";
import Link from "next/link";
import { PlayerAvatar } from "@/components/PlayerAvatar";
import { SchoolLogo } from "@/components/SchoolLogo";
import { getPlayerMediaByName } from "@/lib/media";
import { teamLogoUrl, teamSlug } from "@/lib/teams";
import { pct, slugify, volatilityLabel } from "@/lib/data";
import type { BoardRow, ProspectRow } from "@/lib/data";

interface Props {
  row: BoardRow;
  stdPick?: number;
  prospect?: ProspectRow;
}

export function BoardCard({ row, stdPick, prospect }: Props) {
  const vol = stdPick !== undefined ? volatilityLabel(stdPick) : null;
  const slug = slugify(row.predicted_player);
  const media = getPlayerMediaByName(row.predicted_player);
  const school = media?.school ?? prospect?.school_or_league ?? null;

  return (
    <div className="panel group flex items-center gap-4 p-4 transition hover:border-amber-500/40 hover:bg-white/5">
      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-amber-500/15 text-lg font-bold text-amber-300">
        {row.pick}
      </div>
      <PlayerAvatar
        name={row.predicted_player}
        src={media?.headshot_url}
        size={48}
        className="shrink-0 rounded-xl"
      />
      <Link
        href={`/teams/${teamSlug(row.team)}`}
        className="relative h-10 w-10 shrink-0"
        title={row.team}
      >
        <Image
          src={teamLogoUrl(row.team)}
          alt={row.team}
          fill
          className="object-contain"
        />
      </Link>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <Link
            href={`/players/${slug}`}
            className="truncate text-lg font-semibold text-white group-hover:text-amber-200"
          >
            {row.predicted_player}
          </Link>
          {vol && (
            <span
              className={
                vol === "Low"
                  ? "badge-low"
                  : vol === "Medium"
                    ? "badge-medium"
                    : "badge-high"
              }
            >
              {vol}
            </span>
          )}
        </div>
        <p className="text-sm text-gray-400">
          <Link href={`/teams/${teamSlug(row.team)}`} className="hover:text-amber-300">
            {row.team}
          </Link>
          {prospect?.position && (
            <span className="text-gray-500"> · {prospect.position}</span>
          )}
        </p>
        {prospect && (prospect.height || prospect.weight_lbs) && (
          <p className="text-xs text-gray-500">
            {prospect.height}
            {prospect.weight_lbs ? ` · ${prospect.weight_lbs} lbs` : ""}
          </p>
        )}
        {school && (
          <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
            <SchoolLogo school={school} size={18} />
            <span>{school}</span>
          </div>
        )}
      </div>
      <Link href={`/players/${slug}`} className="text-right">
        <div className="text-2xl font-bold text-amber-300">{pct(row.probability)}</div>
        <div className="text-xs text-gray-500">pick probability</div>
      </Link>
    </div>
  );
}

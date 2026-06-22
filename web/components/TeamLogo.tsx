import Image from "next/image";
import { teamLogoUrl } from "@/lib/teams";

interface Props {
  team: string;
  size?: number;
}

export function TeamLogo({ team, size = 40 }: Props) {
  const src = teamLogoUrl(team);
  if (!src) return null;
  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <Image src={src} alt={`${team} logo`} fill className="object-contain" />
    </div>
  );
}

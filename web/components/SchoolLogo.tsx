"use client";

import Image from "next/image";
import { useState } from "react";
import { schoolLogoUrl } from "@/lib/schools";

interface Props {
  school: string;
  size?: number;
}

export function SchoolLogo({ school, size = 32 }: Props) {
  const src = schoolLogoUrl(school);
  const [failed, setFailed] = useState(false);

  if (!school || failed) return null;

  return (
    <div className="relative shrink-0" style={{ width: size, height: size }} title={school}>
      <Image
        src={src}
        alt={`${school} logo`}
        fill
        className="object-contain"
        onError={() => setFailed(true)}
      />
    </div>
  );
}

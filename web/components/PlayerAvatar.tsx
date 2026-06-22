"use client";

import Image from "next/image";
import { useState } from "react";

interface Props {
  name: string;
  src?: string | null;
  size?: number;
  className?: string;
}

export function PlayerAvatar({ name, src, size = 96, className = "" }: Props) {
  const [failed, setFailed] = useState(false);

  const initials = name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  if (!src || failed) {
    return (
      <div
        className={`flex items-center justify-center rounded-2xl bg-gradient-to-br from-amber-500/30 to-orange-700/20 font-bold text-amber-200 ${className}`}
        style={{ width: size, height: size, fontSize: size * 0.32 }}
      >
        {initials}
      </div>
    );
  }

  return (
    <div
      className={`relative overflow-hidden rounded-2xl border border-line bg-panel ${className}`}
      style={{ width: size, height: size }}
    >
      <Image
        src={src}
        alt={name}
        fill
        className="object-cover object-top"
        onError={() => setFailed(true)}
      />
    </div>
  );
}

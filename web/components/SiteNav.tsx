"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/", label: "Board" },
  { href: "/simulator", label: "Simulator" },
  { href: "/volatility", label: "Volatility" },
  { href: "/team-fit", label: "Team Fit" },
  { href: "/probability", label: "Probability" },
  { href: "/methodology", label: "Methodology" },
  { href: "/about", label: "About" },
];

function navClass(active: boolean, mobile = false) {
  if (mobile) {
    return active
      ? "border-amber-500/50 bg-amber-500/10 text-amber-300"
      : "border-line text-gray-400";
  }
  return active ? "text-amber-300" : "text-gray-300";
}

export function DesktopNav() {
  const pathname = usePathname();
  return (
    <nav className="hidden gap-5 lg:flex">
      {NAV.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={`text-sm transition hover:text-amber-300 ${navClass(pathname === item.href)}`}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}

export function MobileNav() {
  const pathname = usePathname();
  return (
    <nav className="flex gap-2 overflow-x-auto pb-1 lg:hidden">
      {NAV.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={`shrink-0 rounded-full border px-3 py-1 text-xs ${navClass(
            pathname === item.href,
            true
          )}`}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}

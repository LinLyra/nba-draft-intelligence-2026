import Link from "next/link";
import { DesktopNav, MobileNav } from "@/components/SiteNav";
import "./globals.css";

export const metadata = {
  title: "NBA Draft Intelligence System",
  description:
    "AI-powered probabilistic NBA Draft forecasting with consensus, betting odds, team fit, and Monte Carlo simulation.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="sticky top-0 z-50 border-b border-line bg-court/90 backdrop-blur">
          <div className="mx-auto max-w-7xl space-y-3 px-4 py-4">
            <div className="flex items-center justify-between">
              <Link href="/" className="flex flex-col">
                <span className="text-xs uppercase tracking-[0.25em] text-amber-400">
                  DIS 2026
                </span>
                <span className="font-display text-xl font-semibold text-white">
                  Draft Intelligence
                </span>
              </Link>
              <DesktopNav />
            </div>
            <MobileNav />
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-8">{children}</main>
        <footer className="border-t border-line py-8 text-center text-sm text-gray-500">
          NBA Draft Intelligence System · Probabilistic forecasting framework
        </footer>
      </body>
    </html>
  );
}

import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        court: "#0a0f1a",
        panel: "#111827",
        accent: "#f59e0b",
        line: "#1f2937",
      },
      fontFamily: {
        display: ["Syne", "system-ui", "sans-serif"],
        signature: ["Caveat", "cursive"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;

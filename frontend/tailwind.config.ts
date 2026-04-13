import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0b1f1a",
        mint: "#22c1a1",
        sky: "#5fb8ff",
        sand: "#ffe2b3",
        slate: "#1a2e38"
      },
      boxShadow: {
        soft: "0 20px 45px -28px rgba(8, 35, 42, 0.45)"
      }
    }
  },
  plugins: []
};

export default config;

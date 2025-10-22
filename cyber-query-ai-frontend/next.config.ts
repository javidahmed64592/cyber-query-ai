import type { NextConfig } from "next";
import fs from "fs";
import path from "path";
import { ConfigResponse } from "@/lib/types";

// Read backend config to get host and port
const getBackendURL = () => {
  try {
    const configPath = path.resolve(__dirname, "..", "config.json");
    const configData = fs.readFileSync(configPath, "utf-8");
    const config: ConfigResponse = JSON.parse(configData);
    return `http://${config.host}:${config.port}`;
  } catch (error) {
    console.warn(
      "Failed to read config.json, falling back to http://localhost:8000"
    );
    return "http://localhost:8000";
  }
};

const nextConfig: NextConfig = {
  output: "export", // Enable static export
  trailingSlash: true,
  images: {
    unoptimized: true, // Required for static export
  },
  ...(process.env.NODE_ENV === "development" && {
    headers: async () => [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
        ],
      },
    ],
    async rewrites() {
      const backendURL = getBackendURL();
      return [
        {
          source: "/api/:path*",
          destination: `${backendURL}/api/:path*`, // FastAPI backend from config.json
        },
      ];
    },
  }),
};

export default nextConfig;

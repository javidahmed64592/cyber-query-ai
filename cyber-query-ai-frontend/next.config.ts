import type { NextConfig } from "next";
import fs from "fs";
import path from "path";

// Type for reading the backend config.json
interface BackendConfig {
  server: {
    host: string;
    port: number;
  };
}

// Read backend config to get host and port
const getBackendURL = () => {
  try {
    const configPath = path.resolve(
      __dirname,
      "..",
      "configuration",
      "config.json"
    );
    const configData = fs.readFileSync(configPath, "utf-8");
    const config: BackendConfig = JSON.parse(configData);
    return `https://${config.server.host}:${config.server.port}`;
  } catch (error) {
    console.warn(
      "Failed to read config.json, falling back to https://localhost:443"
    );
    return "https://localhost:443";
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

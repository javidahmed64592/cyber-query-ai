import type { NextConfig } from "next";
import fs from "fs";
import path from "path";

// Read environment file to get host and port
const getBackendURL = () => {
  try {
    const variablesPath = path.resolve(__dirname, "..", ".env");
    const variables = fs.readFileSync(variablesPath, "utf-8");
    const matchHost = variables.match(/^HOST=(.*)$/m);
    const matchPort = variables.match(/^PORT=(.*)$/m);
    const host = matchHost ? matchHost[1] : "localhost";
    const port = matchPort ? matchPort[1] : "8000";
    return `http://${host}:${port}`;
  } catch (error) {
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
          destination: `${backendURL}/api/:path*`,
        },
      ];
    },
  }),
};

export default nextConfig;

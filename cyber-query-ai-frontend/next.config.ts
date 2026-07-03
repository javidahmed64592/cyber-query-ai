import type { NextConfig } from "next";

// Backend URL for dev proxy
const getBackendURL = () => {
  return process.env.BACKEND_URL || "https://localhost:443";
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

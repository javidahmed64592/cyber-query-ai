import type { NextConfig } from "next";

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
      return [
        {
          source: "/api/:path*",
          destination: "http://localhost:8000/api/:path*", // FastAPI backend
        },
      ];
    },
  }),
};

export default nextConfig;

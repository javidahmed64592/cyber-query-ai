import type { Metadata } from "next";

import "./globals.css";
import Footer from "@/components/Footer";
import Navigation from "@/components/Navigation";

export const metadata: Metadata = {
  title: "CyberQueryAI",
  description:
    "AI-powered cybersecurity assistant for ethical penetration testing and security research.",
  keywords: [
    "cybersecurity",
    "AI",
    "penetration testing",
    "security research",
    "ethical hacking",
  ],
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  icons: {
    icon: [
      { url: "/icon.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/apple-icon.png", sizes: "180x180", type: "image/png" }],
    other: [
      {
        rel: "android-chrome",
        url: "/android-icon-192x192.png",
        sizes: "192x192",
      },
    ],
  },
  manifest: "/manifest.json",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-[var(--background)]">
          <Navigation />
          <main className="container mx-auto px-4 py-8 max-w-6xl pb-20">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  );
}

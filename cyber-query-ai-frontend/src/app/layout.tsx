import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";

export const metadata: Metadata = {
  title: "CyberQueryAI",
  description: "AI-powered cybersecurity assistant for ethical penetration testing and security research",
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
          <main className="container mx-auto px-4 py-8 max-w-6xl">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}

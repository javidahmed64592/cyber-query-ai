"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { version } from "../lib/version";

import HealthIndicator from "./HealthIndicator";

const Navigation = () => {
  const pathname = usePathname();

  const navItems = [
    {
      name: "Command Gen",
      href: "/command-generation",
      active: pathname === "/command-generation/",
    },
    {
      name: "Script Gen",
      href: "/script-generation",
      active: pathname === "/script-generation/",
      disabled: true,
    },
    {
      name: "Command Explain",
      href: "/command-explanation",
      active: pathname === "/command-explanation/",
      disabled: true,
    },
    {
      name: "Script Explain",
      href: "/script-explanation",
      active: pathname === "/script-explanation/",
      disabled: true,
    },
    {
      name: "Exploit Search",
      href: "/exploit-search",
      active: pathname === "/exploit-search/",
      disabled: true,
    },
    {
      name: "About",
      href: "/about",
      active: pathname === "/about/",
      disabled: true,
    },
  ];

  return (
    <nav className="bg-[var(--background-secondary)] border-b border-[var(--terminal-border)] sticky top-0 z-50 w-full">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex items-center h-16 w-full justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-4">
            <Link href="/" className="flex items-center space-x-2">
              <div className="text-2xl font-bold neon-glow text-[var(--text-primary)]">
                CyberQueryAI
              </div>
              <div className="text-xs text-[var(--text-muted)] hidden sm:block">
                v{version}
              </div>
            </Link>
            <HealthIndicator />
          </div>

          {/* Navigation Links */}
          <div className="flex flex-1 justify-end space-x-1">
            {navItems.map(item => {
              const normalized = (pathname || "").replace(/\/$/, "") || "/";
              const isActive =
                !item.disabled &&
                (normalized === item.href ||
                  (item.href === "/command-generation" && normalized === "/"));

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`
                    px-4 py-2 rounded-md text-sm font-medium transition-all duration-200
                    ${
                      item.disabled
                        ? "text-[var(--text-muted)] cursor-not-allowed opacity-50"
                        : isActive
                          ? "text-[var(--border-accent)] font-bold neon-glow"
                          : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--background-tertiary)]"
                    }
                  `}
                  onClick={e => item.disabled && e.preventDefault()}
                >
                  {item.name}
                  {item.disabled && (
                    <span className="ml-1 text-xs opacity-50">(Soon)</span>
                  )}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

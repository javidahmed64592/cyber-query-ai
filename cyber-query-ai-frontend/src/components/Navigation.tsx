"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

import HealthIndicator from "@/components/HealthIndicator";

const Navigation = () => {
  const pathname = usePathname();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navItems = [
    {
      name: "AI Assistant",
      href: "/assistant",
      active: pathname === "/assistant/",
    },
    {
      name: "Command Generation",
      href: "/command-generation",
      active: pathname === "/command-generation/",
    },
    {
      name: "Script Generation",
      href: "/script-generation",
      active: pathname === "/script-generation/",
    },
    {
      name: "Command Explain",
      href: "/command-explanation",
      active: pathname === "/command-explanation/",
    },
    {
      name: "Script Explain",
      href: "/script-explanation",
      active: pathname === "/script-explanation/",
    },
    {
      name: "Exploit Search",
      href: "/exploit-search",
      active: pathname === "/exploit-search/",
    },
    {
      name: "About",
      href: "/about",
      active: pathname === "/about/",
    },
  ];

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="bg-[var(--background-secondary)] border-b border-[var(--terminal-border)] sticky top-0 z-50 w-full">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex items-center h-16 w-full justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-4">
            <Link href="/" className="flex items-center space-x-3">
              <Image
                src="/logo.svg"
                alt="CyberQueryAI Logo"
                width={32}
                height={32}
                className="neon-glow"
                priority
              />
              <div className="flex flex-col">
                <div className="text-xl sm:text-xl font-bold neon-glow text-[var(--text-primary)] nav-logo-text">
                  CyberQueryAI
                </div>
              </div>
            </Link>
            <HealthIndicator />
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden lg:flex flex-1 justify-end space-x-1">
            {navItems.map(item => {
              const normalized = (pathname || "").replace(/\/$/, "") || "/";
              const isActive =
                normalized === item.href ||
                (item.href === "/assistant" && normalized === "/");

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`
                    px-4 py-2 rounded-md text-sm font-medium transition-all duration-200
                    ${
                      isActive
                        ? "text-[var(--border-accent)] font-bold neon-glow"
                        : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--background-tertiary)]"
                    }
                  `}
                >
                  {item.name}
                </Link>
              );
            })}
          </div>

          {/* Mobile Menu Button */}
          <div className="lg:hidden">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--background-tertiary)] focus:outline-none focus:ring-2 focus:ring-inset focus:ring-[var(--border-accent)]"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {/* Hamburger icon */}
              <svg
                className={`${isMenuOpen ? "hidden" : "block"} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
              {/* Close icon */}
              <svg
                className={`${isMenuOpen ? "block" : "hidden"} h-6 w-6`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        <div className={`lg:hidden ${isMenuOpen ? "block" : "hidden"}`}>
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-[var(--terminal-border)] mt-2">
            {navItems.map(item => {
              const normalized = (pathname || "").replace(/\/$/, "") || "/";
              const isActive =
                normalized === item.href ||
                (item.href === "/assistant" && normalized === "/");

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={closeMenu}
                  className={`
                    block px-3 py-2 rounded-md text-base font-medium transition-all duration-200
                    ${
                      isActive
                        ? "text-[var(--border-accent)] font-bold neon-glow bg-[var(--background-tertiary)]"
                        : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--background-tertiary)]"
                    }
                  `}
                >
                  {item.name}
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

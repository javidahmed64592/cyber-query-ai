'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Navigation = () => {
  const pathname = usePathname();

  const navItems = [
    { name: 'Command Gen', href: '/command-generation', active: pathname === '/command-generation' || pathname === '/' },
    { name: 'Script Gen', href: '/script-generation', active: pathname === '/script-generation', disabled: true },
    { name: 'Exploit Search', href: '/exploit-search', active: pathname === '/exploit-search', disabled: true },
    { name: 'Settings', href: '/settings', active: pathname === '/settings', disabled: true },
  ];

  return (
    <nav className="bg-[var(--background-secondary)] border-b border-[var(--terminal-border)] sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="text-2xl font-bold neon-glow text-[var(--text-primary)]">
                CyberQueryAI
              </div>
              <div className="text-xs text-[var(--text-muted)] hidden sm:block">
                v0.1.0
              </div>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex space-x-1">
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`
                  px-4 py-2 rounded-md text-sm font-medium transition-all duration-200
                  ${item.disabled
                    ? 'text-[var(--text-muted)] cursor-not-allowed opacity-50'
                    : item.active
                      ? 'text-[var(--border-accent)] font-bold neon-glow'
                      : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--background-tertiary)]'
                  }
                `}
                onClick={(e) => item.disabled && e.preventDefault()}
              >
                {item.name}
                {item.disabled && (
                  <span className="ml-1 text-xs opacity-50">(Soon)</span>
                )}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;

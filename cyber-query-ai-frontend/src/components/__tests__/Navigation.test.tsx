import { render, screen } from "@testing-library/react";
import React from "react";

import Navigation from "../Navigation";

// Mock Next.js Link component
jest.mock("next/link", () => {
  const MockLink = ({
    children,
    href,
    ...props
  }: {
    children: React.ReactNode;
    href: string;
    [key: string]: unknown;
  }) => (
    <a href={href} {...props}>
      {children}
    </a>
  );
  MockLink.displayName = "MockLink";
  return MockLink;
});

describe("Navigation", () => {
  it("renders the CyberQueryAI logo", () => {
    render(<Navigation />);
    expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
  });

  it("renders version number", () => {
    render(<Navigation />);
    expect(screen.getByText("v0.1.0")).toBeInTheDocument();
  });

  it("renders all navigation items", () => {
    render(<Navigation />);
    expect(screen.getByText("Command Gen")).toBeInTheDocument();
    expect(screen.getByText("Script Gen")).toBeInTheDocument();
    expect(screen.getByText("Exploit Search")).toBeInTheDocument();
    expect(screen.getByText("Settings")).toBeInTheDocument();
  });

  it('shows "(Soon)" for disabled navigation items', () => {
    render(<Navigation />);
    const soonLabels = screen.getAllByText("(Soon)");
    expect(soonLabels).toHaveLength(3); // Script Gen, Exploit Search, Settings
  });

  it("renders navigation links with correct hrefs", () => {
    render(<Navigation />);
    expect(screen.getByRole("link", { name: /Command Gen/ })).toHaveAttribute(
      "href",
      "/command-generation"
    );
    expect(screen.getByRole("link", { name: /Script Gen/ })).toHaveAttribute(
      "href",
      "/script-generation"
    );
    expect(
      screen.getByRole("link", { name: /Exploit Search/ })
    ).toHaveAttribute("href", "/exploit-search");
    expect(screen.getByRole("link", { name: /Settings/ })).toHaveAttribute(
      "href",
      "/settings"
    );
  });

  it("applies active styling to current page", () => {
    // Mock usePathname to return '/command-generation'
    jest.mock("next/navigation", () => ({
      usePathname: () => "/command-generation",
    }));

    render(<Navigation />);
    const commandGenLink = screen.getByRole("link", { name: /Command Gen/ });
    expect(commandGenLink).toHaveClass("neon-glow");
  });

  it("applies disabled styling to inactive navigation items", () => {
    render(<Navigation />);
    const scriptGenLink = screen.getByRole("link", {
      name: /Script Gen \(Soon\)/,
    });
    expect(scriptGenLink).toHaveClass("cursor-not-allowed", "opacity-50");
  });
});

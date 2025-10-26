import { render, screen, fireEvent } from "@testing-library/react";
import { usePathname } from "next/navigation";
import React from "react";

import Navigation from "@/components/Navigation";
import { useHealthStatus } from "@/lib/api";

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

// Mock Next.js usePathname hook
jest.mock("next/navigation", () => ({
  usePathname: jest.fn(),
}));

// Mock the useHealthStatus hook
jest.mock("../../lib/api", () => ({
  useHealthStatus: jest.fn(),
}));

const mockUseHealthStatus = useHealthStatus as jest.MockedFunction<
  typeof useHealthStatus
>;

const mockUsePathname = usePathname as jest.MockedFunction<typeof usePathname>;

describe("Navigation", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockUseHealthStatus.mockReturnValue("online");
    mockUsePathname.mockReturnValue("/");
  });
  it("renders the CyberQueryAI logo", () => {
    render(<Navigation />);
    expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
  });

  it("renders all navigation items", () => {
    render(<Navigation />);
    // Check that navigation items exist (they appear in both desktop and mobile)
    expect(screen.getAllByText("AI Assistant")).toHaveLength(2);
    expect(screen.getAllByText("Code Generation")).toHaveLength(2);
    expect(screen.getAllByText("Code Explanation")).toHaveLength(2);
    expect(screen.getAllByText("Exploit Search")).toHaveLength(2);
    expect(screen.getAllByText("About")).toHaveLength(2);
  });

  it("renders navigation links with correct hrefs", () => {
    render(<Navigation />);
    // Get desktop navigation links (first occurrence)
    const aiAssistantLinks = screen.getAllByRole("link", {
      name: /AI Assistant/,
    });
    expect(aiAssistantLinks[0]).toHaveAttribute("href", "/assistant");

    const codeGenLinks = screen.getAllByRole("link", {
      name: /Code Generation/,
    });
    expect(codeGenLinks[0]).toHaveAttribute("href", "/code-generation");

    const codeExplainLinks = screen.getAllByRole("link", {
      name: /Code Explanation/,
    });
    expect(codeExplainLinks[0]).toHaveAttribute("href", "/code-explanation");

    const exploitSearchLinks = screen.getAllByRole("link", {
      name: /Exploit Search/,
    });
    expect(exploitSearchLinks[0]).toHaveAttribute("href", "/exploit-search");

    const aboutLinks = screen.getAllByRole("link", { name: /About/ });
    expect(aboutLinks[0]).toHaveAttribute("href", "/about");
  });

  it("applies active styling to current page", () => {
    mockUsePathname.mockReturnValue("/code-generation");

    render(<Navigation />);
    const codeGenLinks = screen.getAllByRole("link", {
      name: /Code Generation/,
    });
    // Both desktop and mobile links should have active styling
    expect(codeGenLinks[0]).toHaveClass("neon-glow");
    expect(codeGenLinks[1]).toHaveClass("neon-glow");
  });

  describe("Mobile Navigation", () => {
    it("renders mobile menu button", () => {
      render(<Navigation />);
      const menuButton = screen.getByRole("button", { name: /Open main menu/ });
      expect(menuButton).toBeInTheDocument();
    });

    it("toggles mobile menu when button is clicked", () => {
      render(<Navigation />);
      const menuButton = screen.getByRole("button", { name: /Open main menu/ });

      // Find all elements with lg:hidden class and get the second one (the mobile menu content)
      const navigation = screen.getByRole("navigation");
      const lgHiddenElements = navigation.querySelectorAll(".lg\\:hidden");
      const mobileMenu = lgHiddenElements[1]; // Second element is the mobile menu content

      expect(mobileMenu).toHaveClass("lg:hidden");
      expect(mobileMenu).toHaveClass("hidden");

      // Click to open menu
      fireEvent.click(menuButton);
      expect(mobileMenu).toHaveClass("lg:hidden");
      expect(mobileMenu).toHaveClass("block");
      expect(mobileMenu).not.toHaveClass("hidden");

      // Click again to close menu
      fireEvent.click(menuButton);
      expect(mobileMenu).toHaveClass("lg:hidden");
      expect(mobileMenu).toHaveClass("hidden");
      expect(mobileMenu).not.toHaveClass("block");
    });

    it("shows hamburger icon when menu is closed", () => {
      render(<Navigation />);
      const hamburgerIcon = screen
        .getByRole("button", { name: /Open main menu/ })
        .querySelector('svg[class*="block"]');
      expect(hamburgerIcon).toBeInTheDocument();
    });

    it("shows close icon when menu is open", () => {
      render(<Navigation />);
      const menuButton = screen.getByRole("button", { name: /Open main menu/ });

      fireEvent.click(menuButton);

      const closeIcon = screen
        .getByRole("button", { name: /Open main menu/ })
        .querySelector('svg[class*="block"]');
      expect(closeIcon).toBeInTheDocument();
    });

    it("closes mobile menu when navigation link is clicked", () => {
      render(<Navigation />);
      const menuButton = screen.getByRole("button", { name: /Open main menu/ });

      // Open menu
      fireEvent.click(menuButton);

      // Find the mobile menu content div (second lg:hidden element)
      const navigation = screen.getByRole("navigation");
      const lgHiddenElements = navigation.querySelectorAll(".lg\\:hidden");
      const mobileMenu = lgHiddenElements[1]; // Second element is the mobile menu content

      expect(mobileMenu).toHaveClass("lg:hidden");
      expect(mobileMenu).toHaveClass("block");

      // Click a navigation link in mobile menu
      const aboutLinks = screen.getAllByRole("link", { name: /About/ });
      const aboutLink = aboutLinks[1]; // Second one is in mobile menu
      if (aboutLink) {
        fireEvent.click(aboutLink);
      }

      // Menu should be closed
      expect(mobileMenu).toHaveClass("lg:hidden");
      expect(mobileMenu).toHaveClass("hidden");
      expect(mobileMenu).not.toHaveClass("block");
    });

    it("renders all navigation items in mobile menu", () => {
      render(<Navigation />);
      const menuButton = screen.getByRole("button", { name: /Open main menu/ });

      fireEvent.click(menuButton);

      // All navigation items should appear twice (desktop and mobile)
      expect(screen.getAllByText("AI Assistant")).toHaveLength(2);
      expect(screen.getAllByText("Code Generation")).toHaveLength(2);
      expect(screen.getAllByText("Code Explanation")).toHaveLength(2);
      expect(screen.getAllByText("Exploit Search")).toHaveLength(2);
      expect(screen.getAllByText("About")).toHaveLength(2);
    });

    it("applies active styling to current page in mobile menu", () => {
      mockUsePathname.mockReturnValue("/about");

      render(<Navigation />);
      const menuButton = screen.getByRole("button", { name: /Open main menu/ });

      fireEvent.click(menuButton);

      const aboutLinks = screen.getAllByRole("link", { name: /About/ });
      const mobileAboutLink = aboutLinks[1]; // Second one is in mobile menu
      expect(mobileAboutLink).toHaveClass("neon-glow");
    });
  });

  describe("HealthIndicator integration", () => {
    it("renders HealthIndicator in the navigation", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      // The HealthIndicator should render a circular indicator
      const indicators = screen
        .getByRole("navigation")
        .querySelectorAll('[title*="Server:"]');
      expect(indicators).toHaveLength(1);
    });

    it("displays online status indicator when server is online", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      const indicator = screen.getByTitle("Server: ONLINE");
      expect(indicator).toBeInTheDocument();
      expect(indicator).toHaveClass("bg-[var(--neon-green)]");
    });

    it("displays offline status indicator when server is offline", () => {
      mockUseHealthStatus.mockReturnValue("offline");

      render(<Navigation />);

      const indicator = screen.getByTitle("Server: OFFLINE");
      expect(indicator).toBeInTheDocument();
      expect(indicator).toHaveClass("bg-[var(--neon-red)]");
    });

    it("displays checking status indicator when status is being checked", () => {
      mockUseHealthStatus.mockReturnValue("checking");

      render(<Navigation />);

      const indicator = screen.getByTitle("Server: CHECKING");
      expect(indicator).toBeInTheDocument();
      expect(indicator).toHaveClass("bg-yellow-400");
      expect(indicator).toHaveClass("animate-pulse-neon");
    });

    it("positions HealthIndicator next to the logo", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      // Check that both the logo and health indicator are present
      expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
      expect(screen.getByTitle("Server: ONLINE")).toBeInTheDocument();

      // Check that they are both in the navigation
      const nav = screen.getByRole("navigation");
      expect(nav).toContainElement(screen.getByText("CyberQueryAI"));
      expect(nav).toContainElement(screen.getByTitle("Server: ONLINE"));
    });

    it("includes tooltip with status information", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      const healthIndicator = screen.getByTitle("Server: ONLINE");
      expect(healthIndicator).toHaveAttribute("title", "Server: ONLINE");
    });

    it("calls useHealthStatus hook when Navigation is rendered", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      expect(mockUseHealthStatus).toHaveBeenCalledTimes(1);
    });
  });
});

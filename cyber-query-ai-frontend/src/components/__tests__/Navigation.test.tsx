import { render, screen, fireEvent } from "@testing-library/react";
import { usePathname } from "next/navigation";
import React from "react";

import { useHealthStatus } from "../../lib/useHealthStatus";
import { version } from "../../lib/version";
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

// Mock Next.js usePathname hook
jest.mock("next/navigation", () => ({
  usePathname: jest.fn(),
}));

// Mock the useHealthStatus hook
jest.mock("../../lib/useHealthStatus", () => ({
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

  it("renders version number", () => {
    render(<Navigation />);
    expect(screen.getByText(`v${version}`)).toBeInTheDocument();
  });

  it("renders all navigation items", () => {
    render(<Navigation />);
    // Check that navigation items exist (they appear in both desktop and mobile)
    expect(screen.getAllByText("Command Generation")).toHaveLength(2);
    expect(screen.getAllByText("Script Generation")).toHaveLength(2);
    expect(screen.getAllByText("Command Explain")).toHaveLength(2);
    expect(screen.getAllByText("Script Explain")).toHaveLength(2);
    expect(screen.getAllByText("Exploit Search")).toHaveLength(2);
    expect(screen.getAllByText("About")).toHaveLength(2);
  });

  it("renders navigation links with correct hrefs", () => {
    render(<Navigation />);
    // Get desktop navigation links (first occurrence)
    const commandGenLinks = screen.getAllByRole("link", {
      name: /Command Generation/,
    });
    expect(commandGenLinks[0]).toHaveAttribute("href", "/command-generation");

    const scriptGenLinks = screen.getAllByRole("link", {
      name: /Script Generation/,
    });
    expect(scriptGenLinks[0]).toHaveAttribute("href", "/script-generation");

    const commandExplainLinks = screen.getAllByRole("link", {
      name: /Command Explain/,
    });
    expect(commandExplainLinks[0]).toHaveAttribute(
      "href",
      "/command-explanation"
    );

    const scriptExplainLinks = screen.getAllByRole("link", {
      name: /Script Explain/,
    });
    expect(scriptExplainLinks[0]).toHaveAttribute(
      "href",
      "/script-explanation"
    );

    const exploitSearchLinks = screen.getAllByRole("link", {
      name: /Exploit Search/,
    });
    expect(exploitSearchLinks[0]).toHaveAttribute("href", "/exploit-search");

    const aboutLinks = screen.getAllByRole("link", { name: /About/ });
    expect(aboutLinks[0]).toHaveAttribute("href", "/about");
  });

  it("applies active styling to current page", () => {
    mockUsePathname.mockReturnValue("/command-generation");

    render(<Navigation />);
    const commandGenLinks = screen.getAllByRole("link", {
      name: /Command Generation/,
    });
    // Both desktop and mobile links should have active styling
    expect(commandGenLinks[0]).toHaveClass("neon-glow");
    expect(commandGenLinks[1]).toHaveClass("neon-glow");
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
      expect(screen.getAllByText("Command Generation")).toHaveLength(2);
      expect(screen.getAllByText("Script Generation")).toHaveLength(2);
      expect(screen.getAllByText("Command Explain")).toHaveLength(2);
      expect(screen.getAllByText("Script Explain")).toHaveLength(2);
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

      // The HealthIndicator should render an icon
      expect(screen.getByText("🟢")).toBeInTheDocument();
    });

    it("displays online status icon when server is online", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      expect(screen.getByText("🟢")).toBeInTheDocument();
      expect(screen.queryByText("🔴")).not.toBeInTheDocument();
      expect(screen.queryByText("🟡")).not.toBeInTheDocument();
    });

    it("displays offline status icon when server is offline", () => {
      mockUseHealthStatus.mockReturnValue("offline");

      render(<Navigation />);

      expect(screen.getByText("🔴")).toBeInTheDocument();
      expect(screen.queryByText("🟢")).not.toBeInTheDocument();
      expect(screen.queryByText("🟡")).not.toBeInTheDocument();
    });

    it("displays checking status icon when status is being checked", () => {
      mockUseHealthStatus.mockReturnValue("checking");

      render(<Navigation />);

      expect(screen.getByText("🟡")).toBeInTheDocument();
      expect(screen.queryByText("🟢")).not.toBeInTheDocument();
      expect(screen.queryByText("🔴")).not.toBeInTheDocument();
    });

    it("positions HealthIndicator next to the logo", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      // Check that both the logo and health indicator are present
      expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
      expect(screen.getByText("🟢")).toBeInTheDocument();

      // Check that they are both in the navigation
      const nav = screen.getByRole("navigation");
      expect(nav).toContainElement(screen.getByText("CyberQueryAI"));
      expect(nav).toContainElement(screen.getByText("🟢"));
    });

    it("includes tooltip with status information", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      const healthIcon = screen.getByText("🟢");
      expect(healthIcon).toHaveAttribute("title", "Server: ONLINE");
    });

    it("calls useHealthStatus hook when Navigation is rendered", () => {
      mockUseHealthStatus.mockReturnValue("online");

      render(<Navigation />);

      expect(mockUseHealthStatus).toHaveBeenCalledTimes(1);
    });
  });
});

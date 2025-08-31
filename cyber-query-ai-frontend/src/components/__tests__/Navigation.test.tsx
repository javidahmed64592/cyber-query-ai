import { render, screen } from "@testing-library/react";
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

// Mock the useHealthStatus hook
jest.mock("../../lib/useHealthStatus", () => ({
  useHealthStatus: jest.fn(),
}));

const mockUseHealthStatus = useHealthStatus as jest.MockedFunction<
  typeof useHealthStatus
>;

describe("Navigation", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockUseHealthStatus.mockReturnValue("online");
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
    expect(screen.getByText("Command Gen")).toBeInTheDocument();
    expect(screen.getByText("Script Gen")).toBeInTheDocument();
    expect(screen.getByText("Exploit Search")).toBeInTheDocument();
    expect(screen.getByText("Command Explain")).toBeInTheDocument();
    expect(screen.getByText("About")).toBeInTheDocument();
  });

  it('shows "(Soon)" for disabled navigation items', () => {
    render(<Navigation />);
    const soonLabels = screen.getAllByText("(Soon)");
    expect(soonLabels).toHaveLength(4);
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
    expect(
      screen.getByRole("link", { name: /Command Explain/ })
    ).toHaveAttribute("href", "/command-explanation");
    expect(screen.getByRole("link", { name: /About/ })).toHaveAttribute(
      "href",
      "/about"
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

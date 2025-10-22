import { render, screen } from "@testing-library/react";
import React from "react";

import { HealthStatus, useHealthStatus } from "../../lib/api";
import HealthIndicator from "../HealthIndicator";

// Mock the useHealthStatus hook
jest.mock("../../lib/api", () => ({
  useHealthStatus: jest.fn(),
}));

const mockUseHealthStatus = useHealthStatus as jest.MockedFunction<
  typeof useHealthStatus
>;

describe("HealthIndicator", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders online status correctly", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    const indicator = screen.getByTitle("Server: ONLINE");
    expect(indicator).toBeInTheDocument();
    expect(indicator).toHaveClass("bg-[var(--neon-green)]");
    expect(indicator).toHaveClass("shadow-[0_0_4px_var(--neon-green)]");
    expect(indicator).toHaveAttribute("title", "Server: ONLINE");
  });

  it("renders offline status correctly", () => {
    mockUseHealthStatus.mockReturnValue("offline");

    render(<HealthIndicator />);

    const indicator = screen.getByTitle("Server: OFFLINE");
    expect(indicator).toBeInTheDocument();
    expect(indicator).toHaveClass("bg-[var(--neon-red)]");
    expect(indicator).toHaveClass("shadow-[0_0_4px_var(--neon-red)]");
    expect(indicator).toHaveAttribute("title", "Server: OFFLINE");
  });

  it("renders checking status correctly", () => {
    mockUseHealthStatus.mockReturnValue("checking");

    render(<HealthIndicator />);

    const indicator = screen.getByTitle("Server: CHECKING");
    expect(indicator).toBeInTheDocument();
    expect(indicator).toHaveClass("bg-yellow-400");
    expect(indicator).toHaveClass("shadow-[0_0_4px_yellow]");
    expect(indicator).toHaveClass("animate-pulse-neon");
    expect(indicator).toHaveAttribute("title", "Server: CHECKING");
  });

  it("applies correct CSS classes for container", () => {
    mockUseHealthStatus.mockReturnValue("online");

    const { container } = render(<HealthIndicator />);

    const outerDiv = container.firstChild;
    expect(outerDiv).toHaveClass("relative", "group");
  });

  it("applies cursor-help class for interactivity indication", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    const indicator = screen.getByTitle("Server: ONLINE");
    expect(indicator).toHaveClass("cursor-help");
  });

  it("renders with correct shape and size", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    const indicator = screen.getByTitle("Server: ONLINE");
    expect(indicator).toHaveClass("w-3", "h-3", "rounded-full");
  });

  it("handles unknown status gracefully", () => {
    // This shouldn't happen in practice, but test edge case
    mockUseHealthStatus.mockReturnValue("unknown" as HealthStatus);

    render(<HealthIndicator />);

    const indicator = screen.getByTitle("Server: UNKNOWN");
    expect(indicator).toBeInTheDocument();
    expect(indicator).toHaveClass("bg-[var(--text-muted)]");
    expect(indicator).toHaveClass("shadow-[0_0_4px_var(--text-muted)]");
    expect(indicator).toHaveAttribute("title", "Server: UNKNOWN");
  });

  it("calls useHealthStatus hook", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    expect(mockUseHealthStatus).toHaveBeenCalledTimes(1);
  });

  it("renders only the indicator shape without additional text", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    expect(screen.getByTitle("Server: ONLINE")).toBeInTheDocument();
    expect(screen.queryByText("Server:")).not.toBeInTheDocument();
    expect(screen.queryByText("ONLINE")).not.toBeInTheDocument();
  });

  it("has transition animation classes", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    const indicator = screen.getByTitle("Server: ONLINE");
    expect(indicator).toHaveClass("transition-all", "duration-200");
  });
});

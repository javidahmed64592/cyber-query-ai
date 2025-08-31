import { render, screen } from "@testing-library/react";
import React from "react";

import { HealthStatus, useHealthStatus } from "../../lib/useHealthStatus";
import HealthIndicator from "../HealthIndicator";

// Mock the useHealthStatus hook
jest.mock("../../lib/useHealthStatus", () => ({
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

    const icon = screen.getByText("🟢");
    expect(icon).toBeInTheDocument();
    expect(icon).toHaveClass("text-green-400");
    expect(icon).toHaveAttribute("title", "Server: ONLINE");
  });

  it("renders offline status correctly", () => {
    mockUseHealthStatus.mockReturnValue("offline");

    render(<HealthIndicator />);

    const icon = screen.getByText("🔴");
    expect(icon).toBeInTheDocument();
    expect(icon).toHaveClass("text-red-400");
    expect(icon).toHaveAttribute("title", "Server: OFFLINE");
  });

  it("renders checking status correctly", () => {
    mockUseHealthStatus.mockReturnValue("checking");

    render(<HealthIndicator />);

    const icon = screen.getByText("🟡");
    expect(icon).toBeInTheDocument();
    expect(icon).toHaveClass("text-yellow-400");
    expect(icon).toHaveAttribute("title", "Server: CHECKING");
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

    const icon = screen.getByText("🟢");
    expect(icon).toHaveClass("cursor-help");
  });

  it("renders with correct text size", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    const icon = screen.getByText("🟢");
    expect(icon).toHaveClass("text-sm");
  });

  it("handles unknown status gracefully", () => {
    // This shouldn't happen in practice, but test edge case
    mockUseHealthStatus.mockReturnValue("unknown" as HealthStatus);

    render(<HealthIndicator />);

    const icon = screen.getByText("⚪");
    expect(icon).toBeInTheDocument();
    expect(icon).toHaveClass("text-gray-400");
    expect(icon).toHaveAttribute("title", "Server: UNKNOWN");
  });

  it("calls useHealthStatus hook", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    expect(mockUseHealthStatus).toHaveBeenCalledTimes(1);
  });

  it("renders only the icon without additional text", () => {
    mockUseHealthStatus.mockReturnValue("online");

    render(<HealthIndicator />);

    expect(screen.getByText("🟢")).toBeInTheDocument();
    expect(screen.queryByText("Server:")).not.toBeInTheDocument();
    expect(screen.queryByText("ONLINE")).not.toBeInTheDocument();
  });
});

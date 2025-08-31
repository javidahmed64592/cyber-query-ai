import { renderHook, waitFor, act } from "@testing-library/react";

import { useHealthStatus, type HealthStatus } from "../useHealthStatus";

// Mock fetch globally
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe("useHealthStatus", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it("should initialize with 'checking' status", () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
    });

    const { result } = renderHook(() => useHealthStatus());

    expect(result.current).toBe("checking");
  });

  it("should set status to 'online' when fetch succeeds", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          status: "healthy",
          timestamp: "2023-01-01T00:00:00Z",
        }),
    });

    const { result } = renderHook(() => useHealthStatus());

    await waitFor(() => {
      expect(result.current).toBe("online");
    });

    expect(mockFetch).toHaveBeenCalledWith("/api/health");
  });

  it("should set status to 'offline' when fetch fails", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Network error"));

    const { result } = renderHook(() => useHealthStatus());

    await waitFor(() => {
      expect(result.current).toBe("offline");
    });
  });

  it("should set status to 'offline' when response is not ok", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    const { result } = renderHook(() => useHealthStatus());

    await waitFor(() => {
      expect(result.current).toBe("offline");
    });
  });

  it("should poll every 30 seconds", async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          status: "healthy",
          timestamp: "2023-01-01T00:00:00Z",
        }),
    });

    renderHook(() => useHealthStatus());

    // Initial call
    expect(mockFetch).toHaveBeenCalledTimes(1);

    // Advance time by 30 seconds
    act(() => {
      jest.advanceTimersByTime(30000);
    });

    expect(mockFetch).toHaveBeenCalledTimes(2);

    // Advance time by another 30 seconds
    act(() => {
      jest.advanceTimersByTime(30000);
    });

    expect(mockFetch).toHaveBeenCalledTimes(3);
  });

  it("should clear interval on unmount", () => {
    const clearIntervalSpy = jest.spyOn(global, "clearInterval");

    mockFetch.mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          status: "healthy",
          timestamp: "2023-01-01T00:00:00Z",
        }),
    });

    const { unmount } = renderHook(() => useHealthStatus());

    unmount();

    expect(clearIntervalSpy).toHaveBeenCalled();
    clearIntervalSpy.mockRestore();
  });

  it("should handle multiple status changes correctly", async () => {
    // First call succeeds
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          status: "healthy",
          timestamp: "2023-01-01T00:00:00Z",
        }),
    });

    const { result } = renderHook(() => useHealthStatus());

    await waitFor(() => {
      expect(result.current).toBe("online");
    });

    // Second call fails
    mockFetch.mockRejectedValueOnce(new Error("Network error"));

    act(() => {
      jest.advanceTimersByTime(30000);
    });

    await waitFor(() => {
      expect(result.current).toBe("offline");
    });

    // Third call succeeds again
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          status: "healthy",
          timestamp: "2023-01-01T00:00:00Z",
        }),
    });

    act(() => {
      jest.advanceTimersByTime(30000);
    });

    await waitFor(() => {
      expect(result.current).toBe("online");
    });
  });

  it("should call fetch with correct URL", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          status: "healthy",
          timestamp: "2023-01-01T00:00:00Z",
        }),
    });

    renderHook(() => useHealthStatus());

    expect(mockFetch).toHaveBeenCalledWith("/api/health");
  });

  it("should handle fetch throwing an error", async () => {
    const consoleSpy = jest
      .spyOn(console, "error")
      .mockImplementation(() => {});
    mockFetch.mockImplementationOnce(() => {
      throw new Error("Fetch failed");
    });

    const { result } = renderHook(() => useHealthStatus());

    await waitFor(() => {
      expect(result.current).toBe("offline");
    });

    consoleSpy.mockRestore();
  });

  it("should return the correct type", () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          status: "healthy",
          timestamp: "2023-01-01T00:00:00Z",
        }),
    });

    const { result } = renderHook(() => useHealthStatus());

    // Type check - result.current should be assignable to HealthStatus
    const status: HealthStatus = result.current;
    expect(["checking", "online", "offline"]).toContain(status);
  });
});

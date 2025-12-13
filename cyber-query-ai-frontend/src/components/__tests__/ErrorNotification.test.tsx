import { render, screen, renderHook, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import ErrorNotification, {
  useErrorNotification,
} from "@/components/ErrorNotification";

jest.useFakeTimers();

describe("ErrorNotification", () => {
  afterEach(() => {
    jest.clearAllTimers();
  });

  describe("Component", () => {
    it("renders with error message", () => {
      const onClose = jest.fn();
      render(
        <ErrorNotification
          message="Test error message"
          onClose={onClose}
          duration={5000}
        />
      );

      expect(screen.getByText("Test error message")).toBeInTheDocument();
      expect(screen.getByText("Error")).toBeInTheDocument();
    });

    it("calls onClose when close button is clicked", async () => {
      const user = userEvent.setup({ delay: null });
      const onClose = jest.fn();

      render(
        <ErrorNotification
          message="Test error"
          onClose={onClose}
          duration={10000}
        />
      );

      const closeButton = screen.getByLabelText("Close notification");
      await user.click(closeButton);

      // Wait for fade out animation
      act(() => {
        jest.advanceTimersByTime(300);
      });

      expect(onClose).toHaveBeenCalled();
    });

    it("auto-closes after duration", () => {
      const onClose = jest.fn();

      render(
        <ErrorNotification
          message="Test error"
          onClose={onClose}
          duration={5000}
        />
      );

      expect(onClose).not.toHaveBeenCalled();

      // Fast-forward time by duration + animation time
      act(() => {
        jest.advanceTimersByTime(5300);
      });

      expect(onClose).toHaveBeenCalled();
    });

    it("uses default duration of 5000ms", () => {
      const onClose = jest.fn();

      render(<ErrorNotification message="Test error" onClose={onClose} />);

      act(() => {
        jest.advanceTimersByTime(4999);
      });
      expect(onClose).not.toHaveBeenCalled();

      act(() => {
        jest.advanceTimersByTime(301);
      });
      expect(onClose).toHaveBeenCalled();
    });

    it("displays error icon", () => {
      render(<ErrorNotification message="Test error" onClose={jest.fn()} />);

      expect(screen.getByText("❌")).toBeInTheDocument();
    });

    it("has proper styling classes", () => {
      const { container } = render(
        <ErrorNotification message="Test error" onClose={jest.fn()} />
      );

      const notification = container.querySelector(".fixed.top-4.right-4");
      expect(notification).toBeInTheDocument();
    });
  });

  describe("useErrorNotification Hook", () => {
    it("initializes with no error", () => {
      const { result } = renderHook(() => useErrorNotification());

      expect(result.current.error).toBeNull();
    });

    it("shows error when showError is called", () => {
      const { result } = renderHook(() => useErrorNotification());

      act(() => {
        result.current.showError("Test error message");
      });

      expect(result.current.error).toBe("Test error message");
    });

    it("clears error when clearError is called", () => {
      const { result } = renderHook(() => useErrorNotification());

      act(() => {
        result.current.showError("Test error");
      });

      expect(result.current.error).toBe("Test error");

      act(() => {
        result.current.clearError();
      });

      expect(result.current.error).toBeNull();
    });

    it("overwrites previous error when new error is shown", () => {
      const { result } = renderHook(() => useErrorNotification());

      act(() => {
        result.current.showError("First error");
      });

      expect(result.current.error).toBe("First error");

      act(() => {
        result.current.showError("Second error");
      });

      expect(result.current.error).toBe("Second error");
    });
  });
});

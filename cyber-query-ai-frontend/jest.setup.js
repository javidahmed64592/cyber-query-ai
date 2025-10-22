import "@testing-library/jest-dom";

// Mock Next.js router
jest.mock("next/navigation", () => ({
  usePathname() {
    return "/";
  },
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
    };
  },
}));

// Mock navigator.clipboard
Object.assign(navigator, {
  clipboard: {
    writeText: jest.fn(),
  },
});

// Global cleanup to prevent "Jest did not exit" warnings
// This handles lingering async operations and timers
afterEach(() => {
  jest.clearAllTimers();
});

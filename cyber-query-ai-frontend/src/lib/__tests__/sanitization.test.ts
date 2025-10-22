import DOMPurify from "dompurify";

import {
  sanitizeInput,
  sanitizeOutput,
  isCommandSafe,
} from "@/lib/sanitization";

// Mock DOMPurify for testing
jest.mock("dompurify", () => ({
  sanitize: jest.fn(),
}));

const mockDOMPurify = DOMPurify as jest.Mocked<typeof DOMPurify>;

describe("Sanitization Tests", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("sanitizeInput", () => {
    it("should return empty string for empty input", () => {
      expect(sanitizeInput("")).toBe("");
    });

    it("should escape HTML special characters", () => {
      expect(sanitizeInput('<script>alert("xss")</script>')).toBe(
        "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"
      );
    });
  });

  describe("sanitizeOutput", () => {
    it("should return empty string for empty input", () => {
      expect(sanitizeOutput("")).toBe("");
    });

    it("should call DOMPurify.sanitize with correct parameters", () => {
      const input = '<script>alert("xss")</script><p>Safe text</p>';
      const expectedOutput = "Safe text";
      mockDOMPurify.sanitize.mockReturnValue(expectedOutput);

      const result = sanitizeOutput(input);

      expect(mockDOMPurify.sanitize).toHaveBeenCalledWith(input, {
        ALLOWED_TAGS: [],
        ALLOWED_ATTR: [],
      });
      expect(result).toBe(expectedOutput);
    });
  });

  describe("isCommandSafe", () => {
    it("should return true for empty input", () => {
      expect(isCommandSafe("")).toBe(true);
    });

    it("should return true for safe commands", () => {
      expect(isCommandSafe("ls -la")).toBe(true);
      expect(isCommandSafe("ping google.com")).toBe(true);
    });

    it("should return false for dangerous commands", () => {
      expect(isCommandSafe("rm -rf /")).toBe(false);
      expect(isCommandSafe("shutdown now")).toBe(false);
      expect(isCommandSafe("cmd /c del")).toBe(false);
    });
  });
});

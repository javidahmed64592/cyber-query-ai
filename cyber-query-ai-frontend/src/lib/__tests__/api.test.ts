import { generateCommand } from "../api";
import { CommandGenerationResponse } from "../types";

// Mock the api module
jest.mock("../api", () => ({
  generateCommand: jest.fn(),
}));

const mockGenerateCommand = generateCommand as jest.MockedFunction<
  typeof generateCommand
>;

describe("API Tests", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("generateCommand", () => {
    const mockResponse: CommandGenerationResponse = {
      commands: ["nmap -sV -p 80,443 target.com", "nikto -h target.com"],
      explanation:
        "These commands will scan the target for open ports and web vulnerabilities.",
    };

    it("should successfully generate commands with valid prompt", async () => {
      mockGenerateCommand.mockResolvedValue(mockResponse);

      const result = await generateCommand(
        "Scan a website for vulnerabilities"
      );

      expect(result).toEqual(mockResponse);
      expect(mockGenerateCommand).toHaveBeenCalledWith(
        "Scan a website for vulnerabilities"
      );
    });

    it("should handle server error with string message", async () => {
      const errorMessage = "Invalid prompt format";
      mockGenerateCommand.mockRejectedValue(new Error(errorMessage));

      await expect(generateCommand("invalid prompt")).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle server error with detail field", async () => {
      const errorDetail = "Prompt too long";
      mockGenerateCommand.mockRejectedValue(new Error(errorDetail));

      await expect(generateCommand("very long prompt...")).rejects.toThrow(
        errorDetail
      );
    });

    it("should handle server error with message field", async () => {
      const errorMessage = "Internal server error";
      mockGenerateCommand.mockRejectedValue(new Error(errorMessage));

      await expect(generateCommand("test prompt")).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle server error with generic status message", async () => {
      const errorMessage = "Server error: 404 Not Found";
      mockGenerateCommand.mockRejectedValue(new Error(errorMessage));

      await expect(generateCommand("test prompt")).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running on localhost:8000";
      mockGenerateCommand.mockRejectedValue(new Error(errorMessage));

      await expect(generateCommand("test prompt")).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle request setup error", async () => {
      const errorMessage = "Request failed: Request timeout";
      mockGenerateCommand.mockRejectedValue(new Error(errorMessage));

      await expect(generateCommand("test prompt")).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle non-Axios error", async () => {
      const errorMessage = "An unexpected error occurred";
      mockGenerateCommand.mockRejectedValue(new Error(errorMessage));

      await expect(generateCommand("test prompt")).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle complex error detail object", async () => {
      const errorDetail = { code: "VALIDATION_ERROR", field: "prompt" };
      const errorMessage = JSON.stringify(errorDetail);
      mockGenerateCommand.mockRejectedValue(new Error(errorMessage));

      await expect(generateCommand("test prompt")).rejects.toThrow(
        errorMessage
      );
    });
  });
});

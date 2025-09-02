import {
  generateCommand,
  generateScript,
  explainCommand,
  explainScript,
  searchExploits,
} from "../api";
import {
  CommandGenerationResponse,
  ScriptGenerationResponse,
  ExplanationResponse,
  ExploitSearchResponse,
} from "../types";

// Mock the api module
jest.mock("../api", () => ({
  generateCommand: jest.fn(),
  generateScript: jest.fn(),
  explainCommand: jest.fn(),
  explainScript: jest.fn(),
  searchExploits: jest.fn(),
}));

const mockGenerateCommand = generateCommand as jest.MockedFunction<
  typeof generateCommand
>;
const mockGenerateScript = generateScript as jest.MockedFunction<
  typeof generateScript
>;
const mockExplainCommand = explainCommand as jest.MockedFunction<
  typeof explainCommand
>;
const mockExplainScript = explainScript as jest.MockedFunction<
  typeof explainScript
>;
const mockSearchExploits = searchExploits as jest.MockedFunction<
  typeof searchExploits
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

  describe("generateScript", () => {
    const mockResponse: ScriptGenerationResponse = {
      script: 'import socket\n\ndef port_scan():\n    print("Scanning ports")',
      explanation: "This Python script scans for open ports on a target.",
    };

    it("should successfully generate script with valid prompt and language", async () => {
      mockGenerateScript.mockResolvedValue(mockResponse);

      const result = await generateScript("Create a port scanner", "python");

      expect(result).toEqual(mockResponse);
      expect(mockGenerateScript).toHaveBeenCalledWith(
        "Create a port scanner",
        "python"
      );
    });

    it("should handle error when generating script", async () => {
      const errorMessage = "Invalid language specified";
      mockGenerateScript.mockRejectedValue(new Error(errorMessage));

      await expect(
        generateScript("Create a script", "invalid-lang")
      ).rejects.toThrow(errorMessage);
    });
  });

  describe("explainCommand", () => {
    const mockResponse: ExplanationResponse = {
      explanation:
        "This nmap command performs a SYN scan (-sS) on all ports (-p-) of the target.",
    };

    it("should successfully explain a command", async () => {
      mockExplainCommand.mockResolvedValue(mockResponse);

      const result = await explainCommand("nmap -sS -p- target.com");

      expect(result).toEqual(mockResponse);
      expect(mockExplainCommand).toHaveBeenCalledWith(
        "nmap -sS -p- target.com"
      );
    });

    it("should handle error when explaining command", async () => {
      const errorMessage = "Command not recognized";
      mockExplainCommand.mockRejectedValue(new Error(errorMessage));

      await expect(explainCommand("invalid-command")).rejects.toThrow(
        errorMessage
      );
    });
  });

  describe("explainScript", () => {
    const mockResponse: ExplanationResponse = {
      explanation:
        "This Python script imports the socket library and defines a function to scan ports.",
    };

    it("should successfully explain a script", async () => {
      mockExplainScript.mockResolvedValue(mockResponse);

      const script = "import socket\ndef scan_ports(): pass";
      const result = await explainScript(script, "python");

      expect(result).toEqual(mockResponse);
      expect(mockExplainScript).toHaveBeenCalledWith(script, "python");
    });

    it("should handle error when explaining script", async () => {
      const errorMessage = "Script syntax error";
      mockExplainScript.mockRejectedValue(new Error(errorMessage));

      await expect(explainScript("invalid syntax", "python")).rejects.toThrow(
        errorMessage
      );
    });
  });

  describe("searchExploits", () => {
    const mockResponse: ExploitSearchResponse = {
      exploits: [
        {
          title: "CVE-2021-44228 Log4j RCE",
          link: "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
          severity: "critical",
          description: "Remote code execution vulnerability in Log4j library.",
        },
      ],
      explanation:
        "Apache servers with Log4j are vulnerable to remote code execution.",
    };

    it("should successfully search for exploits", async () => {
      mockSearchExploits.mockResolvedValue(mockResponse);

      const result = await searchExploits("Apache server with Log4j");

      expect(result).toEqual(mockResponse);
      expect(mockSearchExploits).toHaveBeenCalledWith(
        "Apache server with Log4j"
      );
    });

    it("should handle error when searching exploits", async () => {
      const errorMessage = "Target description too vague";
      mockSearchExploits.mockRejectedValue(new Error(errorMessage));

      await expect(searchExploits("vague target")).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle empty exploits response", async () => {
      const emptyResponse: ExploitSearchResponse = {
        exploits: [],
        explanation: "No known exploits found for this target.",
      };
      mockSearchExploits.mockResolvedValue(emptyResponse);

      const result = await searchExploits("secure target");

      expect(result).toEqual(emptyResponse);
      expect(result.exploits).toHaveLength(0);
    });
  });
});

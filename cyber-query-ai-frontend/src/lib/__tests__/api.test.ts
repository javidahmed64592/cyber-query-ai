import { renderHook } from "@testing-library/react";

import {
  generateCommand,
  generateScript,
  explainCommand,
  explainScript,
  searchExploits,
  getConfig,
  getHealth,
  sendChatMessage,
  useHealthStatus,
  type HealthStatus,
} from "@/lib/api";
import type {
  CommandGenerationResponse,
  ScriptGenerationResponse,
  ExplanationResponse,
  ExploitSearchResponse,
  ConfigResponse,
  HealthResponse,
  ChatResponse,
} from "@/lib/types";

jest.mock("../api", () => {
  const actual = jest.requireActual("../api");
  return {
    ...actual,
    getHealth: jest.fn(),
    getConfig: jest.fn(),
    generateCommand: jest.fn(),
    generateScript: jest.fn(),
    explainCommand: jest.fn(),
    explainScript: jest.fn(),
    searchExploits: jest.fn(),
    sendChatMessage: jest.fn(),
  };
});

// Mock fetch for config endpoint
global.fetch = jest.fn();

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
const mockGetConfig = getConfig as jest.MockedFunction<typeof getConfig>;
const mockGetHealth = getHealth as jest.MockedFunction<typeof getHealth>;
const mockSendChatMessage = sendChatMessage as jest.MockedFunction<
  typeof sendChatMessage
>;

describe("API Tests", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("health", () => {
    it("should fetch health status successfully", async () => {
      const mockHealth: HealthResponse = {
        status: "healthy",
        timestamp: "2023-01-01T00:00:00Z",
      };

      mockGetHealth.mockResolvedValue(mockHealth);

      const health = await getHealth();

      expect(mockGetHealth).toHaveBeenCalled();
      expect(health).toEqual(mockHealth);
      expect(health.status).toBe("healthy");
    });

    it("should handle health check error", async () => {
      const errorMessage = "Service unavailable";
      mockGetHealth.mockRejectedValue(new Error(errorMessage));

      await expect(getHealth()).rejects.toThrow(errorMessage);
    });

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running.";
      mockGetHealth.mockRejectedValue(new Error(errorMessage));

      await expect(getHealth()).rejects.toThrow(errorMessage);
    });
  });

  describe("config", () => {
    it("should fetch config successfully", async () => {
      const mockConfig: ConfigResponse = {
        model: "mistral",
        embedding_model: "bge-m3",
        host: "localhost",
        port: 8000,
      };

      mockGetConfig.mockResolvedValue(mockConfig);

      const config = await getConfig();

      expect(mockGetConfig).toHaveBeenCalledTimes(1);
      expect(config).toEqual(mockConfig);
      expect(config.model).toBe("mistral");
      expect(config.embedding_model).toBe("bge-m3");
      expect(config.host).toBe("localhost");
      expect(config.port).toBe(8000);
    });

    it("should handle config fetch error", async () => {
      const errorMessage = "Failed to fetch config";
      mockGetConfig.mockRejectedValue(new Error(errorMessage));

      await expect(getConfig()).rejects.toThrow(errorMessage);
    });

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running.";
      mockGetConfig.mockRejectedValue(new Error(errorMessage));

      await expect(getConfig()).rejects.toThrow(errorMessage);
    });
  });

  describe("sendChatMessage", () => {
    const mockResponse: ChatResponse = {
      message: "Here's how to use nmap for network scanning...",
    };

    it("should successfully send chat message with empty history", async () => {
      mockSendChatMessage.mockResolvedValue(mockResponse);

      const result = await sendChatMessage(
        "How do I use nmap for network scanning?",
        []
      );

      expect(result).toEqual(mockResponse);
      expect(mockSendChatMessage).toHaveBeenCalledWith(
        "How do I use nmap for network scanning?",
        []
      );
    });

    it("should successfully send chat message with conversation history", async () => {
      const history = [
        { role: "user" as const, content: "What is penetration testing?" },
        {
          role: "assistant" as const,
          content:
            "Penetration testing is a simulated cyber attack against your system...",
        },
      ];

      mockSendChatMessage.mockResolvedValue(mockResponse);

      const result = await sendChatMessage("Tell me more about tools", history);

      expect(result).toEqual(mockResponse);
      expect(mockSendChatMessage).toHaveBeenCalledWith(
        "Tell me more about tools",
        history
      );
    });

    it("should successfully send chat message with long conversation history", async () => {
      const longHistory = Array(10)
        .fill(null)
        .map((_, i) => ({
          role: (i % 2 === 0 ? "user" : "assistant") as "user" | "assistant",
          content: `Message ${i + 1}`,
        }));

      mockSendChatMessage.mockResolvedValue(mockResponse);

      const result = await sendChatMessage("Continue discussion", longHistory);

      expect(result).toEqual(mockResponse);
      expect(mockSendChatMessage).toHaveBeenCalledWith(
        "Continue discussion",
        longHistory
      );
    });

    it("should handle empty message", async () => {
      const emptyMessageResponse: ChatResponse = {
        message: "I need more information to help you.",
      };
      mockSendChatMessage.mockResolvedValue(emptyMessageResponse);

      const result = await sendChatMessage("", []);

      expect(result).toEqual(emptyMessageResponse);
      expect(mockSendChatMessage).toHaveBeenCalledWith("", []);
    });

    it("should handle multiline message", async () => {
      const multilineMessage = `How do I use nmap?
I want to scan for open ports
And check service versions`;

      mockSendChatMessage.mockResolvedValue(mockResponse);

      const result = await sendChatMessage(multilineMessage, []);

      expect(result).toEqual(mockResponse);
      expect(mockSendChatMessage).toHaveBeenCalledWith(multilineMessage, []);
    });

    it("should handle server error with string message", async () => {
      const errorMessage = "Invalid request format";
      mockSendChatMessage.mockRejectedValue(new Error(errorMessage));

      await expect(sendChatMessage("test message", [])).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle server error with detail field", async () => {
      const errorDetail = "Message too long";
      mockSendChatMessage.mockRejectedValue(new Error(errorDetail));

      await expect(sendChatMessage("very long message...", [])).rejects.toThrow(
        errorDetail
      );
    });

    it("should handle server error with generic status message", async () => {
      const errorMessage = "Server error: 500 Internal Server Error";
      mockSendChatMessage.mockRejectedValue(new Error(errorMessage));

      await expect(sendChatMessage("test message", [])).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running.";
      mockSendChatMessage.mockRejectedValue(new Error(errorMessage));

      await expect(sendChatMessage("test message", [])).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle request setup error", async () => {
      const errorMessage = "Request failed: Request timeout";
      mockSendChatMessage.mockRejectedValue(new Error(errorMessage));

      await expect(sendChatMessage("test message", [])).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle non-Axios error", async () => {
      const errorMessage = "An unexpected error occurred";
      mockSendChatMessage.mockRejectedValue(new Error(errorMessage));

      await expect(sendChatMessage("test message", [])).rejects.toThrow(
        errorMessage
      );
    });

    it("should handle special characters in message", async () => {
      const specialMessage = "Test <script>alert('xss')</script> message";
      mockSendChatMessage.mockResolvedValue(mockResponse);

      const result = await sendChatMessage(specialMessage, []);

      expect(result).toEqual(mockResponse);
      expect(mockSendChatMessage).toHaveBeenCalledWith(specialMessage, []);
    });

    it("should handle special characters in history", async () => {
      const historyWithSpecialChars = [
        {
          role: "user" as const,
          content: "What about <>&\"' characters?",
        },
        {
          role: "assistant" as const,
          content: "They are handled properly with sanitization.",
        },
      ];

      mockSendChatMessage.mockResolvedValue(mockResponse);

      const result = await sendChatMessage("Continue", historyWithSpecialChars);

      expect(result).toEqual(mockResponse);
      expect(mockSendChatMessage).toHaveBeenCalledWith(
        "Continue",
        historyWithSpecialChars
      );
    });
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
        "No response from server. Please check if the backend is running.";
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

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running.";
      mockGenerateScript.mockRejectedValue(new Error(errorMessage));

      await expect(generateScript("Create a script", "python")).rejects.toThrow(
        errorMessage
      );
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

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running.";
      mockExplainCommand.mockRejectedValue(new Error(errorMessage));

      await expect(explainCommand("nmap -sS target.com")).rejects.toThrow(
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

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running.";
      mockExplainScript.mockRejectedValue(new Error(errorMessage));

      await expect(explainScript("import socket", "python")).rejects.toThrow(
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

    it("should handle network error (no response)", async () => {
      const errorMessage =
        "No response from server. Please check if the backend is running.";
      mockSearchExploits.mockRejectedValue(new Error(errorMessage));

      await expect(searchExploits("Apache server")).rejects.toThrow(
        errorMessage
      );
    });
  });

  describe("useHealthStatus", () => {
    it("should initialize with 'checking' status", () => {
      const { result, unmount } = renderHook(() => useHealthStatus());
      expect(result.current).toBe("checking");
      unmount();
    });

    it("should return correct HealthStatus type", () => {
      const { result, unmount } = renderHook(() => useHealthStatus());
      const status: HealthStatus = result.current;
      expect(["checking", "online", "offline"]).toContain(status);
      unmount();
    });
  });
});

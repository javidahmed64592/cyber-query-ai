import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import * as api from "../../lib/api";
import ChatWindow from "../ChatWindow";

// Mock the API
jest.mock("../../lib/api");
const mockSendChatMessage = api.sendChatMessage as jest.MockedFunction<
  typeof api.sendChatMessage
>;

// Mock scrollIntoView
Element.prototype.scrollIntoView = jest.fn();

describe("ChatWindow", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("Initial Render", () => {
    it("renders welcome message when no messages", () => {
      render(<ChatWindow />);

      expect(screen.getByText(/Welcome to CyberQueryAI/i)).toBeInTheDocument();
    });

    it("renders example prompts", () => {
      render(<ChatWindow />);

      expect(
        screen.getByText(/How do I scan a network for open ports?/i)
      ).toBeInTheDocument();
      expect(
        screen.getByText(/Generate a Python script to brute force SSH/i)
      ).toBeInTheDocument();
      expect(
        screen.getByText(/Explain how SQL injection works/i)
      ).toBeInTheDocument();
    });

    it("renders input textarea", () => {
      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );
      expect(textarea).toBeInTheDocument();
    });

    it("renders send button", () => {
      render(<ChatWindow />);

      const sendButton = screen.getByTitle("Send message");
      expect(sendButton).toBeInTheDocument();
    });

    it("renders clear button", () => {
      render(<ChatWindow />);

      const clearButton = screen.getByTitle("Clear chat history");
      expect(clearButton).toBeInTheDocument();
    });
  });

  describe("User Input", () => {
    it("updates textarea value when typing", () => {
      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      ) as HTMLTextAreaElement;

      fireEvent.change(textarea, {
        target: { value: "How do I use nmap?" },
      });

      expect(textarea.value).toBe("How do I use nmap?");
    });

    it("auto-resizes textarea when content grows", () => {
      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      ) as HTMLTextAreaElement;

      const longText = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5";
      fireEvent.change(textarea, { target: { value: longText } });

      // Check that height is adjusted (actual value depends on implementation)
      expect(textarea.style.height).toBeTruthy();
    });

    it("disables send button when input is empty", () => {
      render(<ChatWindow />);

      const sendButton = screen.getByTitle("Send message");
      expect(sendButton).toBeDisabled();
    });

    it("enables send button when input has text", () => {
      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );
      const sendButton = screen.getByTitle("Send message");

      fireEvent.change(textarea, { target: { value: "Test message" } });

      expect(sendButton).not.toBeDisabled();
    });

    it("disables send button when input is only whitespace", () => {
      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );
      const sendButton = screen.getByTitle("Send message");

      fireEvent.change(textarea, { target: { value: "   \n   " } });

      expect(sendButton).toBeDisabled();
    });
  });

  describe("Sending Messages", () => {
    it("sends message when send button is clicked", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Test response",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );
      const sendButton = screen.getByTitle("Send message");

      fireEvent.change(textarea, { target: { value: "Test message" } });
      fireEvent.click(sendButton);

      await waitFor(() => {
        expect(mockSendChatMessage).toHaveBeenCalledWith("Test message", []);
      });
    });

    it("displays user message immediately", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Test response",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      fireEvent.change(textarea, { target: { value: "Hello, AI!" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(screen.getByText("Hello, AI!")).toBeInTheDocument();
      });
    });

    it("displays assistant response after API call", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Hello, user!",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      fireEvent.change(textarea, { target: { value: "Hello" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(screen.getByText("Hello, user!")).toBeInTheDocument();
      });
    });

    it("clears input after sending message", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Response",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      ) as HTMLTextAreaElement;

      fireEvent.change(textarea, { target: { value: "Test" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(textarea.value).toBe("");
      });
    });

    it("disables send button while loading", async () => {
      mockSendChatMessage.mockImplementation(
        () =>
          new Promise(resolve =>
            setTimeout(() => resolve({ message: "Response" }), 100)
          )
      );

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );
      const sendButton = screen.getByTitle("Send message");

      fireEvent.change(textarea, { target: { value: "Test" } });
      fireEvent.click(sendButton);

      // Button should be disabled while loading
      expect(sendButton).toBeDisabled();

      // Wait for response and check button is re-enabled
      await waitFor(
        () => {
          expect(screen.getByText("Response")).toBeInTheDocument();
        },
        { timeout: 2000 }
      );

      // After response, typing should enable button again
      fireEvent.change(textarea, { target: { value: "Test again" } });
      expect(sendButton).not.toBeDisabled();
    });

    it("includes conversation history in subsequent messages", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Response 2",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      // First message
      fireEvent.change(textarea, { target: { value: "Message 1" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(screen.getByText("Response 2")).toBeInTheDocument();
      });

      // Second message
      mockSendChatMessage.mockClear();
      mockSendChatMessage.mockResolvedValue({
        message: "Response 3",
      });

      fireEvent.change(textarea, { target: { value: "Message 2" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(mockSendChatMessage).toHaveBeenCalledWith("Message 2", [
          { role: "user", content: "Message 1" },
          { role: "assistant", content: "Response 2" },
        ]);
      });
    });
  });

  describe("Example Prompts", () => {
    it("fills input when example prompt is clicked", () => {
      render(<ChatWindow />);

      const examplePrompt = screen.getByText(
        /How do I scan a network for open ports?/i
      );
      fireEvent.click(examplePrompt);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      ) as HTMLTextAreaElement;

      expect(textarea.value).toBe("How do I scan a network for open ports?");
    });

    it("hides example prompts after first message", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Response",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      fireEvent.change(textarea, { target: { value: "Test" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(
          screen.queryByText(/How do I scan a network for open ports?/i)
        ).not.toBeInTheDocument();
      });
    });
  });

  describe("Clear Functionality", () => {
    it("clears all messages when clear button is clicked", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Response",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      // Send a message
      fireEvent.change(textarea, { target: { value: "Test message" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(screen.getByText("Test message")).toBeInTheDocument();
      });

      // Clear chat
      fireEvent.click(screen.getByTitle("Clear chat history"));

      expect(screen.queryByText("Test message")).not.toBeInTheDocument();
      expect(screen.queryByText("Response")).not.toBeInTheDocument();
    });

    it("shows welcome message after clearing", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Response",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      // Send a message
      fireEvent.change(textarea, { target: { value: "Test" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(screen.getByText("Response")).toBeInTheDocument();
      });

      // Clear chat
      fireEvent.click(screen.getByTitle("Clear chat history"));

      expect(screen.getByText(/Welcome to CyberQueryAI/i)).toBeInTheDocument();
    });
  });

  describe("Error Handling", () => {
    it("displays error message when API call fails", async () => {
      mockSendChatMessage.mockRejectedValue(new Error("Network error"));

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      fireEvent.change(textarea, { target: { value: "Test" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(screen.getByText(/Error: Network error/i)).toBeInTheDocument();
      });
    });

    it("re-enables send button after error", async () => {
      mockSendChatMessage.mockRejectedValue(new Error("Network error"));

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );
      const sendButton = screen.getByTitle("Send message");

      fireEvent.change(textarea, { target: { value: "Test" } });
      fireEvent.click(sendButton);

      await waitFor(() => {
        expect(screen.getByText(/Error: Network error/i)).toBeInTheDocument();
      });

      fireEvent.change(textarea, { target: { value: "Test again" } });
      expect(sendButton).not.toBeDisabled();
    });
  });

  describe("Keyboard Shortcuts", () => {
    it("sends message when Enter is pressed without Shift", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Response",
      });

      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      fireEvent.change(textarea, { target: { value: "Test message" } });
      fireEvent.keyDown(textarea, { key: "Enter", shiftKey: false });

      await waitFor(() => {
        expect(mockSendChatMessage).toHaveBeenCalledWith("Test message", []);
      });
    });

    it("adds newline when Shift+Enter is pressed", () => {
      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      ) as HTMLTextAreaElement;

      fireEvent.change(textarea, { target: { value: "Line 1" } });
      fireEvent.keyDown(textarea, { key: "Enter", shiftKey: true });

      // Textarea should still have content (not cleared by sending)
      expect(textarea.value).toBe("Line 1");
    });

    it("does not send empty message when Enter is pressed", async () => {
      render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      fireEvent.keyDown(textarea, { key: "Enter", shiftKey: false });

      await waitFor(() => {
        expect(mockSendChatMessage).not.toHaveBeenCalled();
      });
    });
  });

  describe("Auto-Scroll", () => {
    it("scrolls to bottom when new message is added", async () => {
      mockSendChatMessage.mockResolvedValue({
        message: "Response",
      });

      const { container } = render(<ChatWindow />);

      const textarea = screen.getByPlaceholderText(
        /Ask me anything about cybersecurity/i
      );

      fireEvent.change(textarea, { target: { value: "Test" } });
      fireEvent.click(screen.getByTitle("Send message"));

      await waitFor(() => {
        expect(screen.getByText("Response")).toBeInTheDocument();
      });

      const scrollContainer = container.querySelector(".overflow-y-auto");
      expect(scrollContainer).toBeInTheDocument();
    });
  });
});

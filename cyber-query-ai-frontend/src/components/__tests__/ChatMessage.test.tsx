import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import ChatMessage from "../ChatMessage";

// Mock clipboard API
Object.assign(navigator, {
  clipboard: {
    writeText: jest.fn(),
  },
});

describe("ChatMessage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("Basic Rendering", () => {
    it("renders user message with correct styling", () => {
      render(<ChatMessage role="user" content="Hello, world!" />);

      expect(screen.getByText("You")).toBeInTheDocument();
      expect(screen.getByText("Hello, world!")).toBeInTheDocument();
    });

    it("renders assistant message with correct styling", () => {
      render(<ChatMessage role="assistant" content="Hello, user!" />);

      expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
      expect(screen.getByText("Hello, user!")).toBeInTheDocument();
    });

    it("applies correct CSS classes for user messages", () => {
      const { container } = render(
        <ChatMessage role="user" content="Test message" />
      );

      const messageWrapper = container.querySelector(".justify-end");
      expect(messageWrapper).toBeInTheDocument();
    });

    it("applies correct CSS classes for assistant messages", () => {
      const { container } = render(
        <ChatMessage role="assistant" content="Test message" />
      );

      const messageWrapper = container.querySelector(".justify-start");
      expect(messageWrapper).toBeInTheDocument();
    });
  });

  describe("Copy Functionality", () => {
    it("shows copy button for assistant messages", () => {
      render(<ChatMessage role="assistant" content="Test message" />);

      const copyButton = screen.getByTitle("Copy message");
      expect(copyButton).toBeInTheDocument();
    });

    it("does not show copy button for user messages", () => {
      render(<ChatMessage role="user" content="Test message" />);

      const copyButton = screen.queryByTitle("Copy message");
      expect(copyButton).not.toBeInTheDocument();
    });

    it("copies message content when copy button is clicked", async () => {
      const content = "Test message to copy";
      render(<ChatMessage role="assistant" content={content} />);

      const copyButton = screen.getByTitle("Copy message");
      fireEvent.click(copyButton);

      await waitFor(() => {
        expect(navigator.clipboard.writeText).toHaveBeenCalledWith(content);
      });
    });

    it("shows checkmark icon after copying", async () => {
      render(<ChatMessage role="assistant" content="Test" />);

      const copyButton = screen.getByTitle("Copy message");
      fireEvent.click(copyButton);

      await waitFor(() => {
        const checkmark = copyButton.querySelector('path[d*="M5 13l4 4L19 7"]');
        expect(checkmark).toBeInTheDocument();
      });
    });

    it("reverts to copy icon after timeout", async () => {
      jest.useFakeTimers();
      render(<ChatMessage role="assistant" content="Test" />);

      const copyButton = screen.getByTitle("Copy message");
      fireEvent.click(copyButton);

      // Fast-forward time
      jest.advanceTimersByTime(2000);

      await waitFor(() => {
        const copyIcon = copyButton.querySelector('path[d*="M8 16H6"]');
        expect(copyIcon).toBeInTheDocument();
      });

      jest.useRealTimers();
    });
  });

  describe("Code Block Rendering", () => {
    it("renders code block with language label", () => {
      const content = "```python\nprint('Hello, world!')\n```";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("python")).toBeInTheDocument();
      expect(screen.getByText("print('Hello, world!')")).toBeInTheDocument();
    });

    it("defaults to bash language when not specified", () => {
      const content = "```\nls -la\n```";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("bash")).toBeInTheDocument();
      expect(screen.getByText("ls -la")).toBeInTheDocument();
    });

    it("renders multiple code blocks in same message", () => {
      const content =
        "First command:\n```bash\nls\n```\nSecond command:\n```python\nprint('hi')\n```";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("bash")).toBeInTheDocument();
      expect(screen.getByText("python")).toBeInTheDocument();
      expect(screen.getByText("ls")).toBeInTheDocument();
      expect(screen.getByText("print('hi')")).toBeInTheDocument();
    });

    it("renders code block with copy button", () => {
      const content = "```bash\necho 'test'\n```";
      render(<ChatMessage role="assistant" content={content} />);

      const copyButton = screen.getByTitle("Copy code");
      expect(copyButton).toBeInTheDocument();
    });

    it("copies code block content when button is clicked", async () => {
      const code = "echo 'test'";
      const content = `\`\`\`bash\n${code}\n\`\`\``;
      render(<ChatMessage role="assistant" content={content} />);

      const copyButton = screen.getByTitle("Copy code");
      fireEvent.click(copyButton);

      await waitFor(() => {
        expect(navigator.clipboard.writeText).toHaveBeenCalledWith(code);
      });
    });

    it("shows checkmark in code block copy button after copying", async () => {
      const content = "```bash\necho 'test'\n```";
      render(<ChatMessage role="assistant" content={content} />);

      const copyButton = screen.getByTitle("Copy code");
      fireEvent.click(copyButton);

      await waitFor(() => {
        const checkmark = copyButton.querySelector('path[d*="M5 13l4 4L19 7"]');
        expect(checkmark).toBeInTheDocument();
      });
    });

    it("handles empty code blocks gracefully", () => {
      const content = "```bash\n\n```";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("bash")).toBeInTheDocument();
    });
  });

  describe("Inline Code Rendering", () => {
    it("renders inline code with correct styling", () => {
      const content = "Use the `nmap` command to scan.";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("nmap")).toBeInTheDocument();
      expect(screen.getByText("Use the")).toBeInTheDocument();
      expect(screen.getByText("command to scan.")).toBeInTheDocument();
    });

    it("renders multiple inline code segments", () => {
      const content = "Use `nmap` or `masscan` for scanning.";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("nmap")).toBeInTheDocument();
      expect(screen.getByText("masscan")).toBeInTheDocument();
    });

    it("handles mixed inline code and code blocks", () => {
      const content =
        "Use the `nmap` command:\n```bash\nnmap -sV 192.168.1.0/24\n```";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("nmap")).toBeInTheDocument(); // inline
      expect(screen.getByText("bash")).toBeInTheDocument(); // code block
      expect(screen.getByText("nmap -sV 192.168.1.0/24")).toBeInTheDocument();
    });
  });

  describe("Text Formatting", () => {
    it("preserves line breaks in text", () => {
      const content = "Line 1\nLine 2\nLine 3";
      const { container } = render(
        <ChatMessage role="assistant" content={content} />
      );

      const breaks = container.querySelectorAll("br");
      expect(breaks.length).toBeGreaterThan(0);
    });

    it("handles empty content", () => {
      render(<ChatMessage role="assistant" content="" />);

      expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
    });

    it("handles content with only whitespace", () => {
      render(<ChatMessage role="assistant" content="   \n   " />);

      expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
    });

    it("trims whitespace from code blocks", () => {
      const content = "```bash\n  \n  ls -la  \n  \n```";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("ls -la")).toBeInTheDocument();
    });
  });

  describe("Edge Cases", () => {
    it("handles special characters in content", () => {
      const content = "Special chars: <>&\"'";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText(/Special chars:/)).toBeInTheDocument();
    });

    it("handles very long content", () => {
      const content = "A".repeat(10000);
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText("CyberQueryAI")).toBeInTheDocument();
    });

    it("handles malformed code block syntax", () => {
      const content = "```incomplete code block";
      render(<ChatMessage role="assistant" content={content} />);

      // Should render as text since it's not properly closed
      expect(screen.getByText(/incomplete code block/)).toBeInTheDocument();
    });

    it("handles nested backticks in inline code", () => {
      const content = "Use `` `backticks` `` for code.";
      render(<ChatMessage role="assistant" content={content} />);

      expect(screen.getByText(/for code/)).toBeInTheDocument();
    });
  });

  describe("Accessibility", () => {
    it("has accessible button labels", () => {
      render(<ChatMessage role="assistant" content="Test" />);

      const copyButton = screen.getByTitle("Copy message");
      expect(copyButton).toHaveAttribute("title");
    });

    it("has accessible code block copy button", () => {
      const content = "```bash\nls\n```";
      render(<ChatMessage role="assistant" content={content} />);

      const copyButton = screen.getByTitle("Copy code");
      expect(copyButton).toHaveAttribute("title");
    });

    it("uses semantic HTML for code blocks", () => {
      const content = "```bash\nls\n```";
      const { container } = render(
        <ChatMessage role="assistant" content={content} />
      );

      const pre = container.querySelector("pre");
      const code = container.querySelector("code");

      expect(pre).toBeInTheDocument();
      expect(code).toBeInTheDocument();
    });
  });
});

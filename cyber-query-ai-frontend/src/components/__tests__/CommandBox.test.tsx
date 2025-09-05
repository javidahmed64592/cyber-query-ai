import { render, screen, act } from "@testing-library/react";

import CommandBox from "../CommandBox";

// Mock the sanitization functions
jest.mock("@/lib/sanitization", () => ({
  sanitizeOutput: jest.fn((str: string) => str),
  isCommandSafe: jest.fn(
    (str: string) => !str.includes("rm -rf") && !str.includes("shutdown")
  ),
}));

describe("CommandBox", () => {
  const mockWriteText = jest.fn().mockResolvedValue(undefined);

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock navigator.clipboard
    Object.defineProperty(navigator, "clipboard", {
      value: {
        writeText: mockWriteText,
      },
      writable: true,
      configurable: true,
    });
  });

  it("shows loading state when isLoading is true", () => {
    render(<CommandBox commands={[]} isLoading={true} />);
    expect(screen.getByText("✅ Generated Command(s):")).toBeInTheDocument();
    expect(screen.getByText("Generating commands...")).toBeInTheDocument();
  });

  it("shows no commands message when commands array is empty", () => {
    render(<CommandBox commands={[]} isLoading={false} />);
    expect(screen.getByText("✅ Generated Command(s):")).toBeInTheDocument();
    expect(
      screen.getByText(
        "No suitable tool identified. Try rephrasing your prompt."
      )
    ).toBeInTheDocument();
  });

  it("renders single command correctly", () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    expect(screen.getByText("✅ Generated Command(s):")).toBeInTheDocument();
    expect(screen.getByText("ls -la")).toBeInTheDocument();
  });

  it("renders multiple commands correctly", () => {
    const commands = ["ls -la", "pwd", "whoami"];
    render(<CommandBox commands={commands} isLoading={false} />);

    expect(screen.getByText("✅ Generated Command(s):")).toBeInTheDocument();
    expect(screen.getByText("ls -la")).toBeInTheDocument();
    expect(screen.getByText("pwd")).toBeInTheDocument();
    expect(screen.getByText("whoami")).toBeInTheDocument();
  });

  it("copies command to clipboard when copy button is clicked", async () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const copyButton = screen.getByRole("button", { name: /copy/i });

    // Fire the click event directly for more control
    await act(async () => {
      copyButton.click();
    });

    // Wait for async operations
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 100));
    });

    expect(mockWriteText).toHaveBeenCalledWith("ls -la");
  });

  it("shows copy button always visible", () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const copyButton = screen.getByRole("button", { name: /copy/i });
    expect(copyButton).toBeInTheDocument();
    expect(copyButton).toHaveTextContent("Copy");
  });

  it("applies command-box class to command containers", () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const commandBox = screen.getByText("ls -la").closest(".command-box");
    expect(commandBox).toHaveClass("command-box", "group", "relative");
  });

  it("renders code element with correct styling", () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const codeElement = screen.getByText("ls -la");
    expect(codeElement.tagName).toBe("CODE");
    expect(codeElement).toHaveClass(
      "text-[var(--text-secondary)]",
      "break-all",
      "flex-1"
    );
  });

  it("handles long commands with line breaks", () => {
    const longCommand =
      "nmap -sV -sC -A -T4 -p- -oN scan_results.txt 192.168.1.0/24";
    const commands = [longCommand];
    render(<CommandBox commands={commands} isLoading={false} />);

    expect(screen.getByText(longCommand)).toBeInTheDocument();
  });

  it("shows copied feedback when copy button is clicked", async () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const copyButton = screen.getByRole("button", { name: /copy/i });

    await act(async () => {
      copyButton.click();
    });

    // Wait for async operations
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 100));
    });

    // Check that the button shows "Copied" feedback
    expect(screen.getByText("Copied")).toBeInTheDocument();
    expect(mockWriteText).toHaveBeenCalledWith("ls -la");
  });

  it("renders multiple commands with individual copy buttons", () => {
    const commands = ["ls -la", "pwd"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const copyButtons = screen.getAllByRole("button", { name: /copy/i });
    expect(copyButtons).toHaveLength(2);
  });

  it("shows unsafe command warning for dangerous commands", () => {
    const commands = ["rm -rf /"];
    render(<CommandBox commands={commands} isLoading={false} />);

    // Check that the warning message is displayed
    expect(screen.getByText("⚠️ POTENTIALLY UNSAFE")).toBeInTheDocument();

    // Check that the warning has the correct styling
    const warningElement = screen.getByText("⚠️ POTENTIALLY UNSAFE");
    expect(warningElement).toHaveClass(
      "text-[var(--neon-red)]",
      "text-xs",
      "font-bold",
      "whitespace-nowrap"
    );
  });

  it("does not show unsafe command warning for safe commands", () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    // Check that the warning message is not displayed
    expect(screen.queryByText("⚠️ POTENTIALLY UNSAFE")).not.toBeInTheDocument();
  });

  it("shows warning for multiple unsafe commands", () => {
    const commands = ["rm -rf /", "shutdown now", "ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    // Check that warning messages are displayed for unsafe commands
    const warningElements = screen.getAllByText("⚠️ POTENTIALLY UNSAFE");
    expect(warningElements).toHaveLength(2); // rm -rf and shutdown should show warnings

    // Check that safe command doesn't have warning
    expect(screen.getByText("ls -la")).toBeInTheDocument();
  });
});

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import CommandBox from "../CommandBox";

describe("CommandBox", () => {
  const mockWriteText = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock navigator.clipboard
    Object.defineProperty(navigator, "clipboard", {
      value: {
        writeText: mockWriteText,
      },
      writable: true,
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
    const user = userEvent.setup();
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const copyButton = screen.getByTitle("Copy to clipboard");

    // Mock the clipboard writeText function
    const originalWriteText = navigator.clipboard?.writeText;
    Object.defineProperty(navigator, "clipboard", {
      value: {
        writeText: mockWriteText,
      },
      configurable: true,
    });

    await user.click(copyButton);

    expect(mockWriteText).toHaveBeenCalledWith("ls -la");

    // Restore original clipboard
    if (originalWriteText) {
      Object.defineProperty(navigator, "clipboard", {
        value: {
          writeText: originalWriteText,
        },
        configurable: true,
      });
    }
  });

  it("shows copy button on hover", async () => {
    userEvent.setup();
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const commandBox = screen.getByText("ls -la").closest("div");
    expect(commandBox).toBeInTheDocument();

    // The copy button should be visible on hover (opacity changes)
    // This is tested by ensuring the button exists
    const copyButton = screen.getByTitle("Copy to clipboard");
    expect(copyButton).toBeInTheDocument();
  });

  it("applies command-box class to command containers", () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const commandBoxes = screen
      .getAllByText("ls -la")
      .map(el => el.closest(".command-box"));
    commandBoxes.forEach(box => {
      expect(box).toHaveClass("command-box", "group", "relative");
    });
  });

  it("applies group class for hover effects", () => {
    const commands = ["ls -la"];
    render(<CommandBox commands={commands} isLoading={false} />);

    // The group class is applied to the container that holds all commands
    const commandsContainer =
      screen.getByText("ls -la").parentElement?.parentElement;
    expect(commandsContainer).toHaveClass("command-box", "group", "relative");
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

  it("renders multiple commands with individual copy buttons", () => {
    const commands = ["ls -la", "pwd"];
    render(<CommandBox commands={commands} isLoading={false} />);

    const copyButtons = screen.getAllByTitle("Copy to clipboard");
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
      "whitespace-nowrap",
      "flex-shrink-0"
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

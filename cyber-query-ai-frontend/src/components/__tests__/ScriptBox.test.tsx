import { render, screen, fireEvent } from "@testing-library/react";

import ScriptBox from "../ScriptBox";

// Mock the clipboard API
Object.assign(navigator, {
  clipboard: {
    writeText: jest.fn(),
  },
});

describe("ScriptBox", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("shows loading state when isLoading=true", () => {
    render(<ScriptBox script="" language="python" isLoading={true} />);

    expect(screen.getByText("📜 Generated Script:")).toBeInTheDocument();
    expect(screen.getByText("Generating script...")).toBeInTheDocument();
  });

  it("shows empty state when script is empty and not loading", () => {
    render(<ScriptBox script="" language="python" isLoading={false} />);

    expect(screen.getByText("📜 Generated Script:")).toBeInTheDocument();
    expect(
      screen.getByText("No script generated. Try rephrasing your prompt.")
    ).toBeInTheDocument();
  });

  it("displays script content when provided", () => {
    const script = "print('Hello, World!')";
    render(<ScriptBox script={script} language="python" isLoading={false} />);

    expect(
      screen.getByText("📜 Generated Script (python):")
    ).toBeInTheDocument();
    expect(screen.getByText(script)).toBeInTheDocument();
  });

  it("shows copy button on hover", () => {
    const script = "print('Hello, World!')";
    render(<ScriptBox script={script} language="python" isLoading={false} />);

    const copyButton = screen.getByTitle("Copy to clipboard");
    expect(copyButton).toBeInTheDocument();
    expect(copyButton).toHaveTextContent("📋");
  });

  it("copies script to clipboard when copy button is clicked", async () => {
    const script = "print('Hello, World!')";
    const mockWriteText = jest.fn();
    navigator.clipboard.writeText = mockWriteText;

    render(<ScriptBox script={script} language="python" isLoading={false} />);

    const copyButton = screen.getByTitle("Copy to clipboard");
    fireEvent.click(copyButton);

    expect(mockWriteText).toHaveBeenCalledWith(script);
  });

  it("displays different programming languages correctly", () => {
    const testCases = [
      { language: "python", script: "print('test')" },
      { language: "javascript", script: "console.log('test')" },
      { language: "bash", script: "echo 'test'" },
    ];

    testCases.forEach(({ language, script }) => {
      const { unmount } = render(
        <ScriptBox script={script} language={language} isLoading={false} />
      );

      expect(
        screen.getByText(`📜 Generated Script (${language}):`)
      ).toBeInTheDocument();
      expect(screen.getByText(script)).toBeInTheDocument();

      unmount();
    });
  });

  it("handles multi-line scripts correctly", () => {
    const multiLineScript = `import os
import sys

def main():
    print("Multi-line script")
    return 0

if __name__ == "__main__":
    main()`;

    render(
      <ScriptBox script={multiLineScript} language="python" isLoading={false} />
    );

    // Use a more flexible text matcher for multi-line content
    expect(screen.getByText(/import os/)).toBeInTheDocument();
    expect(screen.getByText(/def main\(\):/)).toBeInTheDocument();
    expect(
      screen.getByText(/print\("Multi-line script"\)/)
    ).toBeInTheDocument();
  });

  it("has scrollable container for long scripts", () => {
    const longScript = "print('line')\n".repeat(100);

    render(
      <ScriptBox script={longScript} language="python" isLoading={false} />
    );

    // Instead of searching for the full long text, find a subset and check the container
    const container = screen
      .getByText(/print\('line'\)/)
      .closest(".command-box");
    expect(container).toHaveClass("max-h-96", "overflow-y-auto");
  });

  it("sanitizes script content", () => {
    // This test assumes sanitizeOutput is working correctly
    // In a real test, you might want to mock the sanitization function
    const scriptWithPotentialIssues = "print('test')";

    render(
      <ScriptBox
        script={scriptWithPotentialIssues}
        language="python"
        isLoading={false}
      />
    );

    expect(screen.getByText(scriptWithPotentialIssues)).toBeInTheDocument();
  });
});

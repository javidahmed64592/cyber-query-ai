import { render, screen } from "@testing-library/react";

import ExplanationBox from "@/components/ExplanationBox";

describe("ExplanationBox", () => {
  it("does not render when explanation is empty and not loading", () => {
    const { container } = render(
      <ExplanationBox explanation="" isLoading={false} />
    );
    expect(container.firstChild).toBeNull();
  });

  it("shows loading state when isLoading is true", () => {
    render(<ExplanationBox explanation="" isLoading={true} />);
    expect(screen.getByText("📖 Explanation:")).toBeInTheDocument();
    expect(screen.getByText("Generating explanation...")).toBeInTheDocument();
  });

  it("renders explanation when provided", () => {
    const explanation = "This command lists all files in the directory.";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    expect(screen.getByText("📖 Explanation:")).toBeInTheDocument();
    expect(screen.getByText(explanation)).toBeInTheDocument();
  });

  it("preserves whitespace in explanation text", () => {
    const explanation = "Line 1\nLine 2\n  Indented line";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    const explanationTexts = screen.getAllByText((_, element) => {
      return element?.textContent === explanation;
    });
    expect(explanationTexts[1]).toHaveClass("whitespace-pre-wrap");
  });

  it("applies terminal-border class to container", () => {
    const explanation = "Test explanation";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    const container = screen.getByText(explanation).parentElement;
    expect(container).toHaveClass("terminal-border", "rounded-lg", "p-4");
  });

  it("applies scrollable styling for long explanations", () => {
    const longExplanation = "A".repeat(1000);
    render(<ExplanationBox explanation={longExplanation} isLoading={false} />);

    const container = screen.getByText(longExplanation).parentElement;
    expect(container).toHaveClass("max-h-64", "overflow-y-auto");
  });

  it("applies correct text styling", () => {
    const explanation = "Test explanation";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    const textElement = screen.getByText(explanation);
    expect(textElement).toHaveClass(
      "text-[var(--text-secondary)]",
      "whitespace-pre-wrap"
    );
  });

  it("renders loading state with correct styling", () => {
    render(<ExplanationBox explanation="" isLoading={true} />);

    const loadingText = screen.getByText("Generating explanation...");
    const container = loadingText.parentElement;
    expect(container).toHaveClass(
      "terminal-border",
      "rounded-lg",
      "p-4",
      "animate-pulse-neon"
    );
  });

  it("handles multiline explanations correctly", () => {
    const multilineExplanation = `This is a multiline explanation.
It spans multiple lines.
And preserves formatting.`;
    render(
      <ExplanationBox explanation={multilineExplanation} isLoading={false} />
    );

    const explanationElements = screen.getAllByText((_, element) => {
      return element?.textContent === multilineExplanation;
    });
    expect(explanationElements.length).toBeGreaterThan(0);
  });

  it("renders header with correct styling", () => {
    const explanation = "Test";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    const header = screen.getByText("📖 Explanation:");
    expect(header).toHaveClass(
      "text-lg",
      "font-semibold",
      "text-[var(--text-primary)]"
    );
  });
});

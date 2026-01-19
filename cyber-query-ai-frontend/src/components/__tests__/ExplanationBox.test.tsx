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

    const textContainer = screen.getByText(/Line 1/).parentElement;
    expect(textContainer).toHaveClass("whitespace-pre-wrap");
  });

  it("applies terminal-border class to container", () => {
    const explanation = "Test explanation";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    const container =
      screen.getByText(explanation).parentElement?.parentElement;
    expect(container).toHaveClass(
      "border",
      "border-terminal-border",
      "bg-terminal-bg",
      "rounded-lg",
      "p-4"
    );
  });

  it("applies scrollable styling for long explanations", () => {
    const longExplanation = "A".repeat(1000);
    render(<ExplanationBox explanation={longExplanation} isLoading={false} />);

    const container =
      screen.getByText(longExplanation).parentElement?.parentElement;
    expect(container).toHaveClass("max-h-64", "overflow-y-auto");
  });

  it("applies correct text styling", () => {
    const explanation = "Test explanation";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    const textContainer = screen.getByText(explanation).parentElement;
    expect(textContainer).toHaveClass(
      "text-text-secondary",
      "whitespace-pre-wrap"
    );
  });

  it("renders loading state with correct styling", () => {
    render(<ExplanationBox explanation="" isLoading={true} />);

    const loadingText = screen.getByText("Generating explanation...");
    const container = loadingText.parentElement;
    expect(container).toHaveClass(
      "border",
      "border-terminal-border",
      "bg-terminal-bg",
      "rounded-lg",
      "p-4"
    );
    expect(container?.className).toContain(
      "animate-[pulse_2s_cubic-bezier(0.4,0,0.6,1)_infinite]"
    );
  });

  it("handles multiline explanations correctly", () => {
    const multilineExplanation = `This is a multiline explanation.
It spans multiple lines.
And preserves formatting.`;
    render(
      <ExplanationBox explanation={multilineExplanation} isLoading={false} />
    );

    // Text is split by newlines, check that first line is rendered
    expect(
      screen.getByText(/This is a multiline explanation/)
    ).toBeInTheDocument();
    expect(screen.getByText(/It spans multiple lines/)).toBeInTheDocument();
  });

  it("renders header with correct styling", () => {
    const explanation = "Test";
    render(<ExplanationBox explanation={explanation} isLoading={false} />);

    const header = screen.getByText("📖 Explanation:");
    expect(header).toHaveClass("text-lg", "font-semibold", "text-text-primary");
  });
});

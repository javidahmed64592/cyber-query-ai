import { render, screen, fireEvent } from "@testing-library/react";

import LanguageSelector from "../LanguageSelector";

describe("LanguageSelector", () => {
  const defaultProps = {
    value: "python",
    onChange: jest.fn(),
    disabled: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders with correct label", () => {
    render(<LanguageSelector {...defaultProps} />);

    expect(screen.getByText("🧪 Select Language:")).toBeInTheDocument();
  });

  it("renders select element with correct value", () => {
    render(<LanguageSelector {...defaultProps} />);

    const selectElement = screen.getByDisplayValue("🐍 Python");
    expect(selectElement).toBeInTheDocument();
    expect(selectElement).toHaveValue("python");
  });

  it("renders all language options", () => {
    render(<LanguageSelector {...defaultProps} />);

    const expectedLanguages = [
      "🐍 Python",
      "🐚 Bash",
      "💙 PowerShell",
      "🟨 JavaScript",
      "🐹 Go",
      "🦀 Rust",
    ];

    expectedLanguages.forEach(language => {
      expect(screen.getByText(language)).toBeInTheDocument();
    });
  });

  it("calls onChange when selection changes", () => {
    const mockOnChange = jest.fn();
    render(<LanguageSelector {...defaultProps} onChange={mockOnChange} />);

    const selectElement = screen.getByDisplayValue("🐍 Python");
    fireEvent.change(selectElement, { target: { value: "bash" } });

    expect(mockOnChange).toHaveBeenCalledWith("bash");
  });

  it("is disabled when disabled prop is true", () => {
    render(<LanguageSelector {...defaultProps} disabled={true} />);

    const selectElement = screen.getByDisplayValue("🐍 Python");
    expect(selectElement).toBeDisabled();
  });

  it("is enabled when disabled prop is false", () => {
    render(<LanguageSelector {...defaultProps} disabled={false} />);

    const selectElement = screen.getByDisplayValue("🐍 Python");
    expect(selectElement).not.toBeDisabled();
  });

  it("displays correct option for different selected values", () => {
    const { rerender } = render(
      <LanguageSelector {...defaultProps} value="bash" />
    );
    expect(screen.getByDisplayValue("🐚 Bash")).toBeInTheDocument();

    rerender(<LanguageSelector {...defaultProps} value="javascript" />);
    expect(screen.getByDisplayValue("🟨 JavaScript")).toBeInTheDocument();

    rerender(<LanguageSelector {...defaultProps} value="rust" />);
    expect(screen.getByDisplayValue("🦀 Rust")).toBeInTheDocument();
  });
});

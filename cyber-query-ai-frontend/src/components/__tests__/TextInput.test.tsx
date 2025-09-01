import { render, screen, fireEvent } from "@testing-library/react";

import TextInput from "../TextInput";

describe("TextInput", () => {
  const defaultProps = {
    label: "Test Label",
    value: "",
    onChange: jest.fn(),
    onSubmit: jest.fn(),
    placeholder: "Test placeholder",
    buttonText: "Submit",
    isLoading: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders with correct label", () => {
    render(<TextInput {...defaultProps} />);

    expect(screen.getByText("Test Label")).toBeInTheDocument();
  });

  it("renders textarea by default (multiline=true)", () => {
    render(<TextInput {...defaultProps} />);

    const textarea = screen.getByPlaceholderText("Test placeholder");
    expect(textarea.tagName).toBe("TEXTAREA");
  });

  it("renders input when multiline=false", () => {
    render(<TextInput {...defaultProps} multiline={false} />);

    const input = screen.getByPlaceholderText("Test placeholder");
    expect(input.tagName).toBe("INPUT");
  });

  it("displays correct value", () => {
    render(<TextInput {...defaultProps} value="test value" />);

    const input = screen.getByDisplayValue("test value");
    expect(input).toBeInTheDocument();
  });

  it("calls onChange when input value changes", () => {
    const mockOnChange = jest.fn();
    render(<TextInput {...defaultProps} onChange={mockOnChange} />);

    const input = screen.getByPlaceholderText("Test placeholder");
    fireEvent.change(input, { target: { value: "new value" } });

    expect(mockOnChange).toHaveBeenCalledWith("new value");
  });

  it("calls onSubmit when button is clicked", () => {
    const mockOnSubmit = jest.fn();
    render(
      <TextInput {...defaultProps} value="test" onSubmit={mockOnSubmit} />
    );

    const button = screen.getByText("Submit");
    fireEvent.click(button);

    expect(mockOnSubmit).toHaveBeenCalled();
  });

  it("calls onSubmit when Ctrl+Enter is pressed", () => {
    const mockOnSubmit = jest.fn();
    render(
      <TextInput {...defaultProps} value="test" onSubmit={mockOnSubmit} />
    );

    const input = screen.getByPlaceholderText("Test placeholder");
    fireEvent.keyDown(input, { key: "Enter", ctrlKey: true });

    expect(mockOnSubmit).toHaveBeenCalled();
  });

  it("calls onSubmit when Cmd+Enter is pressed", () => {
    const mockOnSubmit = jest.fn();
    render(
      <TextInput {...defaultProps} value="test" onSubmit={mockOnSubmit} />
    );

    const input = screen.getByPlaceholderText("Test placeholder");
    fireEvent.keyDown(input, { key: "Enter", metaKey: true });

    expect(mockOnSubmit).toHaveBeenCalled();
  });

  it("does not call onSubmit when Enter is pressed without modifier", () => {
    const mockOnSubmit = jest.fn();
    render(
      <TextInput {...defaultProps} value="test" onSubmit={mockOnSubmit} />
    );

    const input = screen.getByPlaceholderText("Test placeholder");
    fireEvent.keyDown(input, { key: "Enter" });

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it("disables input and button when isLoading=true", () => {
    render(<TextInput {...defaultProps} isLoading={true} />);

    const input = screen.getByPlaceholderText("Test placeholder");
    const button = screen.getByRole("button");

    expect(input).toBeDisabled();
    expect(button).toBeDisabled();
  });

  it("disables button when value is empty", () => {
    render(<TextInput {...defaultProps} value="" />);

    const button = screen.getByRole("button");
    expect(button).toBeDisabled();
  });

  it("disables button when value is only whitespace", () => {
    render(<TextInput {...defaultProps} value="   " />);

    const button = screen.getByRole("button");
    expect(button).toBeDisabled();
  });

  it("enables button when value has content", () => {
    render(<TextInput {...defaultProps} value="test content" />);

    const button = screen.getByRole("button");
    expect(button).not.toBeDisabled();
  });

  it("shows loading state with custom loading text", () => {
    render(
      <TextInput
        {...defaultProps}
        isLoading={true}
        loadingText="Processing..."
      />
    );

    expect(screen.getByText("Processing...")).toBeInTheDocument();
    expect(screen.getByText("⚡")).toBeInTheDocument();
  });

  it("shows default loading text when none provided", () => {
    render(<TextInput {...defaultProps} isLoading={true} />);

    expect(screen.getByText("Processing...")).toBeInTheDocument();
  });

  it("applies custom height class", () => {
    render(<TextInput {...defaultProps} height="h-64" />);

    const input = screen.getByPlaceholderText("Test placeholder");
    expect(input).toHaveClass("h-64");
  });

  it("applies default height class when none provided", () => {
    render(<TextInput {...defaultProps} />);

    const input = screen.getByPlaceholderText("Test placeholder");
    expect(input).toHaveClass("h-32");
  });
});

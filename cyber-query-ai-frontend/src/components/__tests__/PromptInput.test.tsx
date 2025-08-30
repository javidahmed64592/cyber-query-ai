import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import PromptInput from "../PromptInput";

describe("PromptInput", () => {
  const mockOnChange = jest.fn();
  const mockOnSubmit = jest.fn();

  const defaultProps = {
    value: "",
    onChange: mockOnChange,
    onSubmit: mockOnSubmit,
    isLoading: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the prompt input label", () => {
    render(<PromptInput {...defaultProps} />);
    expect(screen.getByText("🧠 Prompt:")).toBeInTheDocument();
  });

  it("renders textarea with correct placeholder", () => {
    render(<PromptInput {...defaultProps} />);
    const textarea = screen.getByPlaceholderText(
      "Describe the task you want to perform... (Ctrl+Enter to submit)"
    );
    expect(textarea).toBeInTheDocument();
  });

  it("renders the generate button", () => {
    render(<PromptInput {...defaultProps} />);
    expect(
      screen.getByRole("button", { name: /🚀 Generate Command/ })
    ).toBeInTheDocument();
  });

  it("calls onChange when textarea value changes", async () => {
    const user = userEvent.setup();
    render(<PromptInput {...defaultProps} />);

    const textarea = screen.getByRole("textbox");
    await user.type(textarea, "test prompt");

    expect(mockOnChange).toHaveBeenCalledTimes(11); // 't' 'e' 's' 't' ' ' 'p' 'r' 'o' 'm' 'p' 't'
  });

  it("calls onSubmit when button is clicked", async () => {
    const user = userEvent.setup();
    render(<PromptInput {...defaultProps} value="test prompt" />);

    const button = screen.getByRole("button", { name: /🚀 Generate Command/ });
    await user.click(button);

    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
  });

  it("calls onSubmit when Ctrl+Enter is pressed", async () => {
    const user = userEvent.setup();
    render(<PromptInput {...defaultProps} value="test prompt" />);

    const textarea = screen.getByRole("textbox");
    await user.type(textarea, "{Control>}{Enter}{/Control}");

    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
  });

  it("calls onSubmit when Cmd+Enter is pressed on Mac", async () => {
    const user = userEvent.setup();
    render(<PromptInput {...defaultProps} value="test prompt" />);

    const textarea = screen.getByRole("textbox");
    await user.type(textarea, "{Meta>}{Enter}{/Meta}");

    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
  });

  it("disables textarea when loading", () => {
    render(<PromptInput {...defaultProps} isLoading={true} />);
    const textarea = screen.getByRole("textbox");
    expect(textarea).toBeDisabled();
  });

  it("disables button when loading", () => {
    render(<PromptInput {...defaultProps} isLoading={true} />);
    const button = screen.getByRole("button");
    expect(button).toBeDisabled();
  });

  it("disables button when value is empty", () => {
    render(<PromptInput {...defaultProps} value="" />);
    const button = screen.getByRole("button");
    expect(button).toBeDisabled();
  });

  it("enables button when value is not empty", () => {
    render(<PromptInput {...defaultProps} value="test prompt" />);
    const button = screen.getByRole("button");
    expect(button).not.toBeDisabled();
  });

  it("shows loading text when loading", () => {
    render(<PromptInput {...defaultProps} isLoading={true} />);
    expect(screen.getByText("Generating...")).toBeInTheDocument();
  });

  it("applies cyber-input class to textarea", () => {
    render(<PromptInput {...defaultProps} />);
    const textarea = screen.getByRole("textbox");
    expect(textarea).toHaveClass("cyber-input");
  });

  it("applies cyber-button class to button", () => {
    render(<PromptInput {...defaultProps} />);
    const button = screen.getByRole("button");
    expect(button).toHaveClass("cyber-button");
  });
});

import { render, screen } from "@testing-library/react";

import Footer from "@/components/Footer";

describe("Footer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the footer component", async () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toBeInTheDocument();
  });

  it("displays the terminal prompt", async () => {
    render(<Footer />);

    expect(screen.getByText("cyber@query:~$")).toBeInTheDocument();
  });

  it("has fixed positioning at the bottom", async () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("fixed", "bottom-0", "left-0", "right-0");
  });

  it("has proper z-index for overlay", async () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("z-40");
  });

  it("has terminal styling", async () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass(
      "bg-background-secondary",
      "border-t",
      "border-terminal-border"
    );
  });

  it("has responsive layout with flexbox", async () => {
    render(<Footer />);

    const contentDiv = screen.getByText("cyber@query:~$").closest("div");
    expect(contentDiv).toHaveClass(
      "text-center",
      "flex",
      "flex-wrap",
      "justify-center",
      "gap-4"
    );
  });

  it("has monospace font styling", async () => {
    render(<Footer />);

    const contentDiv = screen.getByText("cyber@query:~$").closest("div");
    expect(contentDiv).toHaveClass("font-mono", "text-sm");
  });

  it("has neon green color for terminal prompt", async () => {
    render(<Footer />);

    const terminalPrompt = screen.getByText("cyber@query:~$");
    expect(terminalPrompt).toHaveClass("text-neon-green");
  });

  it("has proper container constraints", async () => {
    render(<Footer />);

    const container = screen
      .getByRole("contentinfo")
      .querySelector(".container");
    expect(container).toHaveClass("mx-auto", "max-w-6xl");
  });

  it("renders with semantic footer element", async () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer.tagName).toBe("FOOTER");
  });
});

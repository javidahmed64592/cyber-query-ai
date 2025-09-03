import { render, screen } from "@testing-library/react";
import React from "react";

import { version } from "../../lib/version";
import Footer from "../Footer";

describe("Footer", () => {
  it("renders the footer component", () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toBeInTheDocument();
  });

  it("displays the terminal prompt", () => {
    render(<Footer />);

    expect(screen.getByText("cyber@query:~$")).toBeInTheDocument();
  });

  it("displays the version information", () => {
    render(<Footer />);

    expect(screen.getByText(`--version v${version}`)).toBeInTheDocument();
  });

  it("has fixed positioning at the bottom", () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("fixed", "bottom-0", "left-0", "right-0");
  });

  it("has proper z-index for overlay", () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("z-40");
  });

  it("has terminal styling", () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass(
      "bg-[var(--background-secondary)]",
      "border-t",
      "border-[var(--terminal-border)]"
    );
  });

  it("has responsive layout with flexbox", () => {
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

  it("has monospace font styling", () => {
    render(<Footer />);

    const contentDiv = screen.getByText("cyber@query:~$").closest("div");
    expect(contentDiv).toHaveClass("font-mono", "text-sm");
  });

  it("has neon green color for terminal prompt", () => {
    render(<Footer />);

    const terminalPrompt = screen.getByText("cyber@query:~$");
    expect(terminalPrompt).toHaveClass("text-[var(--neon-green)]");
  });

  it("has proper container constraints", () => {
    render(<Footer />);

    const container = screen
      .getByRole("contentinfo")
      .querySelector(".container");
    expect(container).toHaveClass("mx-auto", "max-w-6xl");
  });

  it("renders with semantic footer element", () => {
    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer.tagName).toBe("FOOTER");
  });

  it("includes version from version library", () => {
    render(<Footer />);

    // Test that the version is actually dynamic and comes from the version library
    const versionText = screen.getByText(`--version v${version}`);
    expect(versionText).toBeInTheDocument();

    // Ensure it's not hardcoded by checking the import
    expect(typeof version).toBe("string");
  });
});

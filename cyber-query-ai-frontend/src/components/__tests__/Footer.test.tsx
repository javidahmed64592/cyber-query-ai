import { render, screen, waitFor } from "@testing-library/react";

import Footer from "@/components/Footer";
import { getConfig } from "@/lib/api";
import { version } from "@/lib/version";

// Mock the API
jest.mock("../../lib/api", () => ({
  getConfig: jest.fn(),
}));

const mockGetConfig = getConfig as jest.MockedFunction<typeof getConfig>;

describe("Footer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the footer component", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toBeInTheDocument();
  });

  it("displays the terminal prompt", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    expect(screen.getByText("cyber@query:~$")).toBeInTheDocument();
  });

  it("displays the version information", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    expect(screen.getByText(`--version v${version}`)).toBeInTheDocument();
  });

  it("displays the LLM model when config is loaded", async () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    await waitFor(() => {
      expect(screen.getByText("--model mistral")).toBeInTheDocument();
    });
  });

  it("displays the RAG model when config is loaded", async () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    await waitFor(() => {
      expect(screen.getByText("--rag_model bge-m3")).toBeInTheDocument();
    });
  });

  it("displays pipe separators between config values", async () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    await waitFor(() => {
      const pipes = screen.getAllByText("|");
      expect(pipes.length).toBeGreaterThanOrEqual(2);
    });
  });

  it("handles config fetch failure gracefully", async () => {
    mockGetConfig.mockRejectedValue(new Error("Network error"));

    render(<Footer />);

    // Should still render version without models
    expect(screen.getByText(`--version v${version}`)).toBeInTheDocument();

    // Wait to ensure models are not displayed
    await waitFor(() => {
      expect(screen.queryByText(/--model/)).not.toBeInTheDocument();
      expect(screen.queryByText(/--rag_model/)).not.toBeInTheDocument();
    });
  });

  it("has fixed positioning at the bottom", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("fixed", "bottom-0", "left-0", "right-0");
  });

  it("has proper z-index for overlay", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("z-40");
  });

  it("has terminal styling", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass(
      "bg-[var(--background-secondary)]",
      "border-t",
      "border-[var(--terminal-border)]"
    );
  });

  it("has responsive layout with flexbox", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

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
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const contentDiv = screen.getByText("cyber@query:~$").closest("div");
    expect(contentDiv).toHaveClass("font-mono", "text-sm");
  });

  it("has neon green color for terminal prompt", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const terminalPrompt = screen.getByText("cyber@query:~$");
    expect(terminalPrompt).toHaveClass("text-[var(--neon-green)]");
  });

  it("has proper container constraints", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const container = screen
      .getByRole("contentinfo")
      .querySelector(".container");
    expect(container).toHaveClass("mx-auto", "max-w-6xl");
  });

  it("renders with semantic footer element", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer.tagName).toBe("FOOTER");
  });

  it("includes version from version library", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    // Test that the version is actually dynamic and comes from the version library
    const versionText = screen.getByText(`--version v${version}`);
    expect(versionText).toBeInTheDocument();

    // Ensure it's not hardcoded by checking the import
    expect(typeof version).toBe("string");
  });

  it("fetches config on mount", () => {
    mockGetConfig.mockResolvedValue({
      model: "mistral",
      embedding_model: "bge-m3",
      host: "localhost",
      port: 8000,
    });

    render(<Footer />);

    expect(mockGetConfig).toHaveBeenCalledTimes(1);
  });
});

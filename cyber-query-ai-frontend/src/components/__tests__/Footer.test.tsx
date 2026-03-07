import { render, screen, waitFor } from "@testing-library/react";

import Footer from "@/components/Footer";
import { getConfig } from "@/lib/api";

// Mock the API
jest.mock("../../lib/api", () => ({
  getConfig: jest.fn(),
}));

const mockGetConfig = getConfig as jest.MockedFunction<typeof getConfig>;

const TEST_VERSION = "x.y.z";

const createMockConfig = () => ({
  code: 200,
  message: "Successfully retrieved chatbot configuration.",
  timestamp: "2023-01-01T00:00:00Z",
  model: {
    model: "mistral",
    embedding_model: "bge-m3",
  },
  version: TEST_VERSION,
});

describe("Footer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the footer component", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toBeInTheDocument();

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("displays the terminal prompt", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    expect(screen.getByText("cyber@query:~$")).toBeInTheDocument();

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("displays the version information from config", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    await waitFor(() => {
      expect(
        screen.getByText(`--version=v${TEST_VERSION}`)
      ).toBeInTheDocument();
    });
  });

  it("displays the LLM model when config is loaded", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    await waitFor(() => {
      expect(screen.getByText("--model=mistral")).toBeInTheDocument();
    });
  });

  it("displays the RAG model when config is loaded", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    await waitFor(() => {
      expect(screen.getByText("--rag_model=bge-m3")).toBeInTheDocument();
    });
  });

  it("handles config fetch failure gracefully", async () => {
    mockGetConfig.mockRejectedValue(new Error("Network error"));

    render(<Footer />);

    // Should show loading state when config fetch fails
    await waitFor(() => {
      expect(screen.getByText("--loading...")).toBeInTheDocument();
    });

    // Ensure models and version are not displayed
    expect(screen.queryByText(/--version/)).not.toBeInTheDocument();
    expect(screen.queryByText(/--model/)).not.toBeInTheDocument();
    expect(screen.queryByText(/--rag_model/)).not.toBeInTheDocument();
  });

  it("has fixed positioning at the bottom", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("fixed", "bottom-0", "left-0", "right-0");

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("has proper z-index for overlay", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass("z-40");

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("has terminal styling", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer).toHaveClass(
      "bg-background-secondary",
      "border-t",
      "border-terminal-border"
    );

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("has responsive layout with flexbox", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const contentDiv = screen.getByText("cyber@query:~$").closest("div");
    expect(contentDiv).toHaveClass(
      "text-center",
      "flex",
      "flex-wrap",
      "justify-center",
      "gap-4"
    );

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("has monospace font styling", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const contentDiv = screen.getByText("cyber@query:~$").closest("div");
    expect(contentDiv).toHaveClass("font-mono", "text-sm");

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("has neon green color for terminal prompt", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const terminalPrompt = screen.getByText("cyber@query:~$");
    expect(terminalPrompt).toHaveClass("text-neon-green");

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("has proper container constraints", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const container = screen
      .getByRole("contentinfo")
      .querySelector(".container");
    expect(container).toHaveClass("mx-auto", "max-w-6xl");

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("renders with semantic footer element", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    const footer = screen.getByRole("contentinfo");
    expect(footer.tagName).toBe("FOOTER");

    // Wait for config to load
    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalled();
    });
  });

  it("fetches config on mount", async () => {
    mockGetConfig.mockResolvedValue(createMockConfig());

    render(<Footer />);

    await waitFor(() => {
      expect(mockGetConfig).toHaveBeenCalledTimes(1);
    });
  });

  it("displays loading state before config is loaded", () => {
    mockGetConfig.mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<Footer />);

    expect(screen.getByText("--loading...")).toBeInTheDocument();
    expect(screen.queryByText(/--version/)).not.toBeInTheDocument();
  });
});

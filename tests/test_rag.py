"""Unit tests for the cyber_query_ai.rag module."""

import json
import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
from langchain_core.documents import Document

from cyber_query_ai.rag import RAGSystem, ToolsMetadata, ToolSuite


class TestToolsMetadata:
    """Unit tests for the ToolsMetadata class."""

    @pytest.fixture
    def sample_tool_metadata(self) -> ToolsMetadata:
        """Fixture for sample tool metadata."""
        return ToolsMetadata(
            file="nmap_help.txt",
            name="nmap",
            category="reconnaissance",
            subcategory="network_scanning",
            description="Network exploration tool and security/port scanner",
            tags=["network", "port", "scanning", "enumeration"],
            use_cases=["port scanning", "network discovery", "service enumeration", "OS detection"],
        )

    def test_metadata_dict_property(self, sample_tool_metadata: ToolsMetadata) -> None:
        """Test the metadata_dict property returns correct dictionary."""
        expected = {
            "source": "nmap_help.txt",
            "tool": "nmap",
            "category": "reconnaissance",
            "subcategory": "network_scanning",
            "description": "Network exploration tool and security/port scanner",
            "tags": ["network", "port", "scanning", "enumeration"],
            "use_cases": ["port scanning", "network discovery", "service enumeration", "OS detection"],
        }
        assert sample_tool_metadata.metadata_dict == expected


class TestToolSuite:
    """Unit tests for the ToolSuite class."""

    @pytest.fixture
    def sample_tools_data(self) -> dict:
        """Fixture for sample tools data."""
        return {
            "nmap": {
                "file": "nmap_help.txt",
                "name": "nmap",
                "category": "reconnaissance",
                "subcategory": "network_scanning",
                "description": "Network exploration tool",
                "tags": ["network", "scanning"],
                "use_cases": ["port scanning"],
            },
            "hydra": {
                "file": "hydra_help.txt",
                "name": "hydra",
                "category": "password_attacks",
                "subcategory": "brute_force",
                "description": "Network logon cracker",
                "tags": ["brute-force", "network"],
                "use_cases": ["password brute forcing"],
            },
        }

    def test_from_json_with_valid_file(self, sample_tools_data: dict) -> None:
        """Test loading ToolSuite from a valid JSON file."""
        mock_json_data = json.dumps(sample_tools_data)

        with patch("builtins.open", mock_open(read_data=mock_json_data)):
            tool_suite = ToolSuite.from_json("test_file.json")

        expected_tools_count = 2
        assert len(tool_suite.tools) == expected_tools_count
        assert "nmap" in tool_suite.tools
        assert "hydra" in tool_suite.tools
        assert tool_suite.tools["nmap"].name == "nmap"
        assert tool_suite.tools["hydra"].category == "password_attacks"

    def test_from_json_with_nonexistent_file(self) -> None:
        """Test loading ToolSuite from a nonexistent file returns empty suite."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            tool_suite = ToolSuite.from_json("nonexistent.json")

        empty_tools_count = 0
        assert len(tool_suite.tools) == empty_tools_count
        assert tool_suite.tools == {}

    def test_from_json_with_invalid_json(self) -> None:
        """Test loading ToolSuite from an invalid JSON file returns empty suite."""
        invalid_json = "{'invalid': json"

        with patch("builtins.open", mock_open(read_data=invalid_json)):
            tool_suite = ToolSuite.from_json("invalid.json")

        empty_tools_count = 0
        assert len(tool_suite.tools) == empty_tools_count
        assert tool_suite.tools == {}

    def test_from_json_with_empty_file(self) -> None:
        """Test loading ToolSuite from an empty JSON file."""
        with patch("builtins.open", mock_open(read_data="{}")):
            tool_suite = ToolSuite.from_json("empty.json")

        empty_tools_count = 0
        assert len(tool_suite.tools) == empty_tools_count
        assert tool_suite.tools == {}


class TestRAGSystem:
    """Unit tests for the RAGSystem class."""

    @pytest.fixture
    def mock_ollama_embeddings(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock OllamaEmbeddings."""
        with patch("cyber_query_ai.rag.OllamaEmbeddings") as mock:
            yield mock

    @pytest.fixture
    def mock_vector_store(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock InMemoryVectorStore."""
        with patch("cyber_query_ai.rag.InMemoryVectorStore") as mock:
            mock_instance = MagicMock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def mock_text_loader(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock TextLoader."""
        with patch("cyber_query_ai.rag.TextLoader") as mock:
            yield mock

    @pytest.fixture
    def temp_tools_file(self) -> Generator[Path, None, None]:
        """Fixture to create a temporary tools JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            sample_data = {
                "nmap": {
                    "file": "nmap_help.txt",
                    "name": "nmap",
                    "category": "reconnaissance",
                    "subcategory": "network_scanning",
                    "description": "Network exploration tool",
                    "tags": ["network", "scanning"],
                    "use_cases": ["port scanning"],
                }
            }
            json.dump(sample_data, f)
            temp_path = Path(f.name)

        yield temp_path

        # Cleanup
        if temp_path.exists():
            temp_path.unlink()

    @pytest.fixture
    def rag_system(self, mock_ollama_embeddings: MagicMock, temp_tools_file: Path) -> RAGSystem:
        """Fixture for RAGSystem instance."""
        return RAGSystem(
            model="test_model", embedding_model="test_embedding_model", tools_json_filepath=temp_tools_file
        )

    def test_rag_system_initialization(self, rag_system: RAGSystem, mock_ollama_embeddings: MagicMock) -> None:
        """Test RAGSystem initialization."""
        assert rag_system.model == "test_model"
        assert rag_system.embedding_model == "test_embedding_model"
        assert rag_system.vector_store is None
        mock_ollama_embeddings.assert_called_once_with(model="test_embedding_model")

    def test_create_class_method(self, mock_ollama_embeddings: MagicMock) -> None:
        """Test RAGSystem.create class method."""
        with patch.object(RAGSystem, "create_vector_store") as mock_create_vs:
            rag_system = RAGSystem.create("test_model", "test_embedding", Path("test_tools.json"))

        assert rag_system.model == "test_model"
        assert rag_system.embedding_model == "test_embedding"
        assert rag_system.tools_json_filepath == Path("test_tools.json")
        mock_create_vs.assert_called_once()

    def test_load_documents_with_existing_tools_file(self, rag_system: RAGSystem, mock_text_loader: MagicMock) -> None:
        """Test load_documents with existing tools file and text files."""
        # Mock the glob to return some txt files
        mock_txt_files = [Path("nmap_help.txt"), Path("hydra_help.txt")]

        # Mock documents returned by TextLoader
        mock_doc1 = Document(page_content="nmap content", metadata={})
        mock_doc2 = Document(page_content="hydra content", metadata={})

        mock_text_loader.return_value.load.side_effect = [[mock_doc1], [mock_doc2]]

        # Mock the Path.glob method instead of patching the instance
        with patch("pathlib.Path.glob", return_value=mock_txt_files):
            documents = rag_system.load_documents()

        expected_document_count = 2
        assert len(documents) == expected_document_count
        # Check that metadata was added to the nmap document
        assert documents[0].metadata["tool"] == "nmap"
        assert documents[0].metadata["category"] == "reconnaissance"

    def test_load_documents_with_nonexistent_tools_file(self, mock_ollama_embeddings: MagicMock) -> None:
        """Test load_documents with nonexistent tools file."""
        nonexistent_file = Path("nonexistent.json")
        rag_system = RAGSystem("model", "embedding", nonexistent_file)

        documents = rag_system.load_documents()

        assert documents == []

    def test_create_vector_store(self, rag_system: RAGSystem, mock_vector_store: MagicMock) -> None:
        """Test create_vector_store method."""
        # Mock load_documents to return some documents
        mock_docs = [Document(page_content="test content", metadata={})]

        with patch.object(rag_system, "load_documents", return_value=mock_docs):
            with patch.object(rag_system.text_splitter, "split_documents", return_value=mock_docs):
                rag_system.create_vector_store()

        assert rag_system.vector_store is not None
        mock_vector_store.add_documents.assert_called_once_with(mock_docs)

    def test_create_vector_store_with_no_documents(self, rag_system: RAGSystem, mock_vector_store: MagicMock) -> None:
        """Test create_vector_store with no documents."""
        with patch.object(rag_system, "load_documents", return_value=[]):
            rag_system.create_vector_store()

        assert rag_system.vector_store is not None
        mock_vector_store.add_documents.assert_not_called()

    def test_format_context_with_documents(self, rag_system: RAGSystem) -> None:
        """Test format_context with documents containing metadata."""
        documents = [
            Document(
                page_content="nmap is a network scanner",
                metadata={
                    "tool": "nmap",
                    "source": "nmap_help.txt",
                    "category": "reconnaissance",
                    "subcategory": "network_scanning",
                    "description": "Network exploration tool",
                    "tags": ["network", "scanning"],
                    "use_cases": ["port scanning"],
                },
            ),
            Document(
                page_content="hydra is a brute forcer",
                metadata={"tool": "hydra", "source": "hydra_help.txt", "category": "password_attacks"},
            ),
        ]

        context = rag_system.format_context(documents)

        assert "Tool: nmap" in context
        assert "Category: reconnaissance" in context
        assert "nmap is a network scanner" in context
        assert "Tool: hydra" in context
        assert "hydra is a brute forcer" in context
        assert "=" * 80 in context

    def test_format_context_with_empty_documents(self, rag_system: RAGSystem) -> None:
        """Test format_context with empty document list."""
        context = rag_system.format_context([])
        assert context == ""

    def test_get_context_for_template_with_results(self, rag_system: RAGSystem, mock_vector_store: MagicMock) -> None:
        """Test get_context_for_template when vector store returns results."""
        rag_system.vector_store = mock_vector_store

        mock_docs = [Document(page_content="test content", metadata={"tool": "test"})]
        mock_vector_store.similarity_search.return_value = mock_docs

        with patch.object(rag_system, "format_context", return_value="formatted context") as mock_format:
            result = rag_system.get_context_for_template("test query")

        mock_vector_store.similarity_search.assert_called_once_with("test query", k=3)
        mock_format.assert_called_once_with(mock_docs)
        assert result == "formatted context"

    def test_get_context_for_template_with_no_results(
        self, rag_system: RAGSystem, mock_vector_store: MagicMock
    ) -> None:
        """Test get_context_for_template when vector store returns no results."""
        rag_system.vector_store = mock_vector_store
        mock_vector_store.similarity_search.return_value = []

        result = rag_system.get_context_for_template("test query")

        assert result == ""

    def test_get_context_for_template_with_no_vector_store(self, rag_system: RAGSystem) -> None:
        """Test get_context_for_template when vector store is None."""
        rag_system.vector_store = None

        result = rag_system.get_context_for_template("test query")

        assert result == ""

    def test_generate_rag_content_with_context(self, rag_system: RAGSystem) -> None:
        """Test generate_rag_content when context is available."""
        mock_context = "Tool: nmap | Category: reconnaissance\n\nnmap content"

        with patch.object(rag_system, "get_context_for_template", return_value=mock_context):
            result = rag_system.generate_rag_content("test query")

        assert "RELEVANT DOCUMENTATION:" in result
        assert "nmap content" in result
        assert "Use the above documentation" in result
        # Check that braces are escaped for string formatting
        assert "{{" in result or "}}" in result or "{" not in result

    def test_generate_rag_content_without_context(self, rag_system: RAGSystem) -> None:
        """Test generate_rag_content when no context is available."""
        with patch.object(rag_system, "get_context_for_template", return_value=""):
            result = rag_system.generate_rag_content("test query")

        assert result == ""

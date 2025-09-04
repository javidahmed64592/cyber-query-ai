"""RAG system for the CyberQueryAI application."""

from __future__ import annotations

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from cyber_query_ai.config import get_root_dir

RAG_DATA_DIR = get_root_dir() / "rag_data"
TOOLS_FILENAME = "tools.json"
TOOLS_FILEPATH = RAG_DATA_DIR / TOOLS_FILENAME


class RAGSystem:
    """RAG (Retrieval-Augmented Generation) system for cybersecurity documentation."""

    def __init__(self, model: str = "llama3.2", embedding_model: str = "nomic-embed-text") -> None:
        """Initialize the RAG system."""
        self.model = model
        self.embedding_model = embedding_model
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.vector_store: InMemoryVectorStore | None = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )

    def load_documents(self) -> list[Document]:
        """Load all text documents from the rag_data directory."""
        documents = []

        if not RAG_DATA_DIR.exists():
            return documents

        # Load all .txt files from rag_data directory
        for txt_file in RAG_DATA_DIR.glob("*.txt"):
            loader = TextLoader(str(txt_file), encoding="utf-8")
            docs = loader.load()

            # Add metadata about the tool/file
            for doc in docs:
                doc.metadata.update(
                    {
                        "source": txt_file.name,
                        "tool": txt_file.stem.replace("_man", "").replace("_help", ""),
                        "type": "manual" if "_man" in txt_file.name else "help",
                    }
                )

            documents.extend(docs)

        return documents

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """Split documents into smaller chunks for better retrieval."""
        if not documents:
            return []

        return self.text_splitter.split_documents(documents)

    def create_vector_store(self) -> InMemoryVectorStore:
        """Create or return existing vector store."""
        if self.vector_store is not None:
            return self.vector_store

        # Load and split documents
        documents = self.load_documents()
        if not documents:
            self.vector_store = InMemoryVectorStore(self.embeddings)
            return self.vector_store

        splits = self.split_documents(documents)

        # Create vector store and add documents
        self.vector_store = InMemoryVectorStore(self.embeddings)

        if splits:
            try:
                self.vector_store.add_documents(splits)
            except Exception:
                self.vector_store = InMemoryVectorStore(self.embeddings)

        return self.vector_store

    def recreate_vector_store(self) -> InMemoryVectorStore:
        """Force recreation of the vector store."""
        self.vector_store = None
        return self.create_vector_store()

    def get_relevant_context(self, query: str, k: int = 4) -> list[Document]:
        """Retrieve relevant documents for a given query."""
        if self.vector_store is None:
            self.create_vector_store()

        if self.vector_store is None:
            return []

        try:
            # Perform similarity search
            relevant_docs = self.vector_store.similarity_search(query, k=k)
        except Exception:
            return []
        else:
            return relevant_docs

    def format_context(self, documents: list[Document]) -> str:
        """Format retrieved documents into a context string."""
        if not documents:
            return ""

        context_parts = []
        for doc in documents:
            tool = doc.metadata.get("tool", "unknown")
            source = doc.metadata.get("source", "unknown")
            content = doc.page_content.strip()

            context_parts.append(f"[{tool}] ({source}):\n{content}")

        return "\n\n---\n\n".join(context_parts)

    def is_available(self) -> bool:
        """Check if the RAG system is available and ready to use."""
        try:
            if self.vector_store is None:
                self.create_vector_store()
        except Exception:
            return False
        else:
            return self.vector_store is not None

    def get_context_for_template(self, template_type: str) -> str:
        """Get RAG context for a specific template type."""
        if not self.is_available():
            return ""

        # Define queries for different template types
        query_map = {
            "command": "cybersecurity tools commands CLI",
            "script": "cybersecurity scripts programming",
            "explanation": "tools documentation syntax options",
            "exploit": "exploits vulnerabilities CVE",
        }

        query = query_map.get(template_type, "cybersecurity tools")
        relevant_docs = self.get_relevant_context(query, k=2)

        if relevant_docs:
            return self.format_context(relevant_docs)

        return ""

    def enhance_template(self, base_prompt: str, template_type: str) -> str:
        """Enhance a template with RAG context."""
        rag_context = self.get_context_for_template(template_type)

        if rag_context:
            # Escape curly braces in RAG context to prevent format string conflicts
            escaped_context = rag_context.replace("{", "{{").replace("}", "}}")
            return (
                f"{base_prompt}"
                f"\nRELEVANT DOCUMENTATION:\n"
                f"{escaped_context}\n\n"
                f"Use the above documentation to provide more accurate and detailed responses. "
                f"Reference specific tool options, syntax, and examples from the documentation when relevant.\n\n"
            )

        return base_prompt


def create_rag_system(model: str = "llama3.2") -> RAGSystem:
    """Create and initialize the RAG system."""
    rag_system = RAGSystem(model=model)
    rag_system.create_vector_store()
    return rag_system

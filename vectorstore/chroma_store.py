import chromadb
from chromadb.config import Settings


class ChromaStore:
    def __init__(self, persist_dir: str):
        # Create Chroma client
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_dir,
                anonymized_telemetry=False
            )
        )

        # IMPORTANT: create or load collection
        self.collection = self.client.get_or_create_collection(
            name="medical_docs"
        )

    def query(self, query: str, k: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        formatted = []
        for text, meta in zip(documents, metadatas):
            formatted.append({
                "text": text,
                "metadata": meta or {}
            })

        return formatted
import chromadb
from chromadb.config import Settings
import uuid

class ChromaStore:
    def __init__(self, path="./chroma_db"):
        self.client = chromadb.Client(
            Settings(persist_directory=path, anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection("medical_docs")

    def add(self, docs, embeddings):
        for doc, emb in zip(docs, embeddings):
            self.collection.add(
                ids=[str(uuid.uuid4())],
                documents=[doc["text"]],
                embeddings=[emb],
                metadatas=[doc["metadata"]]
            )

    def query(self, embedding, k=5):
        res = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
            include=["documents", "metadatas"]
        )
        return [
            {"text": t, "metadata": m}
            for t, m in zip(res["documents"][0], res["metadatas"][0])
        ]

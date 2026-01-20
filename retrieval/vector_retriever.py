import os
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VECTOR_DB_DIR = os.path.join(PROJECT_ROOT, "data", "vectorstore", "chroma")

model = SentenceTransformer("all-MiniLM-L6-v2")

client = PersistentClient(path=VECTOR_DB_DIR)

collection = client.get_or_create_collection("medical_rag")

def retrieve(query: str, top_k: int = 5):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    return list(zip(docs, metas))

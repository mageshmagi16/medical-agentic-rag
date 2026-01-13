import os
import json
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

# -------- Paths (absolute) --------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNKS_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "chunks.json")
VECTOR_DB_DIR = os.path.join(PROJECT_ROOT, "data", "vectorstore", "chroma")

os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# -------- Load chunks --------
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# -------- Embedding model --------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- Persistent Chroma client --------
client = PersistentClient(path=VECTOR_DB_DIR)

collection = client.get_or_create_collection("medical_rag")

# -------- Prepare data --------
texts = [c["text"] for c in chunks]
metadatas = [c["metadata"] for c in chunks]
ids = [f"chunk_{i}" for i in range(len(chunks))]

# -------- Create embeddings --------
embeddings = model.encode(texts, show_progress_bar=True)

# -------- Add to collection --------
collection.add(
    documents=texts,
    embeddings=embeddings.tolist(),
    metadatas=metadatas,
    ids=ids
)

count = collection.count()
print(f"Stored {count} vectors in collection")

print("Vector index built and saved persistently")
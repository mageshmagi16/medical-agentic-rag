import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval.vector_retriever import retrieve

query = "What is insulin resistance?"

results = retrieve(query)

print("\n Retrieved Chunks:\n")
for i, (text, meta) in enumerate(results, 1):
    print(f"{i}. {text[:200]}...")
    print(f"   Source: {meta}\n")


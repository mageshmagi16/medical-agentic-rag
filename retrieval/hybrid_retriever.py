# retrieval/hybrid_retriever.py

class HybridRetriever:
    def __init__(self, chroma_store):
        self.chroma = chroma_store

    def retrieve(self, query: str, k: int = 5):
        results = self.chroma.query(query, k=k)

        formatted = []
        for r in results:
            formatted.append({
                "text": r["text"],
                "metadata": r.get("metadata", {})
            })

        return formatted
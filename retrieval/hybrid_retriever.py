class HybridRetriever:
    def __init__(self, chroma_store, bm25_store, embedder):
        self.chroma = chroma_store
        self.bm25 = bm25_store
        self.embedder = embedder

    def retrieve(self, query, k=5):
        q_emb = self.embedder.embed([query])[0]
        dense_docs = self.chroma.query(q_emb, k)
        sparse_docs = self.bm25.query(query, k)

        seen, merged = set(), []
        for d in dense_docs:
            if d["text"] not in seen:
                merged.append(d)
                seen.add(d["text"])

        for s in sparse_docs:
            if s not in seen:
                merged.append({
                    "text": s,
                    "metadata": {"source": "BM25", "type": "keyword"}
                })
                seen.add(s)

        return merged

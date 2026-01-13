from rank_bm25 import BM25Okapi

class BM25Store:
    def __init__(self, documents):
        self.docs = documents
        self.tokenized = [d.lower().split() for d in documents]
        self.bm25 = BM25Okapi(self.tokenized)

    def query(self, text, k=5):
        scores = self.bm25.get_scores(text.lower().split())
        ranked = sorted(zip(self.docs, scores), key=lambda x: x[1], reverse=True)
        return [d for d, _ in ranked[:k]]

from rank_bm25 import BM25Okapi
import nltk

nltk.download("punkt", quiet=True)
from nltk.tokenize import word_tokenize


class BM25Store:
    def __init__(self, documents):
        """
        documents: list of dicts
        Each dict must have at least a 'text' field
        """
        self.documents = documents

        # Tokenize documents
        self.tokenized_docs = [
            word_tokenize(doc["text"].lower())
            for doc in documents
        ]

        # Build BM25 index
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def query(self, query: str, k: int = 5):
        tokenized_query = word_tokenize(query.lower())
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        results = []
        for i in top_indices:
            results.append({
                "text": self.documents[i]["text"],
                "metadata": self.documents[i].get("metadata", {})
            })

        return results
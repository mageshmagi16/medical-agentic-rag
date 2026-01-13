def chunk_documents(docs, max_words=250):
    chunks = []

    for doc in docs:
        words = doc["text"].split()
        for i in range(0, len(words), max_words):
            chunks.append({
                "text": " ".join(words[i:i + max_words]),
                "metadata": doc["metadata"]
            })
    return chunks

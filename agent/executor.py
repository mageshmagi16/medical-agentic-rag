MAX_STEPS = 5

def run_agent(question, retriever, reranker, generator):
    memory = []
    for _ in range(MAX_STEPS):
        docs = retriever(question)
        docs = reranker(question, docs)
        memory.extend(docs)
        return generator(question, memory)
    return "Unable to answer confidently."

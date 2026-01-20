class AgentMemory:
    """
    Simple in-memory conversation state.
    Can be extended later to Redis / DB.
    """

    def __init__(self):
        self.history = []

    def add(self, question: str, answer: str):
        self.history.append({
            "question": question,
            "answer": answer
        })

    def get(self):
        return self.history

    def clear(self):
        self.history = []
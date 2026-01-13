class AgentMemory:
    def __init__(self):
        self.context = []

    def add(self, docs):
        self.context.extend(docs)

    def get(self):
        return self.context

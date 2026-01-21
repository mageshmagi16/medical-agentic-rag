class AgentPlanner:
    """
    Very simple planner for Agentic RAG.
    Decides what steps are needed for a question.
    """

    def plan(self, question: str) -> dict:
        # For now, always retrieve + answer
        return {
            "intent": "medical_information",
            "needs_retrieval": True,
            "needs_generation": True
        }

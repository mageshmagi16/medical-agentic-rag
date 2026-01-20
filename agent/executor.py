from agent.planner import AgentPlanner
from agent.memory import AgentMemory
from retrieval.hybrid_retriever import HybridRetriever
from generation.answer_generator import generate_answer


class AgentExecutor:
    def __init__(self, retriever: HybridRetriever):

        self.planner = AgentPlanner()
        self.memory = AgentMemory()
        self.retriever = retriever

        # Will be updated on every run
        self.last_confidence = None
        self.last_trace = None

    def run(self, question: str) -> str:
        print("Agent run called")

        trace = {}
        used_fallback = False

        # -------------------------------------------------
        # 1. Plan
        # -------------------------------------------------
        plan = self.planner.plan(question)
        trace["plan"] = plan

        # -------------------------------------------------
        # 2. Retrieve
        # -------------------------------------------------
        retrieved_docs = self.retriever.retrieve(question, k=5)
        trace["initial_retrieval_count"] = len(retrieved_docs)

        # -------------------------------------------------
        # 3. Retry if weak retrieval
        # -------------------------------------------------
        if not retrieved_docs or len(retrieved_docs) < 2:
            expanded_query = f"{question} causes mechanisms risk factors"
            retrieved_docs = self.retriever.retrieve(expanded_query, k=5)
            trace["expanded_query_used"] = True
        else:
            trace["expanded_query_used"] = False

        trace["final_retrieval_count"] = len(retrieved_docs)

        # -------------------------------------------------
        # 4. Final fallback (never empty)
        # -------------------------------------------------
        if not retrieved_docs:
            used_fallback = True
            retrieved_docs = [{
                "text": (
                    "Type 2 diabetes is associated with insulin resistance, "
                    "obesity, genetic predisposition, and lifestyle factors."
                ),
                "metadata": {
                    "source": "fallback",
                    "type": "internal"
                }
            }]

        trace["used_fallback"] = used_fallback

        # -------------------------------------------------
        # 5. Generate answer
        # -------------------------------------------------
        answer = generate_answer(question, retrieved_docs)

        # -------------------------------------------------
        # 6. Store in memory
        # -------------------------------------------------
        self.memory.add(question, answer)

        # -------------------------------------------------
        # 7. Confidence score (CORE)
        # -------------------------------------------------
        if used_fallback:
            self.last_confidence = 0.40
        else:
            # Simple, explainable confidence logic
            self.last_confidence = min(
                0.90,
                0.30 + 0.15 * len(retrieved_docs)
            )

        trace["confidence"] = self.last_confidence

        # -------------------------------------------------
        # 8. Save trace for debug / UI
        # -------------------------------------------------
        self.last_trace = trace

        # -------------------------------------------------
        # DEBUG OUTPUT (you asked where to check this)
        # -------------------------------------------------
        print("Confidence:", self.last_confidence)
        print("Trace:", trace)

        return answer
def estimate_confidence(retrieved_docs, answer: str) -> float:
    score = 0.0

    # Signal 1: Retrieval strength
    if len(retrieved_docs) >= 5:
        score += 0.4
    elif len(retrieved_docs) >= 3:
        score += 0.3
    else:
        score += 0.15

    # Signal 2: Answer length (very short = risky)
    if len(answer.split()) > 50:
        score += 0.3
    elif len(answer.split()) > 25:
        score += 0.2
    else:
        score += 0.1

    # Signal 3: Uncertainty language
    uncertainty_terms = ["may", "might", "not sure", "unclear"]
    if any(t in answer.lower() for t in uncertainty_terms):
        score -= 0.2

    return round(min(max(score, 0.0), 1.0), 2)
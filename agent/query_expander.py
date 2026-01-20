def expand_query(question: str):
    base = question.lower()

    expansions = [
        question,
        f"pathophysiology of {base}",
        f"risk factors of {base}",
        f"mechanisms of {base}",
        f"clinical overview of {base}",
        f"insulin resistance and {base}",
    ]

    return list(set(expansions))
def faithfulness(answer, context):
    for sentence in answer.split("."):
        if sentence.strip() and sentence.lower() not in context.lower():
            return False
    return True

from .intent_classifier import classify_intent

def safety_check(question):
    if classify_intent(question) == "medical_advice":
        return False, "Medical advice is not allowed."
    return True, None

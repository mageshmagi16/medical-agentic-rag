def classify_intent(text):
    blocked = [
        "diagnose", "treat", "cure",
        "medicine", "dosage", "prescribe"
    ]
    for w in blocked:
        if w in text.lower():
            return "medical_advice"
    return "medical_information"

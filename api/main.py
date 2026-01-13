import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

from safety.medical_rules import safety_check
from generation.answer_generator import generate_answer

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    allowed, msg = safety_check(query.question)
    if not allowed:
        return {"answer": msg}

    # NOTE: Retriever wiring happens during app startup in production
    return generate_answer(query.question, [])


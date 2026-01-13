import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str, retrieved_chunks: list) -> str:
    if not retrieved_chunks:
        return "I don't know. No relevant information was found."

    context = ""
    for i, (text, meta) in enumerate(retrieved_chunks):
        context += f"[{i+1}] {text}\n"

    prompt = f"""
You are a medical information assistant.
Answer ONLY using the provided context.
Do NOT add external knowledge.
If the answer is not in the context, say "I don't know".

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You provide factual, non-diagnostic medical information."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
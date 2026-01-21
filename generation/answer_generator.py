import os
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# Initialize OpenAI client
# -------------------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------------------------
# Answer generation
# -------------------------------------------------
def generate_answer(question, retrieved_docs):
    """
    question: str
    retrieved_docs: list of dicts with 'text' key
    """

    # Build grounded context
    context = "\n\n".join(
        f"- {doc['text']}" for doc in retrieved_docs
    )

    prompt = f"""
You are a medical information assistant.

Answer the question using ONLY the context below.
Do NOT say you lack information.
Do NOT mention documents explicitly.
Use simple, clear medical language.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.2
    )

    return response.output_text.strip()
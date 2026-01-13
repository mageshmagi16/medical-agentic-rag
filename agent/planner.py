from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def plan(question, context):
    prompt = f"""
Question:
{question}

Context so far:
{context}

Decide next action:
retrieve or answer
"""
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    ).choices[0].message.content.lower()

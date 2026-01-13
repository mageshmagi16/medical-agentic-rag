import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval.vector_retriever import retrieve
from generation.answer_generator import generate_answer

question = "What is insulin resistance?"

retrieved = retrieve(question, top_k=5)
answer = generate_answer(question, retrieved)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)
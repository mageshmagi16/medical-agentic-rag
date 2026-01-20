import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from retrieval.hybrid_retriever import HybridRetriever
from vectorstore.chroma_store import ChromaStore
from embeddings.embedder import Embedder
from agent.executor import AgentExecutor
from safety.medical_rules import safety_check

# -------------------------------------------------
# Environment
# -------------------------------------------------
load_dotenv()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# -------------------------------------------------
# Core components (ONLY VECTOR STORE)
# -------------------------------------------------
embedder = Embedder()
chroma = ChromaStore(
    persist_dir=os.path.join(PROJECT_ROOT, "data", "vectorstore", "chroma")
)
retriever = HybridRetriever(chroma)
agent = AgentExecutor(retriever)

# -------------------------------------------------
# FastAPI
# -------------------------------------------------
app = FastAPI(title="Medical Agentic RAG")

class Query(BaseModel):
    question: str

# -------------------------------------------------
# SIMPLE UI
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Medical Agentic RAG</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .chat-box { max-width: 700px; }
            .msg { margin-bottom: 15px; }
            .user { font-weight: bold; }
            .bot { margin-left: 20px; }
            .confidence { font-size: 12px; color: gray; }
        </style>
    </head>

    <body>
        <h2>Medical Agentic RAG</h2>

        <div class="chat-box" id="chat"></div>

        <br>

        <input id="question" type="text" style="width: 500px;"
               placeholder="Ask a medical question..." />
        <button onclick="ask()">Ask</button>

        <script>
            async function ask() {
                const q = document.getElementById("question").value;
                if (!q) return;

                const chat = document.getElementById("chat");

                // Show user question
                chat.innerHTML += `
                    <div class="msg">
                        <div class="user">You:</div>
                        <div>${q}</div>
                    </div>
                `;

                document.getElementById("question").value = "";

                // Call API
                const res = await fetch("/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: q })
                });

                const data = await res.json();

                // Show assistant answer
                chat.innerHTML += `
                    <div class="msg bot">
                        <div class="user">Assistant:</div>
                        <div>${data.answer}</div>
                    </div>
                `;

                chat.scrollTop = chat.scrollHeight;
            }
        </script>

    </body>
    </html>
    """

# -------------------------------------------------
# ASK ENDPOINT
# -------------------------------------------------
@app.post("/ask")
def ask(query: Query):
    allowed, msg = safety_check(query.question)
    if not allowed:
        return JSONResponse({"answer": msg})

    answer = agent.run(query.question)
    return JSONResponse({
        "answer": answer,
        "confidence": agent.last_confidence,
        "trace": agent.last_trace
    })
# Medical Agentic RAG System

## Overview
An end-to-end **Agentic Retrieval-Augmented Generation (RAG)** system for answering **medical questions** safely, accurately, and explainably.

This project goes beyond a basic RAG pipeline by introducing:
- An intelligent **Agent** with planning and memory
- Safe medical answering
- Confidence scoring
- Dockerized deployment
- UI + API access

---

## What This System Does
- Accepts medical questions via web UI or API
- Retrieves relevant medical knowledge from a vector database (Chroma)
- Generates answers strictly grounded in retrieved content
- Uses an Agent to control reasoning flow
- Retries retrieval when results are weak
- Falls back safely when knowledge is insufficient
- Maintains conversation memory
- Computes an internal confidence score
- Runs locally or inside Docker

---

## Architecture
User → FastAPI UI/API → AgentExecutor  
→ Planner → Retriever (Chroma) → Answer Generator (LLM)  
→ Memory + Confidence → Final Answer

---

## Project Structure
medical-agentic-rag/
- agent/
- retrieval/
- ingestion/
- vectorstore/
- embeddings/
- generation/
- safety/
- api/
- scripts/
- data/
- monitoring/
- evalutation/
- Dockerfile
- requirements.txt
- .env
- README.md

---

## Core Components

### AgentExecutor
Controls the full reasoning pipeline:
1. Plan intent
2. Mandatory retrieval
3. Retry retrieval if weak
4. Safe fallback
5. Answer generation
6. Store memory
7. Compute confidence

### Retrieval
- Chroma vector store
- ONNX MiniLM embeddings
- Persistent storage

### Answer Generation
- OpenAI GPT model
- Uses retrieved context only
- Simple medical language
- No hallucination

### Safety
- Medical rules
- Unsafe advice blocked
- Controlled fallback

### Memory
- Question-answer storage
- Enables follow-up queries
- Single-user (extendable to multi-user)

---

## Confidence Score
Each answer gets an internal confidence score based on:
- Retrieval strength
- Retry usage
- Fallback usage

(Not shown in UI by design)

---

## User Interface
- Simple web UI at /
- Direct question input
- No Swagger interaction needed

Open:
http://localhost:8000

---

## Environment Variables (.env)

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx  
HF_HUB_OFFLINE=1  
TRANSFORMERS_OFFLINE=1  
CHROMA_DB_DIR=data/vectorstore/chroma

Notes:
- Do NOT wrap API key in quotes
- Offline flags prevent repeated downloads

---

## Run Locally (Without Docker)

python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  
uvicorn api.main:app --reload  

Open:
http://127.0.0.1:8000

---

## Docker Deployment

### Build Image
docker build -t medical-agentic-rag .

### Run Container (with cache persistence)
docker run \
  --env-file .env \
  -p 8000:8000 \
  -v chroma_cache:/root/.cache \
  medical-agentic-rag

Open:
http://localhost:8000

---

## Why Docker?
- Same environment everywhere
- Easy deployment
- No dependency issues
- Production ready

---

## Model Downloads
- First run downloads ONNX MiniLM model
- Cache volume prevents re-downloads

---

## Future Enhancements
- Sentence-level citations
- Multi-user memory
- ChatGPT-style UI
- Evaluation metrics
- Cloud deployment

---

## Final Notes
This is a **real Agentic RAG system**, not a demo.
Built with production-grade architecture and extensibility in mind.

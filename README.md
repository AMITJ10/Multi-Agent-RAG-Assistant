APP LINK: https://multi-agent-rag-assistant.streamlit.app/

# Multi-Agent RAG Research Assistant

A production-ready **Multi-Agent Retrieval-Augmented Generation (RAG) Assistant** built with **LangChain, LangGraph, LlamaIndex, CrewAI, ChromaDB, FastAPI, and Streamlit**.

It allows users to upload PDF documents, perform semantic retrieval, and get accurate AI-generated answers using a multi-agent reasoning workflow.

## Live Demo

**Frontend (Streamlit):**
https://multi-agent-rag-assistant.streamlit.app

**Backend API (Render):**
https://multi-agent-rag-assistant.onrender.com

---

## Features

* Upload up to **5 PDF files** (max 10MB each)
* Document parsing and chunking
* RAG-based question answering
* Multi-agent workflow using **LangGraph**
* Retrieval pipeline with **ChromaDB**
* Answer validation with critic agent
* Internet fallback if document answer not found
* Background indexing support
* FastAPI backend deployment
* Streamlit frontend deployment
* Lightweight cloud deployment on Render + Streamlit Cloud

---

## Tech Stack

* Python
* FastAPI
* Streamlit
* LangChain
* LangGraph
* LlamaIndex
* CrewAI
* ChromaDB
* Sentence Transformers
* PyPDF
* Requests

---

## Project Structure

```bash
MULTI_AGENT_RAG_ASSISTANT/
│── app/
│   ├── main.py
│   ├── config.py
│
│── agents/
│   ├── graph.py
│
│── rag/
│   ├── ingest.py
│   ├── retriever.py
│   ├── llamaindex_rag.py
│
│── frontend/
│   ├── streamlit_app.py
│
│── data/
│── vector_db/
│── requirements.txt
│── requirements-backend.txt
│── README.md
```

---

## Run Locally

### Backend

```bash
pip install -r requirements-backend.txt
uvicorn app.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

### Frontend

```bash
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
```

Frontend runs on:

```bash
http://localhost:8501
```

---

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "status": "running"
}
```

---

### Upload Documents

```http
POST /upload
```

Upload PDF files for indexing.

---

### Check Index Status

```http
GET /index-status
```

Returns indexing progress.

---

### Ask Questions

```http
POST /chat
```

Request:

```json
{
  "question": "Who is Amit Jadhav?"
}
```

---

## Deployment

### Streamlit Cloud

Deploy:

```bash
frontend/streamlit_app.py
```

### Render

Build Command:

```bash
pip install -r requirements-backend.txt
```

Start Command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

---

## Future Improvements

* Authentication system
* Multi-user file isolation
* Persistent cloud storage
* Better source ranking
* Streaming responses
* Redis background queue
* Better observability and logging

---

## Author

**Amit Jadhav**
AI/ML Engineer | LLM Engineer | Data Science | RAG | RLHF | Multi-Agent Systems

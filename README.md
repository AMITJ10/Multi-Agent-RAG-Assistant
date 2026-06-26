# Multi-Agent RAG Research Assistant

A production-style AI assistant using LangChain, LangGraph, LlamaIndex, CrewAI, ChromaDB, FastAPI, and Streamlit.

## Features

- PDF/TXT document upload
- RAG-based question answering
- Multi-agent workflow using LangGraph
- API-calling agent
- Critic agent for answer verification
- LlamaIndex RAG option
- CrewAI role-based agent option
- LangSmith tracing
- FastAPI backend
- Streamlit frontend

## Tech Stack

- Python
- LangChain
- LangGraph
- LangSmith
- LlamaIndex
- CrewAI
- ChromaDB
- FastAPI
- Streamlit

## Run Project

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run frontend/streamlit_app.py
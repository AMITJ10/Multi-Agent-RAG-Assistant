import os
import shutil
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from rag.ingest import ingest_files, clear_data_folder
from agents.graph import run_multi_agent_system
from app.config import DATA_DIR, MAX_FILES


app = FastAPI(title="Multi-Agent RAG Assistant")


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Multi-Agent RAG Assistant API is active",
    }


@app.post("/upload")
def upload_files(files: List[UploadFile] = File(...)):
    if len(files) > MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"Upload at most {MAX_FILES} PDFs.",
        )

    clear_data_folder()

    file_paths = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        file_path = os.path.join(DATA_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_paths.append(file_path)

    result = ingest_files(file_paths)

    return result


@app.post("/chat")
def chat(request: ChatRequest):
    result = run_multi_agent_system(request.question)

    return {
        "answer": result.get("final_answer"),
        "next_questions": result.get("next_questions", []),
    }
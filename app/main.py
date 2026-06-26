import os
import shutil
from typing import List
from langsmith import traceable
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from rag.ingest import ingest_files, clear_data_folder
from agents.graph import run_multi_agent_system
from app.config import DATA_DIR, MAX_FILES, MAX_FILE_SIZE_MB


app = FastAPI(title="Multi-Agent RAG Assistant")

indexing_status = {
    "status": "idle",
    "message": "No indexing started.",
}


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/index-status")
def get_index_status():
    return indexing_status


@app.post("/upload")
def upload_files(files: List[UploadFile] = File(...)):
    global indexing_status

    if len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload at most {MAX_FILES} PDFs.")

    clear_data_folder()
    os.makedirs(DATA_DIR, exist_ok=True)

    file_paths = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        content = file.file.read()

        if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"Each file must be under {MAX_FILE_SIZE_MB} MB.",
            )

        file_path = os.path.join(DATA_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        file_paths.append(file_path)

    try:
        indexing_status = {"status": "indexing", "message": "Indexing documents..."}
        result = ingest_files(file_paths)
        indexing_status = {"status": "completed", "message": result["message"]}
        return result

    except Exception as e:
        indexing_status = {"status": "failed", "message": str(e)}
        raise HTTPException(status_code=500, detail=str(e))


@traceable(name="multi_agent_chat")
def traced_multi_agent_run(question: str):
    return run_multi_agent_system(question)


@app.post("/chat")
def chat(request: ChatRequest):
    result = traced_multi_agent_run(request.question)

    return {
        "answer": result.get("final_answer"),
        "next_questions": result.get("next_questions", []),
    }
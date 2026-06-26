import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel

from rag.ingest import ingest_files, clear_data_folder
from agents.graph import run_multi_agent_system
from app.config import DATA_DIR, MAX_FILES


app = FastAPI(title="Multi-Agent RAG Assistant")

indexing_status = {
    "status": "idle",
    "message": "No indexing started."
}


class ChatRequest(BaseModel):
    question: str


def background_index(file_paths):
    global indexing_status

    try:
        indexing_status = {
            "status": "indexing",
            "message": "Indexing documents..."
        }

        result = ingest_files(file_paths)

        indexing_status = {
            "status": "completed",
            "message": result.get("message", "Indexing completed.")
        }

    except Exception as e:
        indexing_status = {
            "status": "failed",
            "message": str(e)
        }


@app.get("/")
def home():
    return {"status": "running"}


@app.get("/index-status")
def get_index_status():
    return indexing_status


@app.post("/upload")
def upload_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    if len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail=f"Upload at most {MAX_FILES} PDFs.")

    clear_data_folder()

    os.makedirs(DATA_DIR, exist_ok=True)
    file_paths = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        file_path = os.path.join(DATA_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_paths.append(file_path)

    background_tasks.add_task(background_index, file_paths)

    return {
        "status": "accepted",
        "message": "Files uploaded. Indexing started in background."
    }


@app.post("/chat")
def chat(request: ChatRequest):
    if indexing_status["status"] == "indexing":
        return {
            "answer": "Documents are still indexing. Please wait a few seconds and try again.",
            "next_questions": []
        }

    result = run_multi_agent_system(request.question)

    return {
        "answer": result.get("final_answer"),
        "next_questions": result.get("next_questions", [])
    }
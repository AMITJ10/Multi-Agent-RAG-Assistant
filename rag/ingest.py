import os
import pickle
import shutil
from typing import List

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer

from app.config import DATA_DIR, INDEX_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def clear_data_folder():
    os.makedirs(DATA_DIR, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(path):
            os.remove(path)


def reset_index():
    if os.path.exists(INDEX_PATH):
        os.remove(INDEX_PATH)


def extract_pdf_text(file_path: str):
    reader = PdfReader(file_path)
    pages = []

    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "text": text,
                "page": page_no,
                "source": os.path.basename(file_path),
            })

    return pages


def chunk_text(text: str):
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def ingest_files(file_paths: List[str]):
    reset_index()

    documents = []
    metadatas = []

    for file_path in file_paths:
        pages = extract_pdf_text(file_path)

        for page in pages:
            chunks = chunk_text(page["text"])

            for chunk in chunks:
                documents.append(chunk)
                metadatas.append({
                    "source": page["source"],
                    "page": page["page"],
                })

    if not documents:
        return {
            "status": "failed",
            "message": "No readable text found in uploaded PDFs.",
            "chunks": 0,
        }

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents)

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    with open(INDEX_PATH, "wb") as f:
        pickle.dump(
            {
                "vectorizer": vectorizer,
                "matrix": matrix,
                "documents": documents,
                "metadatas": metadatas,
            },
            f,
        )

    return {
        "status": "success",
        "message": f"{len(file_paths)} file(s) indexed successfully.",
        "chunks": len(documents),
    }
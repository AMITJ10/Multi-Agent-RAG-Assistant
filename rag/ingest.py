import os
import shutil
from typing import List

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.config import (
    DATA_DIR,
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def clear_data_folder():
    os.makedirs(DATA_DIR, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(path):
            os.remove(path)


def reset_vector_store():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH, ignore_errors=True)


def extract_pdf_pages(file_path: str):
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


def ingest_files(file_paths: List[str]):
    reset_vector_store()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    texts = []
    metadatas = []

    for file_path in file_paths:
        pages = extract_pdf_pages(file_path)

        for page in pages:
            chunks = splitter.split_text(page["text"])

            for chunk in chunks:
                texts.append(chunk)
                metadatas.append({
                    "source": page["source"],
                    "page": page["page"],
                })

    if not texts:
        return {
            "status": "failed",
            "message": "No readable text found in uploaded PDFs.",
            "chunks": 0,
        }

    Chroma.from_texts(
        texts=texts,
        embedding=get_embedding_model(),
        metadatas=metadatas,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
    )

    return {
        "status": "success",
        "message": f"{len(file_paths)} file(s) indexed successfully.",
        "chunks": len(texts),
    }
import os
import pickle

from sklearn.metrics.pairwise import cosine_similarity

from app.config import INDEX_PATH, TOP_K


def load_index():
    if not os.path.exists(INDEX_PATH):
        return None

    with open(INDEX_PATH, "rb") as f:
        return pickle.load(f)


def retrieve_documents(query: str):
    index = load_index()

    if not index:
        return []

    vectorizer = index["vectorizer"]
    matrix = index["matrix"]
    documents = index["documents"]
    metadatas = index["metadatas"]

    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, matrix).flatten()

    ranked_indices = scores.argsort()[::-1][:TOP_K]

    docs = []

    for idx in ranked_indices:
        if scores[idx] <= 0:
            continue

        docs.append({
            "text": documents[idx],
            "source": metadatas[idx].get("source", ""),
            "page": metadatas[idx].get("page", ""),
            "score": float(scores[idx]),
        })

    return docs


def get_all_documents():
    index = load_index()

    if not index:
        return []

    documents = index["documents"]
    metadatas = index["metadatas"]

    return [
        {
            "text": text,
            "source": metadata.get("source", ""),
            "page": metadata.get("page", ""),
        }
        for text, metadata in zip(documents, metadatas)
    ]
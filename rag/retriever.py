from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
)


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def get_vectorstore():
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_model(),
    )


def retrieve_documents(query: str):
    try:
        vectorstore = get_vectorstore()

        results = vectorstore.max_marginal_relevance_search(
            query,
            k=TOP_K,
            fetch_k=20,
        )

        docs = []

        for doc in results:
            docs.append({
                "text": doc.page_content,
                "source": doc.metadata.get("source", ""),
                "page": doc.metadata.get("page", ""),
            })

        return docs

    except Exception:
        return []


def get_all_documents():
    try:
        vectorstore = get_vectorstore()
        data = vectorstore.get()

        docs = []

        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])

        for text, metadata in zip(documents, metadatas):
            docs.append({
                "text": text,
                "source": metadata.get("source", ""),
                "page": metadata.get("page", ""),
            })

        return docs

    except Exception:
        return []
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def build_llamaindex_query_engine(data_dir="data"):
    """
    Builds LlamaIndex query engine from documents in data folder.
    Uses local HuggingFace embeddings.
    """

    Settings.llm = None

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = SimpleDirectoryReader(data_dir).load_data()

    index = VectorStoreIndex.from_documents(documents)

    query_engine = index.as_query_engine()

    return query_engine


def ask_llamaindex(question: str):
    query_engine = build_llamaindex_query_engine()
    response = query_engine.query(question)

    return str(response)


if __name__ == "__main__":
    answer = ask_llamaindex("What is the cricket document about?")
    print(answer)
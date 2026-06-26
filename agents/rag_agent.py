import re
from rag.retriever import retrieve_documents, get_all_documents


def clean_text(text: str):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str):
    return re.split(r"(?<=[.!?])\s+", clean_text(text))


def should_use_all_docs(question: str):
    q = question.lower()
    return any(k in q for k in [
        "summarize", "summary", "overview",
        "resume", "cv", "profile", "candidate",
        "skills", "experience", "education",
        "projects", "who is", "about"
    ])


def answer_from_docs(question: str, docs: list):
    if not docs:
        return ""

    all_text = " ".join([doc["text"] for doc in docs])
    sentences = split_sentences(all_text)

    q = question.lower()

    if "summarize" in q or "summary" in q:
        return " ".join(sentences[:12])

    keywords = [
        w.lower().strip("?.!,")
        for w in question.split()
        if len(w) > 2
    ]

    matched = []

    for sentence in sentences:
        s = sentence.lower()
        score = sum(1 for k in keywords if k in s)

        if score > 0:
            matched.append((score, sentence))

    matched.sort(reverse=True, key=lambda x: x[0])

    if matched:
        return " ".join([s for _, s in matched[:8]])

    if should_use_all_docs(question):
        return " ".join(sentences[:10])

    return ""


def generate_next_questions(question: str):
    return [
        "Can you summarize the uploaded document?",
        "What skills or key points are mentioned?",
        "What projects or important details are mentioned?"
    ]


def rag_agent(state):
    question = state["question"]

    if should_use_all_docs(question):
        docs = get_all_documents()
    else:
        docs = retrieve_documents(question)

    answer = answer_from_docs(question, docs)

    if not answer:
        return {
            "retrieved_docs": [],
            "draft_answer": "",
            "source_found": False,
            "next_questions": generate_next_questions(question),
        }

    return {
        "retrieved_docs": docs,
        "draft_answer": answer,
        "source_found": True,
        "next_questions": generate_next_questions(question),
    }
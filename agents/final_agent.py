from tools.internet_tools import get_internet_answer


def rag_fallback_agent(state):
    question = state["question"]

    return {
        "draft_answer": get_internet_answer(question),
        "source_found": False,
        "next_questions": [
            "Can you explain this in simple words?",
            "Can you give examples?",
            "What are the key points?",
        ],
    }


def internet_agent(state):
    question = state["question"]

    return {
        "draft_answer": get_internet_answer(question),
        "source_found": False,
        "next_questions": [
            "Can you give more details?",
            "Can you summarize this?",
            "Can you compare this with another topic?",
        ],
    }


def final_answer_agent(state):
    answer = state.get("draft_answer", "")

    if not answer:
        answer = "I could not find relevant information."

    return {
        "final_answer": answer,
        "next_questions": state.get("next_questions", []),
    }
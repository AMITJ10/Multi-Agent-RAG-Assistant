def critic_agent(state):
    """
    Critic agent without OpenAI.
    Reviews draft answer using simple rule-based checks.
    """
    question = state.get("question", "")
    draft_answer = state.get("draft_answer", "")

    suggestions = []

    if not draft_answer.strip():
        suggestions.append("Draft answer is empty. Generate an answer first.")

    if len(draft_answer.split()) < 20:
        suggestions.append("Answer may be too short. Add more useful details.")

    if "could not find" in draft_answer.lower():
        suggestions.append("Answer correctly avoids hallucination when context is missing.")

    if question and question.lower() not in draft_answer.lower():
        suggestions.append("Ensure the answer directly addresses the user question.")

    if not suggestions:
        suggestions.append("Answer looks clear, relevant, and safe to use.")

    critique = "\n".join([f"- {item}" for item in suggestions])

    return {"critique": critique}
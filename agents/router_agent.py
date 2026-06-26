def router_agent(state):
    question = state["question"].lower()

    internet_only_keywords = [
        "latest", "today", "current news", "weather",
        "stock price", "live score"
    ]

    if any(k in question for k in internet_only_keywords):
        return {"route": "internet"}

    return {"route": "rag"}
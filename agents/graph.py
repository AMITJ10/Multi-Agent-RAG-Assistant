from langgraph.graph import StateGraph, END

from agents.state import AgentState
from agents.router_agent import router_agent
from agents.rag_agent import rag_agent
from agents.final_agent import (
    rag_fallback_agent,
    internet_agent,
    final_answer_agent,
)


def route_decision(state):
    route = state.get("route")

    if route == "internet":
        return "internet_agent"

    return "rag_agent"


def rag_or_fallback(state):
    if state.get("source_found"):
        return "final_answer_agent"

    return "rag_fallback_agent"


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("router_agent", router_agent)
    workflow.add_node("rag_agent", rag_agent)
    workflow.add_node("rag_fallback_agent", rag_fallback_agent)
    workflow.add_node("internet_agent", internet_agent)
    workflow.add_node("final_answer_agent", final_answer_agent)

    workflow.set_entry_point("router_agent")

    workflow.add_conditional_edges(
        "router_agent",
        route_decision,
        {
            "rag_agent": "rag_agent",
            "internet_agent": "internet_agent",
        },
    )

    workflow.add_conditional_edges(
        "rag_agent",
        rag_or_fallback,
        {
            "final_answer_agent": "final_answer_agent",
            "rag_fallback_agent": "rag_fallback_agent",
        },
    )

    workflow.add_edge("rag_fallback_agent", "final_answer_agent")
    workflow.add_edge("internet_agent", "final_answer_agent")
    workflow.add_edge("final_answer_agent", END)

    return workflow.compile()


agent_graph = build_graph()


def run_multi_agent_system(question: str):
    initial_state = {
        "question": question,
        "route": None,
        "retrieved_docs": None,
        "draft_answer": None,
        "final_answer": None,
        "next_questions": [],
        "source_found": False,
    }

    return agent_graph.invoke(initial_state)
from typing import TypedDict, Optional, List, Dict


class AgentState(TypedDict):
    question: str
    route: Optional[str]
    retrieved_docs: Optional[List[Dict]]
    draft_answer: Optional[str]
    final_answer: Optional[str]
    next_questions: Optional[List[str]]
    source_found: Optional[bool]
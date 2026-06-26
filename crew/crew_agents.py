from crewai import Agent, Task, Crew, Process
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.1",
    temperature=0.2
)


def run_crewai_research(question: str, context: str = ""):
    researcher = Agent(
        role="Research Agent",
        goal="Find useful information related to the user's question",
        backstory="Expert at analyzing documents and extracting key facts.",
        verbose=True,
        llm=llm
    )

    analyst = Agent(
        role="Analysis Agent",
        goal="Analyze the research and create a logical answer",
        backstory="Expert in reasoning and structured explanations.",
        verbose=True,
        llm=llm
    )

    reviewer = Agent(
        role="Review Agent",
        goal="Review the answer for accuracy and clarity",
        backstory="Strict reviewer for factual correctness.",
        verbose=True,
        llm=llm
    )

    research_task = Task(
        description=f"""
Question:
{question}

Context:
{context}

Find the most relevant points.
""",
        expected_output="Important facts and useful information.",
        agent=researcher
    )

    analysis_task = Task(
        description="""
Use the research output to create a clear and useful answer.
""",
        expected_output="A structured answer.",
        agent=analyst
    )

    review_task = Task(
        description="""
Review the answer and improve it if needed.
""",
        expected_output="Final improved answer.",
        agent=reviewer
    )

    crew = Crew(
        agents=[researcher, analyst, reviewer],
        tasks=[research_task, analysis_task, review_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    return result


if __name__ == "__main__":
    result = run_crewai_research(
        question="Explain the Indian Constitution",
        context="The Constitution of India came into effect on 26 January 1950."
    )

    print(result)
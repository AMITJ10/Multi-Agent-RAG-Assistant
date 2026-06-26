from agents.graph import run_multi_agent_system


question = "What is this document mainly about?"

result = run_multi_agent_system(question)

print("\nFinal Answer:\n")
print(result["final_answer"])

print("\nRoute Used:\n")
print(result["route"])
from langgraph_supervisor import create_supervisor

def get_supervisor(llm, research_agent, math_agent, tools):
    prompt = (
        "You are a supervisor managing two agents:\n"
        "- a research agent.Assign research-related tasks to this agent.\n"
        "-a math agent.Assign math-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do Not do any work yourself.\n"
    )

    supervisor = create_supervisor(
        model=llm,
        agents=[research_agent, math_agent],
        tools=tools,
        prompt=prompt,
        add_handoff_back_messages=True,
        output_mode="full_history"
    )
    return supervisor.compile()
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch

def get_research_agent(llm, tavily_api_key: str):
    web_search = TavilySearch(tavily_api_key=tavily_api_key, max_results=3)

    prompt = (
        "You are a research agent.\n\n"
        "INSTRUCTIONS:\n"
        "-Assist Only with research-related tasks, DO NOT do any math\n"
        "-After you're done with your tasks, respond to the supervisor directly\n"
        "-RESPOND ONlY with the results of your work, do NOT include ANY other text"
    )

    research_agent = create_react_agent(
        model=llm,
        tools=[web_search],
        prompt=prompt,
        name="research_agent"
    )
    return research_agent, [web_search]
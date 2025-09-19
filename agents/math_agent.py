from langgraph.prebuilt import create_react_agent

def add(a: float, b: float):
    """Adds two numbers."""
    return a + b

def subtract(a: float, b: float):
    """Substracts two numbers."""
    return a - b

def multiply(a: float, b: float):
    """Multiplies two numbers."""
    return a * b

def divide(a: float, b: float):
    """Divides one number by another."""
    return a / b

def get_math_agent(llm):
    tools = [add, subtract, multiply, divide]
    prompt = (
        "You are a math agent.\n\n"
        "INSTRUCTION:\n"
        "-Assist ONLY with math-related tasks.\n"
        "-After you're done with your tasks, respond to the supervisor directly.\n"
        "-Respond only with the results of your work, do NOT include ANY other text."
    )

    math_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt,
        name="math_agent"
    )
    return math_agent, tools
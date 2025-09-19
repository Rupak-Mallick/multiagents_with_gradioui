# Multi-Agent AI System

A multi-agent system with specialized agents for research and mathematical tasks, coordinated by a supervisor agent.

## Features

- Research Agent: Performs web searches using Tavily API
- Math Agent: Handles mathematical calculations
- Supervisor Agent: Coordinates between specialized agents
- Gradio Web Interface: User-friendly UI for interacting with the system

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd multi-agent-project

2.Install dependencies:
pip install -r requirements.txt

3.Set up environment variables:
Create a .env file in the root directory with your API keys:
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

4.Run the application:
python app.py

5.Open your browser and navigate to http://localhost:7860
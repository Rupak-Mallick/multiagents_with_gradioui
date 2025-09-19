import os
from dotenv import load_dotenv

load_dotenv()

# Get API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY or not TAVILY_API_KEY:
    raise ValueError("Please provide GROQ and TAVILY API keys as environment variables.")
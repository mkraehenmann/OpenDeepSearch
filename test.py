from src.opendeepsearch import OpenDeepSearchTool
from smolagents import CodeAgent, LiteLLMModel
import os
from dotenv import load_dotenv

load_dotenv()

# Using Serper (default)
search_agent = OpenDeepSearchTool(
    model_name="fireworks_ai/accounts/fireworks/models/llama-v3-70b-instruct",
    reranker="jina"
)

# Or using SearXNG
# search_agent = OpenDeepSearchTool(
#     model_name="openrouter/google/gemini-2.0-flash-001",
#     reranker="jina",
#     search_provider="searxng",
#     searxng_instance_url="https://your-searxng-instance.com",
#     searxng_api_key="your-api-key-here"  # Optional
# )

model = LiteLLMModel(
    "fireworks_ai/accounts/fireworks/models/llama-v3-70b-instruct",
    temperature=0.2
)

code_agent = CodeAgent(tools=[search_agent], model=model)
query = "How long would a cheetah at full speed take to run the length of Pont Alexandre III?"
result = code_agent.run(query)

print(result)
from opendeepsearch import OpenDeepSearchTool
from opendeepsearch.wolfram_tool import WolframAlphaTool
from opendeepsearch.prompts import REACT_PROMPT
from opendeepsearch.fact_checker import CodeRunnerTool
from smolagents import LiteLLMModel, ToolCallingAgent, Tool
import os

# Set environment variables for API keys
""" os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"
os.environ["JINA_API_KEY"] = "your-jina-api-key-here"
os.environ["WOLFRAM_ALPHA_APP_ID"] = "your-wolfram-alpha-app-id-here"
os.environ["FIREWORKS_API_KEY"] = "your-fireworks-api-key-here" """

model = LiteLLMModel(
    "fireworks_ai/llama-v3p1-70b-instruct",  # Your Fireworks Deepseek model
    temperature=0.8
)
search_agent = OpenDeepSearchTool(model_name="fireworks_ai/llama-v3p1-70b-instruct", reranker="jina") # Set reranker to "jina" or "infinity"

# Initialize the Wolfram Alpha tool
wolfram_tool = WolframAlphaTool(app_id=os.environ["WOLFRAM_ALPHA_APP_ID"])

code_agent  = CodeRunnerTool()
# Initialize the React Agent with search and wolfram tools
react_agent = ToolCallingAgent(
    tools=[search_agent, code_agent, wolfram_tool],
    model=model,
    prompt_templates=REACT_PROMPT # Using REACT_PROMPT as system prompt
)

# Example query for the React Agent
query = "Write a function that merges two sorted lists into a new sorted list. [1,4,6],[2,3,5] to [1,2,3,4,5,6]. You can do this quicker than concatenating them followed by a sort."
result = react_agent.run(query)

print(result)
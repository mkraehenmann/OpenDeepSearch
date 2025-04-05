from src.opendeepsearch import OpenDeepSearchTool
from src.opendeepsearch.wolfram_tool import WolframAlphaTool
from src.opendeepsearch.prompts import REACT_PROMPT
from smolagents import LiteLLMModel, ToolCallingAgent, Tool
import os
from dotenv import load_dotenv

load_dotenv()




model = LiteLLMModel(
    "fireworks_ai/llama-v3p1-70b-instruct",  # Your Fireworks Deepseek model
    temperature=0.7
)
search_agent = OpenDeepSearchTool(model_name="fireworks_ai/llama-v3p1-70b-instruct", reranker="jina") # Set reranker to "jina" or "infinity"

# Initialize the Wolfram Alpha tool
wolfram_tool = WolframAlphaTool(app_id=os.environ["WOLFRAM_ALPHA_APP_ID"])

# Initialize the React Agent with search and wolfram tools
react_agent = ToolCallingAgent(
    tools=[search_agent, wolfram_tool],
    model=model,
    prompt_templates=REACT_PROMPT # Using REACT_PROMPT as system prompt
)

# Example query for the React Agent
query = "What is the distance, in metres, between the Colosseum in Rome and the Rialto bridge in Venice"
result = react_agent.run(query)

print(result)
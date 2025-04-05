import os
import argparse
from dotenv import load_dotenv

# Import necessary classes from smolagents and opendeepsearch
from smolagents import LiteLLMModel, CodeAgent, GradioUI, PythonInterpreterTool
from opendeepsearch import OpenDeepSearchTool
from opendeepsearch.sparql_wikipedia import WikidataSPARQLTool
from opendeepsearch.wolfram_tool import WolframAlphaTool

# Load environment variables from .env file
load_dotenv()

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Run the OpenDeepSearch demo with integrated tools")
parser.add_argument(
    "--model-name",
    default=os.getenv("LITELLM_SEARCH_MODEL_ID", "openrouter/google/gemini-2.0-flash-001"),
    help="Model name for the search tool"
)
parser.add_argument(
    "--orchestrator-model",
    default=os.getenv("LITELLM_ORCHESTRATOR_MODEL_ID", "openrouter/google/gemini-2.0-flash-001"),
    help="Model name for orchestration"
)
parser.add_argument(
    "--server-port",
    type=int,
    default=7860,
    help="Port for running the Gradio UI"
)
args = parser.parse_args()

# Initialize the primary search tool
search_tool = OpenDeepSearchTool(model_name=args.model_name)


# Initialize the Wikidata SPARQL tool (wikitool) and run its setup
wikidata_tool = WikidataSPARQLTool()
wikidata_tool.setup()

# Initialize the Wolfram Alpha tool with your Wolfram app ID from environment variables.
wolfram_app_id = os.getenv("WOLFRAM_ALPHA_APP_ID", "VYG6TK-W6TJK779HX")
wolfram_tool = WolframAlphaTool(app_id=wolfram_app_id)
# Note: The WolframAlphaTool's forward method initializes its client, so no additional setup is needed.

# Initialize the orchestration model
model = LiteLLMModel(
    model_id=args.orchestrator_model,
    temperature=0.2,
)

# Create the CodeAgent with all the integrated tools
agent = CodeAgent(
    tools=[wolfram_tool, search_tool, wikidata_tool],
    model=model
)

# Launch the Gradio UI
GradioUI(agent).launch(
    server_name="127.0.0.1",
    server_port=args.server_port,
    share=False
)

from smolagents import Tool
import wolframalpha
import json
import os

class WolframAlphaTool(Tool):
    name = "calculate"
    description = """
    Performs computational, mathematical, and factual queries using Wolfram Alpha's computational knowledge engine.
    """
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to send to Wolfram Alpha",
        },
    }
    output_type = "string"

    examples = """
    Task: "Calculate the limit of (1 + 1/x)^x as x approaches infinity."
    Action: { "name": "calculate", "arguments": {"query": "limit (1 + 1/x)^x as x -> infinity"} } 
    Observation: "e" 
    Action: { "name": "final_answer", "arguments": {"answer": "The limit of (1 + 1/x)^x as x approaches infinity is e."} }

    Task: "Evaluate the integral of e^x from 0 to 1."
    Action: { "name": "calculate", "arguments": {"query": "integral of e^x from 0 to 1"} } 
    Observation: "e - 1" 
    Action: { "name": "final_answer", "arguments": {"answer": "The integral of e^x from 0 to 1 is e - 1."} }

    Task: "What is the determinant of the matrix [[1, 2], [3, 4]]?"
    Action: { "name": "calculate", "arguments": {"query": "determinant of [[1, 2], [3, 4]]"} } 
    Observation: "-2" 
    Action: { "name": "final_answer", "arguments": {"answer": "The determinant of the matrix [[1, 2], [3, 4]] is -2."} }

    Task: "Solve the system: x + y = 5 and x - y = 1."
    Action: { "name": "calculate", "arguments": {"query": "solve {x + y = 5, x - y = 1}"} } 
    Observation: "x = 3, y = 2" 
    Action: { "name": "final_answer", "arguments": {"answer": "The solution to the system is x = 3 and y = 2."} }

    Task: "What is the factorial of 7?"
    Action: { "name": "calculate", "arguments": {"query": "7!"} } 
    Observation: "5040" 
    Action: { "name": "final_answer", "arguments": {"answer": "The factorial of 7 is 5040."} }

    Task: "Solve the equation 2^x = 32."
    Action: { "name": "calculate", "arguments": {"query": "solve 2^x = 32"} } 
    Observation: "x = 5" 
    Action: { "name": "final_answer", "arguments": {"answer": "The solution to the equation 2^x = 32 is x = 5."} }

    Task: "Find the inverse of the matrix [[2, 1], [5, 3]]."
    Action: { "name": "calculate", "arguments": {"query": "inverse of [[2, 1], [5, 3]]"} } 
    Observation: "[[3, -1], [-5, 2]]" 
    Action: { "name": "final_answer", "arguments": {"answer": "The inverse of the matrix [[2, 1], [5, 3]] is [[3, -1], [-5, 2]]."} }

    """
    
    def __init__(self, app_id: str):
        super().__init__()
        self.app_id = app_id
    
    def setup(self):
        self.search_tool = WolframAlphaTool(
            self.app_id,
        )
        
    def forward(self, query: str):
            
        # Initialize the Wolfram Alpha client
        self.wolfram_client = wolframalpha.Client(self.app_id)
        
        try:
            # Send the query to Wolfram Alpha
            res = self.wolfram_client.query(query)
            
            # Process the results
            results = []
            for pod in res.pods:
                if pod.title:
                    for subpod in pod.subpods:
                        if subpod.plaintext:
                            results.append({
                                'title': pod.title,
                                'result': subpod.plaintext
                            })
                            
            # Convert results to a JSON-serializable format
            formatted_result = {
                'queryresult': {
                    'success': bool(results),
                    'inputstring': query,
                    'pods': [
                        {
                            'title': result['title'], 
                            'subpods': [{'title': '', 'plaintext': result['result']}]
                        } for result in results
                    ]
                }
            }
            
            # Initialize final_result with a default value
            final_result = "No result found."
            
            # Extract the pods from the query result
            pods = formatted_result.get("queryresult", {}).get("pods", [])
            
            # Loop through pods to find the "Result" title
            for pod in pods:
                if pod.get("title") == "Result":
                    # Extract and return the plaintext from the subpods
                    subpods = pod.get("subpods", [])
                    if subpods:
                        final_result = subpods[0].get("plaintext", "").strip()
                        break
            
            # If no "Result" pod was found, use the first available result
            if final_result == "No result found." and results:
                final_result = results[0]['result']
                
            
            print(f"QUERY: {query}\n\nRESULT: {final_result}")
            return final_result
            
        except Exception as e:
            error_message = f"Error querying Wolfram Alpha: {str(e)}"
            print(error_message)
            return error_message
    
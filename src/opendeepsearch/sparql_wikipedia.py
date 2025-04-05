# Define a dummy Tool base class if smolagents is not installed
try:
    from smolagents import Tool
except ImportError:
    class Tool:
        def __init__(self):
            pass

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import traceback

class WikidataSPARQLTool(Tool):
    name = "wikidata"
    description = """
    Performs structured factual queries on Wikidata using the SPARQL API.
    Provide a SPARQL query to retrieve information from Wikidata.
    """
    inputs = {
        "query": {
            "type": "string",
            "description": "The SPARQL query to send to Wikidata.",
        },
    }
    
    output_type = "string"

    def __init__(self, endpoint: str = "https://query.wikidata.org/sparql"):
        super().__init__()
        self.endpoint = endpoint

    def setup(self):
        # Initialize the SPARQL client and set return format
        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql.setReturnFormat(JSON)

    
    def forward(self, query: str):
        try:
            self.sparql.setQuery(query)
            response = self.sparql.query().convert()
            results = response.get("results", {}).get("bindings", [])
            if not results:
                final_result = "No results found."
            else:
                # If there is exactly one result and it has only one field, return that field's value.
                if len(results) == 1 and len(results[0]) == 1:
                    final_result = next(iter(results[0].values())).get("value", "").strip()
                else:
                    # Otherwise, format each binding as "key: value" pairs and join them into lines.
                    lines = []
                    for binding in results:
                        parts = [f"{key}: {binding[key].get('value', '').strip()}" for key in binding]
                        lines.append(", ".join(parts))
                    final_result = "\n".join(lines)
            print(f"QUERY: {query}\n\nRESULT: {final_result}")
            return final_result
        except Exception as e:
            error_message = f"Error querying Wikidata SPARQL API: {str(e)}"
            print(error_message)
            return error_message
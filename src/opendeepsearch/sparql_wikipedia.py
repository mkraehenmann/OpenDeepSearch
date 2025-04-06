from smolagents import Tool


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

            # First attempt
            if not results:
                print("Initial query returned no results, attempting relaxation...")
                # Try fallback: remove FILTERs or P31 clauses heuristically
                relaxed_query = self._relax_query(query)
                self.sparql.setQuery(relaxed_query)
                response = self.sparql.query().convert()
                results = response.get("results", {}).get("bindings", [])

            if not results:
                final_result = "No results found."
            elif len(results) == 1 and len(results[0]) == 1:
                final_result = next(iter(results[0].values())).get("value", "").strip()
            else:
                lines = []
                for binding in results:
                    parts = [f"{key}: {binding[key].get('value', '').strip()}" for key in binding]
                    lines.append(", ".join(parts))
                final_result = "\n".join(lines)

            print(f"QUERY:\n{query}\n\nRESULT:\n{final_result}")
            return final_result

        except Exception as e:
            error_message = f"Error querying Wikidata SPARQL API: {str(e)}"
            print(error_message)
            return error_message


    def _relax_query(self, query: str) -> str:
        """
        Heuristically relax overly constrained SPARQL queries.
        """
        # Remove FILTERs and P31 constraints (just as examples)
        relaxed = query
        relaxed = '\n'.join(
            line for line in relaxed.splitlines()
            if "FILTER" not in line and "wdt:P31" not in line
        )
        return relaxed

"""
Searcher Node: Executes web and academic searches using the Tavily search API. It takes the generated search queries from the planner node and returns raw search results for the evaluator node to assess.
"""

import os
from dotenv import load_dotenv
from tavily import TavilyClient
from state.research_state import ResearchState

load_dotenv()

def searcher(state: ResearchState) -> dict:
    """
    Execute web and academic searches for all generated queries.

    Args:
        state: Current research state containing search queries.

    Returns:
        dict: Updated state fields with web and academic search results.
    """

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    queries = state["search_queries"]

    web_results = []
    academic_results = []

    for query in queries:
        try:
            web_result = client.search(query=query, search_depth="basic")
            web_results.append({"query": query, "results": web_result})
        except Exception as e:
            print(f"Web search failed for '{query}': {e}") 

        try:
            academic_result = client.search(query=f"academic research: {query}", search_depth="advanced")
            academic_results.append({"query": query, "results": academic_result})
            
        except Exception as e:
            print(f"Academic search failed for '{query}': {e}")

    return {
        "web_results": web_results,
        "academic_results": academic_results,
    }

#Code for unit testing the function
if __name__ == "__main__":
    test_state: ResearchState = {
        "topic": "The impact of AI on journalism",
        "depth": "quick",
        "search_queries": [
            "AI tools and applications in journalism",
            "Impact of artificial intelligence on journalism jobs",
            "Ethical implications of AI in news reporting"
        ],
        "web_results": None,
        "academic_results": None,
        "evaluated_sources": None,
        "should_search_more": None,
        "report": None,
        "output_format": "markdown",
        "output_path": None
    }

    result = searcher(test_state)
    print(f"Web results: {len(result['web_results'])} found")
    print(f"Academic results: {len(result['academic_results'])} found")
    print(f"\nFirst web result: {result['web_results'][0] if result['web_results'] else 'None'}")
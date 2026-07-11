"""
Planner Node: The first node in the Scoute research graph. It takes the research topic and depth level from the Research State and generates targeted search queries for the searcher node to execute.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.templates import PLANNER_PROMPT
from state.research_state import ResearchState

load_dotenv()

def planner(state: ResearchState) -> dict:
    """
    Generate search queries based on topic and depth.

    Args:
        state: Current research state containing topic and depth.

    Returns:
        dict: Updated state fields with generated search queries.
    """

    prompt = PLANNER_PROMPT.format(
        topic=state["topic"],
        depth=state["depth"]
    )
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
        response = llm.invoke(prompt)
        content = response.content
        if isinstance(content, list):
            content = content[0].get('text', '') if isinstance(content[0], dict) else str(content[0])
        # Split the response into lines and strip numbering (e.g. "1. ", "2. ") so each query is a clean string with no leading digits or dots
        search_queries = [
            q.strip().lstrip("0123456789. ")
            for q in content.strip().split('\n')
            if q.strip()
        ]
        return {
            "search_queries": search_queries
        }
    except Exception as e:
        print(f"Error in planner: {e}")
        return {
            "search_queries": []
            }

#Code for unit testing the function
if __name__ == "__main__":
    test_state: ResearchState = {
        "topic": "The impact of AI on journalism",
        "depth": "quick",
        "search_queries": None,
        "web_results": None,
        "academic_results": None,
        "evaluated_sources": None,
        "should_search_more": None,
        "report": None,
        "output_format": "markdown",
        "output_path": None
    }

    result = planner(test_state)
    print("Generated search queries:")
    for query in result["search_queries"]:
        print(f"  - {query}")
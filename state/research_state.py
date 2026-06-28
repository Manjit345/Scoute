"""
Research State: Define the shared structure that flows through the graph. TypedDict is used as LangGraph has native dictionary-based state management between nodes.
"""

from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    """
    Shared state object passed between all nodes in the research graph.
    """
    topic: str
    depth: str
    search_queries: Optional[List[str]]
    web_results: Optional[List[dict]]
    academic_results: Optional[List[dict]]
    evaluated_sources: Optional[List[dict]]
    should_search_more: Optional[bool]
    report: Optional[str]
    output_format: str
    output_path: Optional[str]

if __name__ == "__main__":
    state: ResearchState = {
        "topic": "The impact of AI on journalism",
        "depth": "quick",
        "search_queries": None,
        "web_results": None,
        "academic_results": None,
        "evaluated_sources": None,
        "should_search_more": None,
        "report": None,
        "output_format": "pdf",
        "output_path": None
    }
    print(state)
    print(f"Topic: {state['topic']}")
    print(f"Depth: {state['depth']}")
    
"""
Research Graph: Assembles all the Scoute nodes into a LangGraph state graph. It defines the flow of execution of the whole project.
"""

from langgraph.graph import StateGraph, END
from state.research_state import ResearchState
from nodes.planner import planner
from nodes.searcher import searcher
from nodes.evaluator import evaluator
from nodes.synthesizer import synthesizer
from nodes.formatter import formatter

def should_continue_searching(state: ResearchState) -> str:
    """
    Conditional edge function — decides whether to search again or synthesize.
    
    Returns:
        'search' if more searching is needed, 'synthesize' if ready to write report.
    """
    
    if state["should_search_more"]:
        return "search"
    return "synthesize"

def build_graph():
    """
    Build and compile the Scoute research graph.
    
    Returns:
        Compiled LangGraph graph ready for execution.
    """

    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner)
    graph.add_node("searcher", searcher)
    graph.add_node("evaluator", evaluator)
    graph.add_node("synthesizer", synthesizer)
    graph.add_node("formatter", formatter)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "evaluator")

    graph.add_conditional_edges(
        "evaluator",
        should_continue_searching,
        {
            "search": "searcher",
            "synthesize": "synthesizer"
        }
    )

    graph.add_edge("synthesizer", "formatter")
    graph.add_edge("formatter", END)

    return graph.compile()

research_graph = build_graph()

#Code for unit testing the graph
if __name__ == "__main__":
    initial_state: ResearchState = {
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

    result = research_graph.invoke(initial_state)
    print(f"Report generated: {len(result['report'])} characters")
    print(f"Output saved to: {result['output_path']}")
    print(f"\nReport preview:")
    print(result['report'][:500])
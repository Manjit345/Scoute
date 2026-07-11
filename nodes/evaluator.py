"""
Evaluator Node: Scores and filters search results based on relevance and credibility. It takes raw web and academic results from the searcher node and returns only the highest quality sources for the synthesizer node to use.
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.templates import EVALUATOR_PROMPT
from state.research_state import ResearchState

load_dotenv()

# This schema is for a single source's score which enforces that the LLM returns exactly these fields in these types, nothing more, nothing less
class SourceScore(BaseModel):
    source_number: int
    relevance_score: int
    credibility_score: int
    combined_score: float
    reasoning: str

# This schema is for a list of SourceScore objects that the LLM returns
class EvaluationResult(BaseModel):
    scores: List[SourceScore]

def evaluator(state: ResearchState) -> dict:
    """
    Scores and filters search results by relevance and credibility.

    Args:
        state: Current research state containing web and academic results.

    Returns:
        dict: Updated state fields with evaluated and filtered sources.
    """

    llm = ChatGoogleGenerativeAI(
        model = "gemini-3.5-flash",
        google_api_key = os.getenv("GEMINI_API_KEY"),
        temperature = 0.3
    )

    # Tavily returns results nested per-query. Flatten everything into one single list so it can be evaluated and indexed together
    all_sources = []

    for item in state["web_results"]:
        for result in item["results"]["results"]:
            all_sources.append({
                "title": result["title"],
                "url": result["url"],
                "content": result["content"][:500],
                "type": "web"
            })
    
    for item in state["academic_results"]:
        for result in item["results"]["results"]:
            all_sources.append({
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
                "type": "academic"
            })
    # Build a numbered, readable list of sources for the LLM to evaluate.
    sources_text = ""
    for i, source in enumerate(all_sources, 1):
        sources_text += f"{i}. [{source['type'].upper()}] {source['title']}\n"
        sources_text += f"   URL: {source['url']}\n"
        sources_text += f"   Content: {source['content']}\n\n"
    
    prompt = EVALUATOR_PROMPT.format(
        topic = state["topic"],
        sources = sources_text
    )

    try:
        # with_structured_output forces Gemini to return data matching the EvaluationResult schema instead of free-form text
        structured_llm = llm.with_structured_output(EvaluationResult)
        evaluation = structured_llm.invoke(prompt)
    
        # We will attach each returned score back to its original source using source_number to find the right index
        scored_sources = []
        for score_item in evaluation.scores:
            idx = score_item.source_number - 1 # convert LLM's 1-based numbering to Python's 0-based index
            if idx < len(all_sources):
                source = all_sources[idx]
                source["combined_score"] = score_item.combined_score
                scored_sources.append(source)
        
        filtered_sources = [s for s in scored_sources if s["combined_score"] >= 6]
        
        # If a deep-dive research request didn't yield enough quality sources, signal that another search round is needed
        should_search_more = len(filtered_sources) < 3 and state["depth"] == "deep"
        
        return {
            "evaluated_sources": filtered_sources,
            "should_search_more": should_search_more
        }
    
    except Exception as e:
        print(f"Error in evaluator: {e}")
        return {
            "evaluated_sources": all_sources,
            "should_search_more": False
        }
        
#Code for unit testing the function
if __name__ == "__main__":
    from nodes.searcher import searcher

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

    search_result = searcher(test_state)
    test_state["web_results"] = search_result["web_results"]
    test_state["academic_results"] = search_result["academic_results"]

    result = evaluator(test_state)
    print(f"Evaluated sources: {len(result['evaluated_sources'])} total")
    print(f"Should search more: {result['should_search_more']}")
    if result['evaluated_sources']:
        print(f"\nFirst source: {result['evaluated_sources'][0]['title']}")
        print(f"Score: {result['evaluated_sources'][0]['combined_score']}")
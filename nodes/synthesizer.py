"""
Synthesizer Node: Writes the final research report using the evaluated sources filtered using the evaluator node.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.templates import SYNTHESIZER_PROMPT
from state.research_state import ResearchState

load_dotenv()

def synthesizer(state: ResearchState) -> dict:
    """
    Generate the final research report from evaluated sources.

    Args:
        state: Current research state containing evaluated sources, topic, and depth.

    Returns:
        dict: Updated state fields with the synthesized report text.
    """

    llm = ChatGoogleGenerativeAI(
        model = "gemini-3.5-flash",
        google_api_key = os.getenv("GEMINI_API_KEY"),
        temperature = 0.5
    )

    # We are formatting evaluated sources into readable text for the prompt, and the sources are being numbered so that the LLM can cite them as [Source N]
    sources_text = ""
    for i, source in enumerate(state["evaluated_sources"], 1):
        sources_text += f"[Source {i}] {source["title"]}\n"
        sources_text += f"URL: {source["url"]}\n"
        sources_text += f"Content: {source['content']}\n\n"

    prompt = SYNTHESIZER_PROMPT.format(
        topic = state['topic'],
        depth = state['depth'],
        sources = sources_text
    )
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        if isinstance(content, list):
            content = content[0].get('text', '') if isinstance(content[0], dict) else str(content[0])
        return {
            "report": content
        }
    except Exception as e:
        print(f"Error in synthesizer: {e}")
        return{
            "report": "Report generation failed. Please try again."
        }

#Code for unit testing the function
if __name__ == "__main__":
    test_state: ResearchState = {
        "topic": "The impact of AI on journalism",
        "depth": "quick",
        "search_queries": None,
        "web_results": None,
        "academic_results": None,
        "evaluated_sources": [
            {
                "title": "AI Tools for Journalists",
                "url": "https://example.com/article1",
                "content": "AI tools are transforming how journalists conduct research, fact-check claims, and draft articles. Major newsrooms now use AI for transcription and summarization.",
                "type": "web",
                "combined_score": 8.5
            },
            {
                "title": "Ethics of AI in News Reporting",
                "url": "https://example.com/article2",
                "content": "Concerns around AI-generated content include accuracy, bias, and transparency. News organizations are developing guidelines for responsible AI use.",
                "type": "academic",
                "combined_score": 9.0
            }
        ],
        "should_search_more": False,
        "report": None,
        "output_format": "markdown",
        "output_path": None
    }

    result = synthesizer(test_state)
    print("Generated Report:")
    print(result["report"])
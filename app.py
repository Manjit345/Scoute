"""
App: Streamlit frontend for Scoute. It handles the user input, triggers the research graph, displays the report, and provides a download button for the generated file.
"""

import streamlit as st
import os
from graph.research_graph import research_graph

def initialize_session_state():
    """Initialize session state variables."""
    if "research_complete" not in st.session_state:
        st.session_state.research_complete = False
    if "result" not in st.session_state:
        st.session_state.result = None

def main():
    st.title("Scoute")
    st.write("Your AI-powered research agent. Enter a topic and get a structured report in minutes.")

    initialize_session_state()

    st.subheader("Research Settings")
    topic = st.text_input("What do you want to research?", placeholder="e.g. The impact of AI on journalism")
    
    depth = st.radio(
        "Research depth",
        options=["quick", "deep"],
        format_func=lambda x: "Quick Overview (3 queries)" if x == "quick" else "Deep Dive (7 queries)",
        horizontal=True
    )

    output_format = st.selectbox(
        "Output format",
        options=["markdown", "pdf", "docx"],
        format_func=lambda x: {"markdown": "Markdown (.md)", "pdf": "PDF (.pdf)", "docx": "Word Document (.docx)"}[x]
    )

    if st.button("Start Research"):
        if not topic.strip():
            st.error("Please enter a research topic.")
            st.stop()

        with st.spinner("Researching... this may take a minute."):
            try:
                initial_state = {
                    "topic": topic,
                    "depth": depth,
                    "search_queries": None,
                    "web_results": None,
                    "academic_results": None,
                    "evaluated_sources": None,
                    "should_search_more": None,
                    "report": None,
                    "output_format": output_format,
                    "output_path": None
                }
                st.session_state.result = research_graph.invoke(initial_state)
                st.session_state.research_complete = True
            except Exception as e:
                st.error("Research failed. Please try again later.")
                st.stop()

    if st.session_state.research_complete and st.session_state.result:
        result = st.session_state.result

        st.subheader("Research Report")
        st.markdown(result["report"])

        if result["output_path"] and os.path.exists(result["output_path"]):
            with open(result["output_path"], "rb") as f:
                file_bytes = f.read()

            st.download_button(
                label=f"Download Report ({output_format.upper()})",
                data=file_bytes,
                file_name=os.path.basename(result["output_path"]),
                mime={
                    "markdown": "text/markdown",
                    "pdf": "application/pdf",
                    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }[output_format]
            )

if __name__ == "__main__":
    main()
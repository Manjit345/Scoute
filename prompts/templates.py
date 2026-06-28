"""
Prompt Templates: This module is a centralized storage for all LLM prompts used in the application.
"""

PLANNER_PROMPT = """You are a research planning assistant. Generate search queries for the following topic.

Topic: {topic}
Research Depth: {depth}

Rules:
- If depth is "quick": generate exactly 3 broad search queries covering the main aspects of the topic
- If depth is "deep": generate exactly 7 search queries covering multiple specific angles, subtopics, and perspectives

Return only a numbered list of search queries, nothing else."""

EVALUATOR_PROMPT = """You are a research quality evaluator. Rate each search result below for relevance and credibility.

Topic: {topic}

Search Results:
{sources}

For each result, provide:
- A relevance score (1-10): how directly relevant is it to the topic?
- A credibility score (1-10): how trustworthy is the source?
- A combined score (average of both)
- One sentence explaining your rating

Return results as a numbered list matching the input order."""

SYNTHESIZER_PROMPT = """You are an expert research writer. Write a comprehensive research report using the sources provided below.

Topic: {topic}
Depth: {depth}

Structure:
- If depth is "quick": Executive Summary, Key Findings, Conclusion, Sources Cited
- If depth is "deep": Executive Summary, Background, Key Findings (with subsections per angle), Analysis, Conclusion, Sources Cited

Sources:
{sources}

Rules:
- Cite sources inline using [Source N] notation
- List all sources in the Sources Cited section
- Match report length to depth — quick should be concise, deep should be thorough
- Return only the final report text, no preamble"""
# Scoute — AI Research Agent

## Overview
Imagine there is a student starting an essay but they have to spend an hour or two figuring out what they don't know yet. A Youtuber or any other form of content creator making a video, blog etc... on a topic outside of their expertise has to go through a ton of resources before they can finish their script. A journalist who has an interview in two hours and they need to cover an unfamiliar topic by that time. A startup founder who needs to research a new market and synthesize competitor analysis, industry trends, and customer behavior all at once.
These are people with different goals but all of them have a problem in common. All of them want to turn a vague topic into structured, usable knowledge which will take the time they don't have. So, here I present Scoute which is an AI-powered research agent that can solve all of these scenarios in minutes.

## How It Works
You have to provide a topic you want to research about and select the depth you want to choose between "quick" and "deep". Once you click on Start Research, the topic goes to an LLM where it generates search queries around the topic. 3 in case of "quick" and 7 for "deep". Then, the agent searches the topic using those search queries once for general web results and once for more authorative academic/news sources. For each query it gets back a result of title, URL and content snippet. The agent then send these sources to the LLM which evaluates each of these sources on a scale of 0 to 10 for relevance and credibility combined. Sources with a score below 6 are filtered out. Next, the agent synthesizes the remaining sources into a structured report with the sections: 
- Executive Summary
- Key Findings
- Conclusion
- Sources Cited
  
  for a quick search and a longer report with extra sections:

- Background
- Analysis
  
  for a deep search.
  
And at last, the agent gives you the report along with an option to download the report as PDF, DOCX or Markdown.

## Agent Architecture
Scoute is built using LangGraph which is a framework for building stateful, multi-step AI agents. The research pipeline is a directed graph where each node handles one specific job:

| Node | Role |
|------|------|
| Planner | Breaks your topic into targeted search queries based on depth |
| Searcher | Executes web and academic searches via Tavily for each query |
| Evaluator | Scores every source for relevance and credibility, filters out noise |
| Synthesizer | Writes a structured report with inline citations from top sources |
| Formatter | Converts the report into your chosen format amongst PDF, DOCX, or Markdown |

The graph also includes a conditional loop where, if a deep-dive research request doesn't yield enough quality sources after the first search round, the agent automatically searches again before writing the report.

## Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Tavily](https://img.shields.io/badge/Tavily-000000?style=for-the-badge&logo=googlesearchconsole&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## How to Run
Use this link: [Scoute](https://scoute-amujof2suntmkewhthj3jk.streamlit.app/)

To run locally:
1. Clone the repository: `git clone https://github.com/Manjit345/Scoute.git`
2. Navigate to the project: `cd scoute`
3. Install uv if you haven't by following this: [Astral Docs](https://docs.astral.sh/uv/)
4. Install dependencies: `uv sync`
5. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```
6. Run the app: `streamlit run app.py`

## Project Structure
```
scoute/
├── app.py                  # Streamlit frontend
├── graph/
│   └── research_graph.py   # LangGraph graph definition and compilation
├── nodes/
│   ├── planner.py          # Generates search queries from topic and depth
│   ├── searcher.py         # Executes web and academic searches via Tavily
│   ├── evaluator.py        # Scores and filters sources using structured output
│   ├── synthesizer.py      # Writes structured report with citations
│   └── formatter.py        # Converts report to PDF, DOCX, or Markdown
├── state/
│   └── research_state.py   # ResearchState TypedDict — shared state across nodes
├── prompts/
│   └── templates.py        # Centralized LLM prompt templates
├── pyproject.toml          # uv dependency management
└── uv.lock                 # Locked dependency versions
```

## Notes

### Output Quality
The quality of the output depends on a lot of factors:
- The more broad the topic is, the more wide but shallow report will be generated. However, on the other hand, the more specific the topic is, the more focused and useful is the report.
- Do not expect the "deep" depth to produce a better report. It just generates more queries and looks for more sources. If there are lots of higher quality sources for your topic, then it will fetch more of them.
- Even though the sources scoring below 6 are filtered out, keep in mind that it is the LLM which scores these sources and it is not infallible. It is very possible that a relevant resource might get filtered out or an irrelevant may make it through.
- The sources cited and the URLs attached to them are real but they are not verified. The agent does not fully read each of them but works on Tavily's content snippets. It is suggested to verify critical claims if you are using the agent as a part of publishing any of your work.

### API Usage
This project is a demo and runs on the Gemini's free tier which has got a daily request limit. Along with that, it also runs on Tavily's free researcher plan which has got a monthly limit. If the limit of the live demo is exhausted, then it will throw an error asking you to try again later.

## Future Improvements
- Support for custom output templates so that user can have the sections as per their choice
- Persistent research history across sessions incase user wants to retain their report without downloading
- Expand the export options such as Notion or Google Docs

## License
This project is open-source and available under the MIT License.

## Contact
For issues or questions, please open a GitHub issue.

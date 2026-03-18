import os
from typing import List
from pydantic import BaseModel
import arxiv
import textwrap
from agno.agent import Agent
from agno.tools import tool
from agno.tools.arxiv import ArxivTools
from dotenv import load_dotenv
load_dotenv()

# ---------- 1. Data model ----------
class Paper(BaseModel):
    title: str
    pdf_url: str
    summary: str   # abstract

# ---------- 2. Tool ----------
arxiv_tools = ArxivTools(
            enable_search_arxiv=True,
            enable_read_arxiv_papers=False
            )

# ---------- 3. Agent ----------
arxiv_researcher = Agent(
    name="ArxivDigest",
    model="openai:gpt-4.1",          # or gpt-3.5-turbo
    tools=[arxiv_tools],
    description=(
        "You are an AI literature analyst. "
        "Use the search_arxiv tool to find relevant papers. "
        "Then write a concise markdown report: "
        "1. User query 2. Number of papers found 3. For each paper: "
        "**Title**, PDF_URL, and a 2-3 sentence plain-English summary."
    ),
    markdown=True
)

# ---------- 4. Run ----------
if __name__ == "__main__":
    topic = input("Topic? > ") or "large language model reasoning"
    report = arxiv_researcher.run(f"Produce an arXiv digest on: {topic}")
    print(report)
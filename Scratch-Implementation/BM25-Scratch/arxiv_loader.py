import arxiv
import os

def fetch_arxiv_titles(query="cs.AI", max_results=200):
    search = arxiv.Search(
        query=f"cat:{query}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    client = arxiv.Client()
    titles = []

    for result in client.results(search):
        titles.append(result.title.replace("\n", " ").strip())

    return titles


if __name__ == "__main__":
    titles = fetch_arxiv_titles("cs.AI", 200)

    # ensure data directory exists
    os.makedirs("data", exist_ok=True)

    with open("data/arxiv_titles.txt", "w", encoding="utf-8") as f:
        for t in titles:
            f.write(t + "\n")

    print(f"Saved {len(titles)} arXiv titles")

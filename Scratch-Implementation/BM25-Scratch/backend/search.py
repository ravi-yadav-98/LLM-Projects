from .bm25 import BM25
import os

def load_documents(path="data/arxiv_titles.txt"):
    # Handle both relative paths from backend/ and root
    if not os.path.exists(path):
        path = "../data/arxiv_titles.txt"
    
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

documents = load_documents()
bm25 = BM25(documents)

def search(query, k=5):
    results = bm25.rank(query)
    return results[:k]
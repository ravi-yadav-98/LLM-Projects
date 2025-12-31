from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .search import search

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_api(query: str, k: int = 50):
    results = search(query, k)
    # Filter results with score > 0
    filtered_results = [
        {"title": doc, "score": round(score, 4)}
        for doc, score in results if score > 0
    ]
    return filtered_results
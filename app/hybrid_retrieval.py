from app.retrieval import search_documents
from app.bm25_search import bm25_search


def hybrid_search(query: str, top_k: int = 3) -> str:
    vector_results = search_documents(query, limit=top_k)
    bm25_results = bm25_search(query, top_k=top_k)

    combined = []

    for item in bm25_results + vector_results:
        if item not in combined:
            combined.append(item)

    if not combined:
        return "No relevant context found."

    return "\n".join(combined[:top_k])
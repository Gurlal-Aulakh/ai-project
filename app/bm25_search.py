from rank_bm25 import BM25Okapi

DOCS = [
    "MCP stands for Model Context Protocol and is used to connect AI agents to external tools.",
    "This project uses MCP to integrate external tools with the main agent.",
    "Qdrant is used as a vector database for semantic search.",
    "Redis is used for caching and semantic cache.",
    "Neo4j is used as a graph database for relationships.",
]

TOKENIZED_DOCS = [doc.lower().split() for doc in DOCS]
bm25 = BM25Okapi(TOKENIZED_DOCS)


def bm25_search(query: str, top_k: int = 3) -> list[str]:
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(DOCS, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        doc
        for doc, score in ranked[:top_k]
        if score > 0
    ]
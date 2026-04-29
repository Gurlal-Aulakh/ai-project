import os
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from app.config import get_settings


settings = get_settings()


COLLECTION_NAME = settings.qdrant_collection_name
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# client = QdrantClient(":memory:")

client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
)
embedding_model = TextEmbedding(model_name=MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = list(embedding_model.embed(texts))
    return [embedding.tolist() for embedding in embeddings]


def setup_collection() -> None:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE,
        ),
    )


def seed_documents() -> None:
    docs = [
        "MCP is a protocol that lets AI systems connect to tools and resources.",
        "Vector databases store embeddings for semantic search.",
        "Redis is often used for fast caching in AI applications.",
        "Prompt versioning helps you test and improve prompts safely.",
        "This project is an AI assistant built using a main agent and worker agents.",
        "It uses Qdrant as a vector database for semantic search.",
        "Redis is used for caching responses.",
        "MCP is used to connect to external tools.",
        "The system uses prompt versioning to improve agent instructions.",
        "MCP stands for Model Context Protocol and connects AI agents to external tools.",
    ]

    vectors = embed_texts(docs)

    points = [
        models.PointStruct(
            id=i + 1,
            vector=vectors[i],
            payload={"document": docs[i]},
        )
        for i in range(len(docs))
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


def search_documents(query: str, limit: int = 3) -> list[str]:
    query_vector = embed_texts([query])[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    ).points

    return [
        point.payload["document"]
        for point in results
        if point.payload and "document" in point.payload
    ]
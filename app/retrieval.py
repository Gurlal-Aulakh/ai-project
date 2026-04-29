import os
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from app.config import get_settings

settings = get_settings()

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "ai_project_docs")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Use Qdrant Cloud if env variables exist, otherwise use local in-memory Qdrant
if settings.qdrant_url and settings.qdrant_api_key:
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
else:
    client = QdrantClient(":memory:")

embedding_model = TextEmbedding(model_name=MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = list(embedding_model.embed(texts))
    return [embedding.tolist() for embedding in embeddings]


def setup_collection() -> None:
    existing_collections = [
        collection.name
        for collection in client.get_collections().collections
    ]

    if COLLECTION_NAME not in existing_collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            ),
        )

        seed_documents()


def seed_documents() -> None:
    docs = [
        "This project is an AI assistant built using a main agent and worker agents.",
        "MCP stands for Model Context Protocol and connects AI agents to external tools.",
        "The project uses Qdrant as a vector database for semantic search.",
        "Redis is used for caching responses and improving performance.",
        "Prompt versioning is used to manage and improve agent instructions.",
        "BM25 is used for keyword search and combined with vector search for hybrid retrieval.",
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
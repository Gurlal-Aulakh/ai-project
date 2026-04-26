from redisvl.extensions.cache.llm import SemanticCache
from redisvl.utils.vectorize import HFTextVectorizer

from app.config import get_settings

settings = get_settings()

semantic_cache = SemanticCache(
    name="ai_project_semantic_cache",
    redis_url=settings.redis_url,
    distance_threshold=0.15,
    vectorizer=HFTextVectorizer("redis/langcache-embed-v1"),
)


def check_semantic_cache(question: str, filters: dict | None = None) -> str | None:
    results = semantic_cache.check(
    prompt=question,
    return_fields=["prompt", "response", "metadata"],
)

    if not results:
        return None

    best_match = results[0]
    return best_match["response"]


def save_semantic_cache(question: str, answer: str, metadata: dict | None = None) -> None:
    semantic_cache.store(
        prompt=question,
        response=answer,
        metadata=metadata or {
            "source": "main_agent",
            "cache_type": "semantic",
        },
    )
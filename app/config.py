from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    openai_api_key: str
    redis_url: str = "redis://localhost:6379/0"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "password123"
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection_name: str = "ai_project_docs"

def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_username=os.getenv("NEO4J_USERNAME", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "password123"),
        qdrant_url=os.getenv("QDRANT_URL", ""),
        qdrant_api_key=os.getenv("QDRANT_API_KEY", ""),
        qdrant_collection_name=os.getenv("QDRANT_COLLECTION_NAME", "ai_project_docs"),
    )
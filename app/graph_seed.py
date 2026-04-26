from app.graph_db import run_write_query


def seed_project_graph() -> None:
    query = """
    MERGE (project:Project {name: "AI Project G"})

    MERGE (main:Agent {name: "MainAgent"})
    MERGE (concept:Agent {name: "ConceptExplainerAgent"})
    MERGE (projectAgent:Agent {name: "ProjectGuideAgent"})

    MERGE (qdrant:Technology {name: "Qdrant"})
    MERGE (redis:Technology {name: "Redis"})
    MERGE (mcp:Technology {name: "MCP"})
    MERGE (openai:Technology {name: "OpenAI Agents SDK"})
    MERGE (neo4j:Technology {name: "Neo4j"})

    MERGE (memory:Component {name: "LongTermMemory"})
    MERGE (semanticCache:Component {name: "SemanticCache"})
    MERGE (vectorDb:Component {name: "VectorDatabase"})
    MERGE (graphDb:Component {name: "GraphDatabase"})

    MERGE (project)-[:HAS_AGENT]->(main)
    MERGE (project)-[:HAS_AGENT]->(concept)
    MERGE (project)-[:HAS_AGENT]->(projectAgent)

    MERGE (main)-[:CALLS]->(concept)
    MERGE (main)-[:CALLS]->(projectAgent)

    MERGE (main)-[:USES]->(memory)
    MERGE (main)-[:USES]->(semanticCache)
    MERGE (main)-[:USES]->(vectorDb)
    MERGE (main)-[:USES]->(graphDb)

    MERGE (vectorDb)-[:IMPLEMENTED_WITH]->(qdrant)
    MERGE (semanticCache)-[:IMPLEMENTED_WITH]->(redis)
    MERGE (memory)-[:STORED_IN]->(redis)
    MERGE (graphDb)-[:IMPLEMENTED_WITH]->(neo4j)
    MERGE (main)-[:BUILT_WITH]->(openai)
    MERGE (main)-[:CONNECTS_TO_TOOLS_USING]->(mcp)
    """

    run_write_query(query)
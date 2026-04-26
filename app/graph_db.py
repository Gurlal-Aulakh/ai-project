from neo4j import GraphDatabase
from app.config import get_settings

settings = get_settings()

driver = GraphDatabase.driver(
    settings.neo4j_uri,
    auth=(settings.neo4j_username, settings.neo4j_password),
)


def close_graph_driver() -> None:
    driver.close()


def run_write_query(query: str, parameters: dict | None = None) -> None:
    with driver.session() as session:
        session.execute_write(
            lambda tx: tx.run(query, parameters or {}).consume()
        )


def run_read_query(query: str, parameters: dict | None = None) -> list[dict]:
    with driver.session() as session:
        result = session.execute_read(
            lambda tx: list(tx.run(query, parameters or {}))
        )

    return [record.data() for record in result]

def get_project_relationships() -> str:
    query = """
    MATCH (a)-[r]->(b)
    RETURN a.name AS source, type(r) AS relationship, b.name AS target
    LIMIT 50
    """

    rows = run_read_query(query)

    if not rows:
        return "No graph relationships found."

    return "\n".join(
        f"{row['source']} -[{row['relationship']}]-> {row['target']}"
        for row in rows
    )


def get_entity_relationships(entity_name: str) -> str:
    query = """
    MATCH (a {name: $entity_name})-[r]-(b)
    RETURN a.name AS source, type(r) AS relationship, b.name AS target
    LIMIT 30
    """

    rows = run_read_query(query, {"entity_name": entity_name})

    if not rows:
        return f"No relationships found for {entity_name}."

    return "\n".join(
        f"{row['source']} -[{row['relationship']}]- {row['target']}"
        for row in rows
    )
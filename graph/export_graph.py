"""
Export graph data from Neo4j for GNN training.
"""

from graph.connection import get_connection, close_connection
import structlog

logger = structlog.get_logger(__name__)


def export_nodes(conn):
    """Export all nodes."""
    
    query = """
    MATCH (n)
    RETURN id(n) AS node_id, labels(n) AS labels, properties(n) AS props
    """

    nodes = conn.execute_query(query)

    logger.info("Exported nodes", count=len(nodes))
    return nodes


def export_edges(conn):
    """Export all relationships."""

    query = """
    MATCH (a)-[r]->(b)
    RETURN
        id(a) AS source,
        id(b) AS target,
        type(r) AS type,
        properties(r) AS props
    """

    edges = conn.execute_query(query)

    logger.info("Exported edges", count=len(edges))
    return edges


def main():

    conn = get_connection()

    try:

        nodes = export_nodes(conn)
        edges = export_edges(conn)

        print("\nNodes:", len(nodes))
        print("Edges:", len(edges))

        # Print small sample
        print("\nSample Node:", nodes[0])
        print("\nSample Edge:", edges[0])

    finally:
        close_connection()


if __name__ == "__main__":
    main()
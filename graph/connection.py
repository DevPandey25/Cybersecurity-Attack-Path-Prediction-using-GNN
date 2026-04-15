"""
Neo4j connection management and database operations.
"""

import os
from typing import Optional, Dict, Any, List
from neo4j import GraphDatabase
import structlog

logger = structlog.get_logger(__name__)


class Neo4jConnection:
    """Manages Neo4j database connections and operations."""

    def __init__(self, uri: str = None, username: str = None, password: str = None):
        """
        Initialize connection configuration.
        """

        # Aura connection details
        self.uri = uri or "neo4j+s://66b08bbb.databases.neo4j.io"  
        self.username = username or "66b08bbb"
        self.password = password or "_T_2BKKo64Og0rtapzWQ8JdLp-VfYiGL6ppnQuqEKH0"
        self.driver = None

    def connect(self):
        """Establish connection to Neo4j database."""
        try:
            if self.driver is None:
                self.driver = GraphDatabase.driver(
                    self.uri,
                    auth=(self.username, self.password)
                )

                # Test connection
                with self.driver.session() as session:
                    session.run("RETURN 1")

                logger.info("Connected to Neo4j", uri=self.uri)

        except Exception as e:
            logger.error("Failed to connect to Neo4j", error=str(e))
            raise

    def close(self):
        """Close the database connection."""
        if self.driver is not None:
            self.driver.close()
            self.driver = None
            logger.info("Disconnected from Neo4j")

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a read query."""
        if self.driver is None:
            raise RuntimeError("Database not connected")

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]

        except Exception as e:
            logger.error("Query execution failed", query=query[:100], error=str(e))
            raise

    def execute_write_query(self, query: str, parameters: Dict[str, Any] = None) -> int:
        """Execute a write query and return number of updates."""
        if self.driver is None:
            raise RuntimeError("Database not connected")

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                summary = result.consume()

                counters = summary.counters
                return (
                    counters.nodes_created +
                    counters.relationships_created +
                    counters.properties_set
                )

        except Exception as e:
            logger.error("Write query execution failed", query=query[:100], error=str(e))
            raise

    def clear_database(self):
        """Delete all nodes and relationships."""
        logger.warning("Clearing entire Neo4j database")
        self.execute_write_query("MATCH (n) DETACH DELETE n")

    def get_database_info(self) -> Dict[str, Any]:
        """Return node and relationship counts."""

        node_counts = self.execute_query("""
            MATCH (n)
            RETURN labels(n) AS labels, count(n) AS count
            ORDER BY count DESC
        """)

        relationship_counts = self.execute_query("""
            MATCH ()-[r]->()
            RETURN type(r) AS type, count(r) AS count
            ORDER BY count DESC
        """)

        return {
            "nodes": node_counts,
            "relationships": relationship_counts
        }


# Global connection instance
_connection: Optional[Neo4jConnection] = None


def get_connection() -> Neo4jConnection:
    """Get global Neo4j connection."""
    global _connection

    if _connection is None:
        _connection = Neo4jConnection()
        _connection.connect()

    return _connection


def close_connection():
    """Close global Neo4j connection."""
    global _connection

    if _connection:
        _connection.close()
        _connection = None
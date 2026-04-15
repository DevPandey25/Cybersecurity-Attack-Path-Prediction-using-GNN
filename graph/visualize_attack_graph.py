import networkx as nx
import matplotlib.pyplot as plt
from graph.connection import get_connection, close_connection


def visualize_attack_graph():

    conn = get_connection()
    driver = conn.driver

    G = nx.DiGraph()

    with driver.session() as session:

        query = """
        MATCH (n)-[r]->(m)
        RETURN labels(n) AS source_label,
               labels(m) AS target_label
        LIMIT 100
        """

        result = session.run(query)

        for record in result:
            src = record["source_label"][0]
            dst = record["target_label"][0]

            G.add_edge(src, dst)

    close_connection()

    print("Graph Nodes:", G.nodes())
    print("Graph Edges:", G.edges())

    plt.figure(figsize=(8,6))

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        arrows=True
    )

    plt.title("Cyber Attack Graph")
    plt.show()


if __name__ == "__main__":
    visualize_attack_graph()
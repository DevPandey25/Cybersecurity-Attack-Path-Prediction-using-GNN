import torch
from torch_geometric.data import Data
from graph.connection import get_connection, close_connection


def prepare_dataset():

    conn = get_connection()
    driver = conn.driver

    with driver.session() as session:

        # Get nodes
        node_query = """
        MATCH (n)
        RETURN id(n) AS id
        """

        node_result = session.run(node_query)

        nodes = [record["id"] for record in node_result]

        node_map = {node_id: i for i, node_id in enumerate(nodes)}

        num_nodes = len(nodes)

        # Node features
        x = torch.ones((num_nodes, 1), dtype=torch.float)

        # Get edges
        edge_query = """
        MATCH (n)-[r]->(m)
        RETURN id(n) AS source, id(m) AS target
        """

        edge_result = session.run(edge_query)

        edges = []

        for record in edge_result:

            src = node_map[record["source"]]
            dst = node_map[record["target"]]

            edges.append([src, dst])

        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

    close_connection()

    # Create synthetic labels
    y = torch.randint(0, 2, (num_nodes,), dtype=torch.long)

    data = Data(x=x, edge_index=edge_index, y=y)

    print("\nGNN Dataset Created")
    print(data)

    torch.save(data, "gnn_dataset.pt")

    print("\nSaved dataset to gnn_dataset.pt")


if __name__ == "__main__":
    prepare_dataset()
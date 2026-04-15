from graph.connection import get_connection, close_connection


def find_attack_paths():

    conn = get_connection()
    driver = conn.driver

    with driver.session() as session:

        query = """
        MATCH p = (a)-[*1..4]->(b)
        RETURN nodes(p) AS path
        LIMIT 5
        """

        result = session.run(query)

        print("\nPossible Attack Paths:\n")

        for record in result:

            nodes = record["path"]

            node_labels = []

            for node in nodes:
                label = list(node.labels)[0]
                node_labels.append(label)

            print(" -> ".join(node_labels))

    close_connection()


if __name__ == "__main__":
    find_attack_paths()
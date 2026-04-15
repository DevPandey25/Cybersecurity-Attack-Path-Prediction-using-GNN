import streamlit as st
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from graph.connection import get_connection, close_connection

st.set_page_config(page_title="Cyber Attack Prediction Dashboard", layout="wide")

st.title("Cybersecurity Attack Path Prediction using Graph Neural Networks")

st.write(
    "This dashboard demonstrates cyber attack prediction using a Graph Neural Network "
    "and a graph database."
)

st.divider()


# ---------- Function to run scripts and capture output ----------
def run_command(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output


# ---------- Left Column ----------
col1, col2 = st.columns(2)

with col1:

    st.subheader("1. Prepare Graph Dataset")

    if st.button("Prepare Dataset"):
        output = run_command(["python", "-m", "graph.prepare_gnn_data"])
        st.code(output)

    st.subheader("2. Train GNN Model")

    if st.button("Train Model"):
        output = run_command(["python", "-m", "gnn.train_gnn"])
        st.code(output)


# ---------- Right Column ----------
with col2:

    st.subheader("3. Predict Risky Nodes")

    if st.button("Run Prediction"):
        output = run_command(["python", "-m", "gnn.predict_attack"])
        st.code(output)

    st.subheader("4. Discover Attack Paths")

    if st.button("Find Attack Paths"):
        output = run_command(["python", "-m", "graph.find_attack_path"])
        st.code(output)


st.divider()

# ---------- Graph Visualization ----------
st.subheader("5. Cyber Attack Graph Visualization")

if st.button("Show Attack Graph"):

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

    fig, ax = plt.subplots(figsize=(8,6))

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
        arrows=True,
        ax=ax
    )

    st.pyplot(fig)

    st.success("Attack graph generated successfully.")
# Attack Detection using Graph Neural Networks (GNNs)

## 📝 Project Overview
This project leverages **Graph Neural Networks (GNNs)** to detect and predict potential attack paths in a network by analyzing graph-structured data. It supports both **real and synthetic datasets**, and includes functionalities for:

- Training and evaluating a GNN model.
- Predicting attacks on new graphs.
- Visualizing attack paths.
- Interactive dashboard using **Streamlit** for easy exploration.

---

## 📂 Project Structure


project_root/
│
├─ data/ # Data management
│ ├─ init.py
│ ├─ generate_synthetic_data.py
│ └─ synthetic_data/
│
├─ gnn/ # GNN models and scripts
│ ├─ pycache/
│ ├─ gnn_model.py
│ ├─ predict_attack.py
│ └─ train_gnn.py
│
├─ graph/ # Graph processing and visualization
│ ├─ pycache/
│ ├─ init.py
│ ├─ connection.py
│ ├─ export_graph.py
│ ├─ find_attack_path.py
│ ├─ load_data.py
│ ├─ prepare_gnn_data.py
│ ├─ schema.cypher
│ └─ visualize_attack_graph.py
│
├─ dashboard/ # Streamlit app files
│ └─ app.py # Main Streamlit app
│
├─ gnn_dataset.pt # Dataset file (ignored in Git)
├─ gnn_model.pt # Trained model weights (ignored in Git)
├─ requirements.txt
├─ README.md
├─ .gitignore
└─ venv/ # Virtual environment (ignored)


---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/<your_username>/<repo_name>.git
cd <repo_name>

Set up a virtual environment

python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

Install dependencies

pip install -r requirements.txt

The requirements.txt includes:

torch (PyTorch)

torch_geometric (PyTorch Geometric for GNN)

numpy, pandas

networkx, matplotlib

streamlit

📁 Dataset

gnn_dataset.pt is ignored in Git.

For synthetic data generation:

python data/generate_synthetic_data.py

Place datasets in the data/synthetic_data/ folder if using generated data.

🚀 Running the Project
1️⃣ Train the GNN model
python gnn/train_gnn.py

This script will train the model on your dataset and save the weights to gnn_model.pt.

2️⃣ Predict Attacks
python gnn/predict_attack.py --input path/to/graph

This script predicts potential attack paths for a given graph input.

3️⃣ Visualize Attack Graph
python graph/visualize_attack_graph.py --input path/to/graph

Generates visualizations of nodes, connections, and detected attack paths.

4️⃣ Launch Streamlit Dashboard
streamlit run dashboard/app.py

Interactively explore the graph data.

Visualize attack paths and GNN predictions in a user-friendly interface.

🔧 Features

Train and evaluate GNNs for attack detection.

Supports synthetic and real datasets.

Predict attacks on new graphs.

Visualize graph structure and attack paths.

Streamlit dashboard for interactive exploration.

📜 License

MIT License.

📞 Contact

Dev Prasad Pandey

Email Id: devpandey25.in@gamil.com

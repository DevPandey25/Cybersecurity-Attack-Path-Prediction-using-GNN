import torch
from gnn.gnn_model import GNNModel

# Load dataset
data = torch.load("gnn_dataset.pt", weights_only=False)

# Load model
model = GNNModel(input_dim=data.num_features)
model.load_state_dict(torch.load("gnn_model.pt"))

model.eval()

# Prediction
with torch.no_grad():
    out = model(data.x, data.edge_index)

# Convert to probabilities
probs = torch.sigmoid(out).squeeze()

# Threshold
risky_nodes = (probs > 0.5).nonzero(as_tuple=True)[0]

print("\nAttack probability per node:")
print(probs)

print("\nPredicted risky nodes:")
print(risky_nodes)
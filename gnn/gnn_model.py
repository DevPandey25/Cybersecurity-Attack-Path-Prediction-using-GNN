import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


class GNNModel(torch.nn.Module):

    def __init__(self, input_dim):
        super(GNNModel, self).__init__()

        self.conv1 = GCNConv(input_dim, 16)
        self.conv2 = GCNConv(16, 2)   # IMPORTANT

    def forward(self, x, edge_index):

        x = self.conv1(x, edge_index)
        x = F.relu(x)

        x = self.conv2(x, edge_index)

        return x
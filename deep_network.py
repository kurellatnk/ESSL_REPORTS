import torch
import torch.nn as nn

print("=== Building a Deep Neural Network ===\n")

# nn.Sequential allows us to stack layers like building blocks
model = nn.Sequential(
    # 1. The Input Layer (takes our 3 numbers, outputs to 16 hidden neurons)
    nn.Linear(in_features=3, out_features=16),
    
    # 2. The Activation Function (The "spark" that helps it learn complex patterns)
    nn.ReLU(),
    
    # 3. A Hidden Layer (takes the 16 neurons, outputs to another 8 neurons)
    nn.Linear(in_features=16, out_features=8),
    nn.ReLU(),
    
    # 4. The Output Layer (takes the 8 neurons and outputs 1 final prediction)
    nn.Linear(in_features=8, out_features=1)
)

# Print the architecture to the terminal
print(model)
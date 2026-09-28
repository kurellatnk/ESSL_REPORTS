import torch
import torch.nn as nn
import torch.optim as optim

# 1. The Deep Model (Upgraded for Classification)
model = nn.Sequential(
    nn.Linear(in_features=3, out_features=16),
    nn.ReLU(),
    nn.Linear(in_features=16, out_features=8),
    nn.ReLU(),
    nn.Linear(in_features=8, out_features=1),
    nn.Sigmoid() # Forces output to a probability between 0 and 1
)

# 2. Synthetic Threat Data (4 examples, 3 features each)
# Imagine these features represent: [Urgency Words, Links Count, Misspellings]
X_train = torch.tensor([
    [0.0, 0.0, 0.0], # Safe Email
    [1.0, 3.0, 2.0], # Phishing Threat
    [0.0, 1.0, 0.0], # Safe Email
    [1.0, 5.0, 4.0]  # Severe Threat
])

# Target labels (0 = Safe, 1 = Threat)
y_train = torch.tensor([
    [0.0], 
    [1.0], 
    [0.0], 
    [1.0]
])

# 3. Training Tools
loss_function = nn.BCELoss() 
optimizer = optim.Adam(model.parameters(), lr=0.05) 

print("=== Training Deep Network for Threat Detection ===\n")

# 4. The Training Loop
for epoch in range(100):
    predictions = model(X_train)
    loss = loss_function(predictions, y_train)
    
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    
    if epoch % 20 == 0:
        print(f"Epoch {epoch:02d} | Error: {loss.item():.4f}")

# 5. Final Test
print("\nFinal Probabilities (Targeting: 0.0, 1.0, 0.0, 1.0):")
print(model(X_train).detach())
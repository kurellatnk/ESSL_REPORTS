import torch
import torch.nn as nn
import torch.optim as optim

# 1. The Data and the Network
input_data = torch.tensor([1.0, 2.0, 3.0])
layer = nn.Linear(in_features=3, out_features=1)

# 2. The Target (What we WANT the network to predict)
target = torch.tensor([10.0])

# 3. The Tools for Learning
# MSELoss calculates the exact error (how far the guess is from 10.0)
loss_function = nn.MSELoss() 
# SGD (Stochastic Gradient Descent) is the engine that adjusts the weights
optimizer = optim.SGD(layer.parameters(), lr=0.01)

print("=== Starting Training Loop ===\n")

# 4. Train the brain for 100 loops (Epochs)
for epoch in range(100):
    # Make a prediction
    prediction = layer(input_data)
    
    # Calculate how wrong the prediction is
    loss = loss_function(prediction, target)
    
    # Calculate the mathematical adjustments needed (Backpropagation)
    loss.backward()
    
    # Apply the adjustments to the neuron's weights
    optimizer.step()
    
    # Clear the old math for the next loop
    optimizer.zero_grad()
    
    # Print our progress every 20 loops
    if epoch % 20 == 0:
        print(f"Epoch {epoch:02d} | Prediction: {prediction.item():.4f} | Error: {loss.item():.4f}")

print(f"\nFinal Prediction: {layer(input_data).item():.4f}")
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

print("=== Training Computer Vision Model ===")
print("This might take a minute or two... scanning 60,000 images!\n")

# 1. Data Pipeline
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
# download=False because you already downloaded it successfully
train_data = datasets.MNIST(root='./data', train=True, download=False, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# 2. The CNN Architecture
class DigitClassifier(nn.Module):
    def __init__(self):
        super(DigitClassifier, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(16 * 14 * 14, 64)
        self.fc2 = nn.Linear(64, 10) # 10 outputs for digits 0-9

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = x.view(-1, 16 * 14 * 14)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = DigitClassifier()

# 3. Training Tools
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. The Training Loop (1 Epoch)
model.train() # Set model to training mode
for batch_idx, (images, labels) in enumerate(train_loader):
    optimizer.zero_grad()
    predictions = model(images)
    loss = loss_function(predictions, labels)
    loss.backward()
    optimizer.step()
    
    # Print progress every 200 batches
    if batch_idx % 200 == 0:
        print(f"Batch {batch_idx:03d}/938 | Error (Loss): {loss.item():.4f}")

print("\nTraining Complete! The CNN brain is fully wired.")
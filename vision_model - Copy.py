import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

print("=== Setting Up Computer Vision Pipeline ===")

# 1. Pipeline: Convert raw images to tensors and normalize pixel values
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# 2. Download standard training dataset
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# 3. Define the CNN Architecture
class DigitClassifier(nn.Module):
    def __init__(self):
        super(DigitClassifier, self).__init__()
        # Conv layer: scans image with 16 filters
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Fully connected layers to classify into 10 digits (0-9)
        self.fc1 = nn.Linear(16 * 14 * 14, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        # Feature extraction
        x = self.pool(self.relu(self.conv1(x)))
        # Flatten from 2D image grid into a 1D vector
        x = x.view(-1, 16 * 14 * 14)
        # Decision layers
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = DigitClassifier()
print(model)
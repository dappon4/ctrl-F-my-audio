import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms

from model import AudioClassifier
from format_dataset import format

def load_data(type_map):
    res = []
    for type in type_map:
        directory = f"datasets/imgs/{type}"
        file_names = os.listdir(directory)
        for file in file_names:
            resized_image = Image.open(f"datasets/imgs/{type}/{file}")
            
            resized_image = resized_image.convert("RGB")

            # Apply the ToTensor transformation
            transform = transforms.ToTensor()
            image_tensor = transform(resized_image)

            target = torch.tensor(type_map[type])
            # Print the PyTorch matrix
            res.append((image_tensor, target))
    
    return res

def train(train_list,epochs):
    for i in range(epochs):
        print(f"Epoch {i+1}")
        for inputs, labels in loader:
            y_pred = model(inputs)
            loss = loss_fn(y_pred, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

if __name__ == "__main__":
    key_map = {"angry_sound":0,"Bird":1,"Cats":2,"Dog":3,"guns":4}
    batch_size = 32
    model = AudioClassifier(5)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    n_epochs = 20
    
    data = load_data(key_map)
    loader = torch.utils.data.DataLoader(data, batch_size=32, shuffle=True)
    train(loader,n_epochs)
    
    torch.save(model.state_dict(), "models/model_3.pth")
    
    
    
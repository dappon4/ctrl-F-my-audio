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

def load_data(type_map,randomize = False):
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
    
    if randomize:
        np.random.shuffle(res)
    
    return res

def test_model(model,test_loader):
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            y_pred = model(images)
            _, predicted = torch.max(y_pred.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Accuracy of the network on the {total} test images: {100 * correct / total}%")

def main(data,n_epochs,model,loss_fn,optimizer,train_size,split = True):
    if split:
        n = len(data)
        train_num = int(n*train_size)
        train_loader = torch.utils.data.DataLoader(data[:train_num], batch_size=32, shuffle=True)
        test_loader = torch.utils.data.DataLoader(data[train_num:], batch_size=32, shuffle=True)
    else:
        pass
    
    train(train_loader,n_epochs,loss_fn,optimizer)
    
    torch.save(model.state_dict(), "models/model_3.pth")
    test_model(model,test_loader)
    test_model(model,train_loader)
    
        
def train(train_loader,epochs,loss_fn,optimizer):
    for i in range(epochs):
        print(f"Epoch {i+1}")
        for inputs, labels in train_loader:
            y_pred = model(inputs)
            loss = loss_fn(y_pred, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

if __name__ == "__main__":
    key_map = {"angry_sound":0,"Bird":1,"Cats":2,"Dog":3,"guns":4}
    batch_size = 16
    model = AudioClassifier(5)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    n_epochs = 7
    data = load_data(key_map)
    
    main(data,n_epochs,model,loss_fn,optimizer,0.8)
    
    
    
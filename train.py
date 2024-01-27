import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
import time

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
    model.eval()
    loss = 0
    
    t1 = time.time()
    with torch.no_grad():
        for images, labels in test_loader:
            y_pred = model(images)
            _, predicted = torch.max(y_pred.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    t2 = time.time()
    print(f"Accuracy of the network on the {total} test images: {100 * correct / total}%, took {t2-t1} seconds")

def main(data,n_epochs,model,loss_fn,optimizer,train_size,split = True,train_bool = True):
    if split:
        n = len(data)
        train_num = int(n*train_size)
        train_loader = torch.utils.data.DataLoader(data[:train_num], batch_size=32, shuffle=True)
        test_loader = torch.utils.data.DataLoader(data[train_num:], batch_size=32, shuffle=True)
    else:
        pass
    
    if train_bool:
        t1 = time.time()
        train(train_loader,n_epochs,loss_fn,optimizer)
        t2 = time.time()
        print(f"Training took {t2-t1} seconds")
        torch.save(model.state_dict(), "models/model_4.pth")
    
    test_model(model,test_loader)
    test_model(model,train_loader)
    
        
def train(train_loader,epochs,loss_fn,optimizer):
    for i in range(epochs):
        print(f"Epoch {i+1}")
        t1 = time.time()
        for inputs, labels in train_loader:
            y_pred = model(inputs)
            loss = loss_fn(y_pred, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        t2 = time.time()
        print(f"Epoch {i + 1} took {t2-t1} seconds")

def create_dict():
    res = {}
    names = os.listdir("datasets/imgs")
    names.remove("tmp")
    for i,name in enumerate(names):
        res[name] = i
    
    return res

if __name__ == "__main__":
    key_map = create_dict()
    batch_size = 64
    model = AudioClassifier(len(key_map))
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    n_epochs = 15
    
    t1 = time.time()
    data = load_data(key_map)
    t2 = time.time()
    print(f"Loading data took {t2-t1} seconds")
    
    main(data,n_epochs,model,loss_fn,optimizer,0.8)
    
    
    
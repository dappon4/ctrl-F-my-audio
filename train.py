import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn

from model import AudioClassifier
from format_dataset import format



def train(train_list,epochs):
    for _ in range(epochs):
        for inputs, labels in train_list:
            y_pred = model(inputs)
            loss = loss_fn(y_pred, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

if __name__ == "__main__":
    batch_size = 32
    model = AudioClassifier(5)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    n_epochs = 20
    dataset = []
    dataset.append(format())
    
    train(dataset,n_epochs)
    
    
    
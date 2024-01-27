import torch
from torch import nn
import torchaudio

class AudioClassifier(nn.Module):
    def __init__(self,output) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=(5,5), stride=1, padding=0)
        self.act1 = nn.ReLU()
        self.drop1 = nn.Dropout(0.3)
 
        self.conv2 = nn.Conv2d(32, 32, kernel_size=(3,3), stride=1, padding=1)
        self.act2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=(4, 4))
 
        self.flat = nn.Flatten()
 
        self.fc3 = nn.Linear(18432, 512)
        self.act3 = nn.ReLU()
        self.drop3 = nn.Dropout(0.5)
 
        self.fc4 = nn.Linear(512, output)
        
        
    def forward(self, x):
        # input 3x100x100, output 32x96x96
        x = self.act1(self.conv1(x))
        x = self.drop1(x)
        # input 32x96x96, output 32x96x96
        x = self.act2(self.conv2(x))
        # input 32x96x96, output 32x24x24
        x = self.pool2(x)
        # input 32x24x24, output 18432
        x = self.flat(x)
        # input 18432, output 512
        x = self.act3(self.fc3(x))
        x = self.drop3(x)
        # input 512, output 5
        x = self.fc4(x)
        return x
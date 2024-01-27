import torch
from torch import nn
import torchaudio

class AudioClassifier(nn.Module):
    def __init__(self,output) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=(10,10), stride=2, padding=0)
        self.norm1 = nn.BatchNorm2d(32)
        self.act1 = nn.ReLU()
        self.drop1 = nn.Dropout(0.4)
 
        self.conv2 = nn.Conv2d(32, 32, kernel_size=(4,4), stride=1, padding=1)
        self.norm2 = nn.BatchNorm2d(32)
        self.act2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=(4, 4))

        self.conv3 = nn.Conv2d(32, 64, kernel_size=(2,2), stride=1, padding=0)
        self.norm3 = nn.BatchNorm2d(64)
        self.act3 = nn.ReLU()
        self.drop3 = nn.Dropout(0.4)
        
        self.flat = nn.Flatten(start_dim=1)
 
        self.fc4 = nn.Linear(30976, 512)
        self.act4 = nn.ReLU()
        self.drop4 = nn.Dropout(0.6)
        
        self.fc5 = nn.Linear(512, output)
        
        
    def forward(self, x):
        # fofmula: (W−K+2P)/S+1
        
        # input 3x200x200, output 32x96x96
        x = self.conv1(x)
        x = self.norm1(x)
        x = self.act1(x)
        x = self.drop1(x)
        # input 32x96x96, output 64x48x48
        x = self.conv2(x)
        x = self.norm2(x)
        x = self.act2(x)
        # input 64x48x48, output 64x24x24
        x = self.pool2(x)
        
        # input 64x24x24, output 128x12x12
        x = self.conv3(x)
        x = self.norm3(x)
        x = self.act3(x)
        x = self.drop3(x)
        
        
        # input 128x22x22, output 18432
        x = self.flat(x)
        
        # input 18432, output 512
        x = self.fc4(x)
        x = self.act4(x)
        x = self.drop4(x)
        # input 512, output 5
        x = self.fc5(x)
        return x
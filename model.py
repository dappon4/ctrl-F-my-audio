import torch
from torch import nn
import torchaudio

class AudioClassifier(nn.Module):
    def __init__(self,output) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=(9,9), stride=2, padding=1)
        self.norm1 = nn.BatchNorm2d(32)
        self.act1 = nn.ReLU()
        self.drop1 = nn.Dropout(0.3)
        self.pool1 = nn.MaxPool2d(kernel_size=(2, 2))
 
        self.conv2 = nn.Conv2d(32, 64, kernel_size=(5,5), stride=1, padding=1)
        self.norm2 = nn.BatchNorm2d(64)
        self.act2 = nn.ReLU()
        self.drop2 = nn.Dropout(0.3)
        self.pool2 = nn.MaxPool2d(kernel_size=(2, 2))

        self.conv3 = nn.Conv2d(64, 128, kernel_size=(3,3), stride=1, padding=0)
        self.norm3 = nn.BatchNorm2d(128)
        self.act3 = nn.ReLU()
        self.drop3 = nn.Dropout(0.3)
        self.pool3 = nn.MaxPool2d(kernel_size=(2, 2))
        
        self.flat = nn.Flatten(start_dim=1)
 
        self.fc4 = nn.Linear(10368, 2048)
        self.act4 = nn.ReLU()
        self.drop4 = nn.Dropout(0.4)
        
        self.fc5 = nn.Linear(2048, 512)
        self.act5 = nn.ReLU()
        self.drop5 = nn.Dropout(0.4)
        
        self.fc6 = nn.Linear(512, output)
        
        
    def forward(self, x):
        # fofmula: (W−K+2P)/S+1
        
        # input 3x50x50, output 32x22x22
        x = self.conv1(x)
        x = self.norm1(x)
        x = self.act1(x)
        x = self.drop1(x)
        
        #x = self.pool1(x)
        
        # input 32x22x22, output 64x20x20
        x = self.conv2(x)
        x = self.norm2(x)
        x = self.act2(x)
        x = self.drop2(x)
        # input 64x20x20, output 64x22x22
        #x = self.pool2(x)
        
        # input 64x20x20, output 128x18x18
        x = self.conv3(x)
        x = self.norm3(x)
        x = self.act3(x)
        # input 128x18x18, output 128x9x9
        x = self.pool3(x)
        
        # input 128x9x9, output 10368
        x = self.flat(x)
        
        # input 10368, output 2048
        x = self.fc4(x)
        x = self.act4(x)
        x = self.drop4(x)
        # input 2047, output 512
        x = self.fc5(x)
        x = self.act5(x)
        x = self.drop5(x)
        
        # input 512 output 21
        x = self.fc6(x)
        return x
import torch
from torch import nn
import torchaudio

def batch_norm(params):
    def batch_norm_layer():
        return nn.BatchNorm2d(num_features=params['num_features'], eps=params['eps'], momentum=params['momentum'], affine=params['affine'], track_running_stats=params['track_running_stats'])
    
    return batch_norm_layer

def conv(kernl, stride, filters, params):
    def conv_layer():
        output = nn.Conv2d(in_channels=params['in_channels'], out_channels=filters, kernel_size=kernl, stride=stride, padding=params['padding'])
        output = batch_norm(params)(output)
        output = nn.ReLU()(output)
        return output
    return conv_layer

def separable_conv(kernl, stride, filters, params):
    def seperable_conv_layer():
        # TODO - Add depthwise convolution
        #output = depthwise_conv(kernl, stride, filters, params)
        output = batch_norm(params)(output)
        output = nn.ReLU()(output)
        output = nn.Conv2d(in_channels=params['in_channels'], out_channels=filters, kernel_size=1, stride=1, padding=params['padding'], bias = False)
        output = batch_norm(params)(output)
        output = nn.ReLU()(output)
        return output
    return seperable_conv_layer

YAMNET_LAYER_DEFS = [
    # (name, kernel, stride, filters)
    (conv, 3, 2, 32),
    (separable_conv, 3, 1, 64),
    (separable_conv, 3, 2, 128),
    (separable_conv, 3, 1, 128),
    (separable_conv, 3, 2, 256),
    (separable_conv, 3, 1, 256),
    (separable_conv, 3, 2, 512),
    (separable_conv, 3, 1, 512),
    (separable_conv, 3, 1, 512),
    (separable_conv, 3, 1, 512),
    (separable_conv, 3, 1, 512),
    (separable_conv, 3, 1, 512),
    (separable_conv, 3, 2, 1024),
    (separable_conv, 3, 1, 1024),
]

class Yamnet(nn.Module):
    def __init__(self, params):
        super(Yamnet, self).__init__()
        self.params = params
        self.layers = self._build_model()
        self._initialize_weights()
        self.layers = []

    def _build_model(self):
        self.layers = []
        for i, (layer_type, kernel_size, stride, filters) in enumerate(YAMNET_LAYER_DEFS):
            params = {
                'in_channels': self.params['in_channels'] if i == 0 else YAMNET_LAYER_DEFS[i-1][3],
                'num_features': filters,
                'eps': self.params['eps'],
                'momentum': self.params['momentum'],
                'affine': self.params['affine'],
                'track_running_stats': self.params['track_running_stats'],
                'padding': (kernel_size - 1) // 2
            }
            self.layers.append(layer_type(kernel_size, stride, filters, params))
        return nn.Sequential(*self.layers)

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight.data)
                if m.bias is not None:
                    nn.init.constant_(m.bias.data, 0.0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight.data, 1.0)
                nn.init.constant_(m.bias.data, 0.0)

    def forward(self, x):
        x = self.layers(x)
        return x
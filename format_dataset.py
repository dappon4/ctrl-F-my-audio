import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms

def resize_img(path):
    # Open the image
    image = Image.open(path)

    # Resize the image
    resized_image = image.resize((100, 100))

    # Save the resized image
    resized_image.save("imgs/resized_image.png")

# Call the function with the path to your image

def preprocess():
    filename = os.path.join("datasets","4.wav")
    print(os.path.isfile(filename))

    # Load the audio file
    audio, sr = librosa.load(filename)

    # Compute the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)

    # Convert the spectrogram to dB scale
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

    # Display the spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spectrogram_db, sr=sr)
    plt.savefig("imgs/test.png", bbox_inches='tight', pad_inches=0)
    resize_img("imgs/test.png")

def convert_to_tensor():
    resized_image = Image.open("imgs/resized_image.png")

    resized_image = resized_image.convert("RGB")
    # Apply the ToTensor transformation
    transform = transforms.ToTensor()
    image_tensor = transform(resized_image)

    # Convert the integer to an integer tensor
    int_tensor = torch.tensor(1)

    return (image_tensor, int_tensor)
    # Print the PyTorch matrix

def format():
    preprocess()
    tup = convert_to_tensor()
    
    print(tup[1])
    return tup
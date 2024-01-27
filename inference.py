import os
import torch
from PIL import Image
from model import AudioClassifier
from torchvision import transforms
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def audio_to_img(path):
    
    # Load the audio file
    audio, sr = librosa.load(path)

    # Compute the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)

    # Convert the spectrogram to dB scale
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
    
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spectrogram_db, sr=sr)
    plt.savefig(f"datasets/tmp/tmp.png", bbox_inches='tight', pad_inches=0)
    
    image = Image.open(f"datasets/tmp/tmp.png")

    # Resize the image
    resized_image = image.resize((100, 100))

    # Save the resized image
    resized_image.save(f"datasets/tmp/output/tmp.png")
    
def convert(path):
    
    audio_to_img(path)
    
    resized_image = Image.open("datasets/tmp/output/tmp.png")
            
    resized_image = resized_image.convert("RGB")

    # Apply the ToTensor transformation
    transform = transforms.ToTensor()
    image_tensor = transform(resized_image)
    
    return image_tensor

def inference(model_path, audio_path, key_map):
    model = AudioClassifier(len(key_map))
    model.load_state_dict(torch.load(model_path))
    model.eval()

    files = os.listdir(audio_path)
    res = []

    for file in files:
        file_path = os.path.join(audio_path, file)
        
        if os.path.isfile(file_path):
            input_tensor = convert(file_path)

            # Add batch dimension to input_tensor
            input_tensor = input_tensor.unsqueeze(0)

            print(input_tensor.shape)
            output = model(input_tensor)
            _, predicted_class = torch.max(output, 1)

            res.append(predicted_class.item())
    
    print(res)


def create_dict():
    res = {}
    names = os.listdir("datasets/imgs")
    names.remove("tmp")
    for i,name in enumerate(names):
        res[name] = i
    
    return res

def main():
    dic = create_dict()
    model_path = "models/model_3.pth"
    audio_path = "assets/chunks"
    
    inference(model_path,audio_path,dic)
if __name__ == "__main__":
    main()
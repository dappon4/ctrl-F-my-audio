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
    plt.savefig(f"inference_tmp/tmp.png", bbox_inches='tight', pad_inches=0)
    
    image = Image.open(f"inference_tmp/tmp.png")

    # Resize the image
    resized_image = image.resize((50, 50))

    # Save the resized image
    resized_image.save(f"inference_tmp/output/tmp.png")
    plt.close()
    
def convert(path):
    
    audio_to_img(path)
    
    resized_image = Image.open("inference_tmp/output/tmp.png")

    resized_image = resized_image.convert("RGB")

    # Apply the ToTensor transformation
    transform = transforms.ToTensor()
    image_tensor = transform(resized_image)
    
    return image_tensor

def inference(model_path, audio_path, key_map, step):
    
    print(f"using model from {model_path}")
    
    confidence_threshold = 0.7
    
    reverse_map = {v: k for k, v in key_map.items()}
    
    model = AudioClassifier(len(key_map))
    model.load_state_dict(torch.load(model_path))
    model.eval()

    files = os.listdir(audio_path)
    files.sort()
    res = {}

    for i,file in enumerate(files):
        file_path = os.path.join(audio_path, file)
        
        if os.path.isfile(file_path):
            input_tensor = convert(file_path)

            # Add batch dimension to input_tensor
            input_tensor = input_tensor.unsqueeze(0)

            
            output = model(input_tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
            predicted_idx = torch.argmax(output, 1).item()

            probability = probs[0][predicted_idx].item()
            
            print(reverse_map[predicted_idx], probability)
            
            if probability >= confidence_threshold:
                res[str(i*step)] = reverse_map[predicted_idx]
    
    print(res)
    return res


def create_dict():
    with open("index.txt", "r") as file:
            text = file.read()
            tags = text.split("\n")
    res = {}
    for i,name in enumerate(tags):
        res[name] = i
    
    return res

def main():
    step = 3
    print("running from main...")
    dic = create_dict()
    model_path = "models/acc-76-s.pth"
    audio_path = "assets/chunks"
    
    inference(model_path,audio_path,dic, step)
if __name__ == "__main__":
    main()
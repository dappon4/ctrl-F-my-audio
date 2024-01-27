import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image

# FILEPATH: /c:/Users/Dahong Luo/programming/python/ctrl-F-my-audio/test/test.ipynb

def resize_img(path):
    # Open the image
    image = Image.open(path)

    # Resize the image
    resized_image = image.resize((100, 100))

    # Save the resized image
    resized_image.save("imgs/resized_image.png")

# Call the function with the path to your image

def preproces():
    filename = os.path.join("test","AUD-20231109-WA0012.mp3")
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
    plt.show()
    

if __name__ == "__main__":
    preproces()
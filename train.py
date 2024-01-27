import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import numpy as np

# FILEPATH: /c:/Users/Dahong Luo/programming/python/ctrl-F-my-audio/test/test.ipynb

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
    librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.show()
    

if __name__ == "__main__":
    preproces()
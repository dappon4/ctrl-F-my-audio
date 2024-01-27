from moviepy.editor import *

def find_mp4(mp4_folder_location, mp3_folder_location):

    for root, dirs, files in os.walk(mp4_folder_location):
        for filename in files:
            print(filename[:-4])
            print(os.path.join(mp4_folder_location, filename))
            video = VideoFileClip(os.path.join(mp4_folder_location, filename))

            video.audio.write_audiofile(os.path.join(mp3_folder_location,filename[:-4]+".mp3"))
            return os.path.join(mp3_folder_location,filename[:-4]+".mp3")

if __name__ == "__main__":
    mp4_folder_location = r"C:\Users\sange\OneDrive\Desktop\input"

    mp3_folder_location = r"C:\Users\sange\OneDrive\Desktop\output downloads"


    find_mp4(mp4_folder_location, mp3_folder_location)
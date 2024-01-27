from moviepy.editor import *

def find_mp4(mp4_folder_location, mp3_folder_location):
    for root, dirs, files in os.walk(mp4_folder_location):
        for filename in files:
            print("Converting:", filename)
            video = VideoFileClip(os.path.join(mp4_folder_location, filename))

            mp3_output_path = os.path.join(mp3_folder_location, filename[:-4] + ".mp3")
            print("MP3 Output Path:", mp3_output_path)

            video.audio.write_audiofile(mp3_output_path)
            return mp3_output_path




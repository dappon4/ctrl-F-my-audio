from pydub import utils, AudioSegment
import os

def get_prober_name():
    return r"C:\Users\sange\OneDrive\Desktop\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe"  # Replace with the actual path to ffprobe.exe

AudioSegment.converter = r"C:\Users\sange\OneDrive\Desktop\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" # Replace with the actual path to ffmpeg.exe
utils.get_prober_name = get_prober_name

def split_mp3(input_file, output_folder, segment_length=10):
    audio = AudioSegment.from_mp3(input_file)
    
    total_duration = len(audio)

    segment_length_ms = segment_length * 1000

    for start_time in range(0, total_duration, segment_length_ms):
        end_time = start_time + segment_length_ms

        if end_time > total_duration:
            end_time = total_duration

        segment = audio[start_time:end_time]

        output_file = os.path.join(output_folder, f"segment_{start_time // 1000}.mp3")

        # Export the segment as an MP3 file
        segment.export(output_file, format="mp3")

if __name__ == "__main__":
    input_file_path = r"C:\Users\sange\OneDrive\Desktop\output downloads\_Skip the villain arc_.mp3"
    output_folder_path = r"C:\Users\sange\OneDrive\Desktop\output clips"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder_path, exist_ok=True)

    split_mp3(input_file_path, output_folder_path)

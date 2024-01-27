import os
import subprocess

def split_mp3(output_folder, segment_length=10):
    input_folder = r"C:\Users\sange\dahong\ctrl-F-my-audio\assets\mp3"
    output_folder = os.path.abspath(output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    audio_files = [f for f in os.listdir(input_folder) if f.endswith('.mp3')]

    for input_file in audio_files:
        input_file_path = os.path.join(input_folder, input_file)
        output_file_pattern = os.path.join(output_folder, f"segment_%03d.mp3")

        # Run ffmpeg command to split the audio file
        subprocess.run([
            "ffmpeg",
            "-i", input_file_path,
            "-f", "segment",
            "-segment_time", str(segment_length),
            "-c", "copy",
            output_file_pattern
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)



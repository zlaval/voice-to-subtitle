import os
from moviepy import AudioFileClip

def extract_speech_to_mp3(path, file, output):
    input_file = os.path.join(path, file)
    output_file = os.path.join(path, f"{output}.mp3")

    if os.path.exists(output_file):
        print(f"File '{output_file}' already exists. Skipping conversion.")
        return output_file

    try:
        audio = AudioFileClip(input_file)
        audio.write_audiofile(output_file, codec='mp3')
        audio.close()
        print(f"Successfully created: {output_file}")
        return output_file
    except Exception as e:
        raise Exception(f"Error extract speech from the video to mp3: {e}")
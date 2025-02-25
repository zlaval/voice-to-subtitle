import argparse

from grabber import extract_speech_to_mp3
from textractor import speech_to_text


def main(path, file, output):
    mp3_file = extract_speech_to_mp3(path, file, output)
    tsed_text = speech_to_text(mp3_file, path, output)
    print("Successfully extracted text from the audio file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the application with required and optional arguments.")
    parser.add_argument("-p", "--path", required=True, help="Path to the input")
    parser.add_argument("-f", "--file", required=True, help="Name of the file with extension")
    parser.add_argument("-o", "--output", required=False, help="Optional output name")

    args = parser.parse_args()
    main(args.path, args.file, args.output)

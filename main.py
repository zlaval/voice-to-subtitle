import argparse

from grabber import extract_speech_to_mp3
from sentenceprocessor import make_timestamped_sentences
from subtitle import create_subtitle
from textractor import speech_to_text
from translator import translate_fbm2m100


def main(path, file, output, src, tgt, model="m2m100"):
    mp3_file = extract_speech_to_mp3(path, file, output)
    ts_words = speech_to_text(mp3_file, path, output)
    ts_sentences = make_timestamped_sentences(ts_words)
    create_subtitle(path, f'{output}_orig', ts_sentences)
    if src and tgt:
        if model == "ChatGPT":
            print("Translation with ChatGPT does not implemented yet")
        else:
            ts_translated=translate_fbm2m100(ts_sentences, src, tgt)
            create_subtitle(path, f'{output}_{tgt}', ts_translated)

    print("Successfully extracted text from the audio file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the application with required and optional arguments.")
    parser.add_argument("-p", "--path", required=True, help="Path to the input")
    parser.add_argument("-f", "--file", required=True, help="Name of the file with extension")
    parser.add_argument("-o", "--output", required=False, help="Optional output name")
    parser.add_argument("-s", "--src", required=False,
                        help="Set this and tgt for translation. The original language of the video.")
    parser.add_argument("-t", "--tgt", required=False,
                        help="Set this and src for translation. The language the text is translated to.")
    parser.add_argument("-m", "--translator", required=False,
                        help="Default is Facebook m2m100. Options: ChatGPT - api key required")

    args = parser.parse_args()
    main(args.path, args.file, args.output, args.src, args.tgt, args.translator)

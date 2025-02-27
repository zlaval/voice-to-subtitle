import re
import textwrap
from datetime import timedelta

MAX_ROW_LEN = 100

def make_timestamped_sentences(ts_words, fine_grained=True):
    if fine_grained:
        text = wrap_text(ts_words["text"])
        return determine_line_timestamps(text, ts_words["chunks"])
    else:
        return generate_sentence(ts_words["chunks"])



def determine_line_timestamps(text, word_timestamps):
    lines = text.split("\n")
    timestamps = [entry["timestamp"] for entry in word_timestamps]

    result = []
    word_index = 0

    for line in lines:
        line_words = line.split()

        if not line_words:
            continue

        first_word_index = word_index
        last_word_index = first_word_index + len(line_words) - 1

        if first_word_index > 0:
            start_time = timestamps[first_word_index - 1][1]
            if not start_time:
                start_time = timestamps[first_word_index][0]
        else:
            start_time = timestamps[first_word_index][0]

        if last_word_index + 1 < len(timestamps):
            end_time = timestamps[last_word_index + 1][0]
            if not end_time:
                end_time = timestamps[last_word_index][1]
        else:
            end_time = timestamps[last_word_index][1]
            if not end_time:
                end_time = start_time

        start_ts = format_timestamp(start_time)
        end_ts = format_timestamp(end_time)

        result.append({
            "line": line,
            "start_time": start_ts,
            "end_time": end_ts
        })

        word_index = last_word_index + 1

    return result


def format_timestamp(seconds: float) -> str:
    try:
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = td.microseconds // 1000
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    except:
        return "00:00:00,000"

def generate_sentence(subtitles: list) -> str:
    result = []
    for i, entry in enumerate(subtitles, start=1):
        start_time = format_timestamp(entry["timestamp"][0])
        end_time = format_timestamp(entry["timestamp"][1])
        result.append({
            "line": entry['text'],
            "start_time": start_time,
            "end_time": end_time
        })

    return result

def wrap_text(text, width=MAX_ROW_LEN):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    wrapped_lines = []

    for sentence in sentences:
        if len(sentence) > width:
            parts = re.split(r'(, )', sentence)
            current_line = ""
            for part in parts:
                if len(current_line) + len(part) <= width:
                    current_line += part
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = part

            if current_line:
                wrapped_lines.append(current_line.strip())
        else:
            wrapped_lines.append(sentence.strip())

    final_output = []
    for line in wrapped_lines:
        if len(line) > width:
            final_output.extend(textwrap.wrap(line, width=width))
        else:
            final_output.append(line)

    return "\n".join(final_output)

from filewriter import writefile


def create_subtitle(path,output,ts_sentences):
    srt_output = []
    for i, entry in enumerate(ts_sentences, start=1):
        line = entry["line"]
        start_time = entry["start_time"]
        end_time =entry["end_time"]
        srt_output.append(f"{i}\n{start_time} --> {end_time}\n{line}\n")
    srt = "\n".join(srt_output)
    writefile(srt, path, output, "srt")
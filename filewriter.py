import os


def writefile(text, path, name, extension):
    output_file = os.path.join(path, f"{name}.{extension}")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)

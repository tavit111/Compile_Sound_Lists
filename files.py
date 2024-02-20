import os
import re
from pathlib import Path
from itertools import repeat
import csv

dialect = csv.unix_dialect()
dialect.delimiter = ","
dialect.quotechar = "'"


def natural_sort(strings):
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]

    sorted_strings = sorted(strings, key=alphanum_key)
    return sorted_strings


def list_directories(root):
    folders = [item for item in os.listdir(
        root) if Path(root, item).is_dir()]
    sorted = natural_sort(folders)
    return [Path(root, folder) for folder in sorted]


def extractMusicPath(dirs):
    index = -1
    music = ''
    for i, path in enumerate(dirs):
        if path.name.strip() in ['music', 'background', 'bacgraound_muisc', 'bg', 'bg_music']:
            index = i

    if index > -1:
        music = Path(dirs[index])
        del dirs[index]

    return dirs, music


def is_mp3_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension == ".mp3"


def is_text_file(file_path):
    try:
        with open(file_path, "r") as f:
            f.readline()
        return True
    except UnicodeDecodeError:
        return False


def list_mp3s(directory_path):
    # return all the mp3 paths, sorted in natural order
    if not directory_path:
        return []

    files = os.listdir(directory_path)
    filtered_files = [file for file in files if is_mp3_file(file)]
    sorted_files = natural_sort(filtered_files)
    file_paths = [os.path.join(directory_path, file) for file in sorted_files]

    return file_paths


def list_text_files(directory_path):
    files = os.listdir(directory_path.absolute())
    sorted_files = natural_sort(files)
    paths = [Path(directory_path, file) for file in sorted_files]
    file_paths = [path for path in paths if os.path.isfile(path.absolute())]
    filtered_files = [file.absolute()
                      for file in file_paths if is_text_file(file)]

    return filtered_files


def get_missing_contunity_of_numbered_files(files):
    missing_indices = []

    extracted_numbers = []
    for file in files:
        file_name = os.path.basename(file)
        name = os.path.splitext(file_name)[0]
        extracted_numbers_from_files = re.findall(r"\d+", name)

        if not len(extracted_numbers_from_files):
            continue

        extracted_number = extracted_numbers_from_files[0]
        extracted_numbers.append(int(extracted_number))

    try:
        consecutive_numbers = [n for n in range(1, max(extracted_numbers)+1)]
    except:
        consecutive_numbers = []

    missing_indices = [
        index for index, consecutive in enumerate(consecutive_numbers) if consecutive not in extracted_numbers]

    return missing_indices


def extract_transcript(directory_path):
    paths = list_text_files(directory_path)

    if len(paths) == 0:
        return []

    if len(paths) == 1 and paths[0].name.lower() in ["text", "script", "transcription", "transcript", "subs", "sub", "subtitles"]:
        with open(paths[0], 'r') as text_file:
            lines = text_file.readlines()
            return [line.strip() for line in lines]

    lines = []
    for path in paths:
        with open(path, 'r') as file:
            line = file.read()
            lines.append(line)

    missing_indices = get_missing_contunity_of_numbered_files(paths)
    for index in missing_indices:
        lines.insert(index, '')

    return lines


def zip_path_transcript(paths, transcripts, missingAudioIndices=[]):
    missing_count = len(missingAudioIndices)
    for index in missingAudioIndices:
        paths.insert(index, '')

    if len(paths) > len(transcripts):
        diff = len(paths) - len(transcripts)
        transcripts = transcripts + list(repeat('', diff))

    if len(paths) < len(transcripts):
        diff = len(transcripts) - len(paths)
        paths = paths + list(repeat('', diff))

    return [[transcript, path] for path, transcript in zip(paths, transcripts)]


def get_script_dir(root):
    folders = [item for item in os.listdir(
        root) if Path(root, item).is_dir()]
    text_folders = [folder for folder in folders if folder.lower() in ["text", "texts", "script",
                                                                       "scripts", "transcript", "transcripts", "transcription", "transcriptions", "subs", "subtitles"]]

    text_folder = Path(root, text_folders[0]) if text_folders else ''

    return text_folder or root


def readCSV(path, headers=True):
    data = []
    with open(path, newline='') as csv_file:
        reader = csv.reader(csv_file, dialect=dialect)

        for row in reader:
            data.append(row)

        if headers:
            data = data[1:]

    return data


if __name__ == "__main__":
    res = get_script_dir(
        "/home/tavit/Code/Compile_Sound_Lists/media/3 - Freanch")
    print(res)

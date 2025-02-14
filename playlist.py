import os
from files import list_directories, extractMusicPath, list_mp3s, extract_transcript, zip_path_transcript, get_missing_contunity_of_numbered_files, get_script_dir, readCSV
import numpy as np
import random
from table import Table
import math


class Playlist:
    @classmethod
    def creatTable(cls, root_path='', csv_file='', num_arr=np.empty((1,1)), is_anki_path=False):
        if num_arr.any():
            return cls.__read_from_csv(num_arr, root_path, is_anki_path)
        elif csv_file:
            return cls.__read_from_csv(csv_file, root_path, is_anki_path)
        elif root_path:
            return cls.__read_from_dir(root_path)

    @classmethod
    def __read_from_csv(cls, csv_file, root_path, is_anki_path):
        
        if isinstance(csv_file, np.ndarray):
            data = csv_file
        else:
            data = readCSV(csv_file,  False)

        languages_count = len(data[0])/2
        # TODO: if language_count % 2 not 0 than add one column at the end
        if languages_count % 2 != 0:
            data = [[*row, ''] for row in data]
        
        languages_count = math.ceil(languages_count)

        data = np.reshape(data, (-1, languages_count, 2))
        dataId = cls.__addIdsToLanguages(data)

        return Table(dataId, root_path, is_anki_path)

    # TODO: Id system has to be added here
    @classmethod
    def __read_from_dir(cls, root_path):
        if not os.path.isdir(root_path):
            raise FileNotFoundError("Root directory dose not exist")

        dir_paths = list_directories(root_path)
        languages_paths, music_path = extractMusicPath(
            dir_paths)

        languages = []
        for languages_path in languages_paths:
            trasnscription_dir_path = get_script_dir(languages_path)
            mp3_paths = list_mp3s(languages_path)
            transcripts = extract_transcript(trasnscription_dir_path)

            missing_audio_indices = get_missing_contunity_of_numbered_files(
                mp3_paths)

            zipped = zip_path_transcript(
                mp3_paths, transcripts, missing_audio_indices)

            languages.append(zipped)

        max_languages_length = max([len(language) for language in languages])
        for language in languages:
            if len(language) < max_languages_length:
                diff = max_languages_length - len(language)
                language.extend([['', ''] for i in range(diff)])
        swaped_languages = np.swapaxes(languages, 0, 1)

        return Table(swaped_languages, root_path)

    @classmethod
    def __addIdsToLanguages(cls, data):
        dataId = []
        for word in data:
            wordId = []
            for id, language in enumerate(word, start=1):
                wordId.append([id, language[0], language[1]])
            dataId.append(wordId)

        return dataId

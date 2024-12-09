from dataclasses import dataclass
import os
from pydub import AudioSegment
import numpy as np
from audio import Audio
import re
import sys


@dataclass
class Table:
    __table: np.ndarray
    __root: str
    __is_anki_path: bool

    def get_languages_indices(self):
        count = len(self.__table[0])
        return [n for n in range(0, count)]

    def show(self):
        for word in self.__table:
            print("[")
            for language in word:
                print("\t", language)
            print("]")
        
        return type(self)(self.__table, self.__root, self.__is_anki_path)

    def filter(self, language_ids=[]):
        if not language_ids:
            language_ids = self.get_languages_indices()

        if max(language_ids) > len(self.__table[0]):
            raise IndexError("id out of range.")

        table = self.__table
        filtered_table = [self.__filter_language_ids(
            word, language_ids) for word in table]

        return type(self)(filtered_table, self.__root, self.__is_anki_path)

    def __filter_language_ids(self, word, ids):
        return [language for language in word if language[0] in ids]

    def repeatLanguages(self, repeat=0, no_repeat_first_lang=True):
        table = self.__table.repeat(repeat+1, 1)
        if no_repeat_first_lang:
            table = np.delete(table, range(repeat), 1)

        return type(self)(table, self.__root, self.__is_anki_path)

    def repeatWord(self, repeat=0):
        table = self.__table.repeat(repeat+1, 0)

        return type(self)(table, self.__root, self.__is_anki_path)

    def randomLanguageOrder(self):
        table = self.__table
        words_count = len(self.__table)
        [np.random.shuffle(table[i]) for i in range(words_count)]

        return type(self)(table, self.__root, self.__is_anki_path)

    def randomWordOrder(self):
        table = self.__table
        np.random.shuffle(table)

        return type(self)(table, self.__root, self.__is_anki_path)

    def slice(self, start=0, end=-1):
        return type(self)(self.__table[start:end], self.__root, self.__is_anki_path)
    
    def __ankiToNormalPath(self, path):
        if not path:
            return ''

        match = re.search(r'\[sound:(.*?)\]', path)
        
        if not match:
            raise ValueError(f'The input string "{path}" does not contain a valid [sound:filename] pattern.')
        
        return match.group(1)


    def makeAudio(self, series_name='', title_name='', languge_gap=2, word_gap=0, word_speed=1):
        language_silence = AudioSegment.silent(duration=languge_gap * 1000)
        word_silence = AudioSegment.silent(duration=word_gap * 1000)

        wholeSegment = AudioSegment.empty()
        wholeScript = []
        start_time = 0
        for word in self.__table:
            wordSegment = AudioSegment.empty()
            row_script = []
            for language in word:
                script = language[1]
                file_name = language[2]

                if not script:
                    continue
                
                # row_script = script if not row_script else f"{row_script} {script}"
                row_script.append(script)

                if self.__is_anki_path:
                    file_name = self.__ankiToNormalPath(file_name)
                    
                if file_name:
                    file_path = os.path.join(self.__root, file_name)
                    languageSegmet = AudioSegment.from_mp3(file_path)
                    wordSegment = wordSegment + languageSegmet
                    wordSegment = wordSegment + language_silence

            wholeSegment = wholeSegment + wordSegment
            wholeSegment = wholeSegment + word_silence
            # BUG: If I will table.filter([2]) and [2] is just script without file then every time will mesure 0.
            # SOLVED: by adding pickLanguage in saveScript() and saveSrc. I can pick which language will be saved or use combined=True to have them all
            end_time = len(wholeSegment)
            wholeScript.append((start_time, end_time, *row_script))
            start_time = end_time

        return Audio([(wholeSegment, wholeScript)], series_name, title_name)

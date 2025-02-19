from audio import Audio
from pydub import AudioSegment
from dataclasses import dataclass
import numpy as np
import os
import re


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
    
    def length(self):
        return len(self.__table)

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
        new_word = word.copy()

        for language in new_word:
            if language[0] not in ids:
                language[2] = ''
        
        return new_word

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
        """Return new instance of Table with sliced table. Arguments are 1 index start and end at exac number"""
        start = start - 1
        
        return type(self)(self.__table[start:end], self.__root, self.__is_anki_path)
    
    def __ankiToNormalPath(self, path):
        if not path:
            return ''

        match = re.search(r'\[sound:(.*?)\]', path)
        
        if not match:
            raise ValueError(f'The input string "{path}" does not contain a valid [sound:filename] pattern.')
        
        return match.group(1)

    def makeAudio(self, silcen_duration=2):
        silenceSegment = AudioSegment.silent(duration=silcen_duration * 1000)

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
                
                row_script.append(script)

                if self.__is_anki_path:
                    file_name = self.__ankiToNormalPath(file_name)
                    
                if file_name:
                    file_path = os.path.join(self.__root, file_name)
                    languageSegment = AudioSegment.from_mp3(file_path)
                    wordSegment = wordSegment + languageSegment
                    wordSegment = wordSegment + silenceSegment

            wholeSegment = wholeSegment + wordSegment
            wholeSegment = wholeSegment + silenceSegment
            end_time = len(wholeSegment)

            wholeScript.append((start_time, end_time, *row_script))
            start_time = end_time

        return Audio([(wholeSegment, wholeScript)])

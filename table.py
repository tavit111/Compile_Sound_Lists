from dataclasses import dataclass
import os
from pydub import AudioSegment
import numpy as np
from audio import Audio


@dataclass
class Table:
    __table: np.ndarray
    __root: str

    def get_languages_indices(self):
        count = len(self.__table[0])
        return [n for n in range(0, count)]

    def show(self):
        for word in self.__table:
            print("[")
            for language in word:
                print("\t", language)
            print("]")

    def filter(self, language_ids=[]):
        if not language_ids:
            language_ids = self.get_languages_indices()

        if max(language_ids) > len(self.__table[0]):
            raise IndexError("id out of range.")

        table = self.__table
        filtered_table = [self.__filter_language_ids(
            word, language_ids) for word in table]

        return type(self)(filtered_table, self.__root)

    def __filter_language_ids(self, word, ids):
        return [language for language in word if language[0] in ids]

    def repeatLanguages(self, repeat=0, no_repeat_first_lang=True):
        table = self.__table.repeat(repeat+1, 1)
        if no_repeat_first_lang:
            table = np.delete(table, range(repeat), 1)

        return type(self)(table, self.__root)

    def repeatWord(self, repeat=0):
        table = self.__table.repeat(repeat+1, 0)

        return type(self)(table, self.__root)

    def randomLanguageOrder(self):
        table = self.__table
        words_count = len(self.__table)
        [np.random.shuffle(table[i]) for i in range(words_count)]

        return type(self)(table, self.__root)

    def randomWordOrder(self):
        table = self.__table
        np.random.shuffle(table)

        return type(self)(table, self.__root)

    def slice(self, start=0, end=-1):
        return type(self)(self.__table[start:end], self.__root)

    def makeAudio(self, languge_gap=2, word_gap=0, word_speed=1):
        language_silence = AudioSegment.silent(duration=languge_gap * 1000)
        word_silence = AudioSegment.silent(duration=word_gap * 1000)

        wholeSegment = AudioSegment.empty()
        for word in self.__table:
            wordSegment = AudioSegment.empty()

            for language in word:
                if not language[1]:
                    continue

                file_path = os.path.join(self.__root, language[2])
                languageSegmet = AudioSegment.from_mp3(file_path)
                wordSegment = wordSegment + languageSegmet
                wordSegment = wordSegment + language_silence

            wholeSegment = wholeSegment + wordSegment
            wholeSegment = wholeSegment + word_silence

        return Audio([(wholeSegment, '')])

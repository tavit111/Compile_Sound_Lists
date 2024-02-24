from dataclasses import dataclass, field
import os
from pydub import AudioSegment
from pydub.playback import play
from files import list_directories, extractMusicPath, list_mp3s, is_mp3_file, extract_transcript, zip_path_transcript, get_missing_contunity_of_numbered_files, get_script_dir, readCSV
import numpy as np
import random
import math

# HELPER'S FUNCTIONS
# TODO: check __compile is there is stil need for reapet and randomize
# TODO: integreate ids with other functionlities
# TODO: 4. make the channel table 3d
# TODO: 5. make grouping channels functionality
# TODO: 6. make the seperate stats join together to create state with multiple channels

# STATE
# channel_paths = [(path1, script), (path2, script), (path3, script)]


class Playlist:
    @classmethod
    def creatTable(cls, root_path='', csv_file=''):
        if csv_file:
            return cls.__read_from_csv(csv_file, root_path)
        elif root_path:
            return cls.__read_from_dir(root_path)

    @classmethod
    def __read_from_csv(cls, csv_file, root_path):
        data = readCSV(csv_file,  False)

        languages_count = int(len(data[0])/2)
        data = np.reshape(data, (-1, languages_count, 2))
        dataId = cls.__addIdsToLanguages(data)

        return Table(dataId, root_path)

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


@dataclass
class Audio:
    __vocabularySegments: [AudioSegment]
    __music_files: [str] = field(default_factory=list)
    __vocabularySegment_gap: int = 2
    __music_gap: int = 0
    __music_loop: bool = True
    __end_padding: int = 0
    __vocabulary_vol: int = 0
    __music_vol: int = 0

    def setVocabSegmentGaps(self, gap):
        self.__vocabularySegment_gap = gap

    def setMusicGap(self, gap):
        self.__music_gap = gap

    def setMusicLoop(slef, isLooping):
        self.__music_loop = isLooping

    def addEndPad(self, duration):
        self.__end_padding = duration

    def increasVoiceVolume(self, vol):
        self.__vocabulary_vol = vol

    def increasMusicVolume(self, vol):
        self.__music_vol = vol

    def addAudio(self, audioSegments):
        segments = audioSegments.getSegments()
        self.__vocabularySegments.extend(segments)

    def getSegments(self):
        return self.__vocabularySegments

    def __compile(self, repeat=0, randomize=False):
        # segment is tuple (AudioSegment, list_of_caption)
        segments = self.__vocabularySegments

        # VOCABS
        # parameter
        if repeat:
            repeated = []
            for segment in segments:
                for i in range(repeat+1):
                    repeated.append(segment)
            segments = repeated

        if randomize:
            random.shuffle(segments)

        # compilation
        allVocabularySegments = AudioSegment.empty()
        silenceGap = AudioSegment.silent(
            duration=self.__vocabularySegment_gap*1000)
        for segment in segments:
            allVocabularySegments = allVocabularySegments + segment[0]
            allVocabularySegments = allVocabularySegments.apply_gain(
                self.__vocabulary_vol)
            allVocabularySegments = allVocabularySegments + silenceGap

        allVocabularySegments = allVocabularySegments + \
            AudioSegment.silent(duration=self.__end_padding*1000)

        # MUISC
        music = AudioSegment.empty()
        music_silence = AudioSegment.silent(duration=self.__music_gap*1000)
        for path in self.__music_files:
            music = AudioSegment.from_mp3(path)
            # for i in range(music_repeat+1):
            #     music = music + song
            music = music + music_silence
        music = music.apply_gain(self.__music_vol)

        # JOIN VOCABS & MUSIC
        if self.__music_files:
            allVocabularySegments = allVocabularySegments.overlay(
                music, loop=self.__music_loop)

        # TODO: make list of captions
        list_of_caption = ''
        # return allVocabularySegments, list_of_caption
        return allVocabularySegments

    def addMusic(self, path):
        if not is_mp3_file(path):
            raise Exception("Not an mp3 file. addMusic require mp3 file path")

        self.__music_files.append(path)

    def play(self, limit=-1):
        limit = limit*1000 if limit > -1 else -1

        audioSegment = self.__compile()
        play(audioSegment[:limit])

    def saveMp3(self, path=''):
        if not path:
            path = os.getcwd() + '/list.mp3'

        audiosegment = self.__compile()
        audiosegment.export(path, format='mp3')

        print(f"Compilation saved succesfuly in {path}")

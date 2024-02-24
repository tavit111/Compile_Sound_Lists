from dataclasses import dataclass, field
import os
from pydub import AudioSegment
from pydub.playback import play
from files import list_directories, extractMusicPath, list_mp3s, is_mp3_file, extract_transcript, zip_path_transcript, get_missing_contunity_of_numbered_files, get_script_dir, readCSV
import numpy as np
import random
import math

# HELPER'S FUNCTIONS
# TODO: Rename channel to language and word to
# TODO: integreate ids with other functionlities
# TODO: 4. make the channel table 3d
# TODO: 5. make grouping channels functionality
# TODO: 6. make the seperate stats join together to create state with multiple channels

# STATE
# channel_paths = [(path1, script), (path2, script), (path3, script)]


class State:
    chanels = []
    music_files = []

    def __init__(self, root, csv):
        State.root_path = root
        self.__root_path = root
        self.__music_dir = ''
        self.__read_music()
        self.setting_file = ''

    @staticmethod
    def get_chanels_indexis():
        count = len(State.chanels[0])
        return [n for n in range(0, count)]

    def __read_music(self):
        if not self.__music_dir and not self.__root_path:
            return

        if self.__music_dir:
            music_path = self.__music_dir

        elif self.__root_path:
            dir_paths = list_directories(self.__root_path)
            chanel_paths, music_path = extractMusicPath(
                dir_paths)

        music_paths = list_mp3s(music_path)

        for path in music_paths:
            State.music_files.append(path)


class Playlist:
    @classmethod
    def creatTable(cls, root_path='', csv_file=''):
        if csv_file:
            return cls.__read_chanels_from_csv(csv_file, root_path)
        elif root_path:
            return cls.__read_chanels_from_files(root_path)

    @classmethod
    def __read_chanels_from_csv(cls, csv_file, root_path):
        data = readCSV(csv_file,  False)

        chanel_count = int(len(data[0])/2)
        data = np.reshape(data, (-1, chanel_count, 2))
        dataId = cls.__addIdsToChannels(data)

        return Table(dataId, root_path)

    # TODO: Id system has to be added here
    @classmethod
    def __read_chanels_from_files(cls, root_path):
        if not os.path.isdir(root_path):
            raise FileNotFoundError("Root directory dose not exist")

        dir_paths = list_directories(root_path)
        chanel_paths, music_path = extractMusicPath(
            dir_paths)

        chanels = []
        for chanel_path in chanel_paths:
            trasnscription_dir_path = get_script_dir(chanel_path)
            mp3_paths = list_mp3s(chanel_path)
            transcripts = extract_transcript(trasnscription_dir_path)

            missing_audio_indices = get_missing_contunity_of_numbered_files(
                mp3_paths)

            zipped = zip_path_transcript(
                mp3_paths, transcripts, missing_audio_indices)

            chanels.append(zipped)

        max_chanel_length = max([len(chanel) for chanel in chanels])
        for chanel in chanels:
            if len(chanel) < max_chanel_length:
                diff = max_chanel_length - len(chanel)
                chanel.extend([['', ''] for i in range(diff)])
        swaped_chanels = np.swapaxes(chanels, 0, 1)

        return Table(swaped_chanels, root_path)

    @classmethod
    def __addIdsToChannels(cls, data):
        dataId = []
        for word in data:
            wordId = []
            for id, chanel in enumerate(word, start=1):
                wordId.append([id, chanel[0], chanel[1]])
            dataId.append(wordId)

        return dataId


@dataclass
class Table:
    __table: np.ndarray
    __root: str

    def get_chanels_indexis(self):
        count = len(self.__table[0])
        return [n for n in range(0, count)]

    def show(self):
        for chanel in self.__table:
            print("[")
            for file in chanel:
                print("\t", file)
            print("]")

    def filter(self, chanel_ids=[]):
        if not chanel_ids:
            chanel_ids = self.get_chanels_indexis()

        if max(chanel_ids) > len(self.__table[0]):
            raise IndexError("channels out of range.")

        table = self.__table
        filtered_table = [self.__filter_channel_ids(
            word, chanel_ids) for word in table]

        return type(self)(filtered_table, self.__root)

    def __filter_channel_ids(self, word, ids):
        return [chanel for chanel in word if chanel[0] in ids]

    def repeatChanels(self, repeat=0, no_repeat_first_ch=True):
        interval = self.__table.repeat(repeat+1, 1)
        if no_repeat_first_ch:
            interval = np.delete(interval, range(repeat), 1)

        return type(self)(interval, self.__root)

    def repeatWord(self, repeat=0):
        interval = self.__table.repeat(repeat+1, 0)

        return type(self)(interval, self.__root)

    def randomizeChannels(self):
        interval = self.__table
        word_count = len(self.__table)
        [np.random.shuffle(interval[i]) for i in range(word_count)]

        return type(self)(interval, self.__root)

    def randomizeWords(self):
        interval = self.__table
        np.random.shuffle(interval)

        return type(self)(interval, self.__root)

    def slice(self, start=0, end=-1):
        return type(self)(self.__table[start:end], self.__root)

    def makeInterval(self, chanel_gap=2, word_gap=0, word_speed=1):
        channel_silence = AudioSegment.silent(duration=chanel_gap * 1000)
        word_silence = AudioSegment.silent(duration=word_gap * 1000)

        intervalSegment = AudioSegment.empty()
        for word in self.__table:
            wordSegment = AudioSegment.empty()

            for chanel in word:
                if not chanel[1]:
                    continue

                file_path = os.path.join(self.__root, chanel[1])
                chanelSegmet = AudioSegment.from_mp3(file_path)
                wordSegment = wordSegment + chanelSegmet
                wordSegment = wordSegment + channel_silence

            intervalSegment = intervalSegment + wordSegment
            intervalSegment = intervalSegment + word_silence

        return Audio([(intervalSegment, '')])


@dataclass
class Audio:
    __intervalSegments: [AudioSegment]
    __music_files: [str] = field(default_factory=list)
    __interval_gap: int = 2
    __music_gap: int = 0
    __music_loop: bool = True
    __end_padding: int = 0
    __voice_vol: int = 0
    __music_vol: int = 0

    def setIntervalGap(self, gap):
        self.__interval_gap = gap

    def setMusicGap(self, gap):
        self.__music_gap = gap

    def setMusicLoop(slef, isLooping):
        self.__music_loop = isLooping

    def addEndPad(self, duration):
        self.__end_padding = duration

    def increasVoiceVolume(self, vol):
        self.__voice_vol = vol

    def increasMusicVolume(self, vol):
        self.__music_vol = vol

    def addSegments(self, intervals):
        segments = intervals.getSegments()
        self.__intervalSegments.extend(segments)

    def getSegments(self):
        return self.__intervalSegments

    def __compile(self, repeat=0, randomize=False):
        # interval is tuple (AudioSegment, list_of_caption)
        intervals = self.__intervalSegments

        # VOCABS
        # parameter
        if repeat:
            repeated = []
            for interval in intervals:
                for i in range(repeat+1):
                    repeated.append(interval)
            intervals = repeated

        if randomize:
            random.shuffle(intervals)

        # compilation
        intervalsSegments = AudioSegment.empty()
        intervalSilence = AudioSegment.silent(
            duration=self.__interval_gap*1000)
        for interval in intervals:
            intervalsSegments = intervalsSegments + interval[0]
            intervalsSegments = intervalsSegments.apply_gain(self.__voice_vol)
            intervalsSegments = intervalsSegments + intervalSilence

        intervalsSegments = intervalsSegments + \
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
            intervalsSegments = intervalsSegments.overlay(
                music, loop=self.__music_loop)

        # TODO: make list of captions
        list_of_caption = ''
        # return intervalsSegments, list_of_caption
        return intervalsSegments

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

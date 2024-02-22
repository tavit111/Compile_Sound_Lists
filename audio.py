from dataclasses import dataclass
import os
from pydub import AudioSegment
from pydub.playback import play
from files import list_directories, extractMusicPath, list_mp3s, extract_transcript, zip_path_transcript, get_missing_contunity_of_numbered_files, get_script_dir, readCSV
import numpy as np
import random
import math

# HELPER'S FUNCTIONS

# TODO: 3 move the create interval into the State class
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

    def filter(self, channels=[]):
        if not channels:
            channels = self.get_chanels_indexis()

        if max(channels) > len(self.__table[0]) - 1:
            raise IndexError("channels out of range.")

        table = self.__table[:, channels]
        return type(self)(table, self.__root)

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

        return Table(data, root_path)

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


def playTest(segment):
    play(segment)


def makeInterval(chanel_gap=2, word_gap=0, word_speed=1):

    # interval = np.array(State.chanels[:word_count])

    # BUG: we need random in groups (when reped channel) and that include the were the first word is not repete

    channel_silence = AudioSegment.silent(duration=chanel_gap * 1000)
    word_silence = AudioSegment.silent(duration=word_gap * 1000)

    intervalSegment = AudioSegment.empty()

    for word in interval:
        wordSegment = AudioSegment.empty()

        for chanel in word:
            if not chanel[1]:
                continue

            file_path = os.path.join(State.root_path, chanel[1])

            chanelSegmet = AudioSegment.from_mp3(file_path)
            wordSegment = wordSegment + chanelSegmet
            wordSegment = wordSegment + channel_silence

        intervalSegment = intervalSegment + wordSegment
        intervalSegment = intervalSegment + word_silence

    return (intervalSegment, '')


def joinIntervals(intervals, music_gap=0, interval_gap=0, repeat=0, randomize=False, music_mute=False, music_loop=True, music_repeat=0, music_vol=0, voice_vol=0, end_padding=0):
    # interval is tuple (AudioSegment, list_of_caption)

    #   VOCABS
    if repeat:
        repeated = []
        for interval in intervals:
            for i in range(repeat+1):
                repeated.append(interval)

        intervals = repeated

    if randomize:
        random.shuffle(intervals)

    intervalsSegments = AudioSegment.empty()
    intervalSilence = AudioSegment.silent(duration=interval_gap*1000)
    for interval in intervals:
        intervalsSegments = intervalsSegments + interval[0]
        intervalsSegments = intervalsSegments + intervalSilence

    intervalsSegments = intervalsSegments + \
        AudioSegment.silent(duration=end_padding*1000)

    #   MUISC
    if music_mute:
        State.music_files = []

    music = AudioSegment.empty()
    music_silence = AudioSegment.silent(duration=music_gap*1000)
    for path in State.music_files:
        song = AudioSegment.from_mp3(path)
        for i in range(music_repeat+1):
            music = music + song
            music = music + music_vol
        music = music + music_silence

    # JOIN
    if State.music_files:
        intervalsSegments = intervalsSegments.overlay(
            music, gain_during_overlay=voice_vol, loop=music_loop)

    # TODO: make list of captions
    list_of_caption = ''
    return intervalsSegments, list_of_caption


def saveMp3(audiosegment, path=''):
    if not path:
        path = os.getcwd() + '/list.mp3'

    audiosegment.export(path, format='mp3')

    print(f"Compilation saved succesfuly in {path}")

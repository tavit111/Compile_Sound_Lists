import os
from pydub import AudioSegment
from pydub.playback import play
from files import list_directories, extractMusicPath, list_mp3s, extract_transcript, zip_path_transcript, get_missing_contunity_of_numbered_files, get_script_dir, readCSV
import numpy as np
import random
import math

# HELPER'S FUNCTIONS


# STATE
# channel_paths = [(path1, script), (path2, script), (path3, script)]
class State:
    chanels = []
    music_files = []

    def __init__(self, root='', music_dir='', csv_file='', setting_file=''):
        self.__root_path = root
        self.__music_dir = music_dir
        self.__csv_file = csv_file
        self.__setting_file = setting_file
        self.__detectChanels()

    @staticmethod
    def get_chanels_indexis():
        count = len(State.chanels[0])
        return [n for n in range(0, count)]

    def __read_chanels_from_csv(self):
        data = readCSV(self.__csv_file,  False)

        columns_count = len(data[0])
        if columns_count % 2 != 0:
            data = [[*row, ''] for row in data]

        chanel_count = int(len(data[0])/2)
        data = np.reshape(data, (-1, chanel_count, 2)).tolist()

        State.chanels = data

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

    def __read_chanels_from_files(self):
        if not os.path.isdir(self.__root_path):
            raise FileNotFoundError("Root directory dose not exist")

        dir_paths = list_directories(self.__root_path)
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
        swaped_chanels = np.swapaxes(chanels, 0, 1).tolist()
        State.chanels = swaped_chanels

    def __detectChanels(self):
        if self.__csv_file:
            self.__read_chanels_from_csv()
        elif self.__root_path:
            self.__read_chanels_from_files()
        self.__read_music()

    def showChanels(self):
        print("CHANELS")
        for chanel in State.chanels:
            print("[")
            for file in chanel:
                print("\t", file)
            print("]")

        print()
        print("MUSIC")
        for music_path in State.music_files:
            print("\t", music_path)


# showChanels()


def setChanels(setting_file=''):
    # if there is a setting file then don't do any setting twicking
    # set each channel for speed and gains
    # set the backgroudn music for speed and gains
    # playback everithing to test it:
    #   - play all channels against the each backgroud music
    #   - insceas and secres settings for each channel and musci
    # update the state
    pass


def playTest(segment):
    play(segment)


def makeInterval(word_count=0, use_channels=[], repeat_chanel=0, no_repeat_first_ch=False, repeat_word=0, randomize_channels=False, randomize_words=False, chanel_gap=2, word_gap=0, word_speed=1):
    if not use_channels:
        use_channels = State.get_chanels_indexis()

    if max(use_channels) > len(State.chanels[0]) - 1:
        raise IndexError("use_channels out of range.")

    if not word_count:
        word_count = len(State.chanels)

    interval = State.chanels[:word_count]

    if repeat_chanel:
        interval = interval.repeat(repeat_chanel+1, 1)
        if no_repeat_first_ch:
            interval = np.delete(interval, range(repeat_chanel), 1)

    if repeat_word:
        interval = interval.repeat(repeat_word+1, 0)

    if randomize_channels:
        [np.random.shuffle(interval[i]) for i in range(word_count)]

    if randomize_words:
        np.random.shuffle(interval)

    channel_silence = AudioSegment.silent(duration=chanel_gap * 1000)
    word_silence = AudioSegment.silent(duration=word_gap * 1000)

    intervalSegment = AudioSegment.empty()
    for word in interval:
        wordSegment = AudioSegment.empty()

        for chanel in word:
            if not chanel[0]:
                continue

            chanelSegmet = AudioSegment.from_mp3(chanel[0])
            wordSegment = wordSegment + chanelSegmet
            wordSegment = wordSegment + channel_silence

        intervalSegment = intervalSegment + wordSegment
        intervalSegment = intervalSegment + word_silence

    return (intervalSegment, '')


def joinIntervals(intervals, music_gap=0, interval_gap=0, repeat=0, randomize=False, music_loop=True, music_repeat=0, music_vol=0, voice_vol=0, end_padding=0):
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

    music = AudioSegment.empty()
    music_silence = AudioSegment.silent(duration=music_gap*1000)
    for path in State.music_files:
        song = AudioSegment.from_mp3(path)
        for i in range(music_repeat+1):
            music = music + song
            music = music + music_vol
        music = music + music_silence

    # JOIN
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

import os
from pydub import AudioSegment
from pydub.playback import play
from files import list_directories, extractMusicPath, list_mp3s, extract_transcript, zip_path_transcript, get_missing_contunity_of_numbered_files, get_script_dir
import numpy as np
import random
import math

#######   HOW TO    ######
# 1. In root folder all the channels and music folder will be detected automaticy
# 2. To each channel will be assigne number by the natural sort of the folder names
# 3. You can give the path to the music folder but it have to be without / at the end
# 4. If path to music is ommited, than it wil be detected in root folder if have the name "music, background, background_music, bg_music, bg" case insenfitive
# 5. In each channl (folder) will be search for mp3 file and script files
# 6. mp3 file will be detected automaticly directly in the channel's folder
# 7. for the best result number each file consecutivly
# 8. script files will be first looked in the diretory called "text", "texts", "script", "scripts", "transcript", "transcripts", "transcription", "transcriptions", "subs", "subtitles"
# 9. if no directory of the fallowing names, than it will look into the channels directory
# 10. in both cases: first it will look for one text file named "text", "script", "transcription", "transcript", "subs", "sub", "subtitles". Each line will be corespoding to each file by given number. If some line wll be emptu then that audio file will not have script
# 11. if there is more then 1 text files then each file's content coresponding by number will match each audio file. If some text fills are missing (1, 3, 4) then that audio file will not have script (2.mp3).
# 12. If there are missing scripts then the that word will not contain script
# 13. If there are missing audtio then the TTS engine will creat it into audio
# TODO: csv files


# HELPER'S FUNCTIONS

def showChanels(chanels):
    for chanel in chanels:
        print("[")
        for file in chanel:
            print(file)
        print("]")


# STATE
# channel_paths = [(path1, script), (path2, script), (path3, cscript)]
chanels = []
# chanels_settigs = [
#     {id: 0, speed: 1, gain: 0}
# ]
# music_paths_settings = [(path, gain, speed), (path, gain, speed)]
music_files = []

# SETTING JSON FILE INPUT AND OUTPUT
# channels: [folder_name, gain, sepeed], [folder_name, gain, sepeed]
# musci: {sorseAndSettings: [file_name, gain, speed], gap: 20}

# CSV INPUT
# csv with colums: file path, script. This allowy to make custom channes or generating
# if file path is ommited then the script hase to use tts
# if the script is ommited then the script will not generate subs

# SUBS OUTPUT
# csv with colums: time begening of word, time end of word, script


def detectChanels(root_path, music_path='', setting_file=''):
    if not os.path.isdir(root_path):
        raise FileNotFoundError("Root directory dose not exist")
    if music_path and not os.path.isdir(music_path):
        raise FileNotFoundError("Music directory dose not exits")
    # if the root path is scv then dont't scan the folder and don't sort them
    # extract path to all the mp3 files in each
    # music path to he background musci. If it empty then ommit the musci
    # extract musci paths
    # twick each channel for vol and speed

    # set the state of the channels 2d array [
    # [(path1, script), (path2, script), (path3, script), (path3, script)], | <-- this one word consists of 4 channels
    # [(path1, script), (path2, script), (path3, script), (path3, script)]
    # ]

    # set the state of the music

    def read_chanels_from_files(root_path, music_path):

        dir_paths = list_directories(root_path)
        chanel_paths, music_path = extractMusicPath(dir_paths, music_path)

        for chanel_path in chanel_paths:
            trasnscription_dir_path = get_script_dir(chanel_path)
            mp3_paths = list_mp3s(chanel_path)
            transcripts = extract_transcript(trasnscription_dir_path)

            missing_audio_indices = get_missing_contunity_of_numbered_files(
                mp3_paths)

            zipped = zip_path_transcript(
                mp3_paths, transcripts, missing_audio_indices)

            chanels.append(zipped)

        music_paths = list_mp3s(music_path)

        for path in music_paths:
            music_files.append(path)

    # list_csv(root, music_path)
        # if there is one csv split it to channels
        # if more ten one use arleady splited
        # return csv_chanels
    # read_channels_from_csv(csv_chanels)
    # TODO: Test  diffrent functions
    # TODO: Test if ther is not enotuth in one
    read_chanels_from_files(root_path, music_path)
    # chanels = [[word for word in chanel] for chanel in chanels]
    # we will swap axes in make interval
    # swapped = np.swapaxes(chanels, 0, 1)
    # print(chanels)
    # showChanels(rotated)


detectChanels(
    './media', '/home/tavit/Code/Compile_Sound_Lists/media/music')


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


def assigne_all_channels():
    count = len(chanels)
    return [n for n in range(0, count)]


def makeInterval(word_count=0, use_channels=assigne_all_channels(), repeat_chanel=0, no_repeat_first_ch=False, repeat_word=0, randomize_channels=False, randomize_words=False, chanel_gap=2, word_gap=0, word_speed=1):
    if max(use_channels) > len(chanels) - 1:
        raise IndexError("use_channels out of range.")

    max_count = min([len(chanels[index]) for index in use_channels])
    if word_count > max_count:
        raise IndexError(
            f"One of the chanels has maximum items of {max_count} and you requested {word_count}")

    if not word_count:
        word_count = max_count

    chanel_chunks = np.array([chanels[i][:word_count] for i in use_channels])

    interval = chanel_chunks.swapaxes(0, 1)

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

    # print(interval)

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

    # params:
    #
    #         word_count - number of words for interval
    #         use_channels - display channesl in certin order, or ommit the one not listed [0,1,2,3] | [2,1,3,0] | [0,2,3]
    #         randomize_channel - for every word the order of channel is diffrent. If the channel is ommited in show_channels it wil be ommited
    #         randomize_words - show wods in random order

    # return AudioSegment, list of captions


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
    for path in music_files:
        song = AudioSegment.from_mp3(path)
        for i in range(music_repeat+1):
            music = music + song
            music = music + music_vol
        music = music + music_silence

    # JOIN
    intervalsSegments = intervalsSegments.overlay(
        music, gain_during_overlay=voice_vol, loop=music_loop)

    playTest(intervalsSegments)

    # return AudioSegment, list_of_caption


intervalA = makeInterval(5, [0, 1], chanel_gap=1)
intervalB = makeInterval(5, [2, 3], chanel_gap=1)

joinIntervals([intervalA, intervalB], interval_gap=2,
              repeat=5, randomize=True, music_gap=5, music_repeat=1, music_vol=-5, voice_vol=5)

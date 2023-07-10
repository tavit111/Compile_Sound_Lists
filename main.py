import os
from pydub import AudioSegment
from files import list_directories, extractMusicPath, list_mp3s, extract_transcript, zip_path_transcript, get_missing_contunity_of_numbered_files, get_script_dir


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

# STATE
# channel_paths = [(path1, script), (path2, script), (path3, cscript)]
chanels = []
# chanels_settigs = [
#     {id: 0, speed: 1, gain: 0}
# ]
# music_paths_settings = [(path, gain, speed), (path, gain, speed)]
background_musci = []

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

    dir_paths = list_directories(root_path)
    chanel_paths, music_path = extractMusicPath(dir_paths, music_path)

    for chanel_path in chanel_paths:
        trasnscription_dir_path = get_script_dir(chanel_path)
        print("trasnscription_dir_path", trasnscription_dir_path)
        mp3_paths = list_mp3s(chanel_path)
        transcripts = extract_transcript(trasnscription_dir_path)

        missing_audio_indices = get_missing_contunity_of_numbered_files(
            mp3_paths)

        zipped = zip_path_transcript(
            mp3_paths, transcripts, missing_audio_indices)

        chanels.append(zipped)


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


def playTest():
    pass
    # play audio from state for testing
    # play audio from make intervals
    # play audio from join intervals


def makeInterval(word_count, use_channels, repeat_channel=1, repeat_word=1, randomize_channels=False, randomize_words=False, chanel_gap=2, word_gap=0, word_speed=1):
    # params:
    #
    #         word_count - number of words for interval
    #         use_channels - display channesl in certin order, or ommit the one not listed [0,1,2,3] | [2,1,3,0] | [0,2,3]
    #         randomize_channel - for every word the order of channel is diffrent. If the channel is ommited in show_channels it wil be ommited
    #         randomize_words - show wods in random order
    pass
    # return AudioSegment, list of captions


def joinIntervals(intervals, music_gap=0, repeat=1, randomize=False):
    # interval is tuple (AudioSegment, list_of_caption)

    # join the intervals toghether,
    # join the captions together
    # add backgroud musci
    pass
    # return AudioSegment, list_of_caption


# HELPER'S FUNCTIONS

def showChanels():
    for chanel in chanels:
        print("[")
        for file in chanel:
            print(file)
        print("]")


showChanels()

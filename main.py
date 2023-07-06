from pydub import AudioSegment

# STATE
channel_paths = [(path1, script), (path2, script), (path3, script)]
chanels_settigs = [
    {id: 0, speed: 1, gain: 0}
]
music_paths_settings = [(path, gain, speed), (path, gain, speed)]


# SETTING JSON FILE INPUT AND OUTPUT
# channels: [folder_name, gain, sepeed], [folder_name, gain, sepeed]
# musci: {sorseAndSettings: [file_name, gain, speed], gap: 20}

# CSV INPUT
# csv with colums: file path, script. This allowy to make custom channes or generating
# if file path is ommited then the script hase to use tts
# if the script is ommited then the script will not generate subs

# SUBS OUTPUT
# csv with colums: time begening of word, time end of word, script


def detectChanels(root_path, musci_path='', setting_file=''):
    # scan root dir for folders,
    # sort them in natural order
    # if the root path is scv then dont't scan the folder and don't sort them
    # extract path to all the mp3 files in each
    # music path to he background musci. If it empty then ommit the musci
    # extract musci paths
    # twick each channel for vol and speed
    pass
    # set the state of the channels 2d array [
    # [(path1, script), (path2, script), (path3, script), (path3, script)], | <-- this one word consists of 4 channels
    # [(path1, script), (path2, script), (path3, script), (path3, script)]
    # ]

    # set the state of the music

# TODO: setChanels and playTest make it resusable
# TODO: genrate and re-use setings repport: tempo and gain for each channel name and musci(folder), silence gap for music


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

from audio import makeInterval, joinIntervals, saveMp3, State

# TODO: make csv multi channel
# TODO: make some channels miss the files


# State.detectChanels(
#     './media', '/home/tavit/Code/Compile_Sound_Lists/media/music')

s = State(
    root='/home/tavit/Code/Compile_Sound_Lists/media/fiszki-root/',
    csv_file="/home/tavit/Code/Compile_Sound_Lists/media/fiszki-root/transcript.csv"
    # music_dir='/home/tavit/Code/Compile_Sound_Lists/media/music'
)
# s.showChanels()
# intervalA = makeInterval(chanel_gap=1)


intervalB = makeInterval(
    5, chanel_gap=1, repeat_chanel=1, repeat_word=0, no_repeat_first_ch=False, randomize_channels=True)


res, cap = joinIntervals([intervalB], interval_gap=2,
                         repeat=1, randomize=False, music_mute=True)


saveMp3(res, path="/home/tavit/Code/Compile_Sound_Lists/media/fiszki_compilation.mp3")

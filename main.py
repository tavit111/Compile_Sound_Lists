from audio import makeInterval, joinIntervals, saveMp3, State

# TODO: make csv multi channel
# TODO: make some channels miss the files


# State.detectChanels(
#     './media', '/home/tavit/Code/Compile_Sound_Lists/media/music')

s = State(
    root='./media/',
    csv_file="./media/input.csv"
    # music_dir='/home/tavit/Code/Compile_Sound_Lists/media/music'
)
# s.showChanels()
# intervalA = makeInterval(chanel_gap=1)


intervalB = makeInterval(
    5, chanel_gap=1, repeat_chanel=2, repeat_word=2, no_repeat_first_ch=True, randomize_channels=False)


res, cap = joinIntervals([intervalB], interval_gap=2,
                         repeat=1, randomize=False, music_mute=False)


saveMp3(res, path="/home/tavit/Code/Compile_Sound_Lists/media/compilationA.mp3")

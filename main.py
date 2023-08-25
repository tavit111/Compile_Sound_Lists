from audio import makeInterval, joinIntervals, saveMp3, State


# State.detectChanels(
#     './media', '/home/tavit/Code/Compile_Sound_Lists/media/music')

s = State(
    root='./media/',
    # csv_file="./media/input.csv",
    music_dir='/home/tavit/Code/Compile_Sound_Lists/media/music'
)
# s.showChanels()
intervalA = makeInterval(chanel_gap=1)
intervalB = makeInterval(5, [0], chanel_gap=1)


res, cap = joinIntervals([intervalA, intervalB], interval_gap=2,
                         repeat=5, randomize=True, music_gap=5, music_repeat=1, music_vol=-5, voice_vol=5)


saveMp3(res)

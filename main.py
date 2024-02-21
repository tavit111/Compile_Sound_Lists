from audio import makeInterval, joinIntervals, saveMp3, State, Playlist

# s = State(
#     root='/home/tavit/Code/Compile_Sound_Lists/media/fiszki-root/',
#     csv_file="/home/tavit/Code/Compile_Sound_Lists/media/fiszki-root/transcript.csv"
#     # music_dir='/home/tavit/Code/Compile_Sound_Lists/media/music'
# )
s = State(
    root='/home/tavit/Code/Compile_Sound_Lists/media/',
    csv="/home/tavit/Code/Compile_Sound_Lists/media/input.csv"
)
table1 = Playlist.creatTable(
    root_path='/home/tavit/Code/Compile_Sound_Lists/media/',
    csv_file="/home/tavit/Code/Compile_Sound_Lists/media/input.csv"
)
firstChanel = table1.filter([0])
firstChanel.show()


# fiszki = makeInterval(
#     5, [1, 0, 3, 2, 5, 4], chanel_gap=1, repeat_chanel=0, repeat_word=0, no_repeat_first_ch=False, randomize_channels=False)

# intervalB = makeInterval(
#     5, chanel_gap=1, repeat_chanel=0, repeat_word=0, no_repeat_first_ch=False, randomize_channels=False)


# res, cap = joinIntervals([intervalB], interval_gap=2,
#                          repeat=0, randomize=False, music_mute=True)


# saveMp3(res, path="/home/tavit/Code/Compile_Sound_Lists/media/fiszki_compilation.mp3")

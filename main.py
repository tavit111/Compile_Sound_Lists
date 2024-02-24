from audio import State, Playlist, Audio

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
# table2 = Playlist.creatTable(
#     root_path='/home/tavit/Code/Compile_Sound_Lists/media/',
#     csv_file="/home/tavit/Code/Compile_Sound_Lists/media/input.csv"
# )

table1.filter([3, 2, 1]).show()
# one = table2.filter([2]).slice(2).makeInterval()

# two.addSegments(one)
# two.play()

from playlist import Playlist

# TODO: represent languages by ids or grou them in the same array
# TODO: integreate ids with other functionlities
# TODO: join langugages together
# TODO: import csv as one channel (language) (or 2 channels if there is L1 L2 languages)
# TODO: Add repeat and random shaffle each all adudio segments in Adio


table1 = Playlist.creatTable(
    root_path='/home/tavit/Code/Compile_Sound_Lists/media/',
    csv_file="/home/tavit/Code/Compile_Sound_Lists/media/input.csv"
)

audio = table1.filter([3, 2, 1]).randomLanguageOrder(
).randomWordOrder().slice(0, 2).makeAudio()
audio.play()

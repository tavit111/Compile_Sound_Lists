from audio import Playlist, Audio

table1 = Playlist.creatTable(
    root_path='/home/tavit/Code/Compile_Sound_Lists/media/',
    csv_file="/home/tavit/Code/Compile_Sound_Lists/media/input.csv"
)

audio = table1.filter([3, 2, 1]).randomLanguageOrder(
).randomWordOrder().slice(0, 2).makeAudio()
audio.saveMp3()

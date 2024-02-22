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

music_path1 = "/home/tavit/Code/Compile_Sound_Lists/media/empty/1 - mgs2_alert_detected.mp3"
music_path2 = "/home/tavit/Code/Compile_Sound_Lists/media/empty/2 - mgs3_cqc_them.mp3"

chunkAudio = table1.makeInterval()
audio = Audio([chunkAudio])
audio.addMusic(music_path2)
audio.play(5)

# fiszki = makeInterval(
#     5, [1, 0, 3, 2, 5, 4], chanel_gap=1, repeat_chanel=0, repeat_word=0, no_repeat_first_ch=False, randomize_channels=False)

# intervalB = makeInterval(
#     5, chanel_gap=1, repeat_chanel=0, repeat_word=0, no_repeat_first_ch=False, randomize_channels=False)

# saveMp3(res, path="/home/tavit/Code/Compile_Sound_Lists/media/fiszki_compilation.mp3")

from playlist import Playlist

# TODO: represent languages by ids or grou them in the same array
# TODO: integreate ids with other functionlities
# TODO: join langugages together
# TODO: import csv as one channel (language) (or 2 channels if there is L1 L2 languages)
# TODO: Add repeat and random shaffle each all adudio segments in Adio
# IDEA: make function to ignore column by index number


table1 = Playlist.creatTable(
    root_path='/home/tavit/Code/Compile_Sound_Lists/media/iknow_sentences',
    csv_file="/home/tavit/Code/Compile_Sound_Lists/media/iknow_v3.csv",
    is_anki_path=True,
)

#audio = table1.filter([3, 2, 1]).randomLanguageOrder(
#).randomWordOrder().slice(0, 2).makeAudio()
#audio.play()
#audio.play()


#makeAudio(series_name='', title_name='')
#Important for lyric to work. Lyric have to be titled with both of those name and pair mp3 lyric should have uniq combination of both


audio1 = table1.slice(0, 10).makeAudio()
# .makeAudio("iKnow", "1.1_v2")
# randomWordOrder().makeAudio("iKnow", "1.1")
# audio2 = table1.randomWordOrder().makeAudio()
# audio3 = table1.randomWordOrder().makeAudio()

# audio1.addAudio(audio2)
# audio1.addAudio(audio3)

# audio1.saveMp3("./iknow_v2.mp3")
audio1.saveMp3(path="./iknow_v3")
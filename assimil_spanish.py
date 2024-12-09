from playlist import Playlist



table = Playlist.creatTable(
    root_path='/home/tavit/Code/Compile_Sound_Lists/media/assimil_spanish_87/',
    csv_file=f"/home/tavit/Code/Compile_Sound_Lists/media/assimil_spanish_87_lessons_20.csv",
    is_anki_path=False,
)


audio_all = table.filter([2]).makeAudio("Assimil Spanish '87", f"All 20 sp/en").compile()
audio_all.saveMp3(f"compiled/assimil_spanish_20.mp3").saveSrt(f"compiled/assimil_spanish_20.srt", combined=False, pickLanguage=1)

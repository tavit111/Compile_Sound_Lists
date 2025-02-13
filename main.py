from playlist import Playlist

# TODO: represent languages by ids or grou them in the same array
# TODO: integreate ids with other functionlities
# TODO: join langugages together
# TODO: import csv as one channel (language) (or 2 channels if there is L1 L2 languages)
# TODO: Add repeat and random shaffle each all adudio segments in Adio
# IDEA: make function to ignore column by index number


table = Playlist.creatTable(
    root_path='/home/tavit/Code/Compile_Sound_Lists/media/iknow_sentences/',
    csv_file=f"/home/tavit/Code/Compile_Sound_Lists/media/1532_iknow.csv",
    is_anki_path=True
)

def randomized_list(files_number, sentnece_number_per_file):
    # files_number - how many files to generate, sentnece_number_per_file - how many sentences per file you want to have
    
    table_randomized = table.randomWordOrder()
    numbers = range(1, files_number+1)  #make list form 1 to 7 (7 unit blocs)
    count = sentnece_number_per_file
    units = [(n, n*count-count, n*count) for n in numbers]  #100 each unit will have 100 sentences (2 sentence per word)

    for unit in units:
        [id, start, end] = unit
        name = f"{id}_iknow_sentences"
        audio = table_randomized.slice(start, end).makeAudio("iknow 200 sentences", f"Part {id} of 10").compile()
        audio.saveMp3(f"compiled/{name}.mp3").saveSrt(f"compiled/[jp]{name}.srt", combined=False, pickLanguage=1).saveSrt(f"compiled/[en]{name}.srt", combined=False, pickLanguage=2)


def new_words_list(files_number, sentnece_number_per_file):
    # files_number - how many files to generate, sentnece_number_per_file - how many sentences per file you want to have
    
    numbers = range(1, files_number+1)  #make list form 1 to 7 (7 unit blocs)
    count = sentnece_number_per_file
    units = [(n, n*count-count, n*count) for n in numbers]  #100 each unit will have 100 sentences (2 sentence per word)

    for unit in units:
        [id, start, end] = unit
        name = f"{id}_iknow_new_sentences"
        audio = table.slice(start, end).makeAudio("iknow 100 new sentences", f"Part {id} of 10").compile()
        audio.saveMp3(f"compiled/{name}.mp3").saveSrt(f"compiled/[jp]{name}.srt", combined=False, pickLanguage=1).saveSrt(f"compiled/[en]{name}.srt", combined=False, pickLanguage=2)



# randomized_list(10, 100)
new_words_list(7, 100)




################################################################################################
###############################      TESTING AREA      #########################################
################################################################################################

# BUG: I can't have englsih sub over spanish dialog bcouse there is arleady file fore english voice
# TODO: try to add second language on second line of script. Such format: id, time --> time, first language, second language where comma in new line
# TODO: make shifting subtitles e.g it will show up during silence gap or when next sentence is played
# IDEA: each line of subtitle alongside the start, end, script will carry extra int with the number in milsec of gap. This gap information can be used to calculate shifting of time
# TODO: make saveScript(filterLanguages:[2,4] to use with combined=True in order to combine multiple langugages or pick one so combined=True will be redundend)


# test_name="test"
# engjap = table.slice(1, 5).makeAudio("test_5_lines", f"test").compile().saveMp3(f"test/{test_name}.mp3").saveScript(f"test/[jp|en]{test_name}.txt", combined=True).saveSrt(path="test/[jp|en][src]test", combined=True)
# english = table.slice(1, 5).makeAudio("test_5_lines", f"test").compile().saveScript(f"test/[en]{test_name}.txt", combined=False, pickLanguage=2).saveSrt(path="test/[en][src]test", combined=False, pickLanguage=2)
# japanese = table.slice(1, 5).makeAudio("test_5_lines", f"test").compile().saveScript(f"test/[jp]{test_name}.txt", combined=False).saveSrt(path="test/[jp][src]test", combined=False)

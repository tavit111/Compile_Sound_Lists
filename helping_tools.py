import pandas as pd

def make_sets(lenth, step):
    """
    Devide length of table / steps and calcualte ranges indexis (1 index) and id of files
    return iterator of (id, start, end) format where id is file number, start is start index, end is end of index
    """
    
    start = 1
    end = lenth

    for (id, i) in enumerate(range(start, end + 1, step), start=1):
        if i + step - 1 > end:
            yield (id, i, end + 1)
        else:
            yield (id, i, i + step)



def translate_iknow_sentence_list(start=1, end=None):
    """
    Read fron orginal source vocabularies.csv, slice the table (1 index), and traslate it into 3 columns (jp_sentence, jp_anki_path, en_sentence)
    pluse splice the secend example into one 3 column table
    return numpy array of the table
    """

    read_path = "/home/tavit/Shadowing/Sources/iknow_jp/vocabularies.csv"
    start = start - 1

    df = pd.read_csv(read_path, sep=',', quotechar="'")
    df_sliced = df.iloc[start:end]

    first_df = df_sliced.iloc[:, [11, 15, 13]].copy()
    second_df = df_sliced.iloc[:, [17, 21, 19]].copy()

    first_df.columns = ['japanese', 'mp3_path', 'english']
    second_df.columns = ['japanese', 'mp3_path', 'english']

    df_combined = pd.concat([first_df, second_df], axis=0)
    df_filtered_by_sec_examp = df_combined.dropna(subset=[df_combined.columns[1]])
    df_removed_duplicats = df_filtered_by_sec_examp.drop_duplicates()
    
    return df_removed_duplicats.to_numpy()

def translate_assimil(source_df):
    "transalte df of assimil csv lesson to 4 column format returns df"
    table_df = source_df.iloc[:, 3:7].copy()
    return table_df

def translate_assimil_split_by_lesson(surce_csv, start=1, end=None):
    """Rerun 2 lists: lesson number from the csv and numpy tables of each lesson in 4 column format"""
    start = start - 1

    source_df = pd.read_csv(surce_csv, sep=',', quotechar="'")
    id_lesson = source_df.iloc[:, 0:2].copy()
    
    id_lesson_no_duplicats = id_lesson.drop_duplicates(subset=["lesson"])
    first_lesson_ids = id_lesson_no_duplicats['id'].tolist()
    first_indexes = [id-1 for id in first_lesson_ids]

    id_lesson_no_duplicats = id_lesson.drop_duplicates(subset=["lesson"], keep='last')
    last_lesson_ids = id_lesson_no_duplicats['id'].tolist()
    last_indexes = [id-1 for id in last_lesson_ids]

    lesson_ids = zip(first_indexes, last_indexes)
    translate_table = translate_assimil(source_df)
    tables_by_lessons = [translate_table.iloc[id[0]:id[1]+1, :].to_numpy() for id in lesson_ids]

    lesson_numbers = id_lesson_no_duplicats['lesson'].tolist()
    
    return lesson_numbers[start:end], tables_by_lessons[start:end]

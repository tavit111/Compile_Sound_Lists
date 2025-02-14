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



def translate_iknow_sentence_list(strt=1, end=-1):
    """
    Read fron orginal source vocabularies.csv, slice the table (1 index), and traslate it into 3 columns (jp_sentence, jp_anki_path, en_sentence)
    pluse splice the secend example into one 3 column table
    return numpy array of the table
    """

    read_path = "/home/tavit/Shadowing/Sources/iknow_jp/vocabularies.csv"
    start_row = strt - 1
    end_row = end - 1
    save_path = f"./{end}_iknow.csv"

    original_df = pd.read_csv(read_path, sep=',', quotechar="'")
    df = original_df.iloc[start_row:end_row].copy()

    df['japanese'] = df.apply(lambda row: f"{row[11]}", axis=1)
    df['mp3_path'] = df.iloc[:, 15]  # Directly use the 4th column
    df['english'] = df.apply(lambda row: f"{row[13]}", axis=1)

    df['japanese2'] = df.apply(lambda row: f"{row[17]}", axis=1)
    df['mp3_path2'] = df.iloc[:, 21]  # Directly use the 4th column
    df['english2'] = df.apply(lambda row: f"{row[19]}", axis=1)


    first_df = df[['japanese', 'mp3_path', 'english']].copy()
    second_df = df[['japanese2', 'mp3_path2', 'english2']].copy()

    second_df.columns = ['japanese', 'mp3_path', 'english']

    first_df.reset_index(drop=True, inplace=True)
    second_df.reset_index(drop=True, inplace=True)

    df_combined = pd.concat([first_df, second_df], axis=0)
    df_filtered_by_sec_examp = df_combined.dropna(subset=[df_combined.columns[1]])
    df_removed_duplicats = df_filtered_by_sec_examp.drop_duplicates()

    return df_removed_duplicats.to_numpy()
    # df_removed_duplicats.to_csv(save_path, index=False, header=False, sep='\t', quotechar="'")

    # print("New CSV file with the combined column and selected columns created successfully!")


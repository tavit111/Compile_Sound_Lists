from mutagen.id3 import ID3, SYLT, Encoding


mp3 = "./list.mp3"

def display_tags(path):
    audio = ID3(path)
    print(audio.get('SYLT::eng'))


display_tags(mp3)
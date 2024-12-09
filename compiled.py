from pydub import AudioSegment
from pydub.playback import play
from dataclasses import dataclass, field
import os


# TODO: Make suere the script is working on multilingual with all audio and multilingual but single audio multi captions
@dataclass
class Compiled:
    __audio_segments: [AudioSegment]
    __captions:[(int, int, str)] = field(default_factory=list)

    def saveMp3(self, path=''):
        if not path:
            path = os.getcwd() + '/list.mp3'

        audiosegment =  self.__audio_segments
        
        audiosegment.export(path, format='mp3')
        print(f"Compilation saved succesfuly in {path}")

        return type(self)(self.__audio_segments, self.__captions)


    def play(self, limit=-1):
        limit = limit*1000 if limit > -1 else -1

        audioSegment = self.__audio_segments()
        play(audioSegment[:limit])

    # def __imbedLyric(self, mp3_file, langs=[]):
    #     # TODO: Need multilangs adaptation
    #     audio = ID3(mp3_file)
    #     lyric = [(*text, time )for (time, *text) in self.__captions]

    #     lyrics_frame = SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=lyric)
    #     # lyrics_frame = SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=[])
    #     # for timestamp, lyric in self.__captions:
    #     #     lyrics_frame.text.append((lyric, timestamp))


    #     audio.setall("SYLT", [SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=lyric)])
    #     audio.save(v2_version=4)

    #     # audio.add(lyrics_frame)
    #     # audio.save()
    #     print("Synchronized lyrics added successfully!")


    def __milisecondsToStr(self, time):
        total_seconds = time // 1000
        
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours:d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def __milisecondsToStrSrc(self, time):
        total_seconds, milliseconds = divmod(time, 1000)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def __combineScripts(self, captions):
        return [(start_time, end_time, f"{' '.join(line)}") for (start_time, end_time, *line) in captions]


    def __saveScript(self, captions, path='', lang='', pickLanguage=1):
        if not path:
            lang = '' if not lang else f"_{lang}"
            path = os.getcwd() + f"/script{lang}.txt"
        
        with open(path, 'w') as file:
            for (start, end, *text) in captions:
                timeStr = self.__milisecondsToStr(start)
                text = text[pickLanguage-1]
                file.write(f"{timeStr}\t{text}\n")
        
        print(f"Script saved succesfuly in {path}")
    
    def saveScript(self, path='', combined=False, pickLanguage=1):
        captions = self.__captions

        if combined:
            captions = self.__combineScripts(captions)

        self.__saveScript(captions=captions, path=path, pickLanguage=pickLanguage)

        return type(self)(self.__audio_segments, self.__captions)
    
    def saveSrt(self, path='', combined=False, pickLanguage=1):
        captions = self.__captions

        if combined:
            captions = self.__combineScripts(captions)

        with open(path, 'w', encoding='utf-8') as file:
            for id, (start_time, end_time, *text) in enumerate(captions, start=1):
                script = text[pickLanguage-1]
                start_formated = self.__milisecondsToStrSrc(start_time)
                end_formated = self.__milisecondsToStrSrc(end_time)
                formated_line = f"{id}\n{start_formated} --> {end_formated}\n{script}\n\n"
                file.write(formated_line)
        
        print(f"SRC script saved succesfuly in {path}")
        return type(self)(self.__audio_segments, self.__captions)


    def showCaption(self):
        for start_time, end_time, capt in self.__captions:
            print(f"{start_time}\t{end_time}\t{capt}")


# movie_dialog = [
#     [0,3000, "Hello, how are you?"],
#     [3000,7000, "I'm doing great, thank you!"],
#     [7000,12000, "What are you up to today?"],
#     [12000,17000, "Just relaxing, watching a movie."],
#     [17000, 23000, "Sounds like a good plan!"]
# ]
# empty_audio = AudioSegment.silent(duration=5000)
# test = Compiled(empty_audio, movie_dialog)
# test.saveSrc(path="./[src]script")

        
        

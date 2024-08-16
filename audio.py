from dataclasses import dataclass, field
import os
from pydub import AudioSegment
from pydub.playback import play
from files import is_mp3_file
from mutagen.id3 import ID3, SYLT, Encoding


@dataclass
class Audio:
    __vocabularySegments: [AudioSegment]
    __series_name: [str] = ''
    __title_name: [str] = ''
    __music_files: [str] = field(default_factory=list)
    __captions:[(int, str)] = field(default_factory=list)
    __vocabularySegment_gap: int = 2
    __music_gap: int = 0
    __music_loop: bool = True
    __end_padding: int = 0
    __vocabulary_vol: int = 0
    __music_vol: int = 0

    def setVocabSegmentGaps(self, gap):
        self.__vocabularySegment_gap = gap

    def setMusicGap(self, gap):
        self.__music_gap = gap

    def setMusicLoop(slef, isLooping):
        self.__music_loop = isLooping

    def addEndPad(self, duration):
        self.__end_padding = duration

    def increasVoiceVolume(self, vol):
        self.__vocabulary_vol = vol

    def increasMusicVolume(self, vol):
        self.__music_vol = vol

    def addAudio(self, audioSegments):
        segments = audioSegments.getSegments()
        self.__vocabularySegments.extend(segments)

    def getSegments(self):
        return self.__vocabularySegments

    def __milisecondsToStr(self, time):
        total_seconds = time // 1000
        
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        #if hours > 0:
            #return f"{hours:d}:{minutes:02d}:{seconds:02d}"
        #else:
            #return f"{minutes:02d}:{seconds:02d}"
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def __addScripts(self, scripts, previous_segment_len):
        for (time, script) in scripts:
            new_time = time + previous_segment_len
            self.__captions.append((new_time, script))

    def __compile(self, repeat=0, randomize=False):
        # segment is tuple (AudioSegment, list_of_caption)
        segments = self.__vocabularySegments

        allVocabularySegments = AudioSegment.empty()
        list_of_captions = []
        silenceGap = AudioSegment.silent(
            duration=self.__vocabularySegment_gap*1000)
        previous_segment_len = 0
        for segment in segments:
            audio =  segment[0]
            scripts = segment[1]

            self.__addScripts(scripts, previous_segment_len)
            
            allVocabularySegments = allVocabularySegments + audio
            allVocabularySegments = allVocabularySegments.apply_gain(
                self.__vocabulary_vol)
            allVocabularySegments = allVocabularySegments + silenceGap
            previous_segment_len = len(allVocabularySegments)

        allVocabularySegments = allVocabularySegments + \
            AudioSegment.silent(duration=self.__end_padding*1000)

        # MUISC
        music = AudioSegment.empty()
        music_silence = AudioSegment.silent(duration=self.__music_gap*1000)
        for path in self.__music_files:
            music = AudioSegment.from_mp3(path)
            # for i in range(music_repeat+1):
            #     music = music + song
            music = music + music_silence
        music = music.apply_gain(self.__music_vol)

        # JOIN VOCABS & MUSIC
        if self.__music_files:
            allVocabularySegments = allVocabularySegments.overlay(
                music, loop=self.__music_loop)

        # return allVocabularySegments, list_of_captions
        return allVocabularySegments

    def addMusic(self, path):
        if not is_mp3_file(path):
            raise Exception("Not an mp3 file. addMusic require mp3 file path")

        self.__music_files.append(path)

    def play(self, limit=-1):
        limit = limit*1000 if limit > -1 else -1

        audioSegment = self.__compile()
        play(audioSegment[:limit])

    def __imbedLyric(self, mp3_file):
        audio = ID3(mp3_file)
        lyric = [(text, time )for (time, text) in self.__captions]

        lyrics_frame = SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=lyric)
        # lyrics_frame = SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=[])
        # for timestamp, lyric in self.__captions:
        #     lyrics_frame.text.append((lyric, timestamp))


        audio.setall("SYLT", [SYLT(encoding=Encoding.UTF8, lang='eng', format=2, type=1, text=lyric)])
        audio.save(v2_version=4)
        print(audio.get('SYLT::eng'))

        # audio.add(lyrics_frame)
        # audio.save()
        print("Synchronized lyrics added successfully!")


    
    def __saveScript(self, path=''):
        if not path:
            path = os.getcwd() + f"/{self.__title_name} - {self.__series_name}.lrc"
        
        with open(path, 'w') as file:
            file.write(f"[ti:{self.__title_name}]\n")
            file.write(f"[ar:{self.__series_name}]\n")
            file.write(f"[al:iknowJp]\n")

            for script in self.__captions:
                timeMs = script[0]
                timeStr = self.__milisecondsToStr(timeMs)
                text = script[1]
                file.write(f"[{timeStr}] {text}\n")
        
        print(f"Script saved succesfuly in {path}")


    def saveMp3(self, path=''):
        if not path:
            path = os.getcwd() + '/list.mp3'

        audiosegment = self.__compile()
        
        tags = {
            "artist": self.__series_name,
            "title": self.__title_name,
        }
        
        audiosegment.export(path, format='mp3', tags=tags)
        print(f"Compilation saved succesfuly in {path}")
        
        self.__imbedLyric(path)
        self.__saveScript()

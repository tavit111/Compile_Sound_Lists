from dataclasses import dataclass, field
from pydub import AudioSegment
from files import is_mp3_file
from compiled import Compiled



@dataclass
class Audio:
    __vocabularySegments: [AudioSegment]
    __music_files: [str] = field(default_factory=list)
    __captions:[(int, int, str)] = field(default_factory=list)
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

    def setMusicLoop(self, isLooping):
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

    def __addScripts(self, scripts, previous_segment_len):
        for (start_time, end_time, *script) in scripts:
            new_start = start_time + previous_segment_len
            new_end = end_time + previous_segment_len
            self.__captions.append((new_start, new_end, *script))

    def __compile(self):
        segments = self.__vocabularySegments

        allVocabularySegments = AudioSegment.empty()
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

        return allVocabularySegments

    def addMusic(self, path):
        if not is_mp3_file(path):
            raise Exception("Not an mp3 file. addMusic require mp3 file path")

        self.__music_files.append(path)

    def compile(self, artist_name='', album_name='', title_name='', cover_art=''):
        audiosegment = self.__compile()
        
        return Compiled(audiosegment, self.__captions,  artist_name, album_name, title_name, cover_art)
from dataclasses import dataclass, field
import os
from pydub import AudioSegment
from pydub.playback import play
from files import is_mp3_file

# HELPER'S FUNCTIONS
# TODO: integreate ids with other functionlities
# TODO: 4. make the channel table 3d
# TODO: 5. make grouping channels functionality
# TODO: 6. import csv as one channel (or 2 channels if there is L1 L2 languages)
# TODO: Add repeat and random shaffle each all adudio segments in Adio


@dataclass
class Audio:
    __vocabularySegments: [AudioSegment]
    __music_files: [str] = field(default_factory=list)
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

    def __compile(self, repeat=0, randomize=False):
        # segment is tuple (AudioSegment, list_of_caption)
        segments = self.__vocabularySegments

        allVocabularySegments = AudioSegment.empty()
        silenceGap = AudioSegment.silent(
            duration=self.__vocabularySegment_gap*1000)
        for segment in segments:
            allVocabularySegments = allVocabularySegments + segment[0]
            allVocabularySegments = allVocabularySegments.apply_gain(
                self.__vocabulary_vol)
            allVocabularySegments = allVocabularySegments + silenceGap

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

        # TODO: make list of captions
        list_of_caption = ''
        # return allVocabularySegments, list_of_caption
        return allVocabularySegments

    def addMusic(self, path):
        if not is_mp3_file(path):
            raise Exception("Not an mp3 file. addMusic require mp3 file path")

        self.__music_files.append(path)

    def play(self, limit=-1):
        limit = limit*1000 if limit > -1 else -1

        audioSegment = self.__compile()
        play(audioSegment[:limit])

    def saveMp3(self, path=''):
        if not path:
            path = os.getcwd() + '/list.mp3'

        audiosegment = self.__compile()
        audiosegment.export(path, format='mp3')

        print(f"Compilation saved succesfuly in {path}")

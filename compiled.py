from pydub import AudioSegment
from pydub.playback import play
from dataclasses import dataclass, field
from files import loadCoverArt
import os
import numpy as np
from moviepy import ImageClip, ColorClip, CompositeVideoClip, AudioArrayClip


@dataclass
class Compiled:
    __audio_segments: [AudioSegment]
    __captions:[(int, int, str)] = field(default_factory=list)
    __artist_name: [str] = ''
    __album_name: [str] = ''
    __title_name: [str] = ''
    __cover_art: [str] = ''

    def saveMp3(self, path=''):
        if not path:
            path = os.getcwd() + '/list.mp3'

        audiosegment =  self.__audio_segments

        tags = {
            "artist": self.__artist_name,
            "album": self.__album_name,
            "title": self.__title_name,
        }
        
        audiosegment.export(path, format='mp3', tags=tags)

        if self.__cover_art:
            loadCoverArt(path, self.__cover_art)
        
        print(f"Compilation saved succesfuly in {path}")
        return type(self)(self.__audio_segments, self.__captions, self.__artist_name, self.__album_name, self.__title_name, self.__cover_art)


    def play(self, limit=-1):
        limit = limit*1000 if limit > -1 else -1

        audioSegment = self.__audio_segments()
        play(audioSegment[:limit])


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

        return type(self)(self.__audio_segments, self.__captions, self.__artist_name, self.__album_name, self.__title_name, self.__cover_art)

    
    def saveSrt(self, path='', combined=False, pickLanguage=1):
        captions = self.__captions

        if combined:
            captions = self.__combineScripts(captions)

        with open(path, 'w', encoding='utf-8') as file:
            for id, (start_time, end_time, *text) in enumerate(captions, start=1):
                script = text[pickLanguage-1]
                start_formated = self.__milisecondsToStrSrc(start_time)
                end_formated = self.__milisecondsToStrSrc(end_time)
                formated_line = f"\n{id}\n{start_formated} --> {end_formated}\n{script}\n"
                file.write(formated_line)
        
        print(f"SRC script saved succesfuly in {path}")
        return type(self)(self.__audio_segments, self.__captions, self.__artist_name, self.__album_name, self.__title_name, self.__cover_art)


    def showCaption(self):
        for start_time, end_time, capt in self.__captions:
            print(f"{start_time}\t{end_time}\t{capt}")
    
    def saveMp4(self, path, use_cover=True):
        audio_clip = self.__get_audio_clip()
        audio_duration = audio_clip.duration

        if use_cover and self.__cover_art:
            image_clip = ImageClip(self.__cover_art)
        else:
            image_clip = ColorClip(size=(640, 360) ,color=(0, 0, 0))
        image_clip = image_clip.with_duration(audio_duration)
        image_clip = image_clip.with_audio(audio_clip)

        final_clip = CompositeVideoClip([image_clip])
        final_clip = final_clip.with_duration(audio_duration)
        final_clip.write_videofile(path, fps=24, codec='libx264', audio_codec='aac')

        print(f"SRC script saved succesfuly in {path}")
        return type(self)(self.__audio_segments, self.__captions, self.__artist_name, self.__album_name, self.__title_name, self.__cover_art)

    def __get_audio_clip(self):
        audio = self.__audio_segments
        raw_samples = audio.get_array_of_samples()
        samples_np = np.array(raw_samples)
        samples_float = samples_np.astype(np.float32) / (2**(8 * audio.sample_width - 1))

        if audio.channels == 2:
            samples_float = samples_float.reshape((-1, 2))
        else:
            samples_float = samples_float.reshape((-1, 1)).repeat(2, axis=1)

        sample_rate = audio.frame_rate
        return AudioArrayClip(samples_float, sample_rate)
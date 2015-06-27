#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import os
import time
import vlc

MP3_FILE = 'speech.mp3'

class TextToSpeech:
    def __init__(self):
        self._sound = None


    @property
    def sound(self):
        return self._sound


    def say(self, text, language='sv'):
        text = text.lower()
        # get sound response from translate api
        sound_response = self.get_sound_response(text, language)

        if sound_response:
            # write response to file
            file_to_play = self.write_file(sound_response)
            # play sound file
            self.play_sound_file(file_to_play)


    def get_sound_response(self, text, language):
        # url encode text
        text_encoded = urllib.quote_plus(text)[:150]  # limit chars
        url_base = 'http://translate.google.com/translate_tts'
        lang = '?tl={0}'.format(language)
        query = '&q={0}'.format(text_encoded)
        url = '{0}{1}{2}'.format(url_base, lang, query)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')]
        try:
            response = opener.open(url)
        except:
            print('Could not open tts URL.')
            return
        return response.read()


    def play_sound_file(self, file_to_play):
        self._sound = vlc.MediaPlayer(file_to_play)
        self._sound.play()
        time.sleep(self.mp3_len())
        self._sound.stop()


    def write_file(self, sound_response):
        f = open(MP3_FILE,'wb')
        f.write(sound_response)
        f.close()
        return MP3_FILE


    def mp3_len(self):
        ''' return size in seconds of mp3 file '''
        size_k = (os.path.getsize(MP3_FILE) / 1000) / 4
        return size_k



if __name__ == '__main__':
    TextToSpeech()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import os
import time
import vlc

MP3_FILE = 'food.mp3'

def main():
    # get sound response from translate api
    sound_response = get_sound_response()

    # write response to file
    file_to_play = write_file(sound_response)

    # play sound file
    play_sound_file(file_to_play)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print '\nProgram exit.'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


def get_sound_response():
    url_base = 'http://translate.google.com/translate_tts?tl=sv&q='
    text = 'Måndag. Fiskgratäng med stuvade räkor.'
    # url encode text
    text_encoded = urllib.quote_plus(text)
    url = '{0}{1}'.format(url_base, text_encoded)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')]
    response = opener.open(url)
    return response.read()


def play_sound_file(file_to_play):
    p = vlc.MediaPlayer(file_to_play)
    p.play()


def write_file(sound_response):
    f = open(MP3_FILE,'wb')
    f.write(sound_response)
    f.close()
    return MP3_FILE



if __name__ == '__main__':
    main()

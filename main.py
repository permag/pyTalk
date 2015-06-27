#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time
import scraper
import texttospeech

def main():
    text_list = scraper.get_text_list()

    i = 0
    for text in text_list:
        i += 1
        if i is 1:
            texttospeech.say('{0}. {1}'.format(' . Nu är det dags för lunch!', text))
            time.sleep(6)
        else:
            texttospeech.say(text)
            time.sleep(10)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print '\nProgram exit.'
        sys.exit(0)



if __name__ == '__main__':
    main()

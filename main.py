#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, datetime
import json
import scraper
from texttospeech import TextToSpeech

JSON_DATA_FILE = 'data.json'
INTRO = ' . Nu är det {0} och klockan är {1}, och det är dags för lunch! . . .'
OUTRO_SPECIAL = 'Tisdag... ja just det, gå till Grand.'

def main():
    tts = TextToSpeech()
    # intro
    say_intro(tts)

    # get restaurants
    data = get_restaurants()
    for item in data:
        read_restaurant_menu(tts, item)

    if scraper.get_today_as_string() == 'Tisdag':
        tts.say(OUTRO_SPECIAL)

def say_intro(tts):
    time_now = str(datetime.datetime.now().time())[:5]
    # intro
    day_now = scraper.get_today_as_string()
    intro = INTRO.format(day_now, time_now)
    tts.say(intro)


def get_restaurants():
    '''
        returns dict: {name: 'Name of restaurant',
                       name_pronunciation: 'Name with pronunciation help',
                       url: 'http://to.scrape'}
    '''
    with open(JSON_DATA_FILE) as data_file:
        data = json.load(data_file)
    for d in data:
        d['name'] = d['name'].encode('utf-8')
        d['name_pronunciation'] = d['name_pronunciation'].encode('utf-8')
    return data


def read_restaurant_menu(tts, restaurant_item):
    text_list = scraper.get_text_list(restaurant_item['url'])
    if not text_list:
        return
    print('\n********* Restaurat: {0} *********'.format(restaurant_item['name']))
    i = 0
    for text in text_list:
        print(text)
        i += 1
        if i is 1:
            tts.say('{0}. {1}'.format(restaurant_item['name_pronunciation'], text))
        else:
            tts.say('. {0}'.format(text))




if __name__ == '__main__':
    main()

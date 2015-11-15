#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, time, datetime
import json
import scraper
import forecast
import say

JSON_DATA_FILE = 'data.json'
PRONUNCIATION_FILE = 'pronunciation/sv.json'
INTRO = 'Nu är det {0} och klockan är {1}, och det är dags för lunch!'
OUTRO_SPECIAL = 'Tisdag... ja just det, gå till Grand.'

def main(mode):
    data = get_restaurants()
    weather = forecast.get(data['forecast_url'].encode('utf-8'))

    # mode
    if mode == 'suggestions':
        say.say('Här kommer några förslag:')
        for item in data['restaurants']:
            read_restaurant_menu(item, mode, data['prefered'])
        return
    elif mode == 'weather':
        say_weather(weather)
        return

    # intro
    say_intro()

    # get restaurants
    for item in data['restaurants']:
        read_restaurant_menu(item, mode, None)

    # say weather
    say_weather(weather)

    # Tuesday message
    if scraper.get_today_as_string() == 'Tisdag':
        say.say(OUTRO_SPECIAL)


def say_weather(weather):
    if weather:
        if (weather[0] == 'light rain showers' or weather[0] == 'rain showers' or
            weather[0] == 'heavy rain showers' or weather[0] == 'showers'):
            say.say('Och så lite väder. Just nu är det {0}, så det kanske är bäst att ni gå till Tegel idag då.'.format(weather[1]))
        else:
            say.say('Och så lite väder. Just nu är det {0}, så ni kan väl gå vart ni vill.'.format(weather[1]))


def say_intro():
    time_now = str(datetime.datetime.now().time())[:5]
    # intro
    day_now = scraper.get_today_as_string()
    intro = INTRO.format(day_now, time_now)
    say.say(intro)


def get_restaurants():
    with open(JSON_DATA_FILE) as data_file:
        data = json.load(data_file)
    for d in data['restaurants']:
        d['name'] = d['name'].encode('utf-8')
        d['name_pronunciation'] = d['name_pronunciation'].encode('utf-8')
    return data


def read_restaurant_menu(restaurant_item, mode, prefered):
    text_list = scraper.get_text_list(restaurant_item['url'])
    if not text_list:
        return
    if mode == 'suggestions':
        say_suggestions(restaurant_item['name_pronunciation'], text_list, prefered)
    print('\n********* Restaurant: {0} *********'.format(restaurant_item['name']))
    i = 0
    for text in text_list:
        i += 1
        print(text)
        if mode == 'menu':
            if i is 1:
                say.say('{0}. {1}'.format(restaurant_item['name_pronunciation'], text))
            else:
                say.say('. {0}'.format(text))



def say_suggestions(name, text_list, prefered):
    do_break = False
    for pref in prefered:
        for s in pref:
            s = s.encode('utf-8')
            for text in text_list:
                text = text.lower()
                if text.find(s) != -1:
                    do_break = True
                    say.say('På {0} är det {1}.'.format(name, text));
            if do_break:
                do_break = False
                break



if __name__ == '__main__':
    '''
        modes:
            menu (default)
            weather
            suggestions
    '''
    mode = 'menu'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    try:
        main(mode)
    except KeyboardInterrupt:
        print('\nProgram exit.\n')
        sys.exit(0)
    except:
        sys.exit(1)

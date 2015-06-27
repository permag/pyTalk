#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import datetime


def main():
    ''' Kvartersmenyn scrape on restaurant level '''
    # tegel test
    url = 'http://www.kvartersmenyn.se/rest/13586'

    try:
        html = urllib2.urlopen(url)
        data = html.read()
        html.close()
    except:
        print('Could not open URL')
        sys.exit()

    days_data = [];

    soup = BeautifulSoup(data, 'html.parser')
    # print(soup.prettify())
    current_day = get_today_as_string()
    res = soup.find('strong', text=current_day)
    ref = None
    refs = []
    for i in range(15):
        if not ref:
            ref = res.find_next(text=True)
        else:
            if ref != current_day:
                ref_str = ref.encode('utf-8').lower()
                if (ref_str == 'måndag' or ref_str == 'tisdag' or
                    ref_str == 'onsdag' or ref_str == 'torsdag' or
                    ref_str == 'fredag' or ref_str[:4] == 'pris'):
                    break
            refs.append(ref)
            ref = ref.find_next(text=True)

    text_list = []
    for line in refs:
        if len(line) < 4:
            continue
        text_list.append('{0}. '.format(line.encode('utf-8')))


    # text_list structure:
    # text_list[0] DAY
    # text_list[1] DISH 1
    # text_list[2] DISH 2
    # text_list[3] DISH 3
    # ...

    return text_list


def get_text_list():
    return main()


def get_today_as_string():
    datetime.datetime.today()
    datetime.datetime(2012, 3, 23, 23, 24, 55, 173504)
    today_nr = datetime.datetime.today().weekday()
    today = None

    # for testing on weekend
    today_nr = 2

    if today_nr == 0:
        today = u'Måndag'
    elif today_nr == 1:
        today = u'Tisdag'
    elif today_nr == 2:
        today = u'Onsdag'
    elif today_nr == 3:
        today = u'Torsdag'
    elif today_nr == 4:
        today = u'Fredag'
    return today



if __name__ == '__main__':
    main()

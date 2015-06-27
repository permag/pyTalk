#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
from bs4 import BeautifulSoup
import datetime


def main(url):
    ''' Kvartersmenyn scrape on restaurant level '''

    try:
        html = urllib2.urlopen(url)
        data = html.read()
        html.close()
    except:
        print('Could not open URL:' + url)
        return None

    days_data = [];
    soup = BeautifulSoup(data, 'html.parser')
    current_day = get_today_as_string()
    try:
        res = soup.find('strong', text=current_day)
        ref = None
        refs = []
        for i in range(9):
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
    except:
        print('Could not prase tag.')
        return None

    text_list = []
    for line in refs:
        if len(line) < 4:
            continue
        text_list.append('{0}. '.format(line.encode('utf-8')))


    # text_list structure:
    # ### text_list[0] DAY
    # text_list[1] DISH 1
    # text_list[2] DISH 2
    # text_list[3] DISH 3
    # ...

    if len(text_list):
        # remove day
        text_list.pop(0)
        return text_list


def get_text_list(url):
    return main(url)


def get_today_as_string():
    today_nr = datetime.datetime.today().weekday()
    today = None

    # for testing on weekend
    today_nr = 1

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
    elif today_nr == 5 or today_nr == 6:
        today = 'Helg'
    return today



if __name__ == '__main__':
    main()

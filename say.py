#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
from os import system

VOICE = 'Alva'
SPEED = 200
PRONUNCIATION_FILE = 'pronunciation/sv.json'

do_fix_pronunciation = True
pronunciation_words = {}

def say(text):
    global pronunciation_words
    if not pronunciation_words:
        if PRONUNCIATION_FILE:
            set_pronunciation_data(PRONUNCIATION_FILE)
    if do_fix_pronunciation:
        text = pronunciation_fix(text)
    system('say -v {0} {1} -r {2}'.format(VOICE, text, SPEED))


def pronunciation_fix(text):
    global pronunciation_words
    for i, j in pronunciation_words.iteritems():
        text = text.replace(i, j)
    return text


def set_pronunciation_data(filename):
    global pronunciation_words
    with open(filename) as data_file:
        data = json.load(data_file)
    data = byteify(data)
    pronunciation_words = data


def byteify(data):
    if isinstance(data, dict):
        return {byteify(key): byteify(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        return [byteify(element) for element in data]
    elif isinstance(data, unicode):
        return data.encode('utf-8')
    else:
        return data


if __name__ == '__main__':
    say(sys.argv[1])

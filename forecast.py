#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

def main(url):
    symbols_dict = {
        'clear sky': 'solsken',
        'fair': 'sol och lite moln',
        'cloudy': 'molnigt',
        'partly cloudy': 'lite molnigt',
        'light rain': 'lätt regn',
        'rain showers': 'regnskurar',
        'showers': 'regnskurar',
        'heavy rain showers': 'kraftigt regnfall',
        'light rain showers': 'lätta regnskurar',
    }

    try:
        xml = urllib2.urlopen(url)
        data = xml.read()
        xml.close()
    except:
        print('Could not open URL: ' + url)
        return None

    soup = BeautifulSoup(data, 'lxml')
    forecast = soup.forecast.tabular.find('time')  # closest time

    symbol_name = forecast.symbol['name'].lower()

    if symbol_name in symbols_dict:
        return (symbol_name, symbols_dict[symbol_name])
    else:
        return None

def get(url):
    return main(url)


if __name__ == '__main__':
    main()

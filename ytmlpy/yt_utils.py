#!/usr/bin/env python
print('yt_utils')
from urllib.parse import urljoin
import ast
import json

"""
Utils class for the scraper.
"""
__title__ = 'utils'
__author__ = 'Rashiq Ahmad'
__license__ = 'GPLv3'

def dicListConverter(mydict):
    for key, value in mydict.items():
        if isinstance(value, str):
            if value[0:1]=='[':
                # print('配列 : ' + value)
                # print(key, value)
                mydict[key] = json.loads(value)
    # print('====配列変換終了====')
    # print(mydict)
    return mydict

def cleanLine(line):
    line = line.strip()
    line = line.replace('\n',' ')
    line = line.replace('\r',' ')
    # line = line.replace('\','')
    # print(line)
    return line

def create_absolute_link(base, rel_url):
    """
    Creates a absolute Url out of a relative link.
    Will return the given second parameter, if it's already
    an absolute link.
    """
    return urljoin(base, rel_url)


def build_video_page(page):
    """
    Url builder for TED talk video pages.
    Appending the page number to the 'page' parameter.
    """
    return 'http://new.ted.com/talks/browse?page={}'.format(page)


def build_subtitle_pages(video_id, language_list):
    """
    Url builder for the json subtitles page for TED talks.
    Building it from the video specific Id and the language
    we want the subtitles in.
    """

    for language in language_list:
        page = 'http://www.ted.com/talks/subtitles/id/{}/lang/{}' \
            .format(video_id, language['languageCode'])
        language['link'] = page

    return language_list

def get_subtitle_link(video_id, lang):
    link= 'http://www.ted.com/talks/subtitles/id/{}/lang/{}' \
        .format(video_id, lang)
    return link

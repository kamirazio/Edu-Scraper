
"""
Class for scraping www.TED.com.
"""
__title__ = 'webscraper'
__author__ = 'Rashiq Ahmad'
__license__ = 'GPLv3'

from bs4 import BeautifulSoup
# import HTMLTextExtractor
from ytmlpy.HTMLTextExtractor import HTMLTextExtractor
import requests
import json
import re
from pprint import pprint
from urllib.request import urlopen
import urllib
import chardet

from ytmlpy import yt_utils

class TEDScraper:

    URL_ROOT = 'https://www.ted.com/talks/'

    def __init__(self, url):
        print ('0 : create TEDScraper')
        if url != "test" or url != False:
            self.url = url
        else:
            console.log("debug_url:" + debug_url )
            self.url = debug_url

        self.video_lang = "en" #presenterの言語
        self.video_key, self.sub_lang = self.getKey(url)
        print (self.video_key, self.sub_lang, self.video_lang)

    def getKey(self, url):
        # url = "http://www.ted.com/talks/marco_tempest_the_electric_rise_and_fall_of_nikola_tesla?language=ja"
        # url = "http://www.ted.com/talks/marco_tempest_the_electric_rise_and_fall_of_nikola_tesla"
        print("------ TED ID 生成 ------")
        pattern1 = 'ted.com/talks/([^<]+)\?language=([^<]+)'
        pattern2 = 'ted.com/talks/([^<]+)'
        match_elm = re.findall(pattern1, url)
        if match_elm:
            key = match_elm[0][0]
            sub_lang = match_elm[0][1]
        else:
            match_elm = re.findall(pattern2, url)
            key = match_elm[0]
            sub_lang = "en"
        return key, sub_lang

    def getVideoInfo(self):
        print('***** Scrape video info *****')

        # BeautifulSoup instance
        self.soup = None
        self.html = None
        self.json_data = None
        self.video_info = []

        html = requests.get(self.url)
        self.soup = BeautifulSoup(html.text,"lxml")
        json_data = self.soup.select('div.talks-main script')
        # pprint(json_data)
        if len(json_data) == 0: return

        json_data = json_data[-1].text
        json_data = ' '.join(json_data.split(',', 1)[1].split(')')[:-1])
        json_data = json.loads(json_data)
        # print(json_data)
        # print(json_data['__INITIAL_DATA__'])

        # print('==============================')
        #
        # print(json_data['__INITIAL_DATA__'])
        #
        # print('==============================')

        # ------ Extract the video Id of the TED talk video. ------ #
        # We need this to generate the subtitle page.
        # talk_id = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['targeting']['id']
        try:
            talk_id = json_data['__INITIAL_DATA__']['current_talk']
        except:
            talk_id = None

        try:
            title = json_data['__INITIAL_DATA__']['talks'][0]['title']
        except:
            title = None

        try:
            description = json_data['__INITIAL_DATA__']['talks'][0]['description']
        except:
            description = None

        try:
            speaker_data = self.soup.find("meta", attrs={"name" : "author"})
            speaker = speaker_data["content"] if speaker_data else "No meta speaker given"
        except:
            speaker = None

        try:
            duration = json_data['__INITIAL_DATA__']['talks'][0]['duration']
        except:
            duration = None

        try:
            download_link = json_data['__INITIAL_DATA__']['talks'][0]['downloads']['nativeDownloads']['medium']
        except:
            download_link = None

        try:

            speaker_id = json_data['__INITIAL_DATA__']['speakers'][0]['id']
            speaker_profession = json_data['__INITIAL_DATA__']['speakers'][0]['description']
            speaker_bio = json_data['__INITIAL_DATA__']['speakers'][0]['whotheyare']
            whylisten = json_data['__INITIAL_DATA__']['speakers'][0]['whylisten']
            speaker_picture = json_data['__INITIAL_DATA__']['speakers'][0]['photo_url']
            s = HTMLTextExtractor()
            s.feed(whylisten)
            whylisten = s.get_text()

        except:
            speaker_id = None
            speaker_profession = None
            speaker_bio = None
            whylisten = None
            speaker_picture = None

        try:
            event = json_data['__INITIAL_DATA__']['speakers'][0]['events'][0]['event']['name']
            event_id = json_data['__INITIAL_DATA__']['speakers'][0]['events'][0]['event']['id']
            event_date = json_data['__INITIAL_DATA__']['speakers'][0]['events'][0]['event']['starts_at']
        except:
            event = None
            event_id = None
            event_date = None

        try:
            self.video_lang = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['nativeLanguage']
            starting_point = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['introDuration']
            # Extract the thumbnail of the of the TED talk video
            thumb = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['thumb']
        except:
            self.video_lang = None
            starting_point = None
            thumb = None

        subtitles = [{'languageName': lang['languageName'],
                      'languageCode':lang['languageCode']}
                     for lang in json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['languages']]

        # subtitles = yt_utils.build_subtitle_pages(talk_id, subtitles)
        # subtitle_src = "https://www.ted.com/talks/subtitles/id/%s/lang/%s" % (talk_id, self.sub_lang)

        subtitle_src = yt_utils.get_subtitle_link(talk_id, self.sub_lang)
        try:
            json_src = urlopen(subtitle_src)
            subtitle_data = json.loads(json_src.read().decode('utf-8'))
            if subtitle_data:
                plot = json.dumps(subtitle_data, ensure_ascii=False)
                # ====== Extract the subtitle text for analization ====== #
                subtitle_txt = ""
                for caption in subtitle_data['captions']:
                    subtitle_txt += caption['content'] + ' '
                print(subtitle_txt)
        except:
            subtitle_txt = None
            plot = None

        try:
            keywords_data = self.soup.find("meta",  attrs={"name" : "keywords"})
            keywords = keywords_data["content"] if keywords_data else "No meta keywords given"
        except:
            keywords_data = None
            keywords = None

        try:
            tags = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['targeting']['tag']
        except:
            tags = None

        try:
            viewed = json_data['__INITIAL_DATA__']['viewed_count']
        except:
            viewed = None

        self.video_info.append({
            'video_id': talk_id,
            'video_key': self.video_key,

            'host': 'ted',
            'lang_list': subtitles,
            'video_lang': self.video_lang,
            'lang': self.sub_lang,
            'plot': plot,
            'subtitle': subtitle_txt,
            'plot_id': 'plot_id',
            'url': self.url,

            'title': title,
            'description': description,
            'memo': whylisten,
            'img': thumb,
            'video_date': event_date,

            'channel': event,
            'channel_id': event_id,

            'author': speaker,
            'author_id': speaker_id,

            'video_link': download_link,
            'duration': duration,
            'adjustment' : starting_point,

            'keywords': keywords,
            'tags': tags,
            'rating':'rating',
            'viewed': viewed
        })

        # print(self.video_info)
        return self.video_info[0]

if __name__ == '__main__':
    url = "https://www.ted.com/talks/chinaka_hodge_what_will_you_tell_your_daughters_about_2016"
    test = TEDScraper(url)
    # test.test_method('2')
    test.getVideoInfo()

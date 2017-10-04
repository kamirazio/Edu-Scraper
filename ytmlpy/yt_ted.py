
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
        talk_id = json_data['__INITIAL_DATA__']['current_talk']

        # Extract the speaker of the TED talk
        # speaker = json_data['talks'][0]['speaker']
        # speaker = self.soup.select('meta.thumb__image')[0]['src']
        speaker_data = self.soup.find("meta", attrs={"name" : "author"})
        speaker = speaker_data["content"] if speaker_data else "No meta speaker given"

        # # Extract the profession of the speaker of the TED talk
        # speaker_profession = self.soup.select('div.talk-speaker__description')[0].text.strip()
        speaker_id = json_data['__INITIAL_DATA__']['speakers'][0]['id']
        speaker_profession = json_data['__INITIAL_DATA__']['speakers'][0]['description']

        # # Extract the short biography of the speaker of the TED talk
        # speaker_bio = self.soup.select('div.talk-speaker__bio')[0].text.strip()
        speaker_bio = json_data['__INITIAL_DATA__']['speakers'][0]['whotheyare']
        whylisten = json_data['__INITIAL_DATA__']['speakers'][0]['whylisten']
        s = HTMLTextExtractor()
        s.feed(whylisten)
        whylisten = s.get_text()
        # whylisten = re.sub(r'(\s|\t|)*?<\/?(&nbsp;)?p[^>]*?(&nbsp;)?>', "", whylisten)
        # print(whylisten)

        # # Extract the Url to the picture of the speaker of the TED talk
        # speaker_picture = self.soup.select('img.thumb__image')[0]['src']
        speaker_picture = json_data['__INITIAL_DATA__']['speakers'][0]['photo_url']

        # # Extract the title of the TED talk
        # # title = json_data['talks'][0]['title']
        # title_data = self.soup.find("meta",  property="og:title")
        title = json_data['__INITIAL_DATA__']['talks'][0]['title']
        #
        # # Extract the description of the TED talk
        description = json_data['__INITIAL_DATA__']['talks'][0]['description']
        # description_data = self.soup.find("meta",  property="og:description")
        # description = description_data["content"] if description_data else "No meta description given"

        # # Extract the upload date of the TED talk
        # date = self.soup.find('div', class_="player-hero__meta")
        # date = date.find_all('span')[1]
        # date.strong.replace_with('')
        # date = date.text.strip()
        try:
            event = json_data['__INITIAL_DATA__']['speakers'][0]['events'][0]['event']['name']
            event_id = json_data['__INITIAL_DATA__']['speakers'][0]['events'][0]['event']['id']
            event_date = json_data['__INITIAL_DATA__']['speakers'][0]['events'][0]['event']['starts_at']
        except KeyError:
            event = None
            event_id = None
            event_date = None

        # Extract the length of the TED talk in minutes
        duration = json_data['__INITIAL_DATA__']['talks'][0]['duration']
        # duration_data = self.soup.find("meta",  property="video:duration")
        # duration = duration_data["content"] if duration_data else "No meta duration given"

        self.video_lang = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['nativeLanguage']
        starting_point = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['introDuration']

        download_link = json_data['__INITIAL_DATA__']['talks'][0]['downloads']['nativeDownloads']['medium']
        # divmod(x, y)でxをyで割った商とあまりをタプルで返す
        # length = divmod(length, 60)[0]

        # Extract the thumbnail of the of the TED talk video
        thumb = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['thumb']

        subtitles = [{'languageName': lang['languageName'],
                      'languageCode':lang['languageCode']}
                     for lang in json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['languages']]

        # subtitles = yt_utils.build_subtitle_pages(talk_id, subtitles)
        # subtitle_src = "https://www.ted.com/talks/subtitles/id/%s/lang/%s" % (talk_id, self.sub_lang)

        subtitle_src = yt_utils.get_subtitle_link(talk_id, self.sub_lang)
        json_src = urlopen(subtitle_src)
        subtitle_data = json.loads(json_src.read().decode('utf-8'))
        plot = json.dumps(subtitle_data, ensure_ascii=False)

        # ====== Extract the subtitle text for analization ====== #
        subtitle_txt = ""
        for caption in subtitle_data['captions']:
            subtitle_txt += caption['content'] + ' '
        print(subtitle_txt)

        # yt_nlp.getJacetScore(subtitle_txt)
        # yt_nlp.getFeature(subtitle_txt)

        # print(":D :D :D")
        # print(json.dumps(subtitle_data, ensure_ascii=False))

        # # Extract the keywords for the TED talk
        # keywords = self.soup.find('meta', attrs={'name': 'keywords'})['content']
        keywords_data = self.soup.find("meta",  attrs={"name" : "keywords"})
        keywords = keywords_data["content"] if keywords_data else "No meta keywords given"

        tags = json_data['__INITIAL_DATA__']['talks'][0]['player_talks'][0]['targeting']['tag']

        # keywords = [key.strip() for key in keywords.split(',')]
        #
        # # Extract the ratings list for the TED talk
        viewed = json_data['__INITIAL_DATA__']['viewed_count']

        # Append the meta-data to a list

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

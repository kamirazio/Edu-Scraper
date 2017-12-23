# based on the data in row_html, subtitle, this generates wuestion

url_base = 'https://www.ted.com%s'
file_base1 = './row_html/ted_talks_%s.html'
file_base2 = './subtitle/ted_talks_%s_%s.txt'
file_base3 = './subtitle_key/ted_talks_%s_%s.txt'
error_file = './log/error.txt'
access_file = './log/access.txt'
scraped_file = './log/link_list_%s.txt'

from datetime import datetime as dt
from lxml import html
import time

from ytmlpy.yt_ted import TEDScraper
from ytmlpy import yt_nlp
from ytmlpy import yt_q_generator

tdatetime = dt.now()
tstr = tdatetime.strftime('%Y-%m-%d')

# ===== Change based on the trial ===== #

# offline -> False
scraper = False
vformat = True
# for single
page = 2
item_index = 11
# for multi
npages = 72
video_key ="lee_cronin_print_your_own_medicine"

# ===================================== #

profile = {
    'user' : 'test_20171027',
    'user_level' : 1000,
    'mode' : 'blank',
    'blank_rate' : 25,
    'chunk' : 0
}

#===================================================== DB

from ytmlpy.yt_mysql import ORMDB
mydb = ORMDB('ytml')

from sqlalchemy.ext.declarative import DeclarativeMeta
import json

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data, ensure_ascii=False) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)

#=====================================================

def getScriptJson(video_id):
    # print('======= ビデオ情報の取得 =======')

    # print("<<<<< mydb.getVideoInfo")
    session = mydb.Session()
    video_data = mydb.getVideoInfoByID(session, video_id)
    session.close()
    scripts = {}
    if video_data['plot']:
        try:
            # print(video_data['plot'])
            scripts = json.loads(video_data['plot'])
        except:
            scripts['captions'] = None
            add_text('json.loadsエラー Error : \n%s\n\n' % video_id, error_file)
            add_text(video_data['plot'], error_file)
    else:
        scripts['captions'] = None
        add_text('getScriptJson Error : \n%s\n\n' % video_id, error_file)
    return scripts['captions']

def createTask(obj):
    # print('=======  スクリプト分析 + タスクの生成 =======')
    scripts = getScriptJson(obj['video_id'])
    # print(scripts)
    if scripts:
        plot_list = yt_q_generator.analyzeScripts(obj, scripts, profile)
        # print(plot_list)
        # import pdb; pdb.set_trace()

        if plot_list:
            # print('======= @ スクリプトの保存 + ゲーム記録スペースの保存  =======')
            # print("mydb.insertScript >>>>>")
            # print(obj)
            session = mydb.Session()
            tid = mydb.insertScripts(session, obj, profile, plot_list)
            # print(" mydb.createTask >>>>>")
            origin = 0
            follow_id = 0

            # obj['uid'] = user
            obj['mode'] = profile['mode']
            obj['level'] = profile['user_level']
            obj['blank_rate'] = profile['blank_rate']

            # obj['vid'] if obj['vid'] == None else 0
            task = mydb.createTask(session, obj, tid, profile, origin, follow_id, len(plot_list))
            session.close()
        else:
            add_text('might has error : \n%s\n\n' % obj['video_key'], error_file)
    else:
        task = None

    return 'true' if task != None else 'false'

def getTEDVideoInfo(url):

    #=========== スクレーピング Class ===========#
    video = TEDScraper(url)
    video_anal = {}
    #=========== DBで存在確認 ===========#
    session = mydb.Session()
    video_data = mydb.getVideoInfo(session, video.video_key, video.sub_lang)
    task_data = mydb.getTaskByVideoKey(session, video.video_key, profile['user_level'], profile['blank_rate'])

    if video_data is not None and vformat == True:
        # vformat -> True : dbのanalizeをupdateする
        print("DBから取得")
        subtitle = video_data['subtitle']
        if subtitle is not None:
            content_size, content_difficulty, keyword_difficulty, w_cnt, c_cnt = yt_nlp.getJacetScore(subtitle)

            # # 台詞データから、TF-IDF分析を行う
            # video.analyzeVideo()

            video_anal['size'] = content_size
            video_anal['difficulty1'] = content_difficulty
            video_anal['difficulty2'] = keyword_difficulty
            # ['tf-idf']

            video_data = mydb.updateVideoInfo(session, video_anal, video_data['uuid'], profile['user'])

    elif video_data is None:
        # Webからスクレープ
        video.getVideoInfo()
        subtitle = video.video_info[0]['subtitle']

        if subtitle is not None:
            content_size, content_difficulty, keyword_difficulty, w_cnt, c_cnt = yt_nlp.getJacetScore(subtitle)
            # print(content_size)
            # print(content_difficulty)
            # print(keyword_difficulty)

            video_anal['size'] = content_size
            video_anal['difficulty1'] = content_difficulty
            video_anal['difficulty2'] = keyword_difficulty
            # video.video_info[0]['tf-idf']
            # session = mydb.Session()
            video_data = mydb.insertVideoInfo(session, video.video_info[0], video_anal, profile['user'])
            # session.close()
            # print(video_data)
            # # 台詞データから、TF-IDF分析を行う
            # video.analyzeVideo()
            print('======= save video info :D =======')
        else:
            print('======= No Subtitle data -> skip =======')
            video_data = None
            add_text('No Subtitle data : \n%s\n\n' % video.video_key, error_file)

    elif task_data and video_data:
        print(scraper)
        # scraperモードでないときは、DBからの情報で新たな条件でタスクを作成する
        if scraper == True:
            print('======= Finished Video -> skip =======')
            video_data = None
    else:
        print('======= HAVE Vdata =======')

    session.close()
    return video_data

def save_text(text, filename):
    with open(filename, 'w') as f:
        f.write(text)
        print('記入')

def add_text(text, filename):
    with open(filename, 'a') as f:
        f.write(text)
        print('追記: %s' % text)

def parse_item(item):
    talk_link = item.xpath('.//h4[@class="h9 m5"]/a/@href')
    return url_base % talk_link[0]

def multi_spider(npages):
    data = []
    for page_num in range(1, npages+1):
        root = html.parse(file_base1 % page_num)
        # print(root.xpath('//body//text()'))
        items = root.xpath('//div[@id="browse-results"]//div[@class="col"]')
        # print(len(items))
        # data = []
        for item in items:

            link = parse_item(item)
            data.append(link)

            video_data = getTEDVideoInfo(link)

            # ----- 取得済みデータ ----- #
            if video_data is None:
                add_text('skip:\n%s\n\n' % link, error_file)
                continue
            # ------------------------ #

            save_text(video_data['subtitle'], file_base2 % (str(page_num),video_data['video_id']))

            res = createTask(video_data)
            if res == None:
                add_text('error:\n%s\n\n' % link, error_file)
                continue

            print(res)
            print("==========")
            if scraper == True:
                time.sleep(5)

    print(len(data))    # returns 36
    print(data)
    save_text('Finished scraping :\n%s\n\n' % data, scraped_file % tstr)
    print("===== FIN Multi :) =====")

def single_spider(page_num, index):

    root = html.parse(file_base1 % page_num)
    # print(root.xpath('//body//text()')) #test
    items = root.xpath('//div[@id="browse-results"]//div[@class="col"]')
    # print(len(items))
    link = parse_item(items[index])
    video_data = getTEDVideoInfo(link)

    if video_data is not None:
        save_text(video_data['subtitle'], file_base2 % (str(page_num),video_data['video_id']))
        res = createTask(video_data)
        print(res)
        # add_text('===== FIN :) ===== \n %s' % link, access_file)
    else:
        add_text('no video data : \n%s\n\n' % link, error_file)

    save_text('Finished scraping : \n%s\n\n' % link , scraped_file % tstr)
    print(link)
    print("===== FIN Single :) =====")

# Create Task by Specific Link
def link_spider(key):

    link = 'https://www.ted.com/talks/'+ key
    video_data = getTEDVideoInfo(link)

    if video_data is not None:
        save_text(video_data['subtitle'], file_base3 % (str(key),video_data['video_id']))
        res = createTask(video_data)
        print(res)
        # add_text('===== FIN :) ===== \n %s' % link, access_file)
    else:
        add_text('no video data : \n%s\n\n' % link, error_file)

    save_text('Finished scraping : \n%s\n\n' % link , scraped_file % tstr)
    print(link)
    print("===== FIN Single by Link :) =====")


# ===== Chose which function you want to use ===== #
# single_spider(page, item_index)
link_spider('asha_de_vos_why_you_should_care_about_whale_poo')
# https://www.ted.com/talks/asha_de_vos_why_you_should_care_about_whale_poo?language=ja
# multi_spider(npages)

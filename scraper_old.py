
#===================================================== DB

from ytmlpy.yt_mysql import ORMDB
mydb = ORMDB('ytml')

file_base1 = './row_html/ted_talks_%s.html'

file_base2 = './subtitle/ted_talks_%s_%s.txt'

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

#===================================================== DB

npages = 72
page_num = 1
url_base = 'https://www.ted.com%s'
file_base = './row_html/ted_talks_%s.html'

from lxml import html
import time

def parse_item(item):
    talk_link = item.xpath('.//h4[@class="h9 m5"]/a/@href')
    return url_base % talk_link[0]

from ytmlpy.yt_ted import TEDScraper
from ytmlpy import yt_nlp
from ytmlpy import yt_q_generator

def getScriptJson(session, video_id, lang):
    print('======= ビデオ情報の取得 =======')

    print("<<<<< mydb.getVideoInfo")
    session = mydb.Session()
    video_data = mydb.getVideoInfoByID(session, video_id, lang)
    scripts = json.loads(video_data['plot'])
    # sub_scripts = json.loads(video_data['plot_local'])
    return scripts['captions']

def createTask(obj):
    print('=======  スクリプト分析 + タスクの生成 =======')
    # # obj = request.form

    session = mydb.Session()
    scripts = getScriptJson(session, obj['video_id'], obj['lang'])
    print(scripts)
    plot_list = yt_q_generator.analyzeScripts(obj, scripts)
    print(plot_list)
    #
    print('======= @ スクリプトの保存 + ゲーム記録スペースの保存  =======')

    print("mydb.insertScript >>>>> + mydb.insertGameRecords >>>>>")
    # print(obj)
    tid = mydb.insertScripts(session, obj, plot_list)
    print(" mydb.createTask >>>>>")
    origin = 0
    follow_id = 0
    obj['uid'] = 'test20171004'
    # obj['vid'] if obj['vid'] == None else 0
    task = mydb.createTask(session, obj, tid, obj['uid'], origin, follow_id, len(plot_list))
    session.close()
    return 'OK' if task != None else 'Failed in creating task X0'

def getVideoInfo(url):

    #=========== メインビデオ情報の存在確認 + スクレーピング ===========#
    video = TEDScraper(url)

    # DBで存在確認
    video_data = mydb.getVideoInfo(video.video_key, video.sub_lang)

    if video_data is None:
        video.getVideoInfo()
        content_size, content_difficulty, keyword_difficulty = yt_nlp.getJacetScore(video.video_info[0]['subtitle'])
        print(content_size)
        print(content_difficulty)
        print(keyword_difficulty)

        video.video_info[0]['size'] = content_size
        video.video_info[0]['difficulty1'] = content_difficulty
        video.video_info[0]['difficulty2'] = keyword_difficulty
        # video.video_info[0]['tf-idf']
        session = mydb.Session()
        video_data = mydb.insertVideoInfo(session, video.video_info[0])
        session.close()
        # print(video_data)
        # # 台詞データから、TF-IDF分析を行う
        # video.analyzeVideo()
        print('======= save video info :D =======')

    else:
        print('======= HAVE Vdata =======')

    return video_data

def save_text(text, filename):
    with open(filename, 'w') as f:
        f.write(text)
        print('記入')

def add_text(text, filename):
    with open(filename, 'a') as f:
        f.write(text)
        print('追記: %s' % text)

def multi_spider():
    data = []
    for page_num in range(22, npages+1):
        root = html.parse(file_base1 % page_num)
        # print(root.xpath('//body//text()'))
        items = root.xpath('//div[@id="browse-results"]//div[@class="col"]')
        # print(len(items))
        # data = []
        for item in items:

            link = parse_item(item)
            data.append(link)

            video_data = getVideoInfo(link)
            if video_data == None:
                add_text('skip:%s' % link, error_file)
                continue

            save_text(video_data['subtitle'], file_base2 % (str(page_num),video_data['video_id']))

            res = createTask(video_data)
            if res == None:
                add_text('error:%s' % link, error_file)
                continue

            print(res)
            print("==========")
            time.sleep(20)

    print(len(data))    # returns 36
    print(data)
    save_text(data, 'link_list_20171004.txt')
    print("===== FIN :) =====")

def single_spider():
    page_num = 1
    root = html.parse(file_base1 % page_num)
    # print(root.xpath('//body//text()'))
    items = root.xpath('//div[@id="browse-results"]//div[@class="col"]')
    print(len(items))
    # data = []
    link = parse_item(items[0])
    video_data = getVideoInfo(link)
    save_text(video_data['subtitle'], file_base2 % (str(page_num),video_data['video_id']))
    res = createTask(video_data)
    print(res)
    print("===== FIN :) =====")

#single_spider()
multi_spider()
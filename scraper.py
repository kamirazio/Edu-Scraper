
#===================================================== DB

from ytml.py.yt_mysql import ORMDB
mydb = ORMDB('ytml')

from sqlalchemy.ext.declarative import DeclarativeMeta

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

def parse_item(item):
    talk_link = item.xpath('.//h4[@class="h9 m5"]/a/@href')
    return url_base % talk_link[0]

from ytml.py.yt_ted import TEDScraper

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

        # # 台詞データから、TF-IDF分析を行う
        # video.analyzeVideo()
        # print('======= save video info :D =======')
        #
        # print('=======  スクリプト分析 + タスクの生成 =======')
        # # obj = request.form
        #
        # scripts, sub_scripts = getScriptJson(session, obj['video_id'], obj['lang'], obj['local_lang'])
        # plot_list = yt_q_generator.analyzeScripts(obj, scripts, sub_scripts)
        # # print(plot_list)
        #
        # print('======= @ スクリプトの保存 + ゲーム記録スペースの保存  =======')
        # # session = mydb.Session()
        # print("mydb.insertScript >>>>> + mydb.insertGameRecords >>>>>")
        # tid = mydb.insertScripts(session, obj, plot_list)
        # print(" mydb.createTask >>>>>")
        # origin = 0
        # follow_id = 0
        # task = mydb.createTask(session, obj, tid, obj['uid'], origin, follow_id, len(plot_list))
        # session.close()
        # return 'OK' if (task == None) else 'Failed in creating task X0'
        return "true"
    else:
        print('======= HAVE Vdata =======')
        return "false"

def multi_spider():
    data = []
    for page_num in range(1, npages+1):
        root = html.parse(file_base % page_num)
        # print(root.xpath('//body//text()'))
        items = root.xpath('//div[@id="browse-results"]//div[@class="col"]')
        # print(len(items))
        # data = []
        for item in items:
            link = parse_item(item)
            data.append(d)
            getVideoInfo(link)

    print(len(data))    # returns 36
    print(data)

def single_spider():
    data = []
    page_num = 1
    root = html.parse(file_base % page_num)
    # print(root.xpath('//body//text()'))
    items = root.xpath('//div[@id="browse-results"]//div[@class="col"]')
    # print(len(items))
    # data = []
    for item in items:
        link = parse_item(item)
        data.append(d)
        getVideoInfo(link)

    print(len(data))    # returns 36
    print(data)

single_spider()

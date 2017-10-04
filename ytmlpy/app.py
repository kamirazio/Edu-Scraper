
from flask import Flask
from flask import request, url_for, session, redirect, Response, render_template
from flask_cors import CORS, cross_origin

from flask import jsonify
from flask.json import JSONEncoder
import json, re, datetime, math, hashlib

import bcrypt, base64
from bson import json_util, ObjectId
from pprint import pprint

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.security import check_password_hash

import yt_utils
import yt_q_generator
import yt_nlp
from yt_ted import TEDScraper

#===================================================== FLASK

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.update(
    DEBUG = True,
    APPLICATION_ROOT = "/ytml",
    SECRET_KEY = 'kamirazio', # set a 'SECRET_KEY' to enable the Flask session cookies
    MYSQL_CURSORCLASS = 'DictCursor'
)

#===================================================== DB

from yt_mysql import ORMDB
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

#===================================================== テスト用

test_json = [{'key':'foo','value':"foo"},
          {'key':'bar','value':"bar"},
          {'key':'baz','value':"baz"}]

debug_url = "https://www.ted.com/talks/chinaka_hodge_what_will_you_tell_your_daughters_about_2016"

#===================================================== テスト用 ROOT

@app.route("/")
def index():
    print('debug')
    # if 'username' in session:
    #     return '<body>You are %s</body>' % session['username']
    # return 'The URL for this page is {}'.format(url_for('index'))
    # mydb.showTable()
    # mydb.showRecord()

    # yt_q_generator.getExperienceTest()
    mydb.getExperience(2)
    #[経験, 成功, 失敗, 辞書, 保存]

    return "res"

#===================================================== # DICT

@app.route('/_dic_ej', methods=['GET','POST'])
def dic_ej():
    if request.method == 'GET':
        print('======= @ 意味の取得 : %s =======' % request.args.get('word'))
        session = mydb.Session()
        print(" <<<<< mydb.getEdic ")
        res = mydb.getEdic(session, request.args.get('word'))
        # print(res)
        session.close()
        return json.dumps(res, cls=AlchemyEncoder, ensure_ascii=False) if res else 'No Answer stored'

#===================================================== # WORD

@app.route('/_words', methods=['GET','POST'])
def words():
    if request.method == 'GET':
        print('======= @ 登録単語リスト一覧 =======')
        session = mydb.Session()
        if request.args.get('command')=="getAllSavedWords":
            res = mydb.getSavedWords(session, request.args.get('user_id'), request.args.get('tid'), request.args.get('q_num'))
        elif request.args.get('command')=="getDoneWords":
            res = mydb.getDoneWords(session, request.args.get('tid'), request.args.get('q_num'))
        # print(res)
        session.close()
        return json.dumps(res, cls=AlchemyEncoder, ensure_ascii=False) if res else 'No data'

    if request.method == 'POST':
        print('======= @ ゲーム結果の登録 =======')
        obj = request.form
        # print(obj)
        session = mydb.Session()
        print("mydb.insertWords >>>>>")
        res = mydb.insertWords(session, obj)
        print("mydb.updateGameRecord >>>>>")
        res = mydb.updateGameRecord(session, obj['tid'], obj['q_num'])

        print('# ====== @ 次の字幕を再取得する ====== #')
        print("<<<<< mydb.getScriptSource ")
        next_script = mydb.getScriptSource(session, obj['tid'], int(obj['q_num'])+1 )
        # print(next_script)

        if next_script is not None:
            print('======= @ ゲームの分析と新しいQの登録 =======')
            next_script = yt_utils.dicListConverter(next_script)
            # print(next_script)
            # ここで、問題の再検討を行い、
            plot = yt_q_generator.re_analyzeScripts(obj, next_script)
            print(plot)
            # 新しいQをQ1に、古いQをQ2に登録する
            print("mydb.updateQuestion >>>>>")
            res = mydb.updateQuestion(session, plot)
            print(res)

        session.close()
        return jsonify(plot) if plot is not None or next_script is not None else 'false'

#===================================================== # TASK

@app.route('/_task', methods=['GET','POST'])
def task():
    if request.method == 'GET':
        print('======= @ タスク情報の取得  =======')
        session = mydb.Session()
        print(" <<<<< mydb.getGameIniciationInfoByTID")
        task = mydb.getGameIniciationInfoByTID(session, request.args.get('tid'))
        # print(task)
        session.close()
        return jsonify(task) if task else 'Failed in getting task X0'

    if request.method == 'POST':
        print('=======  スクリプト分析 + タスクの生成 =======')
        obj = request.form
        session = mydb.Session()
        scripts, sub_scripts = getScriptJson(session, obj['video_id'], obj['lang'], obj['local_lang'])
        plot_list = yt_q_generator.analyzeScripts(obj, scripts, sub_scripts)
        # print(plot_list)

        print('======= @ スクリプトの保存 + ゲーム記録スペースの保存  =======')
        session = mydb.Session()
        print("mydb.insertScript >>>>> + mydb.insertGameRecords >>>>>")
        tid = mydb.insertScripts(session, obj, plot_list)
        print(" mydb.createTask >>>>>")
        origin = 0
        follow_id = 0
        task = mydb.createTask(session, obj, tid, obj['uid'], origin, follow_id, len(plot_list))
        session.close()
        return 'OK' if (task == None) else 'Failed in creating task X0'

@app.route('/_tasks', methods=['GET','POST'])
def tasks():
    if request.method == 'GET':
        print('======= @ タスクリストの取得 =======')
        session = mydb.Session()
        print("<<<<< mydb.getTasks")
        task_list = mydb.getTasks(session, request.args.get('user_id'), request.args.get('status'))
        session.close()
        return json.dumps(task_list) if task_list else 'No task'

    if request.method == 'POST':
        pass

#===================================================== # CLASSROOM

@app.route('/_classroom', methods=['GET','POST'])
def classroom():
    if request.method == 'GET':
        print("classroom")
    #     # print('======= @ クラスルーム タスクリストの取得 =======')
    #     # session = mydb.Session()
    #     # # print(request.args)
    #     # print("<<<<< mydb.getClassroomTasks")
    #     # task_list = mydb.getClassroomTasks(session, request.args.get('room_id'))
    #     # session.close()
    #     # return json.dumps(task_list) if task_list else 'No task'
    #     pass

    if request.method == 'POST':
        print('======= @ クラスルーム 作成 =======')
        obj = request.form
        print(obj)
        session = mydb.Session()
        print("mydb.insertClassroom >>>>>")
        classroom = mydb.insertClassroom(session, obj)
        session.close()
        return json.dumps(classroom, cls=AlchemyEncoder, ensure_ascii=False) if classroom else 'No classroom'
    # return "res"

@app.route('/_classrooms', methods=['GET','POST'])
def classrooms():
    if request.method == 'GET':
        print(request.args)
        print('======= @ クラスルームリストの取得 =======')
        session = mydb.Session()
        print("<<<<< mydb.getClassrooms")
        classroom_list = mydb.getClassrooms(session, request.args.get('uid'),request.args.get('name'),request.args.get('status'),request.args.get('role'))
        session.close()
        print(classroom_list)
        return json.dumps(classroom_list, cls=AlchemyEncoder, ensure_ascii=False) if classroom_list else 'No classroom'

    if request.method == 'POST':
        pass

#===================================================== # TASKSET

@app.route('/_taskset', methods=['GET','POST'])
def taskset():
    if request.method == 'GET':
        print("taskset")
    #     # print('======= @ クラスルーム タスクリストの取得 =======')
    #     # session = mydb.Session()
    #     # # print(request.args)
    #     # print("<<<<< mydb.getClassroomTasks")
    #     # task_list = mydb.getClassroomTasks(session, request.args.get('room_id'))
    #     # session.close()
    #     # return json.dumps(task_list) if task_list else 'No task'
        pass

    if request.method == 'POST' and request.form['command'] == "addClassroomToTasksets":
        print('======= @ クラスルーム タスク登録 =======')
        obj = request.form
        print(obj)
        session = mydb.Session()
        print("mydb.insertTaskset >>>>>")
        res = mydb.insertTaskset(session, obj)
        print(res)
        session.close()
        # return jsonify(res) if res else 'Fail'
        return jsonify(res)

    if request.method == 'POST' and request.form['command'] == "updateTaskset":
        print('======= @ クラスルーム 変更 =======')
        obj = request.form
        print(obj)
        session = mydb.Session()
        print("mydb.updateTaskset >>>>>")
        res = mydb.updateTaskset(session, obj)
        session.close()
        return res

#===================================================== # CLASSROOM TASK

@app.route('/_tasksets', methods=['GET','POST'])
def tasksets():
    if request.method == 'GET':
        print('======= @ クラスルーム タスクリストの取得 =======')
        print(request.args)
        print("<<<<< mydb.getTasksets")

        session = mydb.Session()
        taskset_list = mydb.getTasksets(session, request.args.get('classroom_id'),request.args.get('status'))
        session.close()
        return json.dumps(taskset_list, cls=AlchemyEncoder, ensure_ascii=False) if taskset_list else 'No taskset'

    if request.method == 'POST':
        pass
#===================================================== VIDEO

@app.route('/_video', methods=['GET','POST'])
def video():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        print('======= ビデオ情報 タスクリストの取得 =======')
        # print('get video info of :'+request.form['url'])
        video_info = getVideoInfo(request.form['url'])
        video_info['_sa_instance_state'] = None
        return jsonify(video_info)

#===================================================== GAME

@app.route('/_game', methods=['GET','POST'])
def game():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        print('======= ゲーム結果の記録 =======')
        obj = request.form
        print(obj)
        print('mydb.updateGameResult >>>>>>')
        res = mydb.updateGameResult(obj)
        return 'game record update : OK'

@app.route('/_games', methods=['GET','POST'])
def games():
    if request.method == 'GET':
        print('======= ゲーム履歴 リストの取得 =======')
        print('<<<<< mydb.getGameRecords')
        # print(request.args.get('tid'))
        game_record_list = mydb.getGameRecords(request.args.get('tid'))
        # print(game_record_list)
        # return jsonify(game_records)
        res = json.dumps(game_record_list, cls=AlchemyEncoder, ensure_ascii=False)
        return res if res else 'No game_record_list'

    if request.method == 'POST':
        pass

#===================================================== SCRIPT

@app.route('/_script', methods=['GET','POST'])
def script():
    if request.method == 'GET':
        # print('<<<<< mydb.getLastRecord')
        # print(request.args)
        # record = mydb.getLastRecord(request.args.get('user_id'))
        # print(record)
        # return json.dumps(record, cls=AlchemyEncoder, ensure_ascii=False)
        # # return jsonify(record)
        pass

    if request.method == 'POST':
        print('======= Edited スクリプトの保存 =======')
        obj = request.form
        # print(obj)
        session = mydb.Session()

        print('>>>>> mydb.updateScript ')
        script_data = mydb.updateScript(session,obj)
        # print(tid + ":success")
        session.close()
        return json.dumps(script_data, cls=AlchemyEncoder, ensure_ascii=False) if script_data else 'No Script_data'

@app.route('/_scripts', methods=['GET','POST'])
def scripts():
    if request.method == 'GET':
        print('======= @ スクリプトの取得 =======')
        session = mydb.Session()
        # print(request.args)
        print('<<<<< mydb.getScripts')
        # print(request.args.get('tid'))
        script_list = mydb.getScripts(session, request.args.get('tid'))
        # print(script_list)
        # return jsonify(game_records)
        # TODO: Refactoring 後ほど良い方法を探る
        session.close()
        return json.dumps(script_list, cls=AlchemyEncoder, ensure_ascii=False) if script_list else 'No Script_list'

    if request.method == 'POST':
        print('======= @ Edit用 スクリプトのコピー =======')
        session = mydb.Session()
        obj = request.form

        tid = obj['tid'] if (int(obj['follow_id']) == 0) else obj['follow_id']
        print(tid)

        print('mydb.copyTask >>>>')
        task = mydb.copyTask(session, tid, obj['uid'])
        print(task)

        print('mydb.copyScripts ------')
        new_tid = mydb.copyScripts(session, tid, obj['uid'], task['uuid'])
        print(new_tid + ":success")

        # TODO: Refactoring 後ほど良い方法を探る
        del task['created']
        del task['modified']
        del task['_sa_instance_state']

        session.close()
        return jsonify(task)

#===================================================== USER

@app.route('/_login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        print('======= ユーザログイン =======')
        obj = request.form
        print('<<<<< mydb.getUser')
        user = mydb.getUser(obj['email'])
        print(user)
        if checkPW(user['password'], obj['password']):
            print('You were logged in (^_^)')
            session['logged_in'] = True
            user['remember'] = obj['remember']
            # TODO: Refactoring 後ほど良い方法を探る
            del user['created']
            del user['password']
            del user['modified']
            del user['_sa_instance_state']
            return jsonify(user)
        else:
            return 'Invalid password'

@app.route('/_signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mydb.users
        existing_email = users.find_one({'email' : request.form['email']})
        existing_username = users.find_one({'username' : request.form['username']})

        if existing_email is None:
            if existing_username is None:
                print('Let\'s registor')
                hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                users.insert({
                'username' : request.form['username'],
                'password' : hashpass,
                'email': request.form['email'],
                'created': datetime.datetime.utcnow()})
                # session['username'] = request.form['username']
                print('registration success :)')
                return jsonify({'result':True, 'comment':'Success to registor ;)'})

            return jsonify({'result':False, 'comment':'That usrname has been already taken!'})
        return jsonify({'result':False, 'comment':'That email already exists!'})

    # return render_template('register.html')

@app.route('/_wordList', methods=['POST', 'GET'])
def word():
    if request.method == 'GET':
        words = mydb.words
        wordlist = words.find({'user_id' : request.form['user_id']})

        return JSONEncoder().encode(wordlist)

    elif request.method == 'POST':
        words = mydb.words
        words.insert({
            'word' : request.form['word'],
            'username' : request.form['username'],
            'user_id' : request.form['user_id'],
            'dateAdded': datetime.datetime.utcnow()})
        print('word registored :)')
        return jsonify({'result':True, 'comment':'Word registored ;)'})

@app.route('/_record', methods=['GET','POST'])
def record():
    if request.method == 'GET':
        print('======= @ 成就成績の取得 =======')
        print(request.args)
        print('<<<<< mydb.getLastRecord')
        session = mydb.Session()
        record = mydb.getLastRecord(session, request.args.get('uid'))
        session.close()
        print(record )
        return json.dumps(record, cls=AlchemyEncoder, ensure_ascii=False) if record else 'false'

@app.route('/_user', methods=['GET','POST'])
def user():
    # chromelogger.log('_user py!')
    # mydb = MyMongodb('localhost', 27017, 'ytml')

    # if user_info:
    #     print('Have Data')
    #     # print('I\'ve already have the info of [%s]' % user_info['id'])
    #     user_info = [{'key':'foo','value':"foo"},
    #               {'key':'bar','value':"bar"},
    #               {'key':'baz','value':"baz"}]
    # else:
    #     print('No Data')
    #     user_info = [{'key':'foo','value':"foo"},
    #               {'key':'bar','value':"bar"},
    #               {'key':'baz','value':"baz"}]

    user_info = [{'key':'foo','value':"foo"},
              {'key':'bar','value':"bar"},
              {'key':'baz','value':"baz"}]

    res = JSONEncoder().encode(user_info)
    return res

#=====================================================

def checkPW(hashed, pw):
    # print(hashed)
    # print(pw)
    pw_tmp = 'PASSWORD_KEY' + pw
    # print(hashlib.sha1(pw_tmp.encode('utf-8')).hexdigest())
    return hashed == hashlib.sha1(pw_tmp.encode('utf-8')).hexdigest()

#=====================================================

def getScriptJson(session, video_id, lang, local_lang):
    print('======= ビデオ情報の取得 =======')
    # session = mydb.Session()
    print("<<<<< mydb.getVideoInfo")

    video_data = mydb.getVideoInfoByID(session, video_id, lang, local_lang)
    scripts = json.loads(video_data['plot'])
    sub_scripts = json.loads(video_data['plot_local'])
    return scripts['captions'], sub_scripts['captions']

#=====================================================

def getVideoInfo(url):

    #=========== サブタイトルビデオ情報の存在確認 + スクレーピング ===========#
    url = url if url else debug_url
    host ='ted' # TODO: ここはJsの段階で行う 今はダミー変数を設置
    if host == 'ted' :
        sub_video = TEDScraper(url)
        sub_url = "https://www.ted.com/talks/%s?language=%s" % (sub_video.video_key,sub_video.sub_lang)
        # print( "SUB TED-URLを生成しました：%s" % sub_video.url)
    else:
        # TODO: Yotube用
        pass

    # DBで存在確認
    sub_video_data = mydb.getVideoInfo(sub_video.video_key,sub_video.sub_lang)

    if sub_video_data is None:
        print("======= No Subtitle Info =======")
        print('Scraping sub video')
        # sub_video_info_data = sub_video.getVideoInfo()
        sub_video.getVideoInfo()
        # print(sub_video.video_info)
        sub_video_data = mydb.insertVideoLocalInfo(sub_video.video_info[0])
        print('save')
    else:
        print('======= HAVE SUB Vdata =======')
    print('======= :) =======')
    # print(sub_video_data['title'])
    # print(sub_video_data)

    #=========== メインビデオ情報の存在確認 + スクレーピング ===========#
    host ='ted' # TODO: ここはJsの段階で行う 今はダミー変数を設置
    if host == 'ted' :
        # main_video sub_video.langからビデオの言語を取得する 主に en がはいる
        main_url = "https://www.ted.com/talks/%s?language=%s" % (sub_video.video_key,sub_video.video_lang)
        video = TEDScraper(main_url)

        # print( "TED-URL for SUB を生成しました：%s" % video.url)
        # print( "TED-URL for SUB の 言語：%s" % video.sub_lang)
    else:
        # TODO: Yotube用
        pass

    # DBで存在確認
    video_data = mydb.getVideoInfo(video.video_key, video.sub_lang)

    if video_data is None:
        print("======= @ No Video info =======")
        print('Scraping main video')
        # video_info_data = video.getVideoInfo()
        video.getVideoInfo()

        # print(video.video_info[0]['subtitle'])
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
        # # 台詞データから、TF-IDF分析を行う
        # video.analyzeVideo()
        print('save')
    else:
        print('======= HAVE Vdata =======')
    print('======= :D =======')
    # print(video_data['title'])
    # print(type(video_data)) #<class 'dict'>

    return video_data

def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Hello WSGI World']

def check_password(hashed_password, user_password):
    print('check PW')
    password, salt = hashed_password.split(':')
    return password == hashlib.sha1(salt.encode() + user_password.encode()).hexdigest()

# request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
app.wsgi_app = DispatcherMiddleware(simple, {'/ytml': app.wsgi_app})


#=====================================================

if __name__ == "__main__":
    app.secret_key ='mysecret'
    app.run(host = "0.0.0.0", port = 8080)

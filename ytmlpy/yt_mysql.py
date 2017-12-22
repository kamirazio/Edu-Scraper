# import MySQLdb
# import MySQLdb.cursors
# from MySQLdb.cursors import DictCursor
# from flask import jsonify
# from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.sql import and_, or_, not_, func
from sqlalchemy.orm import create_session, sessionmaker, attributes, make_transient
from sqlalchemy.ext.serializer import loads, dumps
from pprint import pprint
from datetime import datetime
import json
import uuid

# from ytmlpy.yt_modules import Users, Videos, Tasks, Scripts, Classrooms, Tasksets, Games, Jacet, Ejdic, Words
from ytmlpy.yt_modules import Users, Videos, Tasks, Scripts, Jacet, Ejdic, Words

class ORMDB:
    def __init__(self,dbname):
        print ('DB-00 : connectDB')
        #モデルを作成したら、create_allメソッドでテーブルを作成する
        #テーブル作成時には、DSNを設定したengineオブジェクトを渡します。
        # Engineおよびconnectionの取得
        url = 'mysql+pymysql://kamirazio:g019116@localhost/%s?charset=utf8' % dbname
        self.engine = sa.create_engine(url, echo = False)
        # Base.metadata.create_all(engine, checkfirst=True)
        self.conn = self.engine.connect()

        # セッション生成
        self.Session = sessionmaker(bind = self.engine, autocommit = False)
        # self.session = self.Session()

        # MetaData の生成 -> Engineに結びつける
        # メタデータにはテーブルのスキーマ等が格納される
        self.meta = sa.MetaData()
        self.meta.reflect(bind = self.engine)

        self.scriptsT = self.meta.tables['scripts_ex']
        self.videosT = self.meta.tables['videos_ex']
        self.tasksT = self.meta.tables['tasks_ex']
        self.classroomsT = self.meta.tables['classrooms']
        self.tasksetsT = self.meta.tables['tasksets']
        self.gamesT = self.meta.tables['games']
        self.jacetT = self.meta.tables['jacet']
        self.edicT = self.meta.tables['ejdic']
        self.wordsT = self.meta.tables['words']
        self.usersT = self.meta.tables['users']

    #  ========================================================================================== WORD #
    #  ======================================================================== GET #

    # def getDoneWords(self, session, tid, q_num):
    #     # self.session = self.Session()
    #     print("======= get Done Word List =======")
    #     print(tid, q_num)
    #     res = session.query(Words).filter(Words.tid == tid, Words.q_num == q_num).all()
    #     # if res is None:
    #     #     res = 'no data'
    #     return res
    #
    # def getExperience(self, user_id):
    #     self.session = self.Session()
    #     print("======= getExperience =======")
    #
    #     res_ex = self.session.query(sa.func.avg(Words.jacet)).filter(Words.user_id == user_id, Words.t_dict > 0).all()
    #
    #     ex = {}
    #
    #     ex['ex_all'] = self.session.query(sa.func.avg(Words.jacet),sa.func.max(Words.jacet),sa.func.count(Words.jacet)).filter(Words.user_id == user_id).all()
    #
    #     ex['ex_success'] = self.session.query(sa.func.avg(Words.jacet),sa.func.max(Words.jacet),sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_success > 0).all()
    #
    #     ex['ex_fail'] = self.session.query(sa.func.avg(Words.jacet),sa.func.max(Words.jacet),sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_miss > 0).all()
    #
    #     ex['ex_dic'] = self.session.query(sa.func.avg(Words.jacet),sa.func.max(Words.jacet),sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_dict > 0).all()
    #
    #     ex['ex_save'] = self.session.query(sa.func.avg(Words.jacet),sa.func.max(Words.jacet),sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_save > 0).all()
    #
    #     ex['ex_only'] = self.session.query( \
    #     sa.func.avg(Words.jacet), sa.func.min(Words.jacet), sa.func.max(Words.jacet), sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_success == 0, Words.t_miss == 0, Words.t_dict == 0, Words.t_save == 0).all()
    #
    #     ex['ex_fail_only'] = self.session.query( \
    #     sa.func.avg(Words.jacet), sa.func.min(Words.jacet), sa.func.max(Words.jacet), sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_miss > 0, Words.t_dict == 0, Words.t_save == 0).all()
    #     ex['ex_fail_dic'] = self.session.query( \
    #     sa.func.avg(Words.jacet), sa.func.min(Words.jacet), sa.func.max(Words.jacet), sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_miss > 0, Words.t_dict > 0, Words.t_save == 0).all()
    #     ex['ex_fail_dic_save'] = self.session.query( \
    #     sa.func.avg(Words.jacet), sa.func.min(Words.jacet), sa.func.max(Words.jacet), sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_miss > 0, Words.t_dict > 0, Words.t_save > 0).all()
    #     ex['ex_fail_save'] = self.session.query( \
    #     sa.func.avg(Words.jacet), sa.func.min(Words.jacet), sa.func.max(Words.jacet), sa.func.count(Words.jacet)).filter(Words.user_id == user_id, Words.t_miss > 0, Words.t_dict == 0, Words.t_save > 0).all()
    #
    #     if ex  is None:
    #         ex  = 'no data'
    #     print(ex)
    #     return 'true'
    #
    # def getWordExperience(self, w, user_id):
    #     self.session = self.Session()
    #     print("======= get Saved Word List =======")
    #     print("======= get miss + dic =======")
    #     ex = []
    #
    #     res_ex = self.session.query(sa.func.avg(Words.jacet)).filter(Words.lemma == w, Words.user_id == user_id).count()
    #     ex.append(res_ex)
    #
    #     res_success = self.session.query(Words).filter(Words.lemma == w, Words.user_id == user_id, Words.t_success > 0).count()
    #     ex.append(res_success)
    #
    #     res_fail = self.session.query(Words).filter(Words.lemma == w, Words.user_id == user_id, Words.t_miss > 0).count()
    #     ex.append(res_fail)
    #
    #     res_dic = self.session.query(Words).filter(Words.lemma == w, Words.user_id == user_id, Words.t_dict > 0).count()
    #     ex.append(res_fail_dic)
    #
    #     res_save = self.session.query(Words).filter(Words.lemma == w, Words.user_id == user_id, Words.t_save > 0).count()
    #     ex.append(res_fail_save)
    #
    #     if ex  is None:
    #         ex  = 'no data'
    #     print(ex)
    #     return 'true'
    #
    # def getSavedWords(self, session, user_id, tid, q_num):
    #     # self.session = self.Session()
    #     print("======= get Saved Word List =======")
    #     if tid == 'all':
    #         print("======= get all word List =======")
    #         res = session.query(Words).filter(Words.user_id == user_id, Words.t_save == 1).all()
    #     elif q_num == 'all':
    #         res = session.query(Words).filter(Words.user_id == user_id, Words.t_save == 1, Words.tid == tid).all()
    #     else:
    #         res = session.query(Words).filter(Words.user_id == user_id, Words.t_save == 1, Words.tid == tid, Words.q_num == q_num).all()
    #
    #     # if res is None:
    #     #     res = 'no data'
    #     # print(res)
    #     return res
    #
    # def insertWords(self, session, obj ):
    #     # user_id, uid, tid, q_num, words):
    #     # self.session = self.Session()
    #     # obj['user_id'],obj['uid'], obj['tid'], obj['q_num'], obj['words']
    #     print("======= insert words =======")
    #     # print(obj['words'])
    #     word_list = json.loads(obj['words'])
    #     # print(word_list)
    #     for word_info in word_list:
    #         res = self.insertWord(session, obj['uid'], obj['tid'], obj['q_num'], word_info)
    #         # update below
    #         # res = self.insertGameRecords(tid, row['q_num'])
    #     return 'true'
    #
    # def insertWord(self, session, uid, tid, q_num, word_info):
    #     # self.session = self.Session()
    #     print("======= insert word =======")
    #     # print(tid, q_num, word_info)
    #
    #     ins = self.wordsT.insert().values(
    #         lemma = word_info['lemma'],
    #         word = word_info['word'],
    #         # user_id = user_id,
    #         uid = uid,
    #         tid = tid,
    #         q_num = q_num,
    #
    #         order = word_info['order'],
    #         jacet = word_info['jacet'],
    #
    #         t_success = word_info['t_success'],
    #         t_miss = word_info['t_miss'],
    #
    #         t_dict = word_info['t_dict'],
    #         t_save = word_info['t_save'],
    #
    #         t_repeat = word_info['t_repeat'],
    #         t_cheat = word_info['t_cheat'],
    #         # t_skip = word_info['t_skip'],
    #         created = datetime.now()
    #     )
    #
    #     result = self.conn.execute(ins)
    #     session.commit()
    #
    #     return 'true'
    #
    # #  ========================================================================================== EDIC #
    # #  ======================================================================== GET #
    #
    def getEdic(self, session, w):
        # self.session = self.Session()
        print("======= get Meaning =======")
        # res = self.session.query(Ejdic).filter(Ejdic.en.like(w+"%")).all()
        res = session.query(Ejdic).filter(Ejdic.en == w).all()
        # if res is None:
        #     res = 'no data'
        return res
    #
    # #  ========================================================================================== JACET #
    # #  ======================================================================== GET #
    #
    def getJacet(self, session, w_list):
        # self.session = self.Session()
        print("======= getJACET =======")
        jacets=[]
        for w in w_list:
            jacet = session.query(Jacet.rank).filter(Jacet.en == w).first()
            if jacet:
                jacets.append(jacet[0])
            else:
                jacets.append(0)
        # print(jacets)
        return jacets
    #
    # #  ========================================================================================== TASKSETS #
    # #  ======================================================================== GET #
    #
    # def insertClassroom(self, session, obj):
    #     print("======= insert classroom =======")
    #     ins = self.classroomsT.insert().values(
    #         uuid = str(uuid.uuid4()),
    #         uid = obj['uid'],
    #         role = obj['role'],
    #         status = obj['status'],
    #         title = obj['title'],
    #         memo = obj['memo'],
    #         created = datetime.now()
    #     )
    #     result = self.conn.execute(ins)
    #     session.commit()
    #
    #     classroom_data = session.query(Classrooms).filter(Classrooms.id == result.inserted_primary_key[0]).one()
    #     # print(classroom_data)
    #     return classroom_data
    #
    # def getClassrooms(self, session, uid, name, status, role):
    #     classroom_list =  []
    #     if name == "my_classroom_cv":
    #         print("======= get my_classrooms =======")
    #         classroom_list = session.query(Classrooms, Users)\
    #         .outerjoin(Users, Classrooms.uid == Users.uuid)\
    #         .filter(Classrooms.uid == uid).all()
    #     elif name == "pub_classroom_cv":
    #         print("======= get pub_classrooms =======")
    #         classroom_list = session.query(Classrooms, Users)\
    #         .outerjoin(Users, Classrooms.uid == Users.uuid)\
    #         .filter(Classrooms.status == 1).all()
    #     elif name == "follow_classroom_cv":
    #         print("======= get follow_classrooms =======")
    #         # ここは未だできていない
    #         classroom_list = session.query(Classrooms, Users)\
    #         .outerjoin(Users, Classrooms.uid == Users.uuid)\
    #         .filter(Classrooms.role == 2, Classrooms.uid == uid).all()
    #
    #     if classroom_list:
    #         return classroom_list
    #     else: "false"
    #
    # def getTasksetByTID(self, session, tid, classroom_id):
    #     taskset = session.query(Tasksets).filter(Tasksets.classroom_id == classroom_id, Tasksets.tid == tid, Tasksets.status==1).first()
    #     print(taskset)
    #     return taskset
    #
    # def insertTaskset(self, session, obj):
    #     print("======= insert task in classroom =======")
    #     taskset = self.getTasksetByTID(session, obj['tid'], obj['classroom_id'])
    #     if taskset:
    #         return "Error :( You cannot add a already existing task in the same classroom."
    #     else:
    #         ins = self.tasksetsT.insert().values(
    #                 classroom_id = obj['classroom_id'],
    #                 tid = obj['tid'],
    #                 uid = obj['uid'],
    #                 status = obj['status'],
    #                 created = datetime.now()
    #         )
    #         res = self.conn.execute(ins)
    #         self.session.commit()
    #         # taskset_data = session.query(Tasksets).filter(Tasksets.id == result.inserted_primary_key[0]).one()
    #         # return taskset_data
    #
    #         if res:
    #             return "Success :) your task is registored in the classroom :)"
    #         else:
    #             return "Error :("
    #
    # def updateTaskset(self, session, obj):
    #     print("======= update task in classroom =======")
    #
    #     res = session.query(Tasksets).filter(Tasksets.classroom_id == obj['classroom_id'],Tasksets.tid == obj['tid']).update({Tasks.status : obj['status']})
    #     session.commit()
    #     return "OK"
    #
    # def getTasksets(self, session, classroom_id, status):
    #     print("======= get TASKSETS collection =======")
    #     print(classroom_id)
    #     classroom_id_list = session.query(Tasksets).filter(Tasksets.classroom_id == classroom_id, Tasksets.status == status).all()
    #     print(classroom_id_list)
    #     tasklist = []
    #     print("======= get EACH ID =======")
    #     for row in classroom_id_list:
    #         print(row.tid)
    #         task = self.getTaskByTID(session, row.tid)
    #         # print(task)
    #         if task:
    #             video = self.getVideoInfoByID(session, task['video_id'], task['lang'], task['local_lang'])
    #             # print(video_info)
    #             if video:
    #                 info = {
    #                     'classroom_id': classroom_id,
    #                     'uid': task['uid'],
    #                     'status': task['status'],
    #                     'tid' : task['uuid'],
    #                     'lang': task['lang'],
    #                     'local_lang': task['local_lang'],
    #                     'host': video['host'],
    #                     # 'vid': video['vid'],
    #                     'video_id': video['video_id'],
    #                     'video_key': video['video_key'],
    #                     'img': video['img'],
    #                     'title': video['title'],
    #                     'title_local': video['title_local'],
    #                     'author':video['author']
    #                 }
    #                 tasklist.append(info)
    #             else:
    #                 print("Fail to get video")
    #         else:
    #             print("Fail to get task info")
    #
    #     print(tasklist)
    #     return tasklist
    #
    # #  ========================================================================================== SCRIPT #
    # #  ======================================================================== GET #
    #
    # def getScripts(self, session, tid):
    #     # self.session = self.Session()
    #     print("======= getScripts =======")
    #     script_list = session.query(Scripts).filter(Scripts.tid == tid).all()
    #     return script_list
    #
    # def getScriptSource(self, session, tid, q_num):
    #     # self.session = self.Session()
    #     print("======= getScript =======")
    #     script = session.query(Scripts).filter(Scripts.tid == tid, Scripts.q_num == q_num).first()
    #     if script:
    #         return script.__dict__
    #     else:
    #         return None
    #
    # def getLastTaskRecord(self, session, tid):
    #     # self.session = self.Session()
    #     print("======= getLastRecord =======")
    #     # script = self.session.query(Scripts).join(Tasks, Scripts.tid == Tasks.uuid)\
    #     # .filter(Tasks.user_id == user_id, Scripts.done == 1).first()
    #     script = session.query(Scripts).filter(Scripts.tid == tid, Scripts.done == 1).order_by(Scripts.q_num.desc()).first()
    #     if script:
    #         return script.__dict__
    #     else:
    #         return None
    #
    # def getLastRecord(self, session, uid):
    #     self.session = self.Session()
    #     print("======= getLastRecord =======")
    #     # script = self.session.query(Scripts).join(Tasks, Scripts.tid == Tasks.uuid)\
    #     # .filter(Tasks.user_id == user_id, Scripts.done == 1).first()
    #     res = self.session.query(Scripts)\
    #     .join(Tasks, Scripts.tid == Tasks.uuid).filter( Tasks.uid == uid, Scripts.done == 1, Scripts.user_level2.isnot(None), Scripts.blank_rate2.isnot(None)).order_by(Scripts.created.desc()).first()
    #     if res:
    #         return  res
    #     else:
    #         return None
    #
    #
    # #  ======================================================================== INSERT #
    #
    # def updateScript(self, session, obj):
    #     # self.session = self.Session()
    #     print("======= updateScript =======")
    #     # question = json.dumps(obj['question'])
    #     # timestamp = json.dumps(obj['timestamp'])
    #     res = session.query(Scripts).filter(Scripts.tid == obj['tid'], Scripts.q_num == obj['q_num']).update({
    #     Scripts.question : obj['question'],
    #     Scripts.timestamp : obj['timestamp'],
    #     Scripts.script_local : obj['script_local'],
    #     Scripts.advice : obj['advice'],
    #     Scripts.modified : datetime.now()
    #     })
    #     print(res)
    #     session.commit()
    #     script_data = session.query(Scripts).filter(Scripts.tid == obj['tid'], Scripts.q_num == obj['q_num']).first()
    #     return script_data
    #
    # def copyScripts(self, session, tid, uid, new_tid):
    #
    #     print(tid, uid, new_tid)
    #     print('<<<<< mydb.getScripts')
    #     plot_list = self.getScripts(session, tid)
    #
    #     # self.session = self.Session()
    #     for row in plot_list:
    #         print('mydb.copyScript >>>>')
    #         # self.session.expunge()
    #         print(new_tid, uid)
    #         make_transient(row)
    #         row.id = None
    #         row.tid = new_tid
    #         row.uid = uid
    #         row.created = datetime.now()
    #         self.session.add(row)
    #         # self.copyScript(plot, tid)
    #     self.session.flush()
    #     self.session.commit()
    #     self.session.close()
    #     return new_tid
    #
    # def copyScript(self, plot, tid):
    #     self.session = self.Session()
    #     print("======= insert SCRIPT info =======")
    #     print(plot)
    #     # print(plot['vid'])
    #
    #     # vid = plot['vid'] if plot['vid'] else 0
    #     # video_id = plot['video_id'] if plot['video_id'] else 0
    #     # q_num = plot['q_num'] if plot['q_num'] else 0
    #
    #     Scripts.__table__.insert().execute(plot)
    #
    #     # ins = self.scriptsT.insert().values(
    #     #     tid = tid,
    #     #     vid = plot['vid'],
    #     #     video_id = plot['video_id'],
    #     #     q_num = plot['q_num'],
    #     #     done = 0,
    #     #     created = datetime.now()
    #     # )
    #     # result = self.conn.execute(ins)
    #     self.session.commit()
    #     self.session.close()
    #
    #     return 'true'
    #
    #
    def insertScripts(self, session, obj, profile, plot_list):
        tid = str(uuid.uuid4())
        # print(plot_list)
        for plot in plot_list:
            res = self.insertScript(session, obj, profile, plot, tid)
            # print(res)
        return tid

    def insertScript(self, session, obj, profile, plot, tid):

        # print("======= insert SCRIPT info =======")
        # print(plot)
        ins = self.scriptsT.insert().values(
                tid = tid,
                vid = obj['uuid'],
                video_id = obj['video_id'],
                uid = profile['user'],
                user_level = profile['user_level'],
                blank_rate = profile['blank_rate'],
                q_num = int(plot['q_num']),
                timestamp = plot['timestamp'],
                script_main = plot['script_main'],
                # script_local = plot['script_local'],
                question = plot['question'],
                token = plot['token'],
                stopword = plot['stopword'],
                tagged = plot['tagged'],
                tag_id = plot['tag_id'],
                lemma = plot['lemma'],
                jacet = plot['jacet'],
                probability = plot['probability'],
                created = datetime.now()
        )

        result = self.conn.execute(ins)
        session.commit()
        # self.session.close()

        # print('result %s' % result.inserted_primary_key)
        # script_data = self.session.query(Scripts).filter(Scripts.id == result.inserted_primary_key[0]).one()
        # return script_data.__dict__
        return plot['q_num']

    # #  ========================================================================================== TASK #
    # #  ======================================================================== GET #
    #
    # def copyTask(self, session, tid, uid):
    #     # self.session = self.Session()
    #     print("======= copyTask =======")
    #     origin = tid
    #     follow_id = 0
    #
    #     original_task = self.getTaskByTID(session, tid)
    #     print(original_task)
    #     res = self.switchTask(session, tid)
    #     print(res)
    #
    #     new_tid = str(uuid.uuid4())
    #     task = self.createTask(session, original_task, new_tid, uid, origin, follow_id, original_task['total_q'])
    #     return task.__dict__
    #     # return json.dumps(task, cls=AlchemyEncoder, ensure_ascii=False)
    #
    # # def getTaskByID(self, task_id):
    # #     self.session = self.Session()
    # #     print("======= get TASK by ID =======")
    # #     print(task_id)
    # #     # task = self.session.query(Tasks).filter(Tasks.id == 2128).first()
    # #     task = self.session.query(Tasks).filter(Tasks.id == task_id).first()
    # #     # print(task)
    # #     return task.__dict__
    #
    # def getTaskByTID(self, session, tid):
    #     # self.session = self.Session()
    #     print("======= getTaskByTID =======")
    #     print(tid)
    #     task = session.query(Tasks).filter(Tasks.uuid == tid).first()
    #     return task.__dict__
    #
    # # def getTaskByTID2(self, session, tid):
    # #     # self.session = self.Session()
    # #     print("======= getTaskByTID =======")
    # #     print(tid)
    # #     task = session.query(Tasks, Videos).outerjoin(Tasks, Tasks.video_id == Videos.video_id, Tasks.lang == Videos.lang).filter(Tasks.uuid == tid).first()
    # #     return task.__dict__
    #
    # def switchTask(self, session, tid):
    #     # self.session = self.Session()
    #     print("======= switchTask =======")
    #     print(tid)
    #     res = session.query(Tasks).filter(Tasks.uuid == tid).update({Tasks.status : -1})
    #     session.commit()
    #     session.close()
    #     return res
    #
    # def getGameIniciationInfoByTID(self, session, tid):
    #     # self.session = self.Session()
    #     print("======= get GameIniciationInfo by ID =======")
    #     print(tid)
    #     task_info = session.query(Tasks).filter(Tasks.uuid == tid).first()
    #     video_info = self.getVideoInfoByID(session, task_info.video_id, task_info.lang, task_info.local_lang)
    #
    #     task_dict = {
    #         'status': task_info.status,
    #         'user_id': task_info.user_id,
    #
    #         'id' : task_info.id,
    #         'tid': task_info.uuid,
    #
    #         'mode': task_info.mode,
    #         'level': task_info.level,
    #         'score': task_info.score,
    #         'start_q': task_info.start_q,
    #         'end_q': task_info.end_q,
    #         'total_q': task_info.total_q,
    #
    #         'memo': task_info.memo,
    #         'follow_id': task_info.follow_id,
    #         'origin': task_info.origin,
    #
    #         'lang': task_info.lang,
    #         'local_lang': task_info.local_lang,
    #
    #         'host': video_info['host'],
    #         'vid': video_info['vid'],
    #         'video_id': video_info['video_id'],
    #         'video_key': video_info['video_key'],
    #         'img': video_info['img'],
    #         'download_url': video_info['video_link'],
    #         'title': video_info['title'],
    #         'title_local': video_info['title_local'],
    #         'author':video_info['author'],
    #         'adjustment':video_info['adjustment']
    #     }
    #
    #     return task_dict
    #
    def getTaskByVideoKey(self, session, video_key, user_level, blank_rate):
        print("======= get TASK =======")
        task = session.query(Tasks).filter(Tasks.video_key == video_key, Tasks.level == user_level, Tasks.blank_rate == blank_rate).first()
        return task
    #
    # def getTasks(self, session, user_id, status):
    #     # self.session = self.Session()
    #     print("======= get TASK-LIST =======")
    #     print(user_id, status)
    #
    #     res_list = session.query(Tasks).filter(Tasks.user_id == user_id, Tasks.status == status).all()
    #     # print(resultset)
    #
    #     task_list = []
    #
    #     for row in res_list:
    #         # res = row.__dict__
    #         # print(res)
    #         print("<<<<< self.getVideoInfoByID")
    #         video_info = self.getVideoInfoByID(session, row.video_id, row.lang, row.local_lang)
    #         # progress = self.getProgressInfoByID(row.uuid)
    #
    #         script = self.getLastTaskRecord(session, row.uuid)
    #         print(script)
    #         progress = script['q_num'] if script else 0
    #
    #         # print(video_info)
    #         #返り値を生成
    #         # res['_sa_instance_state'] = None
    #         if video_info:
    #             task = {
    #                 'status': status,
    #                 'user_id': user_id,
    #
    #                 'id' : row.id,
    #                 'tid': row.uuid,
    #
    #                 'mode': row.mode,
    #                 'level': row.level,
    #                 'score': row.score,
    #                 'start_q': row.start_q,
    #                 'end_q': row.end_q,
    #                 'progress': progress,
    #
    #                 'memo': row.memo,
    #                 'follow': 0,
    #                 'follow_id':row.follow_id,
    #
    #                 'lang': row.lang,
    #                 'local_lang': row.local_lang,
    #
    #                 'host': video_info['host'],
    #                 'vid': video_info['vid'],
    #                 'video_id': video_info['video_id'],
    #                 'video_key': video_info['video_key'],
    #                 'img': video_info['img'],
    #                 'video_link': video_info['video_link'],
    #                 'title': video_info['title'],
    #                 'title_local': video_info['title_local'],
    #                 'author':video_info['author'],
    #                 'plot':video_info['plot'],
    #                 'plot_local':video_info['plot_local'],
    #
    #                 'size':video_info['size'],
    #                 'difficulty1':video_info['difficulty1'],
    #                 'difficulty2':video_info['difficulty2']
    #             }
    #             # print(task)
    #             task_list.append(task)
    #         else:
    #             print("getTasks Fail")
    #     return task_list
    #
    # #  ======================================================================== INSERT #
    #
    def createTask(self, session, obj, tid, profile, origin, follow_id, len):
        # self.session = self.Session()
        print("======= insert TASK info =======")
        # print(obj, tid, uid, origin, follow_id, len)
        ins = self.tasksT.insert().values(
                uuid = tid,
                vid = obj['uuid'],
                # user_id = obj['user_id'],
                uid = profile['user'],
                video_id = obj['video_id'],
                video_key = obj['video_key'],
                lang = obj['lang'],
                # local_lang = obj['local_lang'],
                host = obj['host'],

                status = 1,
                memo = obj['memo'],
                mode = obj['mode'],
                chunk = bool(profile['chunk']),
                level = obj['level'],
                blank_rate = profile['blank_rate'],

                # score = obj['score'],
                # progress = obj['progress'],
                # owner_id = obj['owner_id'],
                origin = origin,
                follow_id = follow_id,

                vol = -1,
                start_q = 1,
                end_q = len,
                total_q = len,

                # v_relate = obj['v_relate'],
                # v_enjoy = obj['v_enjoy'],
                # v_play = obj['v_play'],
                # v_understand= obj['v_understand'],
                # comment = obj['comment'],
                created = datetime.now()
        )

        result = self.conn.execute(ins)
        session.commit()
        # session.close()

        # print('result %s' % result.inserted_primary_key)
        task_data = session.query(Tasks).filter(Tasks.id == result.inserted_primary_key[0]).one()

        return task_data
    #
    # #  ========================================================================================== GAME #
    # #  ======================================================================== GET #
    #
    # def updateGameResult(self, obj):
    #     self.session = self.Session()
    #     print("======= update completed game record =======")
    #     res = self.session.query(Tasks).filter(Tasks.uuid == obj['tid']).update({
    #     Tasks.v_enjoy : int(obj['v_enjoy']),
    #     Tasks.v_play : int(obj['v_play']),
    #     Tasks.v_understand : int(obj['v_understand']),
    #     Tasks.v_relate : int(obj['v_relate']),
    #     Tasks.comment : obj['comment'],
    #     Tasks.modified : datetime.now()
    #     })
    #     self.session.commit()
    #     self.session.close()
    #     print(res)
    #     return 'true'
    #
    # # def getProgressInfoByID(self, tid):
    # #     print("======= getProgress =======")
    # #     q_num = self.session.query(Games.q_num).filter(Games.tid == tid, Games.done == 1).order_by(Games.q_num.desc()).first()
    # #     if q_num:
    # #         q_num = q_num[0]
    # #     else:
    # #         q_num = 0
    # #     print(q_num)
    # #     return q_num
    #
    # def getGameRecords(self, tid):
    #     self.session = self.Session()
    #     print("======= getGameRecords =======")
    #
    #     # record_list = self.session.query(Games).filter(Games.tid == tid).order_by(Games.q_num.amount.desc())
    #     res = self.session.query(Games).filter(Games.tid == tid).all()
    #     # print(record_list)
    #
    #     if res:
    #         return res
    #     else:
    #         return None
    #
    # def insertGameRecords(self, tid, q_num):
    #     self.session = self.Session()
    #     print("======= insert GameRecord space =======")
    #
    #     ins = self.gamesT.insert().values(
    #             tid = tid,
    #             q_num = q_num,
    #             done = 0,
    #             created = datetime.now()
    #     )
    #
    #     result = self.conn.execute(ins)
    #     self.session.commit()
    #     self.session.close()
    #
    #     # print('result %s' % result.inserted_primary_key)
    #     # script_data = self.session.query(Scripts).filter(Scripts.id == result.inserted_primary_key[0]).one()
    #     # return script_data.__dict__
    #     return 'true'
    #
    # def updateGameRecord(self, session, tid, q_num):
    #
    #     print("======= update done Script Record =======")
    #     res = session.query(Scripts).filter(Scripts.tid == tid, Scripts.q_num == q_num).update({
    #     Scripts.done : 1,
    #     Scripts.modified : datetime.now()})
    #     session.commit()
    #     return 'true'
    #
    # def updateQuestion(self, session, plot):
    #
    #     print("======= update next Script Record =======")
    #     res = session.query(Scripts).filter(Scripts.tid == plot['tid'], Scripts.q_num == int(plot['q_num'])).update({
    #     Scripts.user_level2 : plot['user_level'],
    #     Scripts.question2 : plot['questions'],
    #     Scripts.probability2 : plot['probability'],
    #     Scripts.blank_rate2 : plot['blank_rate'],
    #     Scripts.modified : datetime.now()})
    #     session.commit()
    #
    #     # res = self.session.query(Games).filter(Games.tid == tid, Games.q_num == int(q_num)).update({Games.done : 1})
    #     return 'true'
    #
    # #  ========================================================================================== VIDEO #
    # #  ======================================================================== GET #
    #
    def getVideoInfo(self, session, video_key, lang):
        # self.session = self.Session()
        print("======= getVideoInfo =======")
        # print(video_key, lang)
        video_data = session.query(Videos).filter(Videos.video_key == video_key, Videos.lang == lang).first()
        if video_data:
            return video_data.__dict__
        else:
            return None
    #
    # def getVideoTaskInfo(self, video_key, lang):
    #     self.session = self.Session()
    #     print("======= getVideoInfo =======")
    #     # print(video_key, lang)
    #     video_data = self.session.query(Videos).filter(Videos.video_key == video_key, Videos.lang == lang).first()
    #     if video_data:
    #         return video_data.__dict__
    #     else:
    #         return None
    #
    def getVideoInfoByID(self, session, video_id):
        # self.session = self.Session()
        print("======= getVideoInfo by ID=======")
        # print(video_id, lang, local_lang)
        res = session.query(Videos).filter(Videos.video_id == video_id).first()
        # res2 = session.query(Videos).filter(Videos.video_id == video_id, Videos.lang == local_lang).first()
        # print(res.id)
        # print(res2)
        if res:
            video_dict = {
                # 'vid': res2.id,
                'vid': res.id,
                'video_id': res.video_id,
                'lang': res.lang,
                # 'local_lang': local_lang,

                'vid': res.id,
                'video_key': res.video_key,
                'host': res.host,

                'url': res.url,
                'title': res.title,
                'subtitle': res.subtitle,

                'author': res.author,
                'plot': res.plot,
                # 'plot_local': res2.plot,
                'plot_id': res.plot_id,
                'description': res.description,
                'memo': res.memo,
                'img': res.img,
                'video_link': res.video_link,
                'duration': res.duration,
                'adjustment': res.adjustment,
                'keywords': res.keywords,
                'tags': res.tags,
                'rating': res.rating,
                'viewed': res.viewed,

                'size': res.size,
                'difficulty1': res.difficulty1,
                'difficulty2': res.difficulty2
            }

            return video_dict
        else:
            return None
    #
    # #  ======================================================================== INSERT #
    #
    # def insertVideoLocalInfo(self,video_info_data):
    #     self.session = self.Session()
    #     print("======= insertVideoLocalInfo =======")
    #
    #     ins = self.videosT.insert().values(
    #         video_id = video_info_data['video_id'],
    #         video_key = video_info_data['video_key'],
    #         host = video_info_data['host'],
    #         video_lang = video_info_data['video_lang'],
    #         lang = video_info_data['lang'],
    #         # lang_list = str(video_info_data['lang_list']),
    #         # lang_list = video_info_data['lang_list'],
    #         # url = video_info_data['url'],
    #         title = video_info_data['title'],
    #         plot = video_info_data['plot'],
    #         subtitle = video_info_data['subtitle'],
    #         # plot_id = video_info_data['plot_id'],
    #         description = video_info_data['description'],
    #         # memo = video_info_data['memo'],
    #         # img = video_info_data['img'],
    #         # video_date = video_info_data['video_date'],
    #         # channel = video_info_data['channel'],
    #         # channel_id = video_info_data['channel_id'],
    #         # author = video_info_data['author'],
    #         # author_id = video_info_data['author_id'],
    #
    #         video_link = video_info_data['video_link'],
    #         # duration = video_info_data['duration'],
    #         # adjustment = video_info_data['adjustment'],
    #         # keywords = video_info_data['keywords'],
    #         # tags = video_info_data['tags'],
    #         # rating = video_info_data['rating'],
    #         # viewed = video_info_data['viewed'],
    #         created = datetime.now()
    #         )
    #
    #     result = self.conn.execute(ins)
    #     self.session.commit()
    #     self.session.close()
    #
    #     print('result %s' % result.inserted_primary_key)
    #     video_data = self.session.query(Videos).filter(Videos.id == result.inserted_primary_key[0]).one()
    #
    #     return video_data.__dict__
    #
    def insertVideoInfo(self, session, video_info_data, video_anal, uid):
        # self.session = self.Session()
        print("======= insertVideoInfo =======")

        ins = self.videosT.insert().values(
            uuid = str(uuid.uuid4()),
            video_id = video_info_data['video_id'],
            video_key = video_info_data['video_key'],
            uid = uid,
            host = video_info_data['host'],
            video_lang = video_info_data['video_lang'],
            lang = video_info_data['lang'],
            lang_list = str(video_info_data['lang_list']),
            # lang_list = video_info_data['lang_list'],

            url = video_info_data['url'],
            title = video_info_data['title'],
            plot = video_info_data['plot'],
            subtitle = video_info_data['subtitle'],
            plot_id = video_info_data['plot_id'],
            description = video_info_data['description'],
            memo = video_info_data['memo'],
            img = video_info_data['img'],
            video_date = video_info_data['video_date'],

            channel = video_info_data['channel'],
            channel_id = video_info_data['channel_id'],

            author = video_info_data['author'],
            author_id = video_info_data['author_id'],

            video_link = video_info_data['video_link'],
            duration = video_info_data['duration'],
            adjustment = video_info_data['adjustment'],

            size = str(video_anal['size']),
            difficulty1 = str(video_anal['difficulty1']),
            difficulty2 = str(video_anal['difficulty2']),

            keywords = video_info_data['keywords'],
            tags = video_info_data['tags'],
            rating = video_info_data['rating'],
            viewed = video_info_data['viewed'],
            created = datetime.now()
            )

        result = self.conn.execute(ins)
        session.commit()
        # self.session.close()

        print('result %s' % result.inserted_primary_key)
        video_data = session.query(Videos).filter(Videos.id == result.inserted_primary_key[0]).one()

        return video_data.__dict__

    def updateVideoInfo(self, session, video_anal, vid, uid):
        # self.session = self.Session()
        print("======= updateVideoInfo =======")
        res = session.query(Videos).filter(Videos.uuid == vid).update({
            Videos.size : str(video_anal['size']),
            Videos.difficulty1 : str(video_anal['difficulty1']),
            Videos.difficulty2 : str(video_anal['difficulty2']),
            Videos.modified : datetime.now()
            })
        session.commit()
        video_data = session.query(Videos).filter(Videos.uuid == vid).first()
        return video_data.__dict__


    # #  ========================================================================================== LOGIN #
    # #  ======================================================================== POST #
    #
    # def getUser(self, email):
    #     self.session = self.Session()
    #     print("======= getUser =======")
    #     # print(email)
    #     user = self.session.query(Users).filter(Users.email == email).first()
    #     if user:
    #         if not user.uuid:
    #             print("======= update uuid =======")
    #             user.uuid = str(uuid.uuid4())
    #             res = self.session.query(Users).filter(Users.email == email).update({Users.uuid : user.uuid })
    #             self.session.commit()
    #             self.session.close()
    #
    #         # print('<<<<< mydb.getLastRecord')
    #         # record = self.getLastRecord(user.id)
    #         # print(record)
    #         # user.user_level = record['user_level']
    #         # user.blank_rate = record['blank_rate']
    #         # return json.dumps(user, cls=AlchemyEncoder)
    #         # print(user)
    #         return user.__dict__
    #     else:
    #         return 'None'

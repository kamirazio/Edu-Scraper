import re
import json
# from flask import jsonify
# from flask.json import JSONEncoder

import math
import numpy as np
from scipy.stats import norm

from ytmlpy import yt_nlp
from ytmlpy import yt_utils
import pdb

used_lemma_list =[]
used_token_list =[]

#===================================================== DB
from ytmlpy.yt_mysql import ORMDB
mydb = ORMDB('ytml')
#=====================================================

# def createTimeStampList():
#     if timestamp == []:
#         # 新しい sucript レコードを生成
#         # [337423, 341424, 4001, false]/[頭,尻,再生時間,段落]
#         timestamp = [script['startTime'], int(script['startTime']) + int(script['duration']), script['duration'], script['startOfParagraph']]
#         script_main = script['content']
#         return script_main, timestamp
#     else:
#         # timelineとscriptをマージする
#         timestamp[1] = timestamp[1] + script['duration']
#         timestamp[2] = timestamp[2] + script['duration']
#         script_main = str(script_main) +' '+ str(script['content'])
#         return script_main, timestamp

def analyzeScripts(obj, scripts, profile):
    # print(obj)
    # obj['chunk'] = 0
    # obj['user_level'] = 1000
    # obj['blank_rate'] = 25

    end_sign = ['.','?','!',';',':',')','"',"'"]
    # pattern = "(\.|\?|\!)(\'|\")"
    # repatter = re.compile(pattern)

    timestamp =[]
    plot_list =[]
    q_num = 1
    # 初期化
    used_lemma_list =[]
    used_token_list =[]
    tw_cnt=0
    tc_cnt=0

    for i in range(len(scripts)):

        # print("======= script分析:%d ========" % i)
        script = scripts[i]

        if timestamp == []:
            # 新しい sucript レコードを生成
            # [337423, 341424, 4001, false]/[頭,尻,再生時間,段落]
            timestamp = [script['startTime'], int(script['startTime']) + int(script['duration']), script['duration'], script['startOfParagraph']]
            script_main = script['content'].rstrip("\r\n")

        else:
            # timelineを上書きし、scriptをマージする
            timestamp[1] = timestamp[1] + script['duration']
            timestamp[2] = timestamp[2] + script['duration']
            script_main = str(script_main) +' '+ str(script['content'])
            script_main = script_main.rstrip("\r\n")

        # print('正規表現 実験') # 文末かChunk Optionが選択されている時の処理 # P['"]$ //句読点
        # print(repatter.match(script_main))
        # もし台詞の最後のletterが句読点・記号だったら or chunkする or 括弧があれば or [." ?"]などの終わり方
        if len(scripts) > i+1:
            if len(script_main.split(' ')) < 3 and profile['chunk'] == 0 :
                print('skip-1 ::',i, len(scripts))
                print(script_main)
                # pdb.set_trace()
                continue

            if script_main[-1] not in end_sign and profile['chunk'] == 0 :
                print('skip-2 ::',i)
                print(script_main)
                # pdb.set_trace()
                continue

            # if repatter.match(script_main) is not None and obj['chunk'] == 0:
            #     print('skip-3 ::',i)
            #     print(script_main)
            #     # pdb.set_trace()
            #     continue

        # if (script_main[-1] in end_sign) or (obj['chunk'] == 1) or (repatter.match(script_main)):
        # print('# ====== 出来上がったスクリプトを分析する ====== #')
        anly_list = yt_nlp.getNLTKRes(script_main)

        # readability calcuration
        tw_cnt += anly_list['w_cnt']
        tc_cnt += anly_list['c_cnt']

        # print('# ============ #')
        # print(anly_list)
        # # ====== Jaset Rank の作成 ====== #
        # jacet_list = mydb.getJacet(session, anly_list['lemma'])
        # print('# ============ #')

        # ====== 出来上がったスクリプトにサブタイトルを振る ====== #
        # script_local = fixScriptLocal(sub_scripts,timestamp)

        # ====== user data の取得 ====== #
        # これはインタラクティブに獲得
        profile.update({
            'complete_list':[],
            'success_list':[],
            'review_list':[],
            'cheat_list':[],
            'repeat_list':[],
            'skip_list':[],
            'save_list':[],
            'dict_list':[],
        })

        print('======= question の生成(仮) =======')
        question_list = []
        # print('<<<<< getProbability')
        prob_val_list = getProbability(profile, anly_list)
        # print('==== 出現確率 ====')
        # print(prob_val_list)

        # 長さによって、どのくらいの文量をブランクにするか決める
        # q_cnt = math.floor(len(anly_list['tagged']) * 0.2)
        # blank_rate = 0.2
        # print(len(anly_list['tagged']), int(obj['blank_rate']))
        q_cnt = math.ceil(len(anly_list['tagged']) * int(profile['blank_rate'])/100)
        # print(q_cnt)

        print('<<<<< getQuestionIndex1')
        question_list = getQuestionIndex1(q_cnt, prob_val_list)

        # print("======= plot : q_num %d : script %d ========" % (q_num, i))
        # バグ修正
        # if len(anly_list['token'])!=len(jacet_list):
        #     print(len(anly_list['token']))
        #     print(anly_list['token'])
        #     print(len(jacet_list))

        plot = {
            # 'q_num': len(plot_list)+1,
            'q_num': q_num,
            'timestamp': json.dumps(timestamp),
            'script_main': yt_utils.cleanLine(script_main),
            # 'script_local': yt_utils.cleanLine(script_local),
            'question': json.dumps(np.asarray(question_list).tolist()[-1]),
            'question_aqg': json.dumps(np.asarray(question_list).tolist()),
            'token': json.dumps(anly_list['token']),
            'stopword': json.dumps(anly_list['stopword']),
            'tagged': json.dumps(anly_list['tagged']),
            'tag_id': json.dumps(anly_list['tag_id']),
            'lemma': json.dumps(anly_list['lemma']),
            'jacet': json.dumps(anly_list['jacet']),
            'probability': json.dumps(prob_val_list)
        }

        # print(script_main)
        plot_list.append(plot)
        timestamp = []
        q_num = q_num + 1

    # readability = (5.89 * (tc_cnt / tw_cnt)) - (0.3 * 100/tw_cnt/len(plot_list) ) - 15.8
    # print("readability:%s:%s:%s" % (tw_cnt,tc_cnt,readability))

    return plot_list

def analyzeScripts_old(obj, scripts):
    # print(obj)

    obj['chunk'] = 1
    obj['user_level'] = 3000
    obj['blank_rate'] = 30
    end_sign = ['.','?','!',';',':']
    pattern = "(\.|\?|\!)(\'|\")"
    repatter = re.compile(pattern)

    timestamp = []
    plot_list = []

    print("分析する文章のラインの長さ：%d" % len(scripts))

    for i in range(len(scripts)):

        print("======= script分析スタート:%d ========" % i)
        script = scripts[i]
        print("======= timeline 合体分析:%d ========" % i)
        # script_main, timestamp = createTimeStampList(script, i)
        if timestamp == []:
            # 新しい sucript レコードを生成
            # [337423, 341424, 4001, false]/[頭,尻,再生時間,段落]
            timestamp = [script['startTime'], int(script['startTime']) + int(script['duration']), script['duration'], script['startOfParagraph']]
            script_main = script['content']
            return script_main, timestamp
        else:
            # timelineとscriptをマージする
            timestamp[1] = timestamp[1] + script['duration']
            timestamp[2] = timestamp[2] + script['duration']
            script_main = str(script_main) +' '+ str(script['content'])
            return script_main, timestamp


        # print('正規表現 実験') # 文末かChunk Optionが選択されている時の処理 # P['"]$ //句読点
        # print(repatter.match(script_main))
        print("======= 句読点のチェック:%d ========" % i)
        if (script_main[-1] in end_sign) or (obj['chunk'] == 1):

            print('# ====== 出来上がったスクリプトを分析する ====== #')
            anly_list = yt_nlp.getNLTKRes(script_main)
            print(anly_list)

            # ====== user data の取得 ====== #
            # これはインタラクティブに獲得
            profile ={
                'user_level': obj['user_level'],
                'complete_list':[],
                'success_list':[],
                'review_list':[],
                'cheat_list':[],
                'repeat_list':[],
                'skip_list':[],
                'save_list':[],
                'dict_list':[],
            }

            print('======= question の生成(仮) =======')
            print('<<<<< getProbability')
            print('==== 出現確率 ====')
            question_list = []
            prob_val_list = getProbability(profile, anly_list)
            print(prob_val_list)

            print('# ====== 問題数 ====== #') # 長さによって、どのくらいの文量をブランクにするか決める
            q_cnt = math.ceil(len(anly_list['tagged']) * int(obj['blank_rate'])/100)
            print(q_cnt)

            print('==== 問題生成 ====')
            question_list = getQuestionIndex1(q_cnt, prob_val_list)
            print(question_list)
            if question_list is not None:
                print("======= plot : q_num %d ========" % i)
                plot = {
                    'q_num': len(plot_list)+1,
                    'timestamp': json.dumps(timestamp),
                    'script_main': yt_utils.cleanLine(script_main),
                    # 'script_local': yt_utils.cleanLine(script_local),
                    'question': json.dumps(question_list),
                    'token': json.dumps(anly_list['token']),
                    'stopword': json.dumps(anly_list['stopword']),
                    'tagged': json.dumps(anly_list['tagged']),
                    'tag_id': json.dumps(anly_list['tag_id']),
                    'lemma': json.dumps(anly_list['lemma']),
                    'jacet': json.dumps(anly_list['jacet']),
                    'probability': json.dumps(prob_val_list)
                }
                plot_list.append(plot)
                timestamp = []
            else:
                print('skip',i)

    return plot_list

def getProbability(profile, anly_list):

    # print(anly_list)
    print("======= profile =======")
    print(profile)

    bracket_flag = False
    start_signs = ['(', '[', '<', '{', '<<', '[[', '«']
    end_signs = [')', ']', '>', '}', '>>', ']]', '»']

    prob_val_list = []


    for i in range( len(anly_list['lemma']) ):
        prob = 1

        w = anly_list['lemma'][i]

        # ------ 1st branch ------#
        if anly_list['stopword'][i] in [3,4,5]:
            # stopwordで、出題しない単語
            prob = prob * 0

        elif anly_list['stopword'][i] == 6:
            # print('# 括弧だったら ')
            prob = prob * 0
            if bracket_flag:
                # print('かっこ>>>')
                bracket_flag = False
            else:
                # print('<<<かっこ')
                bracket_flag = True

        elif bracket_flag:
            # print('かっこ')
            prob = prob * 0

        elif anly_list['stopword'][i] in [1,2]:
            # stopwordで、出題されてもよい単語
            prob = prob * 0.01

        elif anly_list['jacet'][i] == 0:
            # jacetのリストになかった単語
            prob = prob * 0

        elif len(anly_list['lemma'][i]) < 3:
            prob = prob * 0
        else:
            pass

        # ------ 2nd branch ------#
        if i==0:
            # 先頭の単語
            prob = prob * 0.05
        else:
            pass

        # ------ 3rd branch ------#
        if prob is 0:
            pass
        else:
            if anly_list['tagged'][i] == 'NE' or anly_list['tagged'][i] =='CD' or anly_list['tagged'][i] =='FW':
                #固有名詞 # cardinal digit # 外来語
                prob = prob * 0
            elif anly_list['tagged'][i]=='UH':
                # Interjection 感嘆詞
                prob = prob * 0
            elif anly_list['tagged'][i]=='DT':
                # determiner 決定詞、限定詞 this, these, that, those
                prob = prob * 0.1
            elif anly_list['tagged'][i].startswith('V'):
                prob = prob * 0.9
            elif anly_list['tagged'][i].startswith('N'):
                prob = prob * 0.8
            elif anly_list['tagged'][i].startswith('R'):
                prob = prob * 0.7
            elif anly_list['tagged'][i].startswith('J'):
                # Ajective
                prob = prob * 0.7
            elif anly_list['tagged'][i].startswith('W'):
                # 5w1h
                prob = prob * 0.8
            elif anly_list['tagged'][i].startswith('IN'):
                # preposition/subordinating conjunction
                prob = prob * 0.7
            elif anly_list['tagged'][i].startswith('CC'):
                # coordinating conjunction
                prob = prob * 0.5
            elif anly_list['tagged'][i].startswith('MD'):
                # 助動詞
                prob = prob * 0.7
            else:
                prob = prob * 0.1

            # print(w)
            # print(anly_list['stopword'][i])
            # print(anly_list['jacet'][i])

            # ------ 4th Dependancy branch  ------#


            # ------ 5th branch Repetition ------#
            if prob is 0:
                pass
            else:
                if anly_list['token'][i] in used_token_list:
                    # print("ダブった >< %s:%s" % (anly_list['token'][i],prob))
                    prob = prob * 0.1
                    # print(prob)
                elif anly_list['lemma'][i] in used_lemma_list:
                    # print("かすった ;_; %s" % anly_list['lemma'][i])
                    prob = prob * 0.6
                else:
                    used_token_list.append(anly_list['token'][i])
                    used_lemma_list.append(anly_list['lemma'][i])

                # ------ 6th branch Experience ------#


                # ------ 7th branch Jacet8000 ------#
                u_level = int(profile['user_level']) if profile['user_level'] else 3000
                u_level = 1/8000 * u_level

                # x = np.arange(0, 1, 0.01)
                # y = norm.pdf(x,  loc=user_level, scale=1)

                v_level = int(anly_list['jacet'][i])
                # print("v_level = %d" % v_level)
                x1 = 1/8000 * v_level
                y1 = norm.pdf(x1,  loc=u_level, scale=1)
                # distance = abs(int(anly_list['jacet'][i]) - ( level * 0.001 ))
                # print("p value = %d" % y1)
                prob = round(prob * y1, 10)

        # print("prob = %d" % prob)
        prob_val_list.append(prob)

    # print('==== 出現確率 ====')
    # print(prob_val_list)
    return prob_val_list

# def fixScriptLocal(sub_scripts,timestamp):
#     content = ""
#     flag = True
#     while flag and len(sub_scripts) > 0:
#         sub_end_time = int(sub_scripts[0]['startTime']) + int(sub_scripts[0]['duration'])
#         content = str(content) +' '+ str(sub_scripts[0]['content'])
#         sub_scripts.pop(0)
#         flag = timestamp[1] > sub_end_time
#     return content

def getQuestionIndex1(q_cnt, prob_val_list):
    print('問題形式の生成：0/1の生成順序を行列で表現')
    try:
        prob_arr = np.array(prob_val_list)

        # ソートされていない上位k件のインデックス
        unsorted_max_indices = np.argpartition(-prob_arr, q_cnt)[:q_cnt]
        print(unsorted_max_indices)

        # 上位 q_cnt 件の値
        y = prob_arr[unsorted_max_indices]
        print(y)
        # 大きい順にソートし、インデックスを取得
        indices = np.argsort(-y)
        print(indices)
        print('出現確率の１次元配列:上位k件')
        max_k_indices = unsorted_max_indices[indices]
        print(max_k_indices)
        q_index_list = np.full((len(max_k_indices),len(prob_val_list)),0)
        # array([ [0,0,0,0,1,0], [0,0,0,1,1,0], [0,1,0,1,1,0] ])
        ini_list = np.full(len(prob_val_list),0)
        # array([0, 0, 0])

        # q_index_list = []
        for i in range(len(max_k_indices)):
            ini_list[max_k_indices[i]]=1
            # print(ini_list)
            q_index_list[i] = ini_list

        # for i in range(len(prob_val_list)):
        #     if prob_val_list[i] == 0 or prob_val_list[i] == 0.0:
        #         q_index_list.append(0)
        #     elif i in max_k_indices:
        #         q_index_list.append(1)
        #     else:
        #         q_index_list.append(0)
        print(q_index_list)
    except:
        q_index_list = None

    return q_index_list



# def getQuestionIndex2(q_cnt, prob_val_list):
#     q_index_list=[]
#     #探す対象リスト:prob_arrはnumpy
#     prob_arr = np.array(prob_val_list)
#     sum_prob_val = np.sum(prob_arr)
#     ratio = prob_arr/sum_prob_val
#     print(ratio)
#     # print(np.sum(ratio))
#     val_holder = np.where(prob_arr > 0)
#     val_cnt = len(val_holder[0])
#     print(q_cnt, val_cnt)
#
#     print('2の特徴：出現確率によって問題を決定する')
#     q_cnt = q_cnt if q_cnt < val_cnt else val_cnt
#     indices = np.random.choice(len(prob_val_list), q_cnt, p=ratio, replace=False)
#     # indices = np.random.choice(len(prob_val_list), q_cnt, replace=False)
#     print(indices)
#
#     for i in range(len(prob_val_list)):
#         if i in indices:
#             q_index_list.append(1)
#         else:
#             q_index_list.append(0)
#
#     print(q_index_list)
#     print("q_index_list success")
#     return q_index_list


# def getExperienceTest():
#     user_id = 1
#     lemma_list = ['of','study','boring']
#
#     for i in range(len(lemma_list)):
#         ex_list = mydb.getWordExperience( lemma_list[i], user_id)
#     return 'done'
#
# def getExperience(user_id):
#
#     ex_list = []
#
#     for i in range(len(lemma_list)):
#         exs_res = mydb.getWordExperience(lemma_list[i], user_id)
#
#         exs.append(exs_res[0])
#         successes.append(exs_res[1])
#         fails.append(exs_res[2])
#         dics.append(exs_res[3])
#         saves.append(exs_res[4])
#
#         # ex_fail_list.append(ex_list['status'])
#         #
#         # if ex_list[i]['status'] == -1:
#         #
#         #     't_dict':
#         # }
#         #
#         #  = [] # 1:check 0:pass
#         # t_save = [] # 1:save_box1 2:save_box2 0:unreserve
#         # # t_listen = [] # num:listen
#         # t_repeat = [] # num:repeat
#         # mark = # r05ea4 letter-> letter:pass num:miss 0:cheat
#         # t_miss = [] # num: miss 0: no miss
#         # t_cheat = [] # num:cheat 0: no cheat
#         # t_skip = [] # 1:skip 0:not skip
#
#         ex_index_list.append();
#
#     return ex_index_list

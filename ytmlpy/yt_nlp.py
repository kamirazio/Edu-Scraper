# yt_nlp.py

import nltk
from nltk import sent_tokenize, word_tokenize
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import numpy as np
from scipy import stats

# from sklearn.feature_extraction.text import CountVectorizer

# import yt_utils
from ytmlpy import yt_utils

#===================================================== DB
from ytmlpy.yt_mysql import ORMDB
mydb = ORMDB('ytml')
#=====================================================

script = """I hope my artwork creates a safe spacefor this type of honest exchangeand an opportunity
        for people to engage one anotherin real and necessary conversation."""

script = """ The Finland-based company expects a weaker dollar and slower economic growth in the U.S.
and parts of Europe to dampen the overall handset market this year.
About half of Nokia's (NOK) sales are in dollars or currencies tied to it; a weaker dollar makes imports more expensive.
I made it."""

# lemmatizer = WordNetLemmatizer()
# print(lemmatizer.lemmatize("cats"))
tags = {
'CC':11,'CD':12,'DT':13,'EX':14,'FW':15,\
'IN':20,'JJ':30,'JJR':31,'JJS':32,'LS':16,\
'MD':40,'NN':50,'NNS':51,'NNP':52,'NNPS':53,'NE':54,\
'PDT':60,'POS':61,'PRP':62,'PRP$':63,'RB':64,\
'RBR':70,'RBS':71,'RP':72,'SYM':16,'TO':21,'UH':17,\
'VB':80,'VBD':81,'VBG':82,'VBN':83,'VBP':84,'VBZ':85,\
'WDT':90,'WP':91,'WP$':92,'WRB':93
}

script = yt_utils.cleanLine(script)

def getJacetScore(script):

    sents = sent_tokenize(script)
    print("sentence size: {}\n".format( len(sents) ))
    tokens = word_tokenize(script)
    print("Vocabulary size: {}\n".format( len(tokens) ))
    tokens_low = [w.lower() for w in tokens]
    taggeds, tagids, lemmas, w_cnt, c_cnt = getTagged(tokens_low)
    stopwords = findStopwords(lemmas)
    words, c_jacets = getJacets(lemmas) #  TODO: words は必要?
    # print(words)
    # print(c_jacets)
    # print(taggeds)
    # print(tagids)
    # print("Lemma list: {}\n".format( lemmas ))

    # create text object for getting keywords # トークンリスト(lemma)からnltk.Textオブジェクトを作る
    texts = nltk.Text(lemmas)
    fdist_all = nltk.FreqDist( texts[i] for i in range(len(texts)) if (stopwords[i] == 0 or stopwords[i] == 1 or stopwords[i] == 2) )
    fdist_all_key = fdist_all.keys()
    print("Number of Vocabularies: {}\n".format( len(fdist_all_key) ))

    fdist = nltk.FreqDist( texts[i] for i in range(len(texts)) if stopwords[i] == 0 )
    fdist_key = fdist.keys()

    print("文書中の単語の頻度分布: {}\n".format( fdist[list(fdist_key)[0]] ))
    print("文書中の単語の頻度分布: {}\n".format( fdist.freq( list(fdist_key)[0]) ))

    # print("Number of keywords: {}\n".format( fdist.N() ))
    # print(list(fdist_key))
    keywords, k_jacets = getJacets(list(fdist_key))

    levels = [0,0,0,0,0,0,0,0]
    for i in range(len(k_jacets)):
        if 1000 < k_jacets[i] <= 2000:
            levels[1] += 1
        elif 2000 <= k_jacets[i] < 3000:
            levels[2] += 1
        elif 3000 <= k_jacets[i] < 4000:
            levels[3] += 1
        elif 4000 <= k_jacets[i] < 5000:
            levels[4] += 1
        elif 5000 <= k_jacets[i] < 6000:
            levels[5] += 1
        elif 6000 <= k_jacets[i] < 7000:
            levels[6] += 1
        elif 7000 <= k_jacets[i] < 8000:
            levels[7] += 1
        else:
            levels[0] += 1
    levels[0] += len(fdist_all_key)-len(keywords)
    # print(levels)

    # session = mydb.Session()
    # jacet_res = mydb.getJacet(session, list(fdist_key))
    # session.close()
    # # print("Jacet: {}\n".format( jacet_res ))
    #
    # keywords = []
    # k_jacets = []
    # for i in range(len(jacet_res)):
    #     if jacet_res[i] != 0:
    #         # keywords[list(fdist_key)[i]] = jacets[i]
    #         keywords.append(list(fdist_key)[i])
    #         k_jacets.append(jacet_res[i])

    print("Number of keywords: {}\n".format( len(keywords) ))
    # print(keywords)
    # print(k_jacets)




    # print( "合計: {}\n".format( np.sum(data) ))
    # print( "平均: {}\n".format( np.mean(data) ))
    #
    # print( "1Q: {}\n".format( stats.scoreatpercentile(data, 25) ))
    # print( "中央値: {}\n".format( np.median(data) ))
    # print( "3Q: {}\n".format( stats.scoreatpercentile(data, 75) ))
    #
    # # print( "歪度: {}\n".format( jacets.skew() )
    # # print( "尖度: {}\n".format( jacets.kurt() )
    # print( "最小値: {}\n".format( np.min(data) ))
    # print( "最大値: {}\n".format( np.max(data) ))
    # # print( "相関係数: {}\n".format( jacets.corr() )
    # # print( "分散: {}\n".format( np.var(data) ))
    # print( "標準偏差: {}\n".format( np.std(data) ))
    # # print( "共分散: {}\n".format( jacets.cov() )


    content_size = {}
    content_size['r_ability'] = getReadability(c_cnt, w_cnt, len(sents))
    content_size['s_size'] = len(sents)
    content_size['v_size'] = len(tokens)
    content_size['v_num'] = w_cnt #len(fdist_all_key) #Number of Vocabularies
    content_size['c_num'] = c_cnt #len(''.join(fdist_all_key)) #Number of Vocabularie's chara ,
    content_size['k_num'] = len(keywords)

    c_data = np.array(c_jacets)
    content_difficulty = {}
    content_difficulty['sum'] = np.sum(c_data)
    content_difficulty['mean'] = np.mean(c_data)
    content_difficulty['1Q'] = stats.scoreatpercentile(c_data, 25)
    content_difficulty['median'] = np.median(c_data)
    content_difficulty['3Q'] = stats.scoreatpercentile(c_data, 75)
    content_difficulty['min'] = np.min(c_data)
    content_difficulty['max'] = np.max(c_data)
    content_difficulty['std'] = np.std(c_data)

    k_data = np.array(k_jacets)
    keyword_difficulty = {}
    keyword_difficulty['sum'] = np.sum(k_data)
    keyword_difficulty['mean'] = np.mean(k_data)
    keyword_difficulty['1Q'] = stats.scoreatpercentile(k_data, 25)
    keyword_difficulty['median'] = np.median(k_data)
    keyword_difficulty['3Q'] = stats.scoreatpercentile(k_data, 75)
    keyword_difficulty['min'] = np.min(k_data)
    keyword_difficulty['max'] = np.max(k_data)
    keyword_difficulty['std'] = np.std(k_data)
    keyword_difficulty['levels'] = levels

    return content_size, content_difficulty, keyword_difficulty, w_cnt, c_cnt

def getReadability(total_chr_cnt, total_word_cnt, sentence_len):
    # cpw (average number of characters per word)
    cpw =  total_chr_cnt / total_word_cnt
    # wps (average number of words per sentence)
    wps =  total_word_cnt / sentence_len
    # cli Coleman-Liau index
    cli = (5.89 * cpw) - (0.3 * (100/wps)) - 15.8
    print("readability:%s" % round(cli, 3))
    return round(cli, 3)

def getJacets(word_list):
    session = mydb.Session()
    # jacet_res = mydb.getJacet(session, list(fdist_key))
    jacet_res = mydb.getJacet(session, word_list)
    session.close()
    # print("Jacet: {}\n".format( jacet_res ))
    keywords = []
    jacets = []
    for i in range(len(jacet_res)):
        if jacet_res[i] != 0:
            # keywords[list(fdist_key)[i]] = jacets[i]
            keywords.append(word_list[i])
            jacets.append(jacet_res[i])
    return keywords, jacets

def getNLTKRes(script):
    print('====== @ 文のtokenize ======')
    sent_list =[]
    tokens =[]
    stopwords =[]
    taggeds =[]
    lemmas =[]

    sentences =[]
    sentences = getSentenceList(script)
    # 複数文がある場合マージする
    for sentence in sentences:
        # print('====== Tokens ======')
        tokens.extend(word_tokenize(sentence))

    # print('====== getTagged ======')
    tokens_low = [w.lower() for w in tokens]
    taggeds, tagids, lemmas, w_cnt, c_cnt = getTagged(tokens_low)
    # taggeds.extend(taggeds_temp)
    # lemmas.extend(lemmas_temp)

    # print('====== stopwords ======')
    stopwords = findStopwords(lemmas)
    # stopwords.extend(findStopwords(lemmas_temp))

    print(' ====== @ Jaset Rank の作成 ====== # ')
    session = mydb.Session()
    jacets = mydb.getJacet(session, lemmas)
    session.close()

    sent = {
        'token': tokens,
        'stopword': stopwords,
        'tagged': taggeds,
        'tag_id': tagids,
        'lemma': lemmas,
        'jacet': jacets,
        'w_cnt': w_cnt,
        'c_cnt': c_cnt
    }

    return sent

# ======================================

def getSentenceList(str):
    sents = sent_tokenize(str)
    # print(len(sents))
    return sents

# ======================================

# def tree2dict(tree):
#     return {tree.node: [tree2dict(t)  if isinstance(t, Tree) else t
#                         for t in tree]}

def getTagged(tokens):
    print("tokens")
    # print(tokens)
    tagged = pos_tag(tokens)
    # print(tagged)
    # 固有名詞
    chunked = ne_chunk(tagged,binary=True)

    tagged_list =[]
    tagged_id_list = []
    lemma_list =[]
    lemmatizer = WordNetLemmatizer()
    w_cnt = 0
    c_cnt = 0

    for i in range(len(tagged)):
        # tuppleからlistに変換するため
        tagged_data =[]
        # 固有名詞を調べる
        if "NE" in str(chunked.label()):
            # print(tagged[i])
            # print(chunked[i])
            # tagged_data = [tagged[i][0],chunked[i].label()]
            tagged_list.append(chunked[i].label())
            tagged_id_list.append(54)
            lemma = tagged[i][0]
            # tagged_list.append(tagged_data)
        else:
            tagged_data = [tagged[i][0],tagged[i][1]]
            # tagged_list.append(tagged_data)
            tagged_list.append(tagged[i][1])
            if tagged[i][1] in tags:
                # num = int(tags.index(tagged[i][1]))+1
                num = int(tags[tagged[i][1]])
            else:
                num = 0
            tagged_id_list.append(num)
            # 品詞があるか調べる
            pos = getWN(tagged[i][1])
            # 品詞に基づいたlemmaを取得する
            if pos:
                lemma = lemmatizer.lemmatize(tagged[i][0], pos='%s' % pos)
            else:
                lemma = lemmatizer.lemmatize(tagged[i][0])

        lemma_list.append(lemma.lower())

        if tagged[i][1] in tags:
            w_cnt += 1
            c_cnt += len(tagged[i][0])

    # print(len(tagged_list),len(lemma_list))
    return tagged_list, tagged_id_list, lemma_list, w_cnt, c_cnt

def getWN(tag):

    if tag.startswith('J'):
        # ['JJ', 'JJR', 'JJS']
        return wn.ADJ
    elif tag.startswith('N'):
        # ['NN', 'NE', 'NNS', 'NNP', 'NNPS']
        return wn.NOUN
    elif tag.startswith('R'):
        # ['RB', 'RBR', 'RBS']
        return wn.ADV
    elif tag.startswith('V'):
        # ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        return wn.VERB

    return None

def findStopwords(lemma_list):
    stop_words1 = set(stopwords.words("english"))
    # tokens = word_tokenize(string)
    stop_words2 = ['i','it','its','this','that','these','a','an','the','and','but','or','there','so',\
    'am','is','are','was','were','be','been','have','has','had','having','do','doing','do','does','did','not','yeah','wow','oh']
    stop_words3 = ['\'m','\'re','\'s','\'t','\'ve','\'ll','\'d','s','t','don','doesn','didn','isn','aren','weren','haven','couldn','mustn','won','wouldn','shouldn','shan']
    stop_words4 = ['?','!','.',',','’','“','”','\'','\"','\n',':',';','-','+','¥','$','%','`','|']
    stop_words5 = [' ','--','','\b','\t','\n','\r','\r\n','\`\`','\'\'','\'\'\'']
    stop_words6 = ['[', ']', '[[', ']]', '(', ')', '<', '>', '<<', '>>', '{', '}', '«', '»', '‹', '›']
    # print(len(stop_words2))
    # print(stop_words2)

    stopword_list =[]
    for w in lemma_list:

        if w in stop_words6:
            stopword_list.append(6)
        elif w in stop_words5:
            stopword_list.append(5)
        elif w in stop_words4:
            stopword_list.append(4)
        elif w in stop_words3:
            stopword_list.append(3)
        elif w in stop_words2:
            stopword_list.append(2)
        elif w in stop_words1:
            stopword_list.append(1)
        else:
            stopword_list.append(0)

    # print(len(stopword_list))
    # print(stopword_list)
    return stopword_list

# def getLemmas(tokens, tagged_list):
#     lemmatizer = WordNetLemmatizer()
#     Lemma_list =[]
#     for i in range(len(tokens)):
#         res = lemmatizer.lemmatize(tokens[i], pos="%s" % tagged_list[i])
#         print(res.lower())
#         Lemma_list.append(res.lower())
#     # print(len(Lemma_list))
#     return lemma_list

if __name__ == "__main__":

    getJacetScore(script)

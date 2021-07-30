import jieba
import copy
import os
import math
import operator
from collections import defaultdict
from tqdm import tqdm

stopword_file = r'first\stopwordlist\\'

def TF_IDF_cal(articles:list) ->dict:
    seged_words = seg_depart(articles)
    result = feature_select(seged_words)
    return result

# 读取停用词
def read_stopword() -> list:
    file_list = os.listdir(stopword_file)
    stopword_list = []
    for stopword_file_name in file_list:
        f = open(os.path.join(stopword_file,stopword_file_name), 'r', encoding='utf-8')
        stopword_list += f.readlines()
        f.close()
    return list(set(stopword_list))

# 计算tf-idf的值
def feature_select(list_words) -> dict:
    #总词频统计
    doc_frequency=defaultdict(int)
    for word_list in list_words:
        for i in word_list:
            doc_frequency[i]+=1

    #计算每个词的TF值
    word_tf={}  #存储没个词的tf值
    for i in doc_frequency:
        word_tf[i]=doc_frequency[i]/sum(doc_frequency.values())

    #计算每个词的IDF值
    doc_num=len(list_words)
    word_idf={} #存储每个词的idf值
    word_doc=defaultdict(int) #存储包含该词的文档数
    for i in doc_frequency:
        for j in list_words:
            if i in j:
                word_doc[i]+=1
    for i in doc_frequency:
        word_idf[i]=math.log(doc_num/(word_doc[i]+1))

    #计算每个词的TF*IDF的值
    word_tf_idf={}
    for i in doc_frequency:
        word_tf_idf[i]=word_tf[i]*word_idf[i]

    # 对字典按值由大到小排序
    # dict_feature_select=sorted(word_tf_idf.items(),key=operator.itemgetter(1),reverse=True)
    return word_tf_idf


def seg_depart(articles: list) -> list:
    # 对文档中的每一行进行中文分词
    print("正在分词")

    # 创建一个停用词列表
    stopwords = read_stopword()

    # 输出结果为outstr
    outstr = []
    # 去停用词
    for i in tqdm(range(len((articles)))):
        temp = []
        try:
            sentence_depart = jieba.cut(articles[i].strip())
        except Exception:
            print(articles[i])
            continue
        for word in sentence_depart:
            if word not in stopwords:
                if word != '\t':
                    temp.append(word)
        outstr.append(copy.deepcopy(temp))
    return outstr
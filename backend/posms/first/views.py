from django.shortcuts import render
from weibo.models import Comment, Title, User, PeopleNews, Wangyiedu, Xinhuanews
import json
from django.http import JsonResponse
from django.db.models import Q,F
from django.db import connection
import traceback
import datetime
from ema import ema
import random
import pandas as pd


# from seg import *

def s2(num):
    if num > 0.5:
        return 5
    elif num < 0.05:
        return 1
    elif num >= 0.05 and num < 0.15:
        return 2
    elif num >= 0.15 and num < 0.25:
        return 3
    elif num >= 0.25 and num < 0.5:
        return 4


# 0~100	100~1000	1000~10000	10000~50000	50000 S2离散化标准#
def s1(num):
    if num > 50000:
        return 5
    elif num < 100:
        return 1
    elif num>=100 and num<1000:
        return 2
    elif num >= 1000 and num < 10000:
        return 3
    elif num >= 10000 and num < 50000:
        return 4


# 0~1000	1000~5000	5000~20000	20000~100000	100000 S3离散化#
def s3(num):
    if num > 100000:
        return 5
    elif num < 1000:
        return 1
    elif num>=1000 and num<5000:
        return 2
    elif num >= 5000 and num < 20000:
        return 3
    elif num >= 20000 and num < 100000:
        return 4


# 0~50	50~100%	100%~500	500~100	1000 S4离散化

def s4(num):
    if num > 1000:
        return 5
    elif num < 50:
        return 1
    elif num>=50 and num<100:
        return 2
    elif num >= 100 and num < 500:
        return 3
    elif num >= 500 and num < 1000:
        return 4


#

# 0~50	50~100%	100%~500	500~100	1000 S5离散化
def s5(num):
    if num > 1000:
        return 5
    elif num < 50:
        return 1
    elif num>=50 and num<100:
        return 2
    elif num >= 100 and num < 500:
        return 3
    elif num >= 500 and num < 1000:
        return 4


#

# 0~5%	5%~10%	10%~15%	15%~20%	20%+ S6离散化
#
def s6(num):
    if num > 0.2:
        return 5
    elif num < 0.05:
        return 1
    elif num>=0.05 and num<0.1:
        return 2
    elif num >= 0.1 and num < 0.15:
        return 3
    elif num >= 0.15 and num < 0.2:
        return 4


#

# S7	0~50	50~100	100~500	500~1000	1000 s7离散化
def s7(num):
    if num > 1000:
        return 5
    elif num < 50:
        return 1
    elif num >= 50 and num < 100:
        return 2
    elif num >= 100 and num < 500:
        return 3
    elif num >= 500 and num < 1000:
        return 4


# Create your views here.
def index(request):
    return render(request, 'index.html')


def search(request):  # 获取指定文章列表
    # keywords = request.GET.get('keyword')
    request.params = json.loads(request.body)
    try:
        keywords = request.params['Keyword']
    except:
        return JsonResponse({'code': 1, 'msg': '请求参数没拿到'})
    try:
        #取微博的查询结果
        qs_weibo = Title.objects.values('title_id', 'title', 'url','time')  # .order_by('-title_id')
        if keywords:
            conditions = [Q(title__contains=one) for one in keywords.split(' ') if one]  # 所有查询的列表
            query = Q()
            for condition in conditions:  # 所有关键字是或的关系
                query |= condition
            qs_weibo = qs_weibo.filter(query & Q(iscrawled=1))
        qs_list = list(qs_weibo)
        #取人民网的查询结果，人民网url字段取了别名和weibo保持一致
        qs_people = PeopleNews.objects.values('title_id', 'title', 'url','time')  
        
        if keywords:
            conditions = [Q(title__contains=one) for one in keywords.split(' ') if one]  # 所有查询的列表
            query = Q()
            for condition in conditions:  # 所有关键字是或的关系
                query |= condition
            qs_people = qs_people.filter(query)
        qs_list2 = list(qs_people)
        qs_list.extend(qs_list2)

         #取网易教育的查询结果，网易教育url字段取了别名和weibo保持一致
        qs_wy = Wangyiedu.objects.values('title_id', 'title', 'url','time')  
        
        if keywords:
            conditions = [Q(title__contains=one) for one in keywords.split(' ') if one]  # 所有查询的列表
            query = Q()
            for condition in conditions:  # 所有关键字是或的关系
                query |= condition
            qs_wy = qs_wy.filter(query)
        qs_list3 = list(qs_wy)
        qs_list.extend(qs_list3)

         #取新华教育的查询结果，新华教育url字段取了别名和weibo保持一致
        qs_xh = Xinhuanews.objects.values('title_id', 'title', 'url','time')  
        
        if keywords:
            conditions = [Q(title__contains=one) for one in keywords.split(' ') if one]  # 所有查询的列表
            query = Q()
            for condition in conditions:  # 所有关键字是或的关系
                query |= condition
            qs_xh = qs_xh.filter(query)
        qs_list4 = list(qs_xh)
        qs_list.extend(qs_list4)

        qs_list.sort(key=lambda t: t['time'], reverse=True)  # 按时间先后排序
        return JsonResponse({'code': 0, 'News_list': qs_list})
    except:
        return JsonResponse({'code': 1, 'msg': f'未知错误\n{traceback.format_exc()}'})


def get_num(request):  # 获取数据量
    ph = request.GET.get('type', None)
    if ph:
        request.params = request.GET
        if request.params['type'] == 'num':
            province2 = request.params['province']
            today = datetime.datetime.now().date()  # 获取当天的日期
            # today = datetime.date(2021,7,14)
            # qs = Title.objects.all()
            # for i in qs:
            #     a = ema(i.title)
            #     i.sentiment = ema(i.title)['data']['sentiment']
            #     i.save()
            if province2 == '全国':
                # 取微博的查询结果
                Total_num = Title.objects.values().count()  # 全国文章总数
                Today_num = Title.objects.filter(time__date=today).count()  # 日期为当天的数据总数
                Sensitive_num = Title.objects.filter(sentiment=-1).count()  # 负面信息总量
                #取人民网的查询结果
                Total_num += PeopleNews.objects.values().count()  # 全国文章总数
                Today_num += PeopleNews.objects.filter(time__date=today).count()  # 日期为当天的数据总数
                # Sensitive_num += PeopleNews.objects.annotate(openurl=F('url'),time=F('upload_time')).filter(sentiment=-1).count()  # 负面信息总量
                 #取网易教育的查询结果
                Total_num += Wangyiedu.objects.values().count()  # 全国文章总数
                Today_num += Wangyiedu.objects.filter(time__date=today).count()  # 日期为当天的数据总数
                # Sensitive_num += Wangyiedu.objects.annotate(openurl=F('url'),time=F('upload_time')).filter(sentiment=-1).count()  # 负面信息总量
                #取新华网的查询结果
                Total_num += Xinhuanews.objects.values().count()  # 全国文章总数
                Today_num += Xinhuanews.objects.filter(time__date=today).count()  # 日期为当天的数据总数
                # Sensitive_num += Xinhuanews.objects.annotate(openurl=F('url'),time=F('pubtime'),title_id=F('contentid')).filter(sentiment=-1).count()  # 负面信息总量

                Source_num = 4  # 爬取的信息源总数
            else:  # 现在地区字段只有微博的数据有，所以别的平台没算
                Total_num = Title.objects.filter(province=province2).count()  # 地区文章总数
                Today_num = Title.objects.filter(time__date=today, province=province2).count()  # 日期为当天的数据总数
                Sensitive_num = Title.objects.filter(sentiment=-1, province=province2).count()  # 负面信息总量
                Source_num = 4  # 爬取的信息源总数
            return JsonResponse(
                {'code': 0, 'Total_num': Total_num, 'Today_num': Today_num, 'Sensitive_num': Sensitive_num,
                 'Source_num': Source_num})
        else:
            return JsonResponse({'code': 1, 'msg': 'type参数错误'})
    else:
        return JsonResponse({'code': 1, 'msg': '请求需携带type参数'})

def get_tre(request):#获取一周内的舆情趋势
    # import datetime
    # starttime = datetime.datetime.now()
    request.params = json.loads(request.body)
    try:
        province = request.params['Area']
    except:
        return JsonResponse({'code': 1,  'msg': '请求参数没拿到'})
    today = datetime.datetime.today()  # 获取当天的日期
    tomorrow = today +  datetime.timedelta(days=1)
    try:
        if province == '全国':
            tre_list = []
            t_count =  Title.objects.filter(time__date=today.date()).only('title').count()#微博当天的发文量
            print(connection.queries)
            t_count +=  PeopleNews.objects.filter(time__date=today.date()).only('title').count()#人民网当天的发文量
            t_count +=  Wangyiedu.objects.filter(time__date=today.date()).count()#网易教育当天的发文量
            t_count += Xinhuanews.objects.filter(time__date=today.date()).count()#新华网当天的发文量
            tre_list.append({'time':today.date().strftime('%m-%d'),'news_num':t_count})
            for time in range(1,7):#过去7天的发文量
                delta = datetime.timedelta(days=time)#相差天数
                past_date = today-delta
                past_date = past_date.date()

                t_count =  Title.objects.filter(time__date=past_date).count()#
                t_count +=  PeopleNews.objects.filter(time__date=past_date).count()#人民网当天的发文量
                t_count +=  Wangyiedu.objects.filter(time__date=past_date).count()#网易教育当天的发文量
                t_count +=  Xinhuanews.objects.filter(time__date=past_date).count()#新华网当天的发文量

                tre_list.append({'time':past_date.strftime('%m-%d'),'news_num':t_count})
            # endtime = datetime.datetime.now()
            # print (endtime - starttime)
            return JsonResponse({'code': 0, 'Tre_list': tre_list})#返回半个月的舆情趋势
        elif province:#现在地区字段只有微博的数据有，所以别的平台没算
            tre_list = []
            t_count =  Title.objects.filter(time__date=today.date(),province=province).count()
            tre_list.append({'time':today.date().strftime('%m-%d'),'news_num':t_count})
            for time in range(1,7):#过去7天的发文量
                delta = datetime.timedelta(days=time)#相差天数
                past_date = today-delta
                past_date = past_date.date()
                t_count = Title.objects.filter(time__date=past_date, province=province).count()
                tre_list.append({'time': past_date.strftime('%m-%d'), 'news_num': t_count})
            return JsonResponse({'code': 0, 'Tre_list': tre_list})  # 返回半个月的舆情趋势
        else:
            return JsonResponse({'code': 1, 'msg': '地区参数错误'})
    except:
        return JsonResponse({'code': 1, 'msg': f'未知错误\n{traceback.format_exc()}'})


def get_area_news_industry(request):  # 获取对应地区的细分行业文章声量
    request.params = json.loads(request.body)
    Area_name = request.params['Area_name']
    # Area_name = request.POST['Area_name']  #测试版
    if request.method == 'POST':
        if Area_name:
            key_dic = {'code': 0}
            temp_dic = {}
            date = Title.objects.filter(province=Area_name)
            for value in date:
                for word in value.key.split(','):
                    temp_dic[word] = temp_dic.get(word, 0) + 1
            key_dic['date'] = [{'name': item[0], 'value': item[1]} for item in temp_dic.items()]
            return JsonResponse(key_dic)
        return JsonResponse({'code': 1})
    return JsonResponse({'code': 1})


def get_area_hot_word(request):  # 获取热门词云
    request.params = json.loads(request.body)
    Area_name = request.params['Area_name']
    if request.method == 'POST':
        if Area_name:
            date = Title.objects.filter(province=Area_name)
            articles = [value.title for value in date]
            hot_word_dic = {'远程教育': 0.25, '双减': 0.3, 'K12': 0.2, '高考': 0.3, '中考': 0.2, '课外辅导': 0.3, '研学': 0.2,
                            "体育": 0.15, "学科竞赛": 0.2, "无人机": 0.2, "体育教育": 0.15,
                            "智慧教育": 0.15, "学科": 0.15, "竞赛": 0.15, }  # tfidf.tfidf_cal(articles)
            return_dic = {'code': 0, 'date': [{'name': item[0], 'value': item[1]} for item in hot_word_dic.items()]}
            return JsonResponse(return_dic)
        return JsonResponse({'code': 1})
    return JsonResponse({'code': 1})


def get_news_influence(request):  # 获取文章影响力
    request.params = json.loads(request.body)
    Area_name = request.params['Area_name']
    if request.method == 'POST':
        if Area_name:
            date = Title.objects.filter(province=Area_name, iscrawled=1)
            title = pd.DataFrame(list(date.values()))
            user1 = pd.DataFrame(list(User.objects.all().values()))

            user1['gzl'] = (user1['activefans_count']) / (user1['followers_count'])

            user1['gzl'] = user1['gzl'].apply(lambda x: s2(x))
            user1['follow_count'] = user1['follow_count'].apply(lambda x: s1(x))
            user1['followers_count'] = user1['followers_count'].apply(lambda x: s3(x))

            title['pz'] = (title['forward_num']) + (title['comment_num'])
            title['pz'] = title['pz'].apply(lambda x: s4(x))
            title['like_num'] = title['like_num'].apply(lambda x: s5(x))

            user1['ycl'] = (user1['original_count']) / (user1['statuses_count'])
            user1['ycl'] = user1['ycl'].apply(lambda x: s6(x))

            date = pd.merge(title, user1, on='uid')  # 表格合并

            date['yx'] = (date['follow_count']) * 0.1 + (date['gzl']) * 0.15 + (date['followers_count']) * 0.2 + \
                         (date['pz']) * 0.2 + (date['like_num']) * 0.1 + (date['ycl']) * 0.1 + (
                             date['verifiedfans_count']) * 0.15

            columns = ['url', 'key', 'iscrawled', 'uid', 'uname_x', 'read_num', 'forward_num', 'comment_num', 'like_num',
                       'comment_id', 'comment_times', 'sentiment', 'pz', 'uname_y',
                       'follow_count', 'followers_count', 'statuses_count', 'verified',
                       'fans_list_id', 'more_list_id', 'activefans_count',
                       'verifiedfans_count', 'original_count', 'gzl', 'ycl']

            date = date.set_index(['title_id'], drop=True)
            date = date.dropna(axis=0, how='any')
            date = date.drop(columns, axis=1)
            date_dic = date.to_dict(orient='index')
            date_dic2 = [{'id': item[0], 'value': item[1]} for item in date_dic.items()]
            date_dic2.sort(key=lambda t: t['value']['yx'], reverse=True)
            return_dic = {'code': 0, 'date': date_dic2}

            return JsonResponse(return_dic)
        return JsonResponse({'code': 1})
    return JsonResponse({'code': 1})


def get_area_news_source(request):  # 获取文章来源
    request.params = json.loads(request.body)
    Area_name = request.params['Area_name']
    print(Area_name)
    if request.method == 'POST':
        if Area_name:
            wb = Title.objects.all().count()  # 日期为当天的数据总数
            wy = Wangyiedu.objects.all().count()
            rm = PeopleNews.objects.all().count()
            # xh = xinhuanews.objects.all().count()
            #  {'name': '新华', 'value': xh}
            source_dic = {'code': 0, 'date': [{'name': '微博', 'value': wb}, {'name': '网易', 'value': wy},
                                              {'name': '人民', 'value': rm}]}
            return JsonResponse(source_dic)
        return JsonResponse({'code': 1, 'mg': 'Area name erro'})
    return JsonResponse({'code': 1})


def get_area_source_influence(request):  # 获取媒体影响力
    request.params = json.loads(request.body)
    Area_name = request.params['Area_name']
    if request.method == 'POST':
        if Area_name:
            wb = random.uniform(1, 5)
            wy = random.uniform(1, 5)
            rm = random.uniform(1, 5)
            influence_dic = {'code': 0, 'date': [{'name': '微博', 'value': wb}, {'name': '网易', 'value': wy},
                                                 {'name': '人民网', 'value': rm}]}
            return JsonResponse(influence_dic)
        return JsonResponse({'code': 1})
    return JsonResponse({'code': 1})


def get_map(request):
    if request.method == 'GET':
        loc_info = Title.objects.exclude(province='全国')
        temp_dict = {}
        for value in loc_info:
            temp_dict[str(value.province)] = temp_dict.get(str(value.province), 0) + 1
            loc_dict = {'code': 0, 'date': [{'name': item[0], 'value': item[1]} for item in temp_dict.items()]}
        return JsonResponse(loc_dict)

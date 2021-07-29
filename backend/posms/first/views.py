from django.shortcuts import render
from weibo.models import Comment, Title, User,PeopleNews
import json
from django.http import JsonResponse
from django.db.models import Q,F
import traceback
import datetime
from ema import ema


# Create your views here.

def search(request):#获取指定文章列表  
    # keywords = request.GET.get('keyword')
    request.params = json.loads(request.body)
    try:
        keywords = request.params['Keyword']
    except:
        return JsonResponse({'code': 1,  'msg': '请求参数没拿到'})
    try:
        #取微博的查询结果
        qs_weibo = Title.objects.values('title_id', 'title', 'openurl','time')  # .order_by('-title_id')
        if keywords:
            conditions = [Q(title__contains=one) for one in keywords.split(' ') if one]  # 所有查询的列表
            query = Q()
            for condition in conditions:  # 所有关键字是或的关系
                query |= condition
            qs_weibo = qs_weibo.filter(query&Q(iscrawled=1))
        qs_list = list(qs_weibo)
        #取人民网的查询结果，人民网url字段取了别名和weibo保持一致
        qs_people = PeopleNews.objects.annotate(openurl=F('url'),time=F('upload_time')).values('title_id', 'title', 'openurl','time')  
        
        if keywords:
            conditions = [Q(title__contains=one) for one in keywords.split(' ') if one]  # 所有查询的列表
            query = Q()
            for condition in conditions:  # 所有关键字是或的关系
                query |= condition
            qs_people = qs_people.filter(query)
        qs_list2 = list(qs_people)
        qs_list.extend(qs_list2)
        qs_list.sort(key=lambda t:t['time'], reverse=True)#按时间先后排序
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
                Total_num = Title.objects.values().count()  # 全国文章总数
                Today_num = Title.objects.filter(time__date=today).count()  # 日期为当天的数据总数
                Sensitive_num = Title.objects.filter(sentiment=-1).count()  # 负面信息总量
                Source_num = 3  # 爬取的信息源总数
            else:
                Total_num = Title.objects.filter(province=province2).count()  # 地区文章总数
                Today_num = Title.objects.filter(time__date=today,province=province2).count()  # 日期为当天的数据总数
                Sensitive_num = Title.objects.filter(sentiment=-1,province=province2).count()  # 负面信息总量
                Source_num = 3  # 爬取的信息源总数
            return JsonResponse(
                {'code': 0, 'Total_num': Total_num, 'Today_num': Today_num, 'Sensitive_num': Sensitive_num,
                 'Source_num': Source_num})
        else:
            return JsonResponse({'code': 1, 'msg': 'type参数错误'})
    else:
        return JsonResponse({'code': 1, 'msg': '请求需携带type参数'})

def get_tre(request):
    request.params = json.loads(request.body)
    try:
       province = request.params['Area']
    except:
        return JsonResponse({'code': 1,  'msg': '请求参数没拿到'})
    today = datetime.datetime.now()  # 获取当天的日期
    try:
        if province == '全国':
            tre_list = []
            t_count =  Title.objects.filter(time__date=today.date()).count()#当天的发文量
            tre_list.append({'time':today.date().strftime('%Y-%m-%d'),'news_num':t_count})
            for time in range(1,15):#过去14天的发文量
                delta = datetime.timedelta(days=time)#相差天数
                past_date = today-delta
                past_date = past_date.date()
                t_count =  Title.objects.filter(time__date=past_date).count()
                tre_list.append({'time':past_date.strftime('%Y-%m-%d'),'news_num':t_count})
            return JsonResponse({'code': 0, 'Tre_list': tre_list})#返回半个月的舆情趋势
        elif province:
            tre_list = []
            t_count =  Title.objects.filter(time__date=today.date(),province=province).count()
            tre_list.append({'time':today.date().strftime('%Y-%m-%d'),'news_num':t_count})
            for time in range(1,15):#过去14天的发文量
                delta = datetime.timedelta(days=time)#相差天数
                past_date = today-delta
                past_date = past_date.date()
                t_count =  Title.objects.filter(time__date=past_date,province=province).count()
                tre_list.append({'time':past_date.strftime('%Y-%m-%d'),'news_num':t_count})
            return JsonResponse({'code': 0, 'Tre_list': tre_list})#返回半个月的舆情趋势
        else:
            return JsonResponse({'code': 1, 'msg': '地区参数错误'})
    except:
        return JsonResponse({'code': 1, 'msg': f'未知错误\n{traceback.format_exc()}'})


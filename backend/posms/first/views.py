from django.shortcuts import render
from weibo.models import Comment,Title,User
import json
from django.http import JsonResponse
from django.db.models import Q
import traceback
import datetime
from ema import ema

# Create your views here.

def search(request):#获取指定文章列表
    request.params = json.loads(request.body)
    keywords = request.params['Keyword']
    try:
        #只取三个字段
        qs = Title.objects.values('title_id','title','openurl')#.order_by('-title_id')
        if keywords:
            conditions = [Q(title__contains=one) for one in keywords.split(' ') if one] #所有查询的列表
            query = Q()
            for condition in conditions:#所有关键字是或的关系
                query |= condition
            qs = qs.filter(query)
        qs_list = list(qs)
        return JsonResponse({'code': 1, 'News_list':qs_list})
    except:
        return JsonResponse({'code': 1,  'msg': f'未知错误\n{traceback.format_exc()}'})

def get_num(request):#获取数据量
    ph = request.GET.get('type',None)
    if ph:
        request.params = request.GET
        if request.params['type']=='num':
            today = datetime.datetime.now().date()#获取当天的日期
            # today = datetime.date(2021,7,14)
            Total_num = Title.objects.values().count()#文章总数
            # qs = Title.objects.all()
            # for i in qs:
            #     a = ema(i.title)
            #     i.sentiment = ema(i.title)['data']['sentiment']
            #     i.save()
            Today_num = Title.objects.filter(time__date=today).count()#日期为当天的数据总数
            Sensitive_num = Title.objects.filter(sentiment=-1).count()#负面信息总量
            Source_num = 3#爬取的信息源总数
            return JsonResponse({'code': 1, 'Total_num':Total_num, 'Today_num':Today_num, 'Sensitive_num':Sensitive_num, 'Source_num':Source_num})
        else:
            return JsonResponse({'code': 1,  'msg': 'type参数错误'})
    else:
        return JsonResponse({'code': 1,  'msg': '请求需携带type参数'})

    


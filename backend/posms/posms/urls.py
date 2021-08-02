"""posms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from first.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_news/',search),#获取指定文章列表
    path('get_news_num/',get_num),#获取数据量
    path('get_area_news_tre/',get_tre),#获取地区舆情趋势
    path('get_news_map/',get_map),#获取数据量
    path('get_area_news_industry/',get_area_news_industry),# 获取细分行业声量
    path('get_area_hot_word/',get_area_hot_word),
    path('get_news_influence/',get_news_influence),
    path('get_area_news_source/',get_area_news_source),
    path('get_area_source_influence/',get_area_source_influence)
]

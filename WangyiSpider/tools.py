# encoding: utf-8
# Author    : 1476776320@qq.com
# Datetime  : 2021/07/027 9:23
# User      : TianXin
# Product   : PyCharm
# Project   : WangyiSpider
# File      : tools.py
# Explain   : 备注

from datetime import datetime
import mysql
import os

# 写入数据库
def save_data(title_id,title,upload_time,source,url,text):
    sql = "INSERT INTO wangyiedu (`title_id`,`title`,`upload_time`,`source`,`url`,`text`) values('{}','{}','{}','{}','{}','{}')".format(title_id,title,upload_time,source,url,text)
    mysql.exec_(sql)
    return 0

# 查询数据库

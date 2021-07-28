# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from PeopleSpider.items import *
from PeopleSpider.db import db


class TitlePipeline(object):
    db = db(db="weibo")

    def process_item(self, item, spider):

        if isinstance(item, TitleItem):
            sql = f"""insert into people_news(`title_id`,`originalName`,`title`,`url`,`key`,`upload_time`) values ({item['title_id']},'{item['originalName']}','{item['title']}','{item['url']}','{item['key']}','{item['upload_time']}');"""
            self.db.exec_(sql)
            # print(sql)
            print(item)

        if isinstance(item, TextItem):
            sql = f"update people_news set `text`='{item['text']}' where `title_id`='{item['title_id']}'"
            self.db.exec_(sql)
            print(item)
            # print(sql)

# class TextPipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, TextItem):
#             sql = f"update people_news set `text`='{item['text']}' where `title_id`='{item['title_id']}'"
#             db.exec_(sql)
#             print(item)
#             # print(sql)
#             return item

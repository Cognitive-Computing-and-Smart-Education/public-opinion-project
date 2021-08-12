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

        if isinstance(item, PeopleTitle):
            sql = f"""insert into people_news(`title_id`,`originalName`,`title`,`url`,`key`,`time`) values ({item['title_id']},'{item['originalName']}','{item['title']}','{item['url']}','{item['key']}','{item['time']}');"""
            # print(sql)
            self.db.exec_(sql)
            # if item["sentiment"]:
            #     self.db.exec_(f"update people_news set `sentiment`='{item['sentiment']}'")
            return item

        if isinstance(item, PeopleText):
            sql = f"update people_news set `text`='{item['text']}' where `title_id`='{item['title_id']}'"
            self.db.exec_(sql)
            # print(item)
            # print(sql)
            return item

        if isinstance(item, XinhuaTitle):
            sql = """INSERT INTO xinhuanews(`title_id`,`title`,`keyword`,`time`,`originalName`,`url`,`key`) VALUES('{}','{}','{}','{}','{}','{}','{}') ;""".format(
                item['title_id'], item['title'], item['keyword'], item['time'], item['originalName'], item['url'],
                item['key'], )

            # sql = """INSERT INTO xinhuanews(`contentId`,`title`,`keyword`,`pubtime`,`sitename`,`url`,`key`) SELECT  '%s','%s','%s','%s','%s','%s','%s' FROM DUAL WHERE  NOT EXISTS ( SELECT `url`  FROM xinhuanews  WHERE `url`='%s' );""" % (
            #     item['contentId'], item['title'], item['keyword'], item['pubtime'], item['sitename'], item['url'],
            #     item['key'], item['url'],)
            self.db.exec_(sql)
            # print(sql)
            return item

        if isinstance(item, XinhuaText):
            sql = f"""update xinhuanews set text ="{item['text']}" where `title_id`={item['title_id']}"""
            self.db.exec_(sql)
            # print(sql)
            return item

# class TextPipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, TextItem):
#             sql = f"update people_news set `text`='{item['text']}' where `title_id`='{item['title_id']}'"
#             db.exec_(sql)
#             print(item)
#             # print(sql)
#             return item

# class XinhuanetspiderPipeline:
#     def process_item(self, item, spider):
#         if isinstance(item, XinhuaTitle):
#             sql = """INSERT INTO xinhuanews(`title_id`,`title`,`keyword`,`pubtime`,`sitename`,`url`,`key`) VALUES('{}','{}','{}','{}','{}','{}','{}') ;""".format(
#                 item['title_id'], item['title'], item['keyword'], item['pubtime'], item['sitename'], item['url'],
#                 item['key'], )
#
#             # sql = """INSERT INTO xinhuanews(`contentId`,`title`,`keyword`,`pubtime`,`sitename`,`url`,`key`) SELECT  '%s','%s','%s','%s','%s','%s','%s' FROM DUAL WHERE  NOT EXISTS ( SELECT `url`  FROM xinhuanews  WHERE `url`='%s' );""" % (
#             #     item['contentId'], item['title'], item['keyword'], item['pubtime'], item['sitename'], item['url'],
#             #     item['key'], item['url'],)
#             db.exec_(sql)
#             # print(sql)
#             return item
#
#         if isinstance(item, XinhuaText):
#             sql = f"""update xinhuanews set text ="{item['text']}" where `title_id`={item['title_id']}"""
#             db.exec_(sql)
#             # print(sql)
#             return item

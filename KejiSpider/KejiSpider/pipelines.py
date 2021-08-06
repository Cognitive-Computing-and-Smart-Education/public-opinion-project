# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from KejiSpider.items import *
from KejiSpider.db import db


class KejiPipeline(object):
    db = db(db="weibo")

    def process_item(self, item, spider):
        if isinstance(item, TitleItem):
            sql = f"""insert into keji_news(`originalName`,`title`,`url`,`key`,`upload_time`,`target`) values ('{item['originalName']}','{item['title']}','{item['url']}','{item['key']}','{item['upload_time']}','{item['target']}');"""
            # print(sql)
            self.db.exec_(sql)
            return item

        if isinstance(item, TextItem):
            sql = f"update keji_news set text='{item['text']}' where url='{item['url']}'"
            self.db.exec_(sql)
            return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from PeopleSpider.items import *
from PeopleSpider import db


class PeoplespiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TitleItem):
            sql = f"insert into people_news(`title_id`,`originalName`,`title`,`url`) values ({item['title_id']},'{item['originalName']}','{item['title']}','{item['url']}');"

            db.exec_(sql)
            print(item)
            return item

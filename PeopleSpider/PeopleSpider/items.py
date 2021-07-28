# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PeoplespiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TitleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_id = Field()
    originalName = Field()
    key = Field()
    title = Field()
    url = Field()
    upload_time = Field()
    textitem = Field()
    # item['originalName'] = originalName
    # item['title'] = title
    # item['upload_time'] = upload_time
    textitem = Field()


class TextItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_id = Field()
    originalName = Field()
    title = Field()
    text = Field()

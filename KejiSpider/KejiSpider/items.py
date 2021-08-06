# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class TitleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    target = Field()
    title = Field()
    url = Field()
    originalName = Field()
    upload_time = Field()
    sentiment = Field()
    key = Field()


class TextItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = Field()
    text = Field()

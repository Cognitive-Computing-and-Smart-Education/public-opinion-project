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

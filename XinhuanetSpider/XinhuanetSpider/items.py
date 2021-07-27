# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class XinhuanetspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TitleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    contentId = Field()
    title = Field()
    keyword = Field()
    key = Field()
    pubtime = Field()
    sitename = Field()
    url = Field()

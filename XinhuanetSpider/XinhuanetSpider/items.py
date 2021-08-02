# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class XinhuanetspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TitleItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_id = Field()
    title = Field()
    keyword = Field()
    key = Field()
    pubtime = Field()
    sitename = Field()
    url = Field()
    sentiment = Field()


class TextItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = Field()
    title_id = Field()

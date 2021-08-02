# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from XinhuanetSpider.items import *
from XinhuanetSpider import db


class XinhuanetspiderPipeline:
    def process_item(self, item, spider):
        if isinstance(item, TitleItem):
            sql = """INSERT INTO xinhuanews(`title_id`,`title`,`keyword`,`pubtime`,`sitename`,`url`,`key`) VALUES('{}','{}','{}','{}','{}','{}','{}') ;""".format(
                item['title_id'], item['title'], item['keyword'], item['pubtime'], item['sitename'], item['url'],
                item['key'], )

            # sql = """INSERT INTO xinhuanews(`contentId`,`title`,`keyword`,`pubtime`,`sitename`,`url`,`key`) SELECT  '%s','%s','%s','%s','%s','%s','%s' FROM DUAL WHERE  NOT EXISTS ( SELECT `url`  FROM xinhuanews  WHERE `url`='%s' );""" % (
            #     item['contentId'], item['title'], item['keyword'], item['pubtime'], item['sitename'], item['url'],
            #     item['key'], item['url'],)
            db.exec_(sql)
            # print(sql)
            return item

        if isinstance(item, TextItem):
            sql = f"""update xinhuanews set text ="{item['text']}" where `title_id`={item['title_id']}"""
            db.exec_(sql)
            # print(sql)
            return item

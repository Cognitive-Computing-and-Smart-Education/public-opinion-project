# -*- coding: utf-8 -*-
# import scrapy
import json
from scrapy import Request
from PeopleSpider.items import *
from lxml.etree import HTML
from PeopleSpider.db import db
from pymysql.converters import escape_string
import time
from scrapy_redis.spiders import RedisSpider


# from PeopleSpider import ema


class PeopleSpider(RedisSpider):
    # 定义爬取新闻的时间限制，开始与结束，均以秒为单位
    now = int(time.time())  # 获取当前时间

    # # 设置间隔,目前为15天前至今
    limit = 18 * 24 * 60 * 60

    # 设置间隔,目前为一天前至今
    # limit = 1 * 1 * 60 * 60
    statiTime = now - limit

    name = 'people'
    # allowed_domains = ['people.cn', '*']
    # url = 'http://search.people.cn/api-search/elasticSearch/search' #旧接口不能用了
    # url = 'http://search.people.cn/api-search/front/search'
    #

    # keys = ['艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'http://search.people.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.75 Safari/537.36',
    }
    data = {"limit": 100, "hasTitle": True, "hasContent": True, "isFuzzy": True, "type": 1, "sortType": 2,
            "startTime": statiTime * 1000, "endTime": now * 1000}
    db1 = db()
    SQL = "CREATE TABLE IF NOT EXISTS `people_news`  (`title_id` bigint NOT NULL,`originalName` varchar(255) ," \
          "`title` varchar(255) ,`url` varchar(255) ,`key` varchar(255) ,`text` longtext,`time` datetime,PRIMARY KEY " \
          "(`title_id`) USING BTREE); "
    db1.exec_(SQL)
    redis_key = "people:keys"

    # db2 = db(db="redis")

    def make_request_from_data(self, data):
        key = data.decode('utf-8')
        # for key in keys:
        page = 1
        # sql = f"select `page` from people_data where `key`='{key}'"

        # if not self.db2.query(sql):
        #     self.db2.exec_(f"insert into people_data VALUES ('{key}',1)")
        #
        # page = self.db2.query(sql)[0][0]

        self.data['key'] = key
        self.data['page'] = page
        self.headers['Referer'] = f'http://search.people.cn/s/?keyword={key}&st=0&_=1628664973889'
        # data = {}
        # for k, v in self.data.items():
        #     data[k] = str(v).lower()
        yield Request("http://search.people.cn/api-search/front/search", method="POST",
                      body=json.dumps(self.data), headers=self.headers,
                      callback=self.parse, dont_filter=True,
                      meta={'key': key, 'page': page})

    def parse(self, response):

        data = json.loads(response.text).get("data")

        # print(data)
        key = response.meta['key']
        self.data['key'] = key
        pages = data.get('pages')
        if response.meta['page'] <= pages:
            info_lsit = data.get("records")
            for info in info_lsit:
                item = PeopleTitle()
                item['title_id'] = info.get('id')
                item['originalName'] = escape_string(info.get('originalName'))
                title = info.get('title')
                html = HTML(title).xpath("//text()")

                item['title'] = escape_string(''.join(html))
                item['url'] = info.get('url')
                item['key'] = response.meta['key']

                ts = int(info.get("inputTime")) // 1000

                item['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                # item['sentiment'] = ''
                # sentimet = ema.ema(item['title'])
                # if sentimet['desc'] == 'success':
                #    item['sentiment'] = sentimet["data"]['sentiment']

                yield item

                yield Request(url=item['url'], headers=self.headers, callback=self.parse_text,
                              meta={'title_id': item['title_id'], 'item': item}, )
                # break

            # sql = f"select `page` from people_data where `key`='{key}'"
            # page = int(self.db2.query(sql)[0][0])
            page = response.meta['page'] + 1

            # self.db2.exec_(f"update people_data set `page`={page} where `key`='{key}'")

            self.data['page'] = page
            yield Request("http://search.people.cn/api-search/front/search", method="POST",
                          body=json.dumps(self.data), headers=self.headers,
                          callback=self.parse, dont_filter=True,
                          meta={'key': key, 'page': page})

    def parse_text(self, response):
        # 文本内容
        text = response.xpath("//p/text()").extract()
        text = ["".join(i.split()) for i in text]
        text = ''.join(text)

        textitem = PeopleText()

        textitem['title_id'] = response.meta['title_id']
        # item['originalName'] = originalName
        # item['title'] = title
        # item['upload_time'] = upload_time

        textitem['text'] = escape_string(text)

        yield textitem

        # self.db2.exec_('insert into people_url VALUES (%s)' % response.url)

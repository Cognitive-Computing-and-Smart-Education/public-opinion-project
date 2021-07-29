# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, FormRequest
from PeopleSpider.items import *
from lxml.etree import HTML
from PeopleSpider.db import db
from pymysql.converters import escape_string
import time
from fake_useragent import UserAgent
from PeopleSpider import ema


class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['people.cn', ]
    url = 'http://search.people.cn/api-search/elasticSearch/search'
    keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', ] + ['国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育"] + [
        '艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

    # keys = ['艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'http://search.people.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.75 Safari/537.36',
    }
    data = {
        "endTime": 0,
        "hasContent": True,
        "hasTitle": True,
        "isFuzzy": True,
        "limit": 10,
        "sortType": 2,
        "startTime": 0,
        "type": 1,
    }
    db1 = db(db="weibo")
    SQL = "CREATE TABLE IF NOT EXISTS `people_news`  (`title_id` bigint NOT NULL,`originalName` varchar(255) ,`title` varchar(255) ,`url` varchar(255) ,`key` varchar(255) ,`text` longtext,`upload_time` datetime,PRIMARY KEY (`title_id`) USING BTREE);"
    db1.exec_(SQL)

    db2 = db(db="redis")

    def start_requests(self):
        for key in self.keys:
            sql = f"select `page` from people_data where `key`='{key}'"
            if not self.db2.query(sql):
                self.db2.exec_(f"insert into people_data VALUES ('{key}',1)")
            page = self.db2.query(sql)[0][0]

            self.data['key'] = key
            self.data['page'] = page
            self.headers['Referer'] = f'http://search.people.cn/s/?keyword={key}&st=0&_=1627454684554'
            yield Request(self.url, method="POST", body=json.dumps(self.data), headers=self.headers,
                          callback=self.parse,
                          meta={'key': key, 'page': page}, dont_filter=True)

    def parse(self, response):

        data = json.loads(response.text).get("data")

        pages = data.get('pages')
        if response.meta['page'] <= pages:
            info_lsit = data.get("records")
            for info in info_lsit:
                item = TitleItem()
                item['title_id'] = info.get('id')
                item['originalName'] = escape_string(info.get('originalName'))
                title = info.get('title')
                html = HTML(title).xpath("//text()")

                item['title'] = escape_string(''.join(html))
                item['url'] = info.get('url')
                item['key'] = response.meta['key']

                ts = int(info.get("inputTime")) // 1000

                item['upload_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                item['sentiment'] = ''
                sentimet = ema.ema(item['title'])
                if sentimet['desc'] == 'success':
                    item['sentiment'] = sentimet["data"]['sentiment']

                yield item

                if not self.db1.query(
                        f"select `url` from people_news where `url`='{item['url']}'") and 'people.com.cn' in item[
                    'url']:
                    yield Request(url=item['url'], headers=self.headers, callback=self.parse_text,
                                  meta={'title_id': item['title_id'], 'item': item}, dont_filter=True)

            key = response.meta['key']
            # sql = f"select `page` from people_data where `key`='{key}'"
            # page = int(self.db2.query(sql)[0][0])
            page = response.meta['page'] + 1

            self.db2.exec_(f"update people_data set `page`={page} where `key`='{key}'")

            self.data['key'] = key
            self.data['page'] = page
            yield Request(self.url, body=json.dumps(self.data), method='POST', headers=self.headers,
                          callback=self.parse,
                          meta={'key': key, 'page': page}, )

    def parse_text(self, response):
        # 文本内容
        text = response.xpath("//p/text()").extract()
        text = ["".join(i.split()) for i in text]
        text = ''.join(text)

        textitem = TextItem()

        textitem['title_id'] = response.meta['title_id']
        # item['originalName'] = originalName
        # item['title'] = title
        # item['upload_time'] = upload_time
        textitem['text'] = escape_string(text)

        yield textitem

        # self.db2.exec_('insert into people_url VALUES (%s)' % response.url)

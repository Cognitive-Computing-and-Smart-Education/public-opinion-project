# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, FormRequest
from PeopleSpider.items import *
from lxml.etree import HTML
from PeopleSpider import db
from pymysql.converters import escape_string
import re


class PeopleSpider(scrapy.Spider):
    name = 'pTitle'
    allowed_domains = ['search.people.cn']

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'http://search.people.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.75 Safari/537.36',
    }

    def start_requests(self):
        self.stat_sql = "select `title_id`,`url` from people_news where `url` like '%%people.com.cn%%' and `text` is NULL limit 20;"
        self.query = db.query(self.stat_sql)
        # url = 'http://sd.people.com.cn/n2/2021/0720/c386784-34829035.html'
        # url = 'http://gx.people.com.cn/n2/2021/0713/c390645-34817944.html'
        if self.query:
            for i in self.query:
                title_id = i[0]
                url = i[1]
                # print(title_id)
                yield Request(url, headers=self.headers, callback=self.parse_text, meta={'title_id': title_id})

    def parse_text(self, response):

        # 文本内容
        text = response.xpath("//p/text()").extract()
        text = ["".join(i.split()) for i in text]
        text = ''.join(text)

        item = TextItem()

        item['title_id'] = response.meta['title_id']
        # item['originalName'] = originalName
        # item['title'] = title
        # item['upload_time'] = upload_time
        item['text'] = escape_string(text)

        yield item

        self.query = db.query(self.stat_sql)
        # url = 'http://sd.people.com.cn/n2/2021/0720/c386784-34829035.html'
        # url = 'http://gx.people.com.cn/n2/2021/0713/c390645-34817944.html'
        if self.query:
            if self.query:
                for i in self.query:
                    title_id = i[0]
                    url = i[1]
                    # print(title_id)
                    yield Request(url, headers=self.headers, callback=self.parse_text, meta={'title_id': title_id})

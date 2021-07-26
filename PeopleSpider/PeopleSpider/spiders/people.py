# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, FormRequest
from PeopleSpider.items import *
from lxml.etree import HTML
from PeopleSpider import db
from pymysql.converters import escape_string
import time


class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['search.people.cn']
    url = 'http://search.people.cn/api-search/elasticSearch/search'
    keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', ] + ['国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育"] + [
        '艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

    # keys = ['国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育"]

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

    SQL = "CREATE TABLE IF NOT EXISTS `people_news`  (`title_id` bigint NOT NULL,`originalName` varchar(255) ,`title` varchar(255) ,`url` varchar(255) ,`key` varchar(255) ,`text` longtext,`upload_time` datetime,PRIMARY KEY (`title_id`) USING BTREE);"
    db.exec_(SQL)

    def start_requests(self):
        page = 1
        for key in self.keys:
            self.data['key'] = key
            self.data['page'] = page
            yield Request(self.url, body=json.dumps(self.data), method='POST', headers=self.headers,
                          callback=self.parse,
                          meta={'key': key, 'page': page})

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

                yield item

        key = response.meta['key']
        page = response.meta['page'] + 1
        self.data['key'] = key
        self.data['page'] = page
        yield Request(self.url, body=json.dumps(self.data), method='POST', headers=self.headers,
                      callback=self.parse,
                      meta={'key': key, 'page': page})

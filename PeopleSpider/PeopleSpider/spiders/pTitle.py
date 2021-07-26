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

    def start_requests(self):
        stat_sql = "select `title_id`,`url` from people_news where `url` like '%%people.com.cn%%' and `text` is NULL limit 1;"
        query = db.query(stat_sql)
        # url = 'http://sd.people.com.cn/n2/2021/0720/c386784-34829035.html'
        # url = 'http://gx.people.com.cn/n2/2021/0713/c390645-34817944.html'
        if query:
            title_id = query[0][0]
            url = query[0][1]
            print(title_id)
            yield Request(url, headers=self.headers, callback=self.parse, meta={'title_id': title_id})

    def parse(self, response):
        # 修正标题，部分文章没有标题或者作者

        title = response.xpath("//h1/text()").extract_first()
        title = "".join(title.split())

        # 其他信息，时间，来源
        other_info = response.xpath("//div[@class='channel cf']/div[1]//text()").extract()
        # 对定位的元素进行去空，整理
        # 时间
        upload_time = "".join(other_info.split())
        "2021年07月13日09:47|来源："
        upload_time = re.findall(r"^(\d+)年(\d+)月(\d+)日(\d+:\d+)", upload_time)[0]
        upload_time = upload_time[0] + '-' + upload_time[1] + '-' + upload_time[2] + " " + upload_time[3]
        # 作者
        originalName = "".join(other_info[1].split())
        # 文本内容
        text = response.xpath("//p[@style=\"text-indent: 2em;\"]//text()").extract()
        text = ["".join(i.split()) for i in text]
        text = ''.join(text)

        item = TitleItem()

        item['title_id'] = response.meta['title_id']
        item['originalName'] = originalName
        item['title'] = title
        # item['upload_time'] = upload_time
        item['text'] = text

        print(item)

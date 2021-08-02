# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, FormRequest, Spider
from KejiSpider.items import *
from lxml.etree import HTML
from KejiSpider.db import db
from pymysql.converters import escape_string
import time


class PeopleSpider(Spider):
    name = 'keji'
    allowed_domains = ['search01.stdaily.com:8080', 'stdaily.com']
    "%25E6%2595%2599%25E8%2582%25B2"

    url = 'http://search01.stdaily.com:8080/guestweb/s?searchWord={key}&column=%25E5%2585%25A8%25E9%2583%25A8&wordPlace=0&orderBy=0&startTime=&endTime=&pageSize=10&pageNum={page}&timeStamp=0&siteCode=N000008328&siteCodes=&checkHandle=1&strFileType=%25E5%2585%25A8%25E9%2583%25A8%25E6%25A0%25BC%25E5%25BC%258F&sonSiteCode=&areaSearchFlag=1&secondSearchWords=&countKey=%200&left_right_index=0'
    # keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', ] + ['国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育"] + [
    #     '艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

    keys = ['K12']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'host': 'search01.stdaily.com:8080',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.75 Safari/537.36',
    }

    db1 = db(db="weibo")
    SQL = "CREATE TABLE IF NOT EXISTS `keji_news`  (`title_id` bigint NOT NULL,`originalName` varchar(255) ,`title` varchar(255) ,`url` varchar(255) ,`key` varchar(255) ,`text` longtext,`upload_time` datetime,PRIMARY KEY (`title_id`) USING BTREE);"
    db1.exec_(SQL)

    db2 = db(db="redis")

    def start_requests(self):
        for key in self.keys:
            sql = f"select `page` from keji_data where `key`='{key}'"

            if not self.db2.query(sql):
                self.db2.exec_(f"insert into keji_data VALUES ('{key}',0)")

            page = self.db2.query(sql)[0][0]

            # self.data['key'] = key
            # self.data['page'] = page
            # self.headers['Referer'] = f'http://search.people.cn/s/?keyword={key}&st=0&_=1627454684554'

            yield Request(self.url.format(key=key, page=page), headers=self.headers,
                          callback=self.parse,
                          meta={'key': key, 'page': page}, dont_filter=True)

    def parse(self, response):
        print(response.xpath("//div[@id=1]/").extract())

    def p(self, response):

        data = json.loads(response.text).get("data")

        pages = data.get('pages')
        if response.meta['page'] <= pages:
            info_lsit = data.get("records")
            for info in info_lsit:
                item = Item()
                item['title_id'] = info.get('id')
                item['originalName'] = escape_string(info.get('originalName'))
                title = info.get('title')
                html = HTML(title).xpath("//text()")

                item['title'] = escape_string(''.join(html))
                item['url'] = info.get('url')
                item['key'] = response.meta['key']

                ts = int(info.get("inputTime")) // 1000

                item['upload_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
                # item['sentiment'] = ''
                # sentimet = ema.ema(item['title'])
                # if sentimet['desc'] == 'success':
                #    item['sentiment'] = sentimet["data"]['sentiment']

                yield item

                yield Request(url=item['url'], headers=self.headers, callback=self.parse_text,
                              meta={'title_id': item['title_id'], 'item': item}, dont_filter=True)

            key = response.meta['key']
            # sql = f"select `page` from people_data where `key`='{key}'"
            # page = int(self.db2.query(sql)[0][0])
            page = response.meta['page'] + 1

            self.db2.exec_(f"update keji_data set `page`={page} where `key`='{key}'")

            self.data['key'] = key
            self.data['page'] = page
            yield Request(self.url, body=json.dumps(self.data), method='POST', headers=self.headers,
                          callback=self.parse,
                          meta={'key': key, 'page': page}, )
        else:
            return

    def parse_text(self, response):
        # 文本内容
        text = response.xpath("//p/text()").extract()
        text = ["".join(i.split()) for i in text]
        text = ''.join(text)

        textitem = Item()

        textitem['title_id'] = response.meta['title_id']
        # item['originalName'] = originalName
        # item['title'] = title
        # item['upload_time'] = upload_time
        textitem['text'] = escape_string(text)

        yield textitem

        # self.db2.exec_('insert into people_url VALUES (%s)' % response.url)

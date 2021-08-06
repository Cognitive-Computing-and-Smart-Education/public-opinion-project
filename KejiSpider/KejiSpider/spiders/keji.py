# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request, Spider
from KejiSpider.items import *
from lxml.etree import HTML
from KejiSpider.db import db
import time
from pymysql.converters import escape_string


class PeopleSpider(Spider):
    name = 'keji'
    allowed_domains = ['search01.stdaily.com:8080', 'www.stdaily.com']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'host': 'search01.stdaily.com:8080',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.75 Safari/537.36',
    }

    url = 'http://search01.stdaily.com:8080/guestweb/s?searchWord={key}&column=%25E5%2585%25A8%25E9%2583%25A8&wordPlace=0&orderBy=0&startTime=&endTime=&pageSize=10&pageNum={page}&timeStamp=0&siteCode=N000008328&siteCodes=&checkHandle=1&strFileType=%25E5%2585%25A8%25E9%2583%25A8%25E6%25A0%25BC%25E5%25BC%258F&sonSiteCode=&areaSearchFlag=1&secondSearchWords=&countKey=%200&left_right_index=0'
    keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', ] + ['国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育"] + [
        '艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]

    # keys = ['四川']

    db1 = db(db="weibo")
    SQL = "CREATE TABLE IF NOT EXISTS `keji_news`  (`title` varchar(255) NOT NULL ,`target` varchar(255),`originalName` varchar(255) ,`url` varchar(255) ,`key` varchar(255) ,`text` longtext,`upload_time` date,PRIMARY KEY (`url`) USING BTREE);"
    db1.exec_(SQL)

    db2 = db(db="redis")

    def start_requests(self):

        for key in self.keys:
            sql = f"select `page` from keji_data where `key`='{key}'"

            if not self.db2.query(sql):
                self.db2.exec_(f"insert into keji_data VALUES ('{key}',0)")

            page = self.db2.query(sql)[0][0]

            yield Request(self.url.format(key=key, page=page), headers=self.headers,
                          callback=self.parse,
                          meta={'key': key, 'page': page}, dont_filter=True)

    def parse(self, response):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'host': 'www.stdaily.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.75 Safari/537.36',
            'Referer': 'http://search01.stdaily.com:8080/',
        }

        page = response.meta['page']
        key = response.meta['key']

        data_list = response.xpath("//div[@class=\"wordGuide Residence-permit\"]")
        for data in data_list:
            # 标签，类型
            target = data.xpath(
                "./div[@class=\"bigTit clearfix\"]/span[@class=\"fl columnLabel \"]/text()").extract_first()

            # 标题与连接
            title_data = data.xpath("./div[@class=\"bigTit clearfix\"]/a")
            title = title_data.xpath("./@title").extract_first()
            url = title_data.xpath("./@href").extract_first()

            # 来源及时间
            other = data.xpath("./div/div/p[@class=\"time\"]")
            originalName = other.xpath("./a/text()").extract_first()
            upload_time = other.xpath("./span/text()").extract_first()
            try:
                item = TitleItem()

                item['target'] = escape_string(target)
                item['title'] = escape_string(title)
                item['url'] = url
                item['originalName'] = escape_string(originalName)
                item['upload_time'] = upload_time
                # sentiment = Field()
                item['key'] = key

                yield item
                yield Request(url=url, headers=headers, callback=self.parse_text, meta={'url': url})
            except:
                pass

        page += 1
        self.db2.exec_(f"update keji_data set `page`={page} where `key`='{key}'")

        yield Request(self.url.format(key=key, page=page), headers=self.headers,
                      callback=self.parse,
                      meta={'key': key, 'page': page}, )

    def parse_text(self, response):
        # print(response.text)
        url = response.meta['url']
        text = response.xpath('//div[@class="content"]//text()').extract()
        text = ''.join(text)
        text = ''.join(text.split())

        item = TextItem()

        item['text'] = escape_string(text)
        item['url'] = url

        yield item

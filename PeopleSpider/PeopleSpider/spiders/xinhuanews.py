import scrapy
from scrapy import Spider, Request
import json
from lxml.etree import HTML
from pymysql.converters import escape_string
from PeopleSpider.items import *
from PeopleSpider.db import db
from scrapy_redis.spiders import RedisSpider


class XinhuanewsSpider(RedisSpider):
    name = 'xinhuanews'
    allowed_domains = ['so.news.cn', ]
    keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', '国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', '婴儿教育', '幼儿教育', '艺术培训',
            '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育']
    # keys = ['教育']
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    start_urls = 'http://so.news.cn/getNews?keyword={key}&curPage={page}&sortField=0&searchFields=1&lang=cn'

    db = db(db="weibo")
    SQL = """CREATE TABLE IF NOT EXISTS `xinhuanews`  (
    `title_id` bigint NOT NULL,
    `title` varchar(255),
    `keyword` varchar(255) ,
    `time` datetime ,
    `originalName` varchar(255) ,
    `url` varchar(255),
    `key` varchar(255),
    `text` longtext,
    `sentiment` int,
    PRIMARY KEY (`title_id`) USING BTREE) ;"""
    db.exec_(SQL)

    def start_requests(self):
        page = 1
        for key in self.keys:
            yield Request(url=self.start_urls.format(key=key, page=page), callback=self.parse,
                          meta={'key': key, "page": page}, dont_filter=True)
            # break

    def parse(self, response):
        data = json.loads(response.text).get("content")
        page = response.meta['page']
        key = response.meta['key']

        if data.get("results"):
            results = data.get("results")
            for result in results:
                # 新闻ID
                title_id = result.get("contentId")

                # 获取标题，并对标题文字提取，去除空字符，，使其符合mysql标准
                title = HTML(result.get("title")).xpath("//text()")
                title = "".join(title)
                title = ''.join(title.split())
                title = escape_string(title)

                # 标签
                keyword = result.get("keyword")

                # 时间
                upload_time = result.get("pubtime")

                # 来源
                sitename = result.get("sitename")

                # 链接
                url = result.get("url")

                item = XinhuaTitle()

                item['title_id'] = title_id
                item['title'] = title
                item['keyword'] = keyword
                item['time'] = upload_time
                item['originalName'] = sitename
                item['url'] = url
                item['key'] = key
                for k, v in item.items():
                    if not v:
                        item[k] = ''

                yield item
                yield Request(url=url, callback=self.parse_text, meta={'title_id': title_id}, dont_filter=True)

                # break
            # 下一页
            page += 1
            yield Request(url=self.start_urls.format(key=key, page=page), callback=self.parse,
                          meta={'key': key, "page": page})

    # 获取文章内容
    def parse_text(self, response):
        title_id = response.meta['title_id']

        text = response.xpath("//p/text()").extract()
        text = ''.join(text)
        text = ''.join(text.split())

        textitem = XinhuaText()
        textitem['text'] = text
        textitem['title_id'] = title_id

        yield textitem

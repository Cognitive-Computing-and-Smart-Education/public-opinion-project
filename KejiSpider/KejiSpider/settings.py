# -*- coding: utf-8 -*-

# Scrapy settings for KejiSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'KejiSpider'

SPIDER_MODULES = ['KejiSpider.spiders']
NEWSPIDER_MODULE = 'KejiSpider.spiders'

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

ITEM_PIPELINES = {
    'KejiSpider.pipelines.KejiPipeline': 300,
    # 'PeopleSpider.pipelines.TextPipeline': 400,

}

# 指定Redis的主机名和端口
REDIS_HOST = 'localhost'
REDIS_HOST = '172.18.40.39'
REDIS_PORT = 6379
#
# # 设置重复过滤器模块
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # 设置调度器,scrapy_redis中的调度器具备与数据库交互的功能
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # 设置当爬虫结束的时候是否保持redis数据库中的去重集合与任务队列
SCHEDULER_PERSIST = True
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"


DOWNLOAD_DELAY = 2.5

# LOG_LEVEL = 'WARNING'
LOG_LEVEL = 'DEBUG'

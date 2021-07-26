# coding:utf-8
import random
import json
import requests
import re
# from weibo import db
import time

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
    "key": '教育',
    "limit": 10,
    "page": 1,
    "sortType": 2,
    "startTime": 0,
    "type": 0,
}
url = 'http://search.people.cn/api-search/elasticSearch/search'

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response)
# print(json.loads(response.text))
data = json.loads(response.text)
titile_list = data.get('data').get('records')
searchCount = data.get('data').get('optimizeCountSql')
for titile in titile_list:
    sourceId = titile.get("sourceId")
    print(sourceId)
print(searchCount)
"""
32070198
34788772
32060387
34707727
32084804
34557783
32076980
34719003
32115859
34540924
"""
"""
34634634
34722056
34793113
34741523
32070198
34788772
32060387
34707727
32084804
34557783
"""



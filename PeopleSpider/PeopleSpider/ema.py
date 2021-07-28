#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64

# 用于计算文本的情感倾向
# sentiment = ema(i.title)['data']['sentiment']
# 接口地址
url = "http://ltpapi.xfyun.cn/v2/sa"
# 开放平台应用ID
x_appid = "8c0dfa09"
# 开放平台应用接口秘钥
api_key = "d187daa5aae1e3ec0a4f43129b429ac5"


# 语言文本
# text="汉皇重色思倾国，御宇多年求不得。杨家有女初长成，养在深闺人未识。天生丽质难自弃，一朝选在君王侧。"


def ema(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    result = result.decode('utf-8')
    result = json.loads(result)
    return result


if __name__ == '__main__':
    # 语言文本
    text = "汉皇重色思倾国，御宇多年求不得。杨家有女初长成，养在深闺人未识。天生丽质难自弃，一朝选在君王侧。"
    print(ema(text))

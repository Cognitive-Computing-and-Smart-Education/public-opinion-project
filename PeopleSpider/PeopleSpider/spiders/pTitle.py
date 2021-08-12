# a=b'\xe7\x88\xb1\xe5\x9b\xbd\xe6\x95\x99\xe8\x82\xb2'.decode()
# print(a.decode('utf-8'))
import time

# now = int(time.time())
#
# s = 1627776900000 // 1000
# print(now)
# print(now -s)
import json

a = '{"code":200,"content":{"recommendation":null,"keyword":"资源","sortField":"0","optionsSearchTypes":null,"curPage":793,"results":null}}'
b = json.loads(a)
print(b)

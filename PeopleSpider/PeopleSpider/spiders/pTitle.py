# a=b'\xe7\x88\xb1\xe5\x9b\xbd\xe6\x95\x99\xe8\x82\xb2'.decode()
# print(a.decode('utf-8'))
import time

# now = int(time.time())
#
# s = 1627776900000 // 1000
# print(now)
# print(now -s)
import json

now = int(time.time())

tt = "2021-08-01 19:24:02"
now2Str = time.strptime(tt, "%Y-%m-%d %H:%M:%S")

print(now)
print(int(time.mktime(now2Str)))
print(tt)

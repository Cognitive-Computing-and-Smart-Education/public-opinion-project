import time
import datetime

ts = 1626923488000//1000

dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
print(dt)
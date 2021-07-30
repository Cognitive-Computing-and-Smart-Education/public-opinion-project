def s2(num):
    if num > 0.5:
        return 5
    elif num < 0.05:
        return 1
    elif num>=0.05 and num<0.15:
        return 2
    elif num >= 0.15 and num < 0.25:
        return 3
    elif num >= 0.25 and num < 0.5:
        return 4

#0~100	100~1000	1000~10000	10000~50000	50000 S2离散化标准#
def s1(num):
    if num > 50000:
        return 5
    elif num < 100:
        return 1
    elif num>=100and num<1000:
        return 2
    elif num >= 1000 and num < 10000:
        return 3
    elif num >= 10000and num < 50000:
        return 4


#0~1000	1000~5000	5000~20000	20000~100000	100000 S3离散化#
def s3(num):
    if num > 100000:
        return 5
    elif num < 1000:
        return 1
    elif num>=1000and num<5000:
        return 2
    elif num >= 5000 and num < 20000:
        return 3
    elif num >= 20000and num < 100000:
        return 4


#0~50	50~100%	100%~500	500~100	1000 S4离散化

def s4(num):
    if num > 1000:
        return 5
    elif num < 50:
        return 1
    elif num>=50and num<100:
        return 2
    elif num >= 100 and num < 500:
        return 3
    elif num >= 500and num < 1000:
        return 4
#

#0~50	50~100%	100%~500	500~100	1000 S5离散化
def s5(num):
    if num > 1000:
        return 5
    elif num < 50:
        return 1
    elif num>=50and num<100:
        return 2
    elif num >= 100 and num < 500:
        return 3
    elif num >= 500and num < 1000:
        return 4
#

# 0~5%	5%~10%	10%~15%	15%~20%	20%+ S6离散化
#
def s6(num):
    if num > 0.2:
        return 5
    elif num < 0.05:
        return 1
    elif num>=0.05and num<0.1:
        return 2
    elif num >= 0.1 and num < 0.15:
        return 3
    elif num >= 0.15and num < 0.2:
        return 4
#

#S7	0~50	50~100	100~500	500~1000	1000 s7离散化
def s7(num):
    if num > 1000:
        return 5
    elif num < 50:
        return 1
    elif num>=50 and num<100:
        return 2
    elif num >= 100 and num < 500:
        return 3
    elif num >= 500 and num < 1000:
        return 4
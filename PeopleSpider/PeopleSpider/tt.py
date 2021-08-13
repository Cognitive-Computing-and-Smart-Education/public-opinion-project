import redis

rd = redis.Redis('172.18.40.131', port=6379, db=0)
keys = ['教育', '教学', '体育教育', '智慧教育', '科技', '体育', '国际教育', '特殊教育', '学科竞赛', '职业教育', 'K12', "婴儿教育", "幼儿教育",
        '艺术培训', '远程教育', '线下教育', 'steam教育', '应试教育', '中考', '高考', '课外辅导', '科普教育', '海外教育', '爱国教育', ]
# keys = ['K12']

for _ in keys:
    rd.lpush('pp:keyword', _)
    rd.lpush('xinhuanews:keyword', _)

#
# for _ in keys:
#     rd.lpush('xinhuanews:keyword', _)
